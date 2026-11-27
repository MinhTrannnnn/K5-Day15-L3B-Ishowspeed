"""Kiểm các hành vi mới: quyền, duyệt, bộ nhớ, trùng ca và dữ liệu ETA."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'codebase'))
from cp2_demo import CaseStore, Demo, delivery_estimate
from app import command


class CP2DemoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = CaseStore(Path(self.temp.name)/'cases.sqlite3')
        self.demo = Demo(self.store)

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def test_clarifies_and_remembers_but_not_other_customer(self):
        self.assertIn('Bạn muốn', self.demo.chat('demo', 'D004 tôi chờ lâu'))
        self.assertIn('HỒ SƠ NHÁP', self.demo.chat('demo', 'Tôi muốn hủy'))
        draft = self.store.session('demo')['draft']
        self.assertEqual(draft['order_id'], 'D004')
        self.assertFalse(draft['executed'])
        self.assertEqual(self.store.find('demo', 'D004'), [])
        self.assertIn('cung cấp mã đơn', self.demo.chat('other', 'Tôi muốn hủy'))
        self.assertIsNone(self.store.session('other')['draft'])

    def test_goal_before_order_is_retained(self):
        self.demo.chat('demo', 'Tôi muốn hủy')
        self.demo.chat('demo', 'D001')
        self.assertEqual(self.store.session('demo')['draft']['customer_goal'], 'cancel_review')

    def test_conflicting_claims_are_not_promoted_to_facts(self):
        self.demo.chat('demo', 'D007 tôi chưa nhận món, cần hỗ trợ')
        draft = self.store.session('demo')['draft']
        self.assertTrue(draft['conflicts'])
        self.assertEqual(draft['facts']['status'], 'delivered')
        self.assertEqual(draft['proposal_vnd'], 0)
        self.assertIn('Nhân viên xác minh', draft['proposal'])
        self.assertIn('nhận món chưa', self.demo.chat('other', 'D007 cần hỗ trợ'))

    def test_explicit_staff_request_survives_model_clarification(self):
        with patch('cp2_demo.MODEL_PROVIDER', 'ollama'), patch('cp2_demo.choose_action', return_value='clarify'):
            self.demo.chat('demo', 'D007 kiểm tra đơn giúp mình')
            self.assertIn('Bạn đã nhận món chưa?', self.demo.chat('demo', 'Nhân viên xử lý giúp mình'))
            self.assertIn('HỒ SƠ NHÁP', self.demo.chat('demo', 'Chưa'))
        draft = self.store.session('demo')['draft']
        self.assertEqual(draft['customer_goal'], 'human_review')
        self.assertTrue(draft['conflicts'])
        self.assertEqual(self.store.find('demo', 'D007'), [])

    def test_receipt_confirmation_waits_before_preparing_staff_draft(self):
        self.assertIn('Bạn đã nhận món chưa?', self.demo.chat('demo', 'D007 nhờ nhân viên kiểm tra'))
        self.assertIn('bạn có thể dừng ở đây', self.demo.chat('demo', 'Tôi đã nhận món.'))
        self.assertIsNone(self.store.session('demo')['draft'])
        self.assertIn('HỒ SƠ NHÁP', self.demo.chat('demo', 'Tôi vẫn cần nhân viên hỗ trợ đơn này.'))
        self.assertEqual(self.store.session('demo')['draft']['customer_goal'], 'human_review')

    def test_only_operator_staff_can_receive_and_no_duplicate_or_cross_customer(self):
        self.demo.chat('demo', 'D001 tôi muốn hủy')
        with self.assertRaises(ValueError):
            command(self.store, 'demo', 'customer', '/tiepnhan')
        case, created = self.store.receive('demo')
        self.assertTrue(created)
        self.assertFalse(self.store.receive('demo')[1])
        self.assertIn('không tạo ca trùng', self.demo.chat('demo', 'Tôi muốn hủy'))
        with self.assertRaises(ValueError):
            command(self.store, 'other', 'customer', '/trangthai C%03d' % case['id'])
        with self.assertRaises(ValueError):
            self.store.update(case['id'], 1, 'resolved', 'đóng ngay')
        updated = self.store.update(case['id'], 1, 'verifying', 'Đang kiểm tra')
        self.assertEqual(updated['version'], 2)
        with self.assertRaises(ValueError):
            self.store.update(case['id'], 1, 'pending_approval', 'cập nhật cũ')

    def test_staff_feedback_customer_supplement_and_full_lifecycle(self):
        self.demo.chat('demo', 'D007 tôi chưa nhận món, cần hỗ trợ')
        case, _ = self.store.receive('demo')
        cid = case['id']
        self.store.update(cid, 1, 'verifying', 'Đang kiểm tra')
        self.store.update(cid, 2, 'needs_info', 'Bạn đã kiểm tra nơi nhận chưa?')
        with self.assertRaises(ValueError):
            self.store.update(cid, 3, 'verifying', 'Chưa có câu trả lời')
        self.demo.chat('demo', 'Tôi đã kiểm tra nơi nhận, chưa thấy món')
        case = self.store.get(cid, 'demo')
        self.assertEqual(case['version'], 4)
        self.assertEqual(case['events'][-1]['type'], 'customer_claim')
        for version, status in [(4, 'verifying'), (5, 'pending_approval'), (6, 'in_progress'), (7, 'resolved')]:
            case = self.store.update(cid, version, status, 'Kết quả thao tác mô phỏng: '+status)
        self.assertEqual(case['status'], 'resolved')
        self.assertFalse(case['body']['executed'])

    def test_malicious_planner_cannot_run_mutation_and_loop_is_bounded(self):
        reply = {'text': json.dumps({'tool': 'issue_refund'})}
        with patch('cp2_demo.call_model', return_value=reply) as model:
            self.assertIn('không hợp lệ', self.demo.chat('demo', 'D004 hỗ trợ'))
            self.assertEqual(model.call_count, 1)
        self.assertEqual(self.store.find('demo', 'D004'), [])
        with patch('cp2_demo.call_model', return_value={'text': 'null'}):
            self.assertIn('không hợp lệ', self.demo.chat('demo', 'D004 hỗ trợ'))
        with patch('cp2_demo.call_model', return_value={'text': '{"tool":[]}'}):
            self.assertIn('không hợp lệ', self.demo.chat('demo', 'D004 hỗ trợ'))
        with patch('cp2_demo.call_model', return_value={'text': '{"tool":"finish"}'}):
            self.assertIn('đủ căn cứ', self.demo.chat('demo', 'D004 hỗ trợ'))

    def test_refund_question_does_not_offer_voucher_for_active_order(self):
        self.demo.chat('demo', 'D004 khi nào hoàn tiền?')
        draft = self.store.session('demo')['draft']
        self.assertEqual(draft['proposal_vnd'], 0)
        self.assertIn('chưa ghi nhận khoản hoàn', draft['proposal'])

    def test_estimate_uses_completed_history_and_fallback(self):
        result = delivery_estimate('demo', 'S001')
        self.assertTrue(result['available'])
        self.assertEqual(result['group'], 'personal_shop')
        self.assertGreaterEqual(result['n'], 10)
        self.assertLessEqual(result['p20_minutes'], result['median_minutes'])
        self.assertLessEqual(result['median_minutes'], result['p80_minutes'])
        self.assertEqual(delivery_estimate('new_customer', 'S001')['group'], 'shop_fallback')
        self.assertFalse(delivery_estimate('demo', 'S002')['available'])
        self.assertFalse(delivery_estimate('demo', 'S001', '2026-11-01T00:00:00+07:00')['available'])

    def test_draft_survives_reopen_and_switch_order_clears_context(self):
        path = Path(self.temp.name)/'cases.sqlite3'
        self.demo.chat('demo', 'D001 tôi muốn hủy')
        self.store.receive('demo')
        self.store.close()
        self.store = CaseStore(path)
        self.demo = Demo(self.store)
        self.assertEqual(len(self.store.find('demo', 'D001')), 1)
        self.demo.chat('demo', 'D005 khi nào hoàn tiền')
        self.assertEqual(self.store.session('demo')['draft']['order_id'], 'D005')
        self.assertEqual(self.store.session('demo')['goal'], 'refund_status')


if __name__ == '__main__':
    unittest.main()
