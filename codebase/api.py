"""FastAPI boundary for the local D1 demo. Both views share a browser session."""

import json
import os
import re
from contextlib import closing
from pathlib import Path
from threading import Lock
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import tracing
from ai import HostedModelError, MODEL_NAME, MODEL_PROVIDER
from agent import Agent
from cases import CaseStore, LABELS, STATES

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'frontend/dist'
ORDERS = {row['order_id']: row for row in json.loads((ROOT / 'data/demo_orders.json').read_text(encoding='utf-8'))['orders']}
LOCAL_HOST = re.compile(r'(?:localhost|127\.0\.0\.1)(?::\d+)?')
CASE_LINE = re.compile(r'^Ca C(\d+) ·', re.MULTILINE)
ORDER_LABELS = {'awaiting_driver': 'đang chờ tài xế', 'preparing': 'quán đang chuẩn bị',
                'delivering': 'đang giao', 'delivered': 'đã giao', 'cancelled': 'đã hủy'}
TRACE_LOCK = Lock()
app = FastAPI(title='Ishowspeed D1', docs_url='/api/docs', openapi_url='/api/openapi.json')


class Message(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class CaseUpdate(BaseModel):
    status: str
    version: int = Field(ge=1)
    note: str = Field(min_length=1, max_length=800)


@app.middleware('http')
async def local_only(request: Request, call_next):
    host = request.headers.get('host', '')
    if not LOCAL_HOST.fullmatch(host):
        return JSONResponse({'detail': 'Chỉ truy cập bản demo qua localhost.'}, status_code=403)
    if request.method in {'POST', 'PATCH'} and request.headers.get('origin') != f'http://{host}':
        return JSONResponse({'detail': 'Chỉ gửi yêu cầu từ giao diện localhost.'}, status_code=403)
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    if request.url.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.exception_handler(ValueError)
async def invalid_action(_request: Request, error: ValueError):
    return JSONResponse({'detail': str(error)}, status_code=400)


def session_owner(request: Request, response: Response) -> str:
    owner = request.cookies.get('d1_session', '')
    if re.fullmatch(r'[a-f0-9]{32}', owner):
        return owner
    owner = uuid4().hex
    response.set_cookie('d1_session', owner, httponly=True, samesite='strict')
    return owner


def database():
    return closing(CaseStore(os.environ.get('CP3_DB_PATH')))


def order_view(order_id):
    order = ORDERS.get(order_id)
    if not order:
        return None
    visible = {key: order[key] for key in ('order_id', 'restaurant', 'updated_at', 'consistent')}
    visible['status'] = ORDER_LABELS.get(order['status'], 'chưa rõ') if order['consistent'] else 'chưa xác minh'
    visible['eta'] = order['updated_eta'] if order['consistent'] and order['status'] in ('awaiting_driver', 'preparing', 'delivering') else None
    visible['delay_minutes'] = order['delay_minutes'] if order['consistent'] else None
    visible['refund'] = order['refund_status'] if order['consistent'] and order['status'] == 'cancelled' else None
    return visible


def case_view(case, *, staff=False):
    note = next((event['note'] for event in reversed(case['events']) if event['actor'] == 'staff-demo'), '')
    result = {'id': case['id'], 'code': f'C{case["id"]:03d}', 'order_id': case['order_id'],
              'status': case['status'], 'label': LABELS[case['status']], 'response': note,
              'order': order_view(case['order_id'])}
    if staff:
        result.update(version=case['version'], draft=case['body'],
                      events=[{'at': event['at'], 'status': event['status'], 'note': event['note'],
                               'actor': 'staff' if event['actor'] == 'staff-demo' else 'customer'} for event in case['events']],
                      next_statuses=[{'value': key, 'label': label} for key, label in LABELS.items()
                                     if key in STATES[case['status']]])
    return result


def draft_view(draft):
    if not draft:
        return None
    proposal = draft['proposal']
    if proposal.startswith('Nhân viên xác minh dữ kiện'):
        proposal = 'Nhân viên sẽ kiểm tra thông tin đơn sau khi tiếp nhận yêu cầu.'
    return {'order_id': draft['order_id'], 'proposal': proposal,
            'conflicts': draft['conflicts'], 'missing': draft['missing']}


def case_rows(store, owner):
    rows = store.db.execute('SELECT id FROM cases WHERE owner=? ORDER BY id DESC', (owner,)).fetchall()
    return [store.get(row['id'], owner) for row in rows]


def pending_draft(store, owner, session):
    draft = session.get('draft')
    if not draft:
        return None
    if any(case['status'] != 'resolved' or case['body'].get('created_at') == draft.get('created_at')
           for case in store.find(owner, draft['order_id'])):
        return None
    return draft


def customer_view(store, owner):
    session = store.session(owner)
    return {'order': order_view(session.get('order_id')), 'messages': session.get('web_messages', []),
            'draft': draft_view(pending_draft(store, owner, session)),
            'cases': [case_view(case) for case in case_rows(store, owner)]}


@app.get('/health')
@app.get('/api/health')
def health():
    return {'provider': MODEL_PROVIDER, 'model': MODEL_NAME if MODEL_PROVIDER != 'fake' else 'fake'}


@app.get('/api/customer')
def customer(owner: str = Depends(session_owner)):
    with database() as store:
        return customer_view(store, owner)


@app.post('/api/customer/messages')
def customer_message(body: Message, owner: str = Depends(session_owner)):
    message = body.text.strip()
    if not message:
        raise ValueError('Nhập nội dung cần hỗ trợ.')
    with TRACE_LOCK, database() as store:
        before = store.session(owner)
        tracing.begin('cp3-web')
        try:
            agent = Agent(store)
            output = agent.chat(owner, message)
        except HostedModelError as error:
            store.save_session(owner, before)
            raise HTTPException(503, str(error)) from None
        except (RuntimeError, TypeError, KeyError) as error:
            store.save_session(owner, before)
            raise HTTPException(503, 'Chưa lấy được phản hồi từ model. Bạn có thể thử lại.') from error
        finally:
            trace, _ = tracing.end()
        session = store.session(owner)
        draft = session.get('draft')
        active = CASE_LINE.search(output)
        choices = []
        if agent.last_result.get('draft') and draft:
            summary = draft_view(draft)
            output = '\n'.join([*summary['conflicts'], *summary['missing'], summary['proposal']])
        elif agent.last_result['action'] == 'case_status' and active:
            case = case_view(store.get(int(active[1]), owner))
            output = f"Ca {case['code']} · {case['label']}. {case['response']}"
        elif 'Bạn đã nhận món chưa?' in output:
            choices = ['Tôi chưa nhận món.', 'Tôi đã nhận món.']
        elif 'hãy chọn Tiếp tục nhờ nhân viên.' in output:
            output = output.replace('hãy chọn Tiếp tục nhờ nhân viên.', 'bạn có thể nhờ nhân viên hỗ trợ tiếp.')
            choices = ['Tôi vẫn cần nhân viên hỗ trợ đơn này.']
        session['web_messages'] = [*before.get('web_messages', []), {'role': 'customer', 'text': message},
                                   {'role': 'assistant', 'text': output, 'choices': choices}][-40:]
        store.save_session(owner, session)
        return {**customer_view(store, owner), 'trace': trace}


@app.post('/api/customer/reset')
def customer_reset(owner: str = Depends(session_owner)):
    with TRACE_LOCK, database() as store:
        store.save_session(owner, {'order_id': None, 'goal': None, 'messages': [], 'draft': None})
        return customer_view(store, owner)


@app.get('/api/staff')
def staff_queue(owner: str = Depends(session_owner)):
    with database() as store:
        draft = pending_draft(store, owner, store.session(owner))
        return {'draft': {**draft, 'order': order_view(draft['order_id'])} if draft else None,
                'cases': [case_view(case, staff=True) for case in case_rows(store, owner)]}


@app.post('/api/staff/receive')
def staff_receive(owner: str = Depends(session_owner)):
    with TRACE_LOCK, database() as store:
        if not pending_draft(store, owner, store.session(owner)):
            raise HTTPException(409, 'Hồ sơ này đã được tiếp nhận hoặc không còn hồ sơ nháp.')
        case, _ = store.receive(owner)
        return case_view(case, staff=True)


@app.patch('/api/staff/cases/{case_id}')
def staff_update(case_id: int, body: CaseUpdate, owner: str = Depends(session_owner)):
    with TRACE_LOCK, database() as store:
        store.get(case_id, owner)
        return case_view(store.update(case_id, body.version, body.status, body.note), staff=True)


if (DIST / 'assets').is_dir():
    app.mount('/assets', StaticFiles(directory=DIST / 'assets'), name='assets')


@app.get('/', include_in_schema=False)
def frontend():
    if not (DIST / 'index.html').is_file():
        raise HTTPException(503, 'Chạy npm run build trong frontend để tạo giao diện.')
    return FileResponse(DIST / 'index.html', headers={'Cache-Control': 'no-cache'})
