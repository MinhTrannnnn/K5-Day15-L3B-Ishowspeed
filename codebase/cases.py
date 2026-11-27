"""CP2 fake nhiều lượt; nháp do máy tạo, ca/trạng thái chỉ người vận hành xác nhận.

Không có đăng nhập production: local CLI là bàn mô phỏng của một người vận hành.
Không có quyền duyệt trong danh sách công cụ model. Không giao dịch/gửi tin thật.
"""
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from tools import get_order
from tracing import tool
from case_review import review_case

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
        if target in ('pending_approval', 'in_progress', 'resolved'):
            review = self.checklist(case_id)
            if not review['ready_for_approval']:
                raise ValueError('Checklist chưa sẵn sàng: ' + '; '.join(review['blockers'] + review['warnings']))
        events = case['events'] + [{'actor': 'staff-demo', 'at': now(), 'status': target, 'type': 'status',
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


    def checklist(self, case_id):
        case = self.get(case_id)
        return review_case(case['body'], case['events'])

    def _append(self, case, event, expected_version, status=None):
        target = status or case['status']
        try:
            with self.db:
                cur = self.db.execute('UPDATE cases SET status=?,version=version+1,events=? WHERE id=? AND version=?',
                    (target, json.dumps(case['events']+[event], ensure_ascii=False), case['id'], expected_version))
                if cur.rowcount != 1:
                    raise ValueError('Phiên bản cũ; tải lại ca.')
        except sqlite3.IntegrityError:
            raise ValueError('Đơn đã có ca đang mở khác; cần nhân viên đối chiếu, không tự gộp.')
        return self.get(case['id'])

    def verify(self, case_id, version, evidence_ref, note):
        case = self.get(case_id)
        if case['status'] != 'verifying' or not evidence_ref.strip() or not note.strip():
            raise ValueError('Chỉ xác minh ở bước verifying, cần mã căn cứ và nhận định nhân viên.')
        event = {'actor': 'staff-demo', 'at': now(), 'status': case['status'],
                 'type': 'verification', 'evidence_ref': evidence_ref.strip(), 'note': note.strip()}
        return self._append(case, event, version)

    def reminder_drafts(self, threshold_minutes, at=None):
        if type(threshold_minutes) is not int or threshold_minutes <= 0:
            raise ValueError('Ngưỡng nhắc nội bộ phải là số phút nguyên dương.')
        clock = datetime.fromisoformat(at or now())
        if clock.tzinfo is None:
            raise ValueError('Thời điểm kiểm cần múi giờ.')
        drafts = []
        for row in self.db.execute("SELECT id FROM cases WHERE status!='resolved' ORDER BY id").fetchall():
            case = self.get(row['id'])
            status_event = next(e for e in reversed(case['events'])
                                if e.get('actor') == 'staff-demo' and e.get('type', 'status') == 'status')
            elapsed = (clock-datetime.fromisoformat(status_event['at'])).total_seconds()/60
            if elapsed >= threshold_minutes:
                drafts.append({'case_id': case['id'], 'status': case['status'],
                    'wait_minutes': round(elapsed, 1), 'threshold_minutes': threshold_minutes,
                    'reminder_key': '%s:%s' % (case['id'], status_event['at']),
                    'draft_only': True, 'sent': False,
                    'note': 'Nháp nhắc nhân viên theo ngưỡng nội bộ; không phải SLA hãng, chưa gửi tin.'})
        return drafts

    def feedback(self, case_id, owner, rating, note):
        case = self.get(case_id, owner)
        if case['status'] != 'resolved' or rating not in ('satisfied', 'unresolved') or not note.strip():
            raise ValueError('Phản hồi sau kết quả cần satisfied/unresolved và nội dung.')
        event = {'actor': owner, 'at': now(), 'status': 'resolved', 'type': 'feedback',
                 'rating': rating, 'note': note.strip(), 'verified': False}
        latest = next((e for e in reversed(case['events']) if e.get('type') == 'feedback'), None)
        if latest and latest['rating'] == rating and latest['note'] == note.strip():
            return case  # gửi lặp không thêm sự kiện hoặc tăng đếm
        return self._append(case, event, case['version'])

    def reopen(self, case_id, version, reason):
        case = self.get(case_id)
        if case['status'] != 'resolved' or not reason.strip():
            raise ValueError('Chỉ nhân viên mở lại ca đã có kết quả, cần lý do.')
        event = {'actor': 'staff-demo', 'at': now(), 'status': 'verifying',
                 'type': 'status', 'note': 'Mở lại để xác minh: '+reason.strip(), 'reopened': True}
        return self._append(case, event, version, 'verifying')

    def feedback_summary(self):
        counts = {'cases_with_feedback': 0, 'satisfied': 0, 'unresolved': 0,
                  'unverified_customer_feedback': True}
        for row in self.db.execute('SELECT id FROM cases').fetchall():
            events = self.get(row['id'])['events']
            latest = next((e for e in reversed(events) if e.get('type') == 'feedback'), None)
            if latest:
                counts['cases_with_feedback'] += 1
                counts[latest['rating']] += 1
        return counts


@tool
def order_timeline(order_id):
    """order_timeline · mã đơn → mốc có trong snapshot · chỉ đọc, không dựng lịch sử sự kiện không tồn tại."""
    order = get_order(order_id)
    if not order:
        return []
    return [{'source': order_id, 'snapshot_at': order['updated_at'],
             'original_eta': order['original_eta'], 'updated_eta': order['updated_eta'],
             'status': order['status'], 'consistent': order['consistent'],
             'delay_minutes': order['delay_minutes'], 'eta_source': 'platform_demo_snapshot',
             'live': False}]


def show_case(case):
    lines = ['Ca C%03d · đơn %s · v%d · %s' % (case['id'], case['order_id'], case['version'], LABELS[case['status']]),
             'Hồ sơ: ' + json.dumps(case['body'], ensure_ascii=False)]
    for event in case['events']:
        lines.append('%s · %s · %s: %s' % (event['at'], event['actor'], LABELS[event['status']], event['note']))
    return '\n'.join(lines)
