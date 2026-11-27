"""Quy tắc an toàn và dựng phản hồi từ dữ kiện; dùng chung cho agent và CLI."""
import unicodedata
from tools import check_limit
from tracing import note

def normalize(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text.lower().replace('đ', 'd'))
                   if not unicodedata.combining(c))


def _result(action, message, order=None, proposal_vnd=0):
    sources = ['DEMO-P1']
    if order:
        sources.insert(0, order['order_id'])
    output = '[DEMO — dữ liệu giả lập, chưa giao dịch thật]\n' + message
    output += '\nCăn cứ: ' + ', '.join(sources) + '.'
    return {'output': output, 'action': action, 'proposal_vnd': proposal_vnd,
            'requires_approval': action in ('human_review', 'cancel_review', 'safety_escalate') or proposal_vnd > 0,
            'executed': False, 'sources': sources}


def guard_decision(order, action):
    """Chặn cả output model sai: mọi trạng thái ngoài danh sách đóng đều chuyển người."""
    if not order.get('consistent') or type(order.get('delay_minutes')) is not int:
        return 'human_review'
    status = order.get('status')
    if status == 'cancelled':
        return 'refund_status'
    if status == 'delivered':
        return 'human_review'
    if status not in ('awaiting_driver', 'preparing', 'delivering'):
        return 'human_review'
    if action not in ('wait', 'cancel_review', 'human_review', 'out_of_scope'):
        return 'human_review'
    return action


def preflight(text):
    user = normalize(text)
    if any(term in user for term in ('ngo doc', 'di ung', 'di vat')):
        return _result('safety_escalate', 'Sự cố an toàn thực phẩm cần nhân viên xử lý ngay. '
                       'Đây là đề xuất chuyển người, chưa gửi yêu cầu; nếu đang có triệu chứng cần tìm hỗ trợ y tế trực tiếp.')
    if any(term in user for term in ('so dien thoai', 'dia chi', 'sdt', 'so the')):
        return _result('refuse_private', 'Không cung cấp thông tin cá nhân của bên kia. '
                       'Bạn có thể liên hệ qua kênh hỗ trợ trong ứng dụng.')
    return None


def render_response(order, policy, action):
    action = guard_decision(order, action)
    # Model chỉ chọn action. Mọi số tiền và khẳng định hiển thị được dựng từ dữ liệu đã kiểm.
    note('D1 action sau kiểm bằng code: ' + action)
    if action == 'refund_status':
        state = order.get('refund_status')
        message = {'pending': 'Đơn đã hủy; khoản hoàn đang chờ xử lý, chưa có ngày hoàn xác nhận.',
                   'completed': 'Đơn đã hủy; dữ liệu demo ghi khoản hoàn đã hoàn tất.'}.get(
                       state, 'Đơn đã hủy; chưa đủ dữ liệu về khoản hoàn.')
        return _result(action, message + ' Nếu cần xác minh, có thể yêu cầu nhân viên; chưa gửi yêu cầu.', order)
    if action == 'human_review':
        if not order.get('consistent'):
            reason = 'Dữ liệu đơn mâu thuẫn, chưa thể xác nhận trạng thái.'
        elif type(order.get('delay_minutes')) is not int:
            reason = 'Thiếu dữ liệu thời gian trễ, chưa thể kết luận điều kiện xử lý.'
        elif order.get('status') == 'delivered':
            reason = 'Dữ liệu demo ghi đơn đã giao; khiếu nại còn lại cần nhân viên kiểm tra.'
        else:
            reason = 'Yêu cầu cần nhân viên xem xét theo chính sách demo; không tự thực hiện hoặc bồi thường vượt hạn mức.'
        return _result(action, reason + ' Đề xuất chuyển nhân viên, chưa gửi yêu cầu và chưa hủy hay hoàn tiền.', order)
    if action == 'out_of_scope':
        return _result(action, 'Yêu cầu nằm ngoài phạm vi kiểm tra đơn chờ giao. Đề xuất nhân viên xử lý; chưa thực hiện thao tác nào.', order)
    if action == 'cancel_review':
        can_cancel = (order['status'] == policy['cancel_status'] and not order['prepared'])
        message = ('Đơn đang chờ tài xế, quán chưa làm món: đủ điều kiện đề xuất hủy theo chính sách demo. '
                   'Chờ người phụ trách duyệt; chưa hủy đơn.' if can_cancel else
                   'Không thể đề xuất hủy tự động vì đơn đã được chuẩn bị hoặc đang giao. '
                   'Đề xuất chuyển nhân viên, chưa gửi yêu cầu; chưa hủy đơn.')
        return _result(action, message, order)
    labels = {'awaiting_driver': 'đang chờ tài xế', 'preparing': 'quán đang chuẩn bị', 'delivering': 'đang giao'}
    amount = policy['max_voucher_vnd']
    limit = check_limit(order, amount)
    message = ('Đơn %s %s. Giờ dự kiến ban đầu %s, cập nhật %s; trễ %d phút so với mốc ban đầu. '
               'Dữ liệu chụp tại %s; đây không phải giờ giao được bảo đảm, chưa xác nhận lý do chậm. '
               'Bạn có thể tiếp tục theo dõi hoặc yêu cầu nhân viên hỗ trợ.' %
               (order['order_id'], labels[order['status']], order['original_eta'], order['updated_eta'],
                order['delay_minutes'], order['updated_at']))
    if limit['allowed']:
        message += ' Đề xuất voucher 50.000 VND theo chính sách demo, chờ người duyệt; chưa phát hành voucher.'
    else:
        message += ' Chưa đủ điều kiện đề xuất voucher (phải trễ quá 30 phút); không bồi thường vượt hạn mức.'
    return _result(action, message, order, amount if limit['allowed'] else 0)
