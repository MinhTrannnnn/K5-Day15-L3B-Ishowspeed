"""Sinh lại bộ đơn synthetic cố định; không phải bằng chứng pain."""
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

SEED = 27112026
rng = random.Random(SEED)
rows = []
as_of = datetime.fromisoformat('2026-11-27T12:30:00+07:00')
cases = [
    ('D001', 'awaiting_driver', 20, False, 'not_started', True),
    ('D002', 'preparing', 29, True, 'not_started', True),
    ('D003', 'delivering', 30, True, 'not_started', True),
    ('D004', 'delivering', 31, True, 'not_started', True),
    ('D005', 'cancelled', 60, False, 'pending', True),
    ('D006', 'delivering', 40, True, 'not_started', False),
    ('D007', 'delivered', 22, True, 'not_started', True),
    ('D008', 'awaiting_driver', 70, True, 'not_started', True),
    ('D009', 'preparing', None, True, 'not_started', True),
    ('D010', 'cancelled', 10, False, 'completed', True),
]
for order_id, status, delay, prepared, refund, consistent in cases:
    rows.append(dict(order_id=order_id, restaurant='Quán Mẫu', status=status,
                     delay_minutes=delay, prepared=prepared, refund_status=refund,
                     consistent=consistent, total_vnd=rng.choice([80000, 120000, 200000]),
                     original_eta=(as_of - timedelta(minutes=delay)).strftime('%H:%M') if delay is not None else None,
                     updated_eta='12:45', updated_at='2026-11-27T12:30:00+07:00'))
path = Path(__file__).with_name('demo_orders.json')
path.write_text(json.dumps({'version': 'd1-cp2-v1', 'synthetic': True, 'seed': SEED,
                            'as_of': '2026-11-27T12:30:00+07:00', 'orders': rows},
                           ensure_ascii=False, indent=2) + '\n')
print('Đã sinh 10 đơn synthetic, seed', SEED)
