"""Kiểm các hành vi mới: quyền, duyệt, bộ nhớ, trùng ca và ETA từ nền tảng."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'codebase'))
from agent import Agent, answer
from cases import CaseStore, order_timeline
from app import command


class CP2DemoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = CaseStore(Path(self.temp.name)/'cases.sqlite3')
        self.demo = Agent(self.store)

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

    def test_benchmark_calls_are_isolated_from_cli_sessions(self):
        self.demo.chat('demo', 'D004 tôi muốn hủy')
        self.store.receive('demo')
        first = answer('D001 tôi muốn hủy')
        second = answer('D005 khi nào hoàn tiền?')
        missing = answer('Tôi muốn hủy')
        self.assertEqual(first['action'], 'cancel_review')
        self.assertEqual(second['action'], 'refund_status')
        self.assertEqual(missing['action'], 'ask_order')
        self.assertEqual(first['draft']['order_id'], 'D001')
        self.assertEqual(second['draft']['order_id'], 'D005')
        self.assertEqual(self.store.session('demo')['draft']['order_id'], 'D004')
        self.assertEqual(len(self.store.find('demo', 'D004')), 1)
        self.assertEqual(self.store.find('demo', 'D001'), [])

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
        self.assertIn('nhân viên kiểm tra', draft['proposal'])
        self.assertIn('nhận món chưa', self.demo.chat('other', 'D007 cần hỗ trợ'))

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
        self.store.update(cid, 4, 'verifying', 'Đã nhận bổ sung')
        self.store.verify(cid, 5, 'DEMO-EVIDENCE', 'Nhân viên ghi nhận đã đối chiếu mô phỏng; chưa quy lỗi bên nào')
        for version, status in [(6, 'pending_approval'), (7, 'in_progress'), (8, 'resolved')]:
            case = self.store.update(cid, version, status, 'Kết quả thao tác mô phỏng: '+status)
        self.assertEqual(case['status'], 'resolved')
        self.assertFalse(case['body']['executed'])

    def test_malicious_planner_cannot_run_mutation_and_loop_is_bounded(self):
        reply = {'text': json.dumps({'tool': 'issue_refund'})}
        with patch('agent.call_model', return_value=reply) as model:
            self.assertIn('không hợp lệ', self.demo.chat('demo', 'D004 hỗ trợ'))
            self.assertEqual(model.call_count, 1)
        self.assertEqual(self.store.find('demo', 'D004'), [])
        with patch('agent.call_model', return_value={'text': 'null'}):
            self.assertIn('không hợp lệ', self.demo.chat('demo', 'D004 hỗ trợ'))
        with patch('agent.call_model', return_value={'text': '{"tool":"finish"}'}):
            self.assertIn('đủ căn cứ', self.demo.chat('demo', 'D004 hỗ trợ'))

    def test_eta_reads_platform_snapshot_without_predicting(self):
        row = order_timeline('D004')[0]
        self.assertEqual(row['original_eta'], '11:59')
        self.assertEqual(row['updated_eta'], '12:45')
        self.assertEqual(row['delay_minutes'], 31)
        self.assertEqual(row['eta_source'], 'platform_demo_snapshot')
        self.assertFalse(row['live'])
        output, _, _ = command(self.store, 'demo', 'customer', '/eta D004')
        self.assertIn('agent không tự dự báo', output)
        self.assertIn('không bảo đảm', output)
        with self.assertRaises(ValueError):
            command(self.store, 'demo', 'customer', '/eta D9999')

    def test_eta_conflicting_and_missing_data_are_not_filled_in(self):
        output, _, _ = command(self.store, 'demo', 'customer', '/eta D006')
        self.assertIn('mâu thuẫn', output)
        self.assertIn('chưa kết luận', output)
        row = order_timeline('D009')[0]
        self.assertIsNone(row['original_eta'])
        self.assertIsNone(row['delay_minutes'])
        result = answer('D009 thời gian giao không rõ')
        self.assertEqual(result['action'], 'human_review')
        self.assertEqual(result['proposal_vnd'], 0)

    def test_draft_survives_reopen_and_switch_order_clears_context(self):
        path = Path(self.temp.name)/'cases.sqlite3'
        self.demo.chat('demo', 'D001 tôi muốn hủy')
        self.store.receive('demo')
        self.store.close()
        self.store = CaseStore(path)
        self.demo = Agent(self.store)
        self.assertEqual(len(self.store.find('demo', 'D001')), 1)
        self.demo.chat('demo', 'D005 khi nào hoàn tiền')
        self.assertEqual(self.store.session('demo')['draft']['order_id'], 'D005')
        self.assertEqual(self.store.session('demo')['goal'], 'refund_status')


if __name__ == '__main__':
    unittest.main()
