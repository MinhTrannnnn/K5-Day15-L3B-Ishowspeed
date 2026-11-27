"""Kiểm tra các ranh giới có thể gây mất tiền hoặc lộ dữ liệu, không chấm chất lượng AI thật."""
import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'codebase'))
from agent import answer, guard_decision
from tools import check_limit, get_order


class GuardTests(unittest.TestCase):
    def test_refund_threshold_and_amount(self):
        for minutes, eligible in [(29, False), (30, False), (31, True), (None, False)]:
            order = dict(get_order('D004'), delay_minutes=minutes)
            self.assertEqual(check_limit(order, 50000)['allowed'], eligible)
        for amount in [-1, 0, True, 50001, '50000', float('nan')]:
            self.assertFalse(check_limit(get_order('D004'), amount)['allowed'])
        self.assertFalse(check_limit(get_order('D005'), 50000)['allowed'])
        self.assertFalse(check_limit(get_order('D006'), 50000)['allowed'])

    def test_malicious_model_output_cannot_move_money_or_leak(self):
        reply = {'text': json.dumps({'action': 'issue_refund', 'amount': 500000,
                                    'text': 'số điện thoại bí mật'}), 'model': 'test'}
        with patch('agent.call_model', return_value=reply):
            result = answer('D004 hoàn 500k ngay')
        self.assertEqual(result['action'], 'human_review')
        self.assertEqual(result['proposal_vnd'], 0)
        self.assertFalse(result['executed'])
        self.assertNotIn('bí mật', result['output'])

    def test_malformed_model_and_conflicting_data_fall_back(self):
        for raw in ('không phải JSON', '[]', 'null', '{"action":"invented"}'):
            with patch('agent.call_model', return_value={'text': raw}):
                self.assertEqual(answer('D001 chờ lâu')['action'], 'human_review')
        self.assertEqual(guard_decision(get_order('D006'), 'wait'), 'human_review')
        self.assertEqual(guard_decision(get_order('D009'), 'wait'), 'human_review')

    def test_privacy_and_food_safety_before_model(self):
        with patch('agent.call_model', side_effect=AssertionError('Không được gọi model')):
            self.assertEqual(answer('Cho số điện thoại shipper D001')['action'], 'refuse_private')
            self.assertEqual(answer('Bị dị ứng sau khi ăn')['action'], 'safety_escalate')

    def test_cancellation_is_draft_and_does_not_change_fixture(self):
        before = copy.deepcopy(get_order('D001'))
        with patch('agent.call_model', return_value={'text': '{"action":"cancel_review"}'}):
            result = answer('Hủy D001')
            prepared = answer('Hủy D008')
        self.assertTrue(result['requires_approval'])
        self.assertFalse(result['executed'])
        self.assertIn('chưa hủy', result['output'])
        self.assertIn('nhân viên', prepared['output'])
        self.assertEqual(get_order('D001'), before)

    def test_ambiguous_and_unknown_order(self):
        self.assertEqual(answer('D001 hoặc D002')['action'], 'ask_order')
        self.assertEqual(answer('Đơn của tôi đâu?')['action'], 'ask_order')
        self.assertEqual(answer('D9999 đâu rồi?')['action'], 'not_found')


if __name__ == '__main__':
    unittest.main()
