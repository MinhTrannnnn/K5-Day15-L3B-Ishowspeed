"""Công cụ D1 chỉ đọc fixtures; không gửi tin, hủy đơn hoặc chuyển tiền."""
import json
from pathlib import Path
from tracing import tool

DATA = Path(__file__).resolve().parents[1] / 'data'


def _read(name):
    return json.loads((DATA / name).read_text(encoding='utf-8'))


@tool
def get_order(order_id: str):
    """get_order · input mã đơn · output snapshot synthetic hoặc None · chỉ đọc, không tác động ngoài."""
    for row in _read('demo_orders.json')['orders']:
        if row['order_id'] == order_id:
            return row
    return None


@tool
def get_policy(issue_type: str) -> dict:
    """get_policy · input late_delivery · output chính sách dựng · chỉ đọc, không tác động ngoài."""
    if issue_type != 'late_delivery':
        return {}
    return _read('demo_policy.json')


@tool
def check_limit(order: dict, amount: int) -> dict:
    """check_limit · input snapshot, số tiền VND · output eligible/allowed/reason · kiểm bằng code, không chuyển tiền."""
    policy = _read('demo_policy.json')
    delay = order.get('delay_minutes')
    eligible = (order.get('consistent') is True
                and order.get('status') in ('preparing', 'delivering', 'delivered', 'awaiting_driver')
                and type(delay) is int and delay > policy['late_threshold_minutes'])
    valid_amount = type(amount) is int and 0 < amount <= policy['max_voucher_vnd']
    return {'eligible': eligible, 'allowed': eligible and valid_amount,
            'max_vnd': policy['max_voucher_vnd'] if eligible else 0,
            'reason': 'Chỉ đề xuất voucher khi trễ quá 30 phút; tối đa 50.000 VND, chờ người duyệt.'}
