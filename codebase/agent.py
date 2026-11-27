"""Một lõi agent cho CLI có phiên và hợp đồng answer(text) của harness BTC.

Planner hiện là fake, công cụ đọc bị giới hạn. Mọi thao tác ca cần người duyệt.
"""
import json
import re
from ai import call_model
from tools import get_order, get_policy
from policy import normalize, _result, preflight, render_response, guard_decision
from cases import CaseStore, order_timeline, show_case, now

class Agent:
    def __init__(self, store):
        self.store = store

    def _finish(self, result):
        self.last_result = result
        return result['output']

    def _fallback(self, message, order=None):
        return self._finish(_result('human_review', message, order))

    def chat(self, owner, message, clarify=True):
        session = self.store.session(owner)
        user = normalize(message)
        self.last_result = None
        blocked = preflight(message)
        if blocked:
            return self._finish(blocked)
        ids = set(re.findall(r'\bD\d{3,}\b', message.upper()))
        if len(ids) > 1:
            return self._finish(_result('ask_order', 'Bạn muốn xử lý đơn nào? Hãy chọn một mã.'))
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
        elif any(w in user for w in ('nhan vien', 'khieu nai', 'chua nhan', 'chua thay', 'can ho tro', 'xu ly')):
            session['goal'] = 'human_review'
        elif any(w in user for w in ('cho tiep', 'theo doi', 'dang o dau', 'trang thai')):
            session['goal'] = 'wait'
        self.store.save_session(owner, session)
        if not session['order_id']:
            return self._finish(_result('ask_order', 'Bạn cung cấp mã đơn (ví dụ D004) nhé; mình sẽ giữ thông tin trong phiên demo này.'))
        if any(w in user for w in ('thieu mon', 'sai mon', 'doi tai xe', 'khoa shop')):
            return self._finish(_result('out_of_scope', 'Yêu cầu ngoài phạm vi giao trễ; đề xuất nhân viên, chưa thực hiện thao tác.'))
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
                               json.dumps({'message': message,
                                           'observations': observations}, ensure_ascii=False))
            try:
                decision = json.loads(reply['text'])
                step = decision.get('tool') if isinstance(decision, dict) else None
            except (ValueError, TypeError, KeyError):
                return self._fallback('Không đọc được quyết định model; cần nhân viên kiểm tra, chưa tạo ca.')
            if step == 'finish':
                break
            if step not in allowed or step in observations:
                return self._fallback('Dừng vì bước công cụ không hợp lệ; chưa tạo hoặc cập nhật ca.')
            observations[step] = allowed[step]()
        else:
            return self._fallback('Đã chạm giới hạn bước demo; đề xuất nhân viên kiểm tra, chưa tạo ca.')
        if 'get_order' not in observations:
            return self._fallback('Chưa đủ căn cứ công cụ để soạn hồ sơ; cần nhân viên kiểm tra.')
        order = observations.get('get_order')
        if not order:
            return self._finish(_result('not_found', 'Không tìm thấy đơn demo; hãy kiểm tra mã.'))
        if 'get_policy' not in observations or 'order_timeline' not in observations:
            return self._fallback('Chưa đủ căn cứ công cụ để soạn hồ sơ; cần nhân viên kiểm tra.')
        existing = self.store.find(owner, session['order_id'])
        active = next((c for c in existing if c['status'] != 'resolved'), None)
        if active:
            if active['status'] == 'needs_info':
                case = self.store.supplement(active['id'], owner, message)
                return self._finish(_result('case_status', 'Đã lưu lời khách bổ sung trong ca mô phỏng, chưa xác minh nội dung.\n' + show_case(case), order))
            return self._finish(_result('case_status', 'Đơn này đã có ca đang mở; không tạo ca trùng.\n' + show_case(active), order))
        if not session['goal']:
            if clarify:
                return self._finish(_result('ask_goal',
                    'Đơn %s: %s, snapshot %s. Bạn muốn theo dõi, kiểm tra hủy hay nhờ nhân viên xử lý?'
                    % (order['order_id'], order['status'], order['updated_at']), order))
            session['goal'] = 'wait'
        claim_text = normalize(' '.join(session['messages']))
        conflicts = []
        if not order['consistent']:
            conflicts.append('Snapshot có cờ mâu thuẫn; chưa xác nhận trạng thái.')
        if order['status'] == 'delivered' and any(w in claim_text for w in ('chua nhan', 'chua thay')):
            conflicts.append('Hệ thống ghi đã giao; khách nói chưa nhận. Chưa xác minh bên nào đúng.')
        missing = []
        if clarify and order['status'] == 'delivered' and not any(w in claim_text for w in ('chua nhan', 'da nhan', 'chua thay')):
            return self._finish(_result('ask_receipt', 'Hệ thống ghi đã giao. Bạn đã nhận món chưa? Mình cần làm rõ trước khi lập hồ sơ.', order))
        if type(order['delay_minutes']) is not int:
            missing.append('Chưa có dữ liệu thời gian trễ đáng tin.')
        action = session['goal']
        if conflicts or missing or any(w in claim_text for w in ('bo qua', '500k', '500.000', '100%')):
            action = 'human_review'
        result = render_response(order, observations['get_policy'], action)
        amount = result['proposal_vnd']
        proposal = result['output']
        draft = {'order_id': order['order_id'], 'customer_goal': session['goal'],
                 'customer_claims': session['messages'], 'facts': order,
                 'sources': [order['order_id'], 'DEMO-P1'], 'timeline': observations['order_timeline'],
                 'conflicts': conflicts, 'missing': missing, 'proposal': proposal,
                 'proposal_vnd': amount, 'requires_approval': True, 'executed': False,
                 'synthetic': True, 'created_at': now()}
        session['draft'] = draft
        self.store.save_session(owner, session)
        result['draft'] = draft
        result['requires_approval'] = True
        if clarify:
            result['output'] += ('\nHỒ SƠ NHÁP — chưa gửi ca/chưa giao dịch thật.\n'
                                 + json.dumps(draft, ensure_ascii=False, indent=2)
                                 + '\nNhân viên dùng /tiepnhan để xác nhận lưu ca mô phỏng.')
        return self._finish(result)


def answer(text: str) -> dict:
    """Cùng agent với CLI, phiên riêng trong RAM cho mỗi input độc lập của harness."""
    store = CaseStore(':memory:')
    try:
        agent = Agent(store)
        agent.chat('benchmark', text, clarify=False)
        return agent.last_result
    finally:
        store.close()
