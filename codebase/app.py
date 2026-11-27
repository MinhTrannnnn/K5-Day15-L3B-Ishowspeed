"""Bàn demo CP2 local, hai vai do người vận hành chuyển; không đăng nhập production."""
import json
import re

import tracing
from agent import Agent
from cases import CaseStore, LABELS, order_timeline, show_case

HELP = '''CP2 — AI GIẢ, DỮ LIỆU SYNTHETIC, KHÔNG GIAO DỊCH THẬT
Đang dùng khách demo. Nhập câu hỏi tự nhiên, mã đơn sẽ được nhớ trong phiên.
  /khach demo                 chuyển về khách demo (hoặc mã khách giả khác)
  /nhanvien                   bàn nhân viên do người vận hành demo chọn
  /hoso                       xem nháp đang có của khách đang chọn
  /tiepnhan                   nhân viên xác nhận lưu nháp thành ca (không tạo trùng)
  /danhsach                   nhân viên xem các ca
  /capnhat C001 1 verifying lý do       cập nhật với số phiên bản hiện tại
  /trangthai C001             khách xem ca của mình, nhân viên xem ca bất kỳ
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
    if name in ('/tiepnhan', '/capnhat', '/danhsach') and role != 'staff':
        raise ValueError('Chức năng này chỉ có ở bàn nhân viên; model không được phép duyệt.')
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
    print(HELP)
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
            tracing.begin('cp2-demo')
            try:
                if text.startswith('/'):
                    output, owner, role = command(store, owner, role, text)
                elif role == 'customer':
                    output = demo.chat(owner, text)
                else:
                    output = 'Bàn nhân viên dùng /tiepnhan, /capnhat hoặc /khach demo; gõ /help.'
                print('[DEMO CP2 — chưa giao dịch thật]\n'+output)
            except (ValueError, TypeError, KeyError, NotImplementedError) as error:
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
