"""CP2 fake nhiều lượt; nháp do máy tạo, ca/trạng thái chỉ người vận hành xác nhận.

Không có đăng nhập production: local CLI là bàn mô phỏng của một người vận hành.
Không có quyền duyệt trong danh sách công cụ model. Không giao dịch/gửi tin thật.
"""
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from agent import answer, normalize
from ai import call_model
from tools import get_order, get_policy, check_limit
from tracing import tool

ROOT = Path(__file__).resolve().parents[1]
STATES = {
    'received': {'verifying'},
    'verifying': {'needs_info', 'pending_approval'},
    'needs_info': {'verifying'},
    'pending_approval': {'in_progress', 'verifying'},
    'in_progress': {'resolved', 'verifying'},
    'resolved': set(),
}
LABELS = {'received': 'Đã tiếp nhận', 'verifying': 'Đang xác minh',
          'needs_info': 'Cần bổ sung', 'pending_approval': 'Chờ duyệt',
          'in_progress': 'Đang thực hiện (mô phỏng)', 'resolved': 'Đã có kết quả (mô phỏng)'}


def now():
    return datetime.now(timezone.utc).isoformat()


class CaseStore:
    """SQLite local chỉ chứa demo, transaction + version chặn cập nhật cũ/trùng."""
    def __init__(self, path=None):
        path = Path(path or ROOT / 'data/runtime/cp2.sqlite3')
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(path))
        self.db.row_factory = sqlite3.Row
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT NOT NULL,
                order_id TEXT NOT NULL, status TEXT NOT NULL, version INTEGER NOT NULL,
                body TEXT NOT NULL, events TEXT NOT NULL);
            CREATE UNIQUE INDEX IF NOT EXISTS active_order
                ON cases(owner, order_id) WHERE status != 'resolved';
        ''')

    def close(self):
        self.db.close()

    def session(self, owner):
        row = self.db.execute('SELECT body FROM sessions WHERE id=?', (owner,)).fetchone()
        return json.loads(row['body']) if row else {'order_id': None, 'goal': None, 'messages': [], 'draft': None}

    def save_session(self, owner, value):
        with self.db:
            self.db.execute('INSERT OR REPLACE INTO sessions VALUES (?,?)',
                            (owner, json.dumps(value, ensure_ascii=False)))

    def get(self, case_id, owner=None):
        row = self.db.execute('SELECT * FROM cases WHERE id=?', (case_id,)).fetchone()
        if not row or (owner is not None and row['owner'] != owner):
            raise ValueError('Không tìm thấy ca trong phạm vi khách này.')
        result = dict(row)
        result['body'] = json.loads(result['body'])
        result['events'] = json.loads(result['events'])
        return result

    def find(self, owner, order_id):
        rows = self.db.execute('SELECT id FROM cases WHERE owner=? AND order_id=? ORDER BY id DESC',
                               (owner, order_id)).fetchall()
        return [self.get(row['id'], owner) for row in rows]

    def receive(self, owner):
        draft = self.session(owner).get('draft')
        if not draft:
            raise ValueError('Chưa có hồ sơ nháp; hãy để khách mô tả yêu cầu trước.')
        # Chỉ bàn nhân viên gọi hàm này; model không có công cụ ghi ca.
        with self.db:
            active = self.db.execute("SELECT id FROM cases WHERE owner=? AND order_id=? AND status!='resolved'",
                                     (owner, draft['order_id'])).fetchone()
            if active:
                return self.get(active['id'], owner), False
            event = {'actor': 'staff-demo', 'at': now(), 'status': 'received',
                     'note': 'Nhân viên xác nhận tiếp nhận hồ sơ nháp; chưa giao dịch thật.'}
            cur = self.db.execute('INSERT INTO cases(owner,order_id,status,version,body,events) VALUES (?,?,?,?,?,?)',
                                  (owner, draft['order_id'], 'received', 1,
                                   json.dumps(draft, ensure_ascii=False), json.dumps([event], ensure_ascii=False)))
            case_id = cur.lastrowid
        return self.get(case_id, owner), True

    def update(self, case_id, expected_version, target, note):
        if not note.strip():
            raise ValueError('Cần phản hồi/lý do để khách theo dõi.')
        case = self.get(case_id)
        if target not in STATES.get(case['status'], set()):
            raise ValueError('Bước chuyển không hợp lệ từ %s.' % case['status'])
        if case['status'] == 'needs_info' and target == 'verifying':
            if not any(e.get('actor') == case['owner'] for e in case['events'][
                    max(i for i, e in enumerate(case['events']) if e['status'] == 'needs_info' and e['actor'] == 'staff-demo') + 1:]):
                raise ValueError('Chưa có thông tin bổ sung của khách.')
        events = case['events'] + [{'actor': 'staff-demo', 'at': now(), 'status': target,
                                    'note': note.strip(), 'synthetic': True}]
        with self.db:
            cur = self.db.execute('UPDATE cases SET status=?,version=version+1,events=? WHERE id=? AND version=?',
                                  (target, json.dumps(events, ensure_ascii=False), case_id, expected_version))
            if cur.rowcount != 1:
                raise ValueError('Phiên bản cũ; tải lại hồ sơ trước khi cập nhật.')
        return self.get(case_id)

    def supplement(self, case_id, owner, message):
        case = self.get(case_id, owner)
        if case['status'] != 'needs_info':
            raise ValueError('Ca chưa ở bước cần bổ sung.')
        events = case['events'] + [{'actor': owner, 'at': now(), 'status': 'needs_info',
                                   'note': message, 'type': 'customer_claim'}]
        with self.db:
            cur = self.db.execute('UPDATE cases SET version=version+1,events=? WHERE id=? AND version=?',
                                  (json.dumps(events, ensure_ascii=False), case_id, case['version']))
            if cur.rowcount != 1:
                raise ValueError('Ca vừa thay đổi; vui lòng gửi lại phần bổ sung.')
        return self.get(case_id, owner)


@tool
def order_timeline(order_id):
    """order_timeline · mã đơn → mốc có trong snapshot · chỉ đọc, không dựng lịch sử sự kiện không tồn tại."""
    order = get_order(order_id)
    if not order:
        return []
    return [{'source': order_id, 'snapshot_at': order['updated_at'],
             'original_eta': order['original_eta'], 'updated_eta': order['updated_eta'],
             'status': order['status'], 'consistent': order['consistent']}]


@tool
def delivery_estimate(owner, shop, as_of='2026-11-27T12:30:00+07:00'):
    """delivery_estimate · khách giả/shop/thời điểm → khoảng lịch sử, số mẫu · chỉ đọc synthetic, không hứa giờ giao."""
    from datetime import datetime
    path = ROOT / 'data/demo_delivery_history.json'
    if not path.exists():
        return {'available': False, 'reason': 'Chưa có dữ liệu lịch sử.'}
    data = json.loads(path.read_text(encoding='utf-8'))
    cutoff = datetime.fromisoformat(as_of)
    all_rows = [r for r in data['orders'] if r['shop_id'] == shop
                and r['status'] == 'completed'
                and datetime.fromisoformat(r['received_at']) < cutoff]
    personal = [r for r in all_rows if r['customer_id'] == owner]
    rows = personal if len(personal) >= 10 else all_rows
    if len(rows) < 10:
        return {'available': False, 'n': len(rows), 'reason': 'Không đủ 10 đơn hoàn tất trước thời điểm dự báo.'}
    values = sorted((datetime.fromisoformat(r['received_at']) - datetime.fromisoformat(r['placed_at'])).total_seconds()/60
                    for r in rows)
    def quantile(q):
        position = (len(values)-1)*q
        lo = int(position)
        hi = min(lo+1, len(values)-1)
        return round(values[lo]+(values[hi]-values[lo])*(position-lo), 1)
    return {'available': True, 'synthetic': True, 'shop_id': shop, 'n': len(rows),
            'group': 'personal_shop' if len(personal) >= 10 else 'shop_fallback',
            'p20_minutes': quantile(.2), 'median_minutes': quantile(.5), 'p80_minutes': quantile(.8),
            'as_of': as_of, 'latest_received_at': max(r['received_at'] for r in rows),
            'limits': 'Chưa xét khoảng cách, khung giờ hay tình trạng tài xế hiện tại; chưa kiểm chứng ngoài thực tế.'}


def show_case(case):
    lines = ['Ca C%03d · đơn %s · v%d · %s' % (case['id'], case['order_id'], case['version'], LABELS[case['status']]),
             'Hồ sơ: ' + json.dumps(case['body'], ensure_ascii=False)]
    for event in case['events']:
        lines.append('%s · %s · %s: %s' % (event['at'], event['actor'], LABELS[event['status']], event['note']))
    return '\n'.join(lines)


class Demo:
    def __init__(self, store):
        self.store = store

    def chat(self, owner, message):
        session = self.store.session(owner)
        user = normalize(message)
        # Dùng chốt an toàn cũ trước khi nhận văn bản vào hồ sơ.
        if any(term in user for term in ('ngo doc', 'di ung', 'di vat', 'so dien thoai', 'dia chi', 'sdt', 'so the')):
            return answer(message)['output']
        ids = set(re.findall(r'\bD\d{3,}\b', message.upper()))
        if len(ids) > 1:
            return 'Bạn muốn xử lý đơn nào? Hãy chọn một mã.'
        if ids and next(iter(ids)) != session['order_id']:
            if session['order_id'] is None:
                session['order_id'] = next(iter(ids))
            else:
                session = {'order_id': next(iter(ids)), 'goal': None, 'messages': [], 'draft': None}
        session['messages'].append(message)
        session['messages'] = session['messages'][-12:]
        if 'huy' in user:
            session['goal'] = 'cancel_review'
        elif 'hoan' in user:
            session['goal'] = 'refund_status'
        elif any(w in user for w in ('nhan vien', 'khieu nai', 'chua nhan', 'chua thay', 'ho tro', 'xu ly')):
            session['goal'] = 'human_review'
        elif any(w in user for w in ('cho tiep', 'theo doi', 'dang o dau', 'trang thai')):
            session['goal'] = 'wait'
        self.store.save_session(owner, session)
        if not session['order_id']:
            return 'Bạn cung cấp mã đơn (ví dụ D004) nhé; mình sẽ giữ thông tin trong phiên demo này.'
        if any(w in user for w in ('thieu mon', 'sai mon', 'doi tai xe', 'khoa shop')):
            return answer(message)['output']
        observations = {}
        allowed = {
            'get_order': lambda: get_order(session['order_id']),
            'get_policy': lambda: get_policy('late_delivery'),
            'order_timeline': lambda: order_timeline(session['order_id']),
        }
        # Fake planner chọn công cụ; dispatcher không nhận tên/args tự do từ model.
        # 4 vòng: tối đa 3 công cụ đọc và 1 quyết định kết thúc.
        for _ in range(4):
            reply = call_model('CP2: chỉ gọi công cụ đọc cho mã đơn đã chọn, rồi kết thúc.',
                               json.dumps({'mode': 'cp2_demo', 'message': message,
                                           'observations': observations}, ensure_ascii=False))
            try:
                decision = json.loads(reply['text'])
                step = decision.get('tool') if isinstance(decision, dict) else None
            except (ValueError, TypeError, KeyError):
                return 'Không đọc được quyết định model; cần nhân viên kiểm tra, chưa tạo ca.'
            if step == 'finish':
                break
            if step not in allowed or step in observations:
                return 'Dừng vì bước công cụ không hợp lệ; chưa tạo hoặc cập nhật ca.'
            observations[step] = allowed[step]()
        else:
            return 'Đã chạm giới hạn bước demo; đề xuất nhân viên kiểm tra, chưa tạo ca.'
        if 'get_order' not in observations:
            return 'Chưa đủ căn cứ công cụ để soạn hồ sơ; cần nhân viên kiểm tra.'
        order = observations.get('get_order')
        if not order:
            return 'Không tìm thấy đơn demo; hãy kiểm tra mã.'
        if 'get_policy' not in observations or 'order_timeline' not in observations:
            return 'Chưa đủ căn cứ công cụ để soạn hồ sơ; cần nhân viên kiểm tra.'
        existing = self.store.find(owner, session['order_id'])
        active = next((c for c in existing if c['status'] != 'resolved'), None)
        if active:
            if active['status'] == 'needs_info':
                case = self.store.supplement(active['id'], owner, message)
                return 'Đã lưu lời khách bổ sung trong ca mô phỏng, chưa xác minh nội dung.\n' + show_case(case)
            return 'Đơn này đã có ca đang mở; không tạo ca trùng.\n' + show_case(active)
        if not session['goal']:
            return ('Đơn %s: %s, snapshot %s. Bạn muốn theo dõi, kiểm tra hủy hay nhờ nhân viên xử lý?'
                    % (order['order_id'], order['status'], order['updated_at']))
        claim_text = normalize(' '.join(session['messages']))
        conflicts = []
        if not order['consistent']:
            conflicts.append('Snapshot có cờ mâu thuẫn; chưa xác nhận trạng thái.')
        if order['status'] == 'delivered' and any(w in claim_text for w in ('chua nhan', 'chua thay')):
            conflicts.append('Hệ thống ghi đã giao; khách nói chưa nhận. Chưa xác minh bên nào đúng.')
        missing = []
        if order['status'] == 'delivered' and not any(w in claim_text for w in ('chua nhan', 'da nhan', 'chua thay')):
            return 'Hệ thống ghi đã giao. Bạn đã nhận món chưa? Mình cần làm rõ trước khi lập hồ sơ.'
        if type(order['delay_minutes']) is not int:
            missing.append('Chưa có dữ liệu thời gian trễ đáng tin.')
        action = session['goal']
        if conflicts or missing or any(w in claim_text for w in ('bo qua', '500k', '500.000', '100%')):
            action = 'human_review'
        amount = 0
        if action == 'cancel_review':
            if order['status'] == 'awaiting_driver' and not order['prepared']:
                proposal = 'Đủ điều kiện đề xuất hủy theo DEMO-P1; chờ nhân viên duyệt, chưa hủy.'
            else:
                proposal = 'Chưa đủ điều kiện đề xuất hủy theo DEMO-P1; nhân viên xem xét yêu cầu.'
        elif order['status'] == 'cancelled':
            proposal = 'Khoản hoàn: %s theo snapshot; chưa xác nhận ngày hoàn hoặc giao dịch mới.' % order['refund_status']
        elif action == 'human_review':
            proposal = 'Nhân viên xác minh dữ kiện và xem xét phương án; chưa hủy/hoàn/phát voucher.'
        else:
            limit = check_limit(order, observations['get_policy']['max_voucher_vnd'])
            amount = limit['max_vnd'] if limit['allowed'] else 0
            proposal = ('Đề xuất voucher %s VND chờ duyệt; chưa phát hành.' % amount if amount
                        else 'Theo dõi hoặc nhờ nhân viên; chưa đủ điều kiện voucher theo DEMO-P1.')
        draft = {'order_id': order['order_id'], 'customer_goal': session['goal'],
                 'customer_claims': session['messages'], 'facts': order,
                 'sources': [order['order_id'], 'DEMO-P1'], 'timeline': observations['order_timeline'],
                 'conflicts': conflicts, 'missing': missing, 'proposal': proposal,
                 'proposal_vnd': amount, 'requires_approval': True, 'executed': False,
                 'synthetic': True, 'created_at': now()}
        session['draft'] = draft
        self.store.save_session(owner, session)
        return ('HỒ SƠ NHÁP — chưa gửi ca/chưa giao dịch thật.\n'
                + json.dumps(draft, ensure_ascii=False, indent=2)
                + '\nNhân viên dùng /tiepnhan để xác nhận lưu ca mô phỏng.')
