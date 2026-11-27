"""Bàn demo CP2 local, hai vai do người vận hành chuyển; không đăng nhập production."""
import json
import re

import tracing
from agent import Agent
from ai import MODEL_PROVIDER
from cases import CaseStore, LABELS, order_timeline, show_case

HELP = '''D1 — DỮ LIỆU SYNTHETIC, KHÔNG GIAO DỊCH THẬT
Đang dùng khách demo. Nhập câu hỏi tự nhiên, mã đơn sẽ được nhớ trong phiên.
  /khach demo                 chuyển về khách demo (hoặc mã khách giả khác)
  /nhanvien                   bàn nhân viên do người vận hành demo chọn
  /hoso                       xem nháp đang có của khách đang chọn
  /tiepnhan                   nhân viên xác nhận lưu nháp thành ca (không tạo trùng)
  /danhsach                   nhân viên xem các ca
  /capnhat C001 1 verifying lý do       cập nhật với số phiên bản hiện tại
  /trangthai C001             khách xem ca của mình, nhân viên xem ca bất kỳ
  /checklist C001             nhân viên xem trường thiếu, căn cứ và chặn duyệt
  /xacminh C001 2 DEMO-E1 ghi nhận      nhân viên ghi căn cứ xác minh
  /nhac 30                    nhân viên xem nháp nhắc ca chờ >=30 phút nội bộ
  /phanhoi C001 unresolved nội dung    khách phản hồi sau kết quả (hoặc satisfied)
  /molai C001 8 lý do         nhân viên mở lại ca để xác minh
  /tonghop                    nhân viên xem số ca có phản hồi, không thông tin cá nhân
  /eta D004                   xem ETA do nền tảng cung cấp trong snapshot demo
  /moi                       xóa ngữ cảnh/nháp của phiên; giữ lịch sử ca đã tiếp nhận
  /help                       xem hướng dẫn; /thoat để thoát
Trạng thái: received → verifying → pending_approval → in_progress → resolved.
Nhánh bổ sung: verifying → needs_info → (khách trả lời) → verifying.
Chuyển vai là thao tác của người chạy demo trên máy local, chưa có xác thực tài khoản.
'''


def case_number(value):
    if not re.fullmatch(r'C\d+', value.upper()):
        raise ValueError('Mã ca cần có dạng C001.')
    return int(value[1:])


def command(store, owner, role, text):
    parts = text.split()
    name = parts[0].lower()
    if name == '/help':
        return HELP, owner, role
    if name == '/khach' and len(parts) == 2:
        if not re.fullmatch(r'[a-zA-Z0-9_-]{1,40}', parts[1]):
            raise ValueError('Chỉ dùng mã khách giả gồm chữ/số/_/-.')
        return 'Khách demo: '+parts[1], parts[1], 'customer'
    if name == '/nhanvien':
        return 'Bàn nhân viên local. Cập nhật chỉ là mô phỏng, chưa giao dịch thật.', owner, 'staff'
    if name == '/eta' and len(parts) == 2:
        timeline = order_timeline(parts[1].upper())
        if not timeline:
            raise ValueError('Không tìm thấy mã đơn trong dữ liệu demo.')
        row = timeline[0]
        warning = ('Dữ liệu mâu thuẫn; cần nhân viên xác minh, chưa kết luận giờ giao.'
                   if not row['consistent'] else
                   'ETA là dự kiến của nền tảng tại thời điểm chụp, không bảo đảm giờ đến.')
        return ('ETA TỪ NỀN TẢNG — snapshot giả lập, không live; agent không tự dự báo.\n'
                + warning + '\n' + json.dumps(row, ensure_ascii=False, indent=2)), owner, role
    if name == '/moi':
        store.save_session(owner, {'order_id': None, 'goal': None, 'messages': [], 'draft': None})
        return 'Đã xóa ngữ cảnh/nháp; ca đã tiếp nhận vẫn được giữ.', owner, role
    if name == '/hoso':
        return json.dumps(store.session(owner).get('draft'), ensure_ascii=False, indent=2), owner, role
    if name == '/trangthai' and len(parts) == 2:
        return show_case(store.get(case_number(parts[1]), owner if role == 'customer' else None)), owner, role
    if name in ('/tiepnhan', '/capnhat', '/danhsach', '/checklist', '/xacminh', '/nhac', '/molai', '/tonghop') and role != 'staff':
        raise ValueError('Chức năng này chỉ có ở bàn nhân viên; model không được phép duyệt.')
    if name == '/checklist' and len(parts) == 2:
        return json.dumps(store.checklist(case_number(parts[1])), ensure_ascii=False, indent=2), owner, role
    if name == '/xacminh' and len(parts) >= 5:
        case = store.verify(case_number(parts[1]), int(parts[2]), parts[3], ' '.join(parts[4:]))
        return show_case(case), owner, role
    if name == '/nhac' and len(parts) == 2:
        return json.dumps(store.reminder_drafts(int(parts[1])), ensure_ascii=False, indent=2), owner, role
    if name == '/phanhoi' and len(parts) >= 4:
        if role != 'customer':
            raise ValueError('Phản hồi cần ở bàn khách, không phải đánh giá thay khách.')
        case = store.feedback(case_number(parts[1]), owner, parts[2], ' '.join(parts[3:]))
        return 'Đã ghi phản hồi của khách, chưa xác minh hoặc tự mở lại ca.\n'+show_case(case), owner, role
    if name == '/molai' and len(parts) >= 4:
        case = store.reopen(case_number(parts[1]), int(parts[2]), ' '.join(parts[3:]))
        return show_case(case), owner, role
    if name == '/tonghop':
        return json.dumps(store.feedback_summary(), ensure_ascii=False, indent=2), owner, role
    if name == '/tiepnhan':
        case, created = store.receive(owner)
        return ('Đã tiếp nhận mô phỏng.' if created else 'Đã có ca đang mở; không tạo trùng.')+'\n'+show_case(case), owner, role
    if name == '/capnhat' and len(parts) >= 5:
        case = store.update(case_number(parts[1]), int(parts[2]), parts[3], ' '.join(parts[4:]))
        return show_case(case), owner, role
    if name == '/danhsach':
        rows = store.db.execute('SELECT id,owner,order_id,status,version FROM cases ORDER BY id').fetchall()
        return '\n'.join('C%03d · %s · %s · %s · v%d' %
                         (r['id'], r['owner'], r['order_id'], LABELS[r['status']], r['version']) for r in rows) or 'Chưa có ca.', owner, role
    raise ValueError('Lệnh chưa đúng; gõ /help để xem cú pháp.')


def main():
    store = CaseStore()
    demo = Agent(store)
    owner, role = 'demo', 'customer'
    print(f'Model: {MODEL_PROVIDER}\n{HELP}')
    blank = 0
    try:
        while True:
            try:
                text = input('%s:%s> ' % (role, owner)).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return 0
            if text == '/thoat':
                return 0
            if not text:
                blank += 1
                if blank >= 2:
                    return 0
                continue
            blank = 0
            tracing.begin('d1-demo')
            try:
                if text.startswith('/'):
                    output, owner, role = command(store, owner, role, text)
                elif role == 'customer':
                    output = demo.chat(owner, text)
                else:
                    output = 'Bàn nhân viên dùng /tiepnhan, /capnhat hoặc /khach demo; gõ /help.'
                print('[DEMO D1 — chưa giao dịch thật]\n'+output)
            except (ValueError, TypeError, KeyError, RuntimeError) as error:
                print('[Chưa thực hiện] '+str(error))
            finally:
                summary, _ = tracing.end()
                print('  (model %s · gọi model %d · công cụ %d · token %d/%d)' %
                      (','.join(summary['models']) or '—', summary['model_calls'], summary['tool_calls'],
                       summary['tokens_in'], summary['tokens_out']))
    finally:
        store.close()


if __name__ == '__main__':
    raise SystemExit(main())
