"""Checklist đọc hồ sơ CP2, không sửa dữ kiện và không tự duyệt."""
import re
from tools import check_limit, get_order, get_policy


def review_case(body, events=()):
    blockers, warnings = [], []
    for field in ('order_id', 'customer_goal', 'customer_claims', 'facts', 'sources', 'timeline', 'proposal', 'session_id', 'policy_version'):
        if not body.get(field):
            blockers.append('Thiếu trường '+field)
    order_id = body.get('order_id')
    facts = body.get('facts') if isinstance(body.get('facts'), dict) else {}
    snapshot = get_order(order_id) if order_id else None
    policy = get_policy('late_delivery')
    if snapshot is None or facts != snapshot:
        blockers.append('Dữ kiện hồ sơ không khớp snapshot có nguồn.')
    sources = body.get('sources') or []
    if order_id not in sources or policy['policy_id'] not in sources:
        blockers.append('Thiếu căn cứ mã đơn hoặc chính sách.')
    if body.get('policy_version') != policy['version']:
        blockers.append('Phiên bản chính sách không khớp nguồn.')
    if body.get('executed') is not False or body.get('requires_approval') is not True:
        blockers.append('Hồ sơ phải là nháp chưa thực hiện và cần người duyệt.')
    amount = body.get('proposal_vnd')
    if type(amount) is not int or amount < 0 or (amount > 0 and not check_limit(facts, amount)['allowed']):
        blockers.append('Tiền đề xuất không hợp lệ hoặc vượt điều kiện chính sách.')
    # Kiểm cả văn bản nháp, không chỉ trường tiền có cấu trúc.
    for number, unit in re.findall(r'(\d[\d.,]*)\s*(VND|đồng|đ|k)\b', body.get('proposal', ''), re.I):
        value = int(re.sub(r'\D', '', number)) * (1000 if unit.lower() == 'k' else 1)
        if value > policy['max_voucher_vnd'] or (value > 0 and value != amount):
            blockers.append('Văn bản chứa số tiền vượt hạn mức; cần kiểm lại.')
    warnings.extend(body.get('conflicts') or [])
    warnings.extend(body.get('missing') or [])
    if not facts.get('consistent'):
        warnings.append('Snapshot mâu thuẫn, cần người xác minh.')
    if type(facts.get('delay_minutes')) is not int:
        warnings.append('Thiếu thời gian trễ đáng tin.')
    reset = max((i+1 for i, e in enumerate(events) if e.get('reopened') or e.get('type') == 'customer_claim'), default=0)
    verified = any(e.get('type') == 'verification' and e.get('actor') == 'staff-demo'
                   and e.get('evidence_ref') and e.get('note') for e in events[reset:])
    return {'blockers': list(dict.fromkeys(blockers)), 'warnings': list(dict.fromkeys(warnings)),
            'staff_verification_recorded': verified,
            'ready_for_approval': not blockers and (not warnings or verified),
            'note': 'Kiểm kỹ thuật; xác minh nhân viên không tự đổi snapshot hoặc thực hiện giao dịch.'}
