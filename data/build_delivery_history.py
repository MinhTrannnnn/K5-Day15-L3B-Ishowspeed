"""Lịch sử synthetic cho demo ETA CP2; không là bằng chứng hay mô hình dự báo thật."""
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path


def build():
    rng = random.Random(27112026)
    rows = []
    start = datetime(2026, 11, 1, 11, 0, tzinfo=timezone(timedelta(hours=7)))
    for i in range(120):
        placed = start + timedelta(hours=i*5)
        duration = rng.randint(25, 65)
        cancelled = i % 13 == 0
        rows.append({'order_id': 'H%04d' % i, 'customer_id': 'demo' if i % 2 == 0 else 'other',
                     'shop_id': 'S001' if i < 110 else 'S002',
                     'placed_at': placed.isoformat(),
                     'received_at': None if cancelled else (placed+timedelta(minutes=duration)).isoformat(),
                     'status': 'cancelled' if cancelled else 'completed', 'had_complaint': i % 7 == 0})
    return {'synthetic': True, 'seed': 27112026, 'version': 'cp2-upgrade-v1', 'orders': rows}


if __name__ == '__main__':
    (Path(__file__).parent/'demo_delivery_history.json').write_text(
        json.dumps(build(), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
