"""Kiểm các tác động và quyền của phần mở rộng CP2, không chấm AI thật."""
import copy
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'codebase'))
from agent import Agent
from app import command
from cases import CaseStore
from case_review import review_case


class ExtensionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = CaseStore(Path(self.tmp.name)/'cases.sqlite3')
        self.agent = Agent(self.store)

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def create(self, owner='demo', message='D001 tôi muốn hủy'):
        self.agent.chat(owner, message)
        return self.store.receive(owner)[0]

    def resolve(self, case):
        for target in ('verifying', 'pending_approval', 'in_progress', 'resolved'):
            case = self.store.update(case['id'], case['version'], target, 'Bước mô phỏng '+target)
        return case

    def test_checklist_detects_tampering_missing_fields_and_money_in_text(self):
        case = self.create()
        original = copy.deepcopy(case['body'])
        self.assertTrue(self.store.checklist(case['id'])['ready_for_approval'])
        for field in ('sources', 'customer_claims', 'session_id', 'policy_version'):
            body = copy.deepcopy(original)
            body.pop(field)
            self.assertFalse(review_case(body)['ready_for_approval'])
        for proposal in ('Hoàn 500k ngay', 'Voucher 500.000 VND', 'Đã hoàn 50000 VND'):
            body = dict(original, proposal=proposal)
            self.assertTrue(review_case(body)['blockers'])
        body = copy.deepcopy(original)
        body['facts']['prepared'] = True
        self.assertTrue(review_case(body)['blockers'])
        self.assertEqual(self.store.get(case['id'])['body'], original)

    def test_conflicts_block_approval_until_staff_records_evidence(self):
        case = self.create(message='D007 tôi chưa nhận món, cần hỗ trợ')
        case = self.store.update(case['id'], 1, 'verifying', 'Kiểm tra')
        with self.assertRaises(ValueError):
            self.store.update(case['id'], 2, 'pending_approval', 'Bỏ qua mâu thuẫn')
        with self.assertRaises(ValueError):
            self.store.verify(case['id'], 2, '', 'Không căn cứ')
        case = self.store.verify(case['id'], 2, 'DEMO-E1', 'Đã kiểm mô phỏng, đề xuất người xử lý, không quy lỗi')
        self.assertTrue(self.store.checklist(case['id'])['ready_for_approval'])
        self.assertTrue(self.store.checklist(case['id'])['warnings'])
        case = self.store.update(case['id'], 3, 'pending_approval', 'Duyệt đề xuất xử lý mô phỏng')
        self.assertFalse(case['body']['executed'])
        self.assertEqual(case['body']['facts']['status'], 'delivered')

    def test_reminders_use_status_age_are_drafts_and_do_not_reset_or_duplicate(self):
        case = self.create()
        timestamp = datetime.fromisoformat(case['events'][0]['at'])
        self.assertEqual(self.store.reminder_drafts(30, (timestamp+timedelta(minutes=29)).isoformat()), [])
        clock = (timestamp+timedelta(minutes=30)).isoformat()
        first = self.store.reminder_drafts(30, clock)
        self.assertEqual(first, self.store.reminder_drafts(30, clock))
        self.assertEqual(len(first), 1)
        self.assertFalse(first[0]['sent'])
        self.assertEqual(self.store.get(case['id'])['version'], 1)
        self.resolve(case)
        self.assertEqual(self.store.reminder_drafts(30, clock), [])
        for value in (0, -1, True):
            with self.assertRaises(ValueError):
                self.store.reminder_drafts(value)

    def test_feedback_is_owned_unverified_idempotent_and_does_not_reopen(self):
        case = self.resolve(self.create())
        cid = case['id']
        with self.assertRaises(ValueError):
            self.store.feedback(cid, 'other', 'unresolved', 'Ca khác')
        case = self.store.feedback(cid, 'demo', 'unresolved', 'Tôi vẫn cần hỗ trợ')
        self.assertEqual(case['status'], 'resolved')
        self.assertFalse(case['events'][-1]['verified'])
        same = self.store.feedback(cid, 'demo', 'unresolved', 'Tôi vẫn cần hỗ trợ')
        self.assertEqual(same['version'], case['version'])
        summary = self.store.feedback_summary()
        self.assertEqual(summary['cases_with_feedback'], 1)
        self.assertEqual(summary['unresolved'], 1)
        self.assertNotIn('note', summary)
        with self.assertRaises(ValueError):
            self.store.reopen(cid, case['version']-1, 'Cũ')
        reopened = self.store.reopen(cid, case['version'], 'Đọc phản hồi khách, cần xác minh tiếp')
        self.assertEqual(reopened['status'], 'verifying')

    def test_customer_cannot_use_staff_extensions_and_staff_cannot_rate_for_customer(self):
        for text in ('/checklist C001', '/xacminh C001 1 E ghi nhận', '/nhac 30', '/tonghop', '/molai C001 1 lý do'):
            with self.assertRaises(ValueError):
                command(self.store, 'demo', 'customer', text)
        with self.assertRaises(ValueError):
            command(self.store, 'demo', 'staff', '/phanhoi C001 satisfied ổn')

    def test_reopen_conflict_does_not_reuse_old_verification(self):
        case = self.create(message='D007 tôi chưa nhận món, cần hỗ trợ')
        self.store.update(case['id'], 1, 'verifying', 'Kiểm')
        case = self.store.verify(case['id'], 2, 'E1', 'Xác minh vòng đầu')
        for target in ('pending_approval', 'in_progress', 'resolved'):
            case = self.store.update(case['id'], case['version'], target, 'Mô phỏng')
        case = self.store.reopen(case['id'], case['version'], 'Cần đối chiếu lại')
        self.assertFalse(self.store.checklist(case['id'])['ready_for_approval'])


if __name__ == '__main__':
    unittest.main()
