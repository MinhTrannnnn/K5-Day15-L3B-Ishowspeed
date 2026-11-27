# Demo CP2 nâng cấp — AI giả, hội thoại và hồ sơ có nhân viên duyệt

Chạy trong thư mục chứa `run.py`:

```bash
MODEL_PROVIDER=fake python3 run.py
```

Không cần key hoặc thư viện ngoài. Khung giả mô phỏng chọn công cụ theo luật, 0 token; chưa chứng minh năng lực model thật. Đây là CLI hai vai trên một máy do người vận hành chuyển, chưa có web/đăng nhập/phân quyền production.

## 1. Làm rõ và nhớ thông tin

```text
/moi
D004 tôi chờ lâu rồi
Tôi muốn hủy
/hoso
```

Lượt đầu hỏi mong muốn; lượt sau nhớ D004. Hồ sơ ghi lời khách riêng với snapshot, chính sách và đề xuất. D004 đã chuẩn bị/đang giao nên chưa đủ điều kiện đề xuất hủy theo DEMO-P1; nhân viên cần xem xét. Chưa có ca được gửi hoặc giao dịch thật.

## 2. Nhân viên tiếp nhận và cập nhật từng bước

```text
/nhanvien
/tiepnhan
/danhsach
```

Dùng đúng mã ca và số phiên bản được in ra. Với database mới hoàn toàn, ca đầu là C001 v1:

```text
/capnhat C001 1 verifying Đang xác minh yêu cầu của khách
/capnhat C001 2 pending_approval Đã tổng hợp hồ sơ để người phụ trách xem xét
/capnhat C001 3 in_progress Đã duyệt phương án xử lý mô phỏng, chưa có giao dịch thật
/capnhat C001 4 resolved Đã ghi nhận kết quả mô phỏng và phản hồi cho khách
/khach demo
/trangthai C001
```

Nhân viên phải nhập lý do/phản hồi. Mọi cập nhật có người, thời điểm và phiên bản; bước sai hoặc phiên bản cũ bị chặn. Kết quả mô phỏng không đổi snapshot đơn hoặc số dư nào.

## 3. Mâu thuẫn và yêu cầu bổ sung

```text
/moi
D007 tôi chưa nhận món, cần hỗ trợ
/nhanvien
/tiepnhan
```

Agent giả giữ riêng trạng thái hệ thống “delivered” và lời khách “chưa nhận”, đề xuất xác minh, không kết luận khách hay tài xế sai. Lấy mã ca mới từ output, ví dụ C002:

```text
/capnhat C002 1 verifying Đang đối chiếu thông tin giao nhận
/capnhat C002 2 needs_info Bạn đã kiểm tra khu vực nhận hàng chưa?
/khach demo
Tôi đã kiểm tra khu vực nhận hàng, chưa thấy món
/trangthai C002
/nhanvien
/capnhat C002 4 verifying Đã nhận thông tin bổ sung, tiếp tục xác minh
```

Lời bổ sung được ghi là phản ánh khách, không tự thành dữ kiện xác nhận. Nhân viên chưa thể chuyển từ needs_info về verifying khi khách chưa trả lời. Cùng khách/đơn đang có ca mở thì dùng lại ca, không tạo trùng. Bản demo gom theo khách + đơn; phân biệt nhiều loại khiếu nại độc lập cùng đơn còn là giới hạn.

## 4. Đơn hủy và khoản hoàn

```text
/khach refund_demo
D005 tôi muốn kiểm tra khoản hoàn
```

Hiển thị `pending` theo snapshot; chưa có ngày hoàn xác nhận hoặc thực hiện khoản hoàn mới.

## 5. Đọc ETA do nền tảng cung cấp

```text
/khach demo
/eta D004
/eta D006
/eta D009
```

D004 hiển thị ETA ban đầu 11:59, cập nhật 12:45 và snapshot 12:30 ngày 27/11/2026 UTC+07; đây là giờ dự kiến từ nền tảng giả lập, không bảo đảm giờ giao. D006 cảnh báo dữ liệu mâu thuẫn; D009 giữ nguyên thời gian ban đầu/độ trễ bị thiếu, không tự điền.

Không có lệnh /shop hoặc công cụ tự dự báo thời gian giao. Chưa kết nối API nền tảng thật. Nhân viên cập nhật ca chỉ thay tiến độ xử lý, không thay ETA hãng hoặc tự cập nhật snapshot đơn.

## Kiểm và lưu trữ

```bash
python3 run.py check
MODEL_PROVIDER=fake python3 -m unittest discover -s tests -v
```

Phiên, nháp, ca và sự kiện lưu trong `data/runtime/cp2.sqlite3`, được gitignore, còn sau khi thoát. `/moi` chỉ xóa ngữ cảnh/nháp của khách, không xóa ca đã lưu. Muốn xem mã/phiên bản hiện tại dùng `/danhsach` ở bàn nhân viên. Không sửa artifact đánh giá đã chạy để làm sạch demo.

CLI và `answer(text)` của harness cùng gọi `Agent.chat` trong `agent.py`; harness tạo phiên RAM độc lập mỗi input. Không có lệnh quay lại bản cũ. Benchmark/metric CP2 v1 giữ nguyên. [Kết quả kiểm kỹ thuật CP2](../eval/cp2-upgrade-check.md) tách khỏi phiếu 5/5 cũ và kết quả model thật.

## 6. Checklist, nhắc ca và phản hồi sau xử lý — đã có ở CP2

Ở bàn nhân viên, dùng mã ca và số phiên bản hiện tại:

```text
/checklist C001
/nhac 30
```

Checklist chỉ đọc; thiếu trường/nguồn, số tiền trái chính sách hoặc thông tin chưa xác minh thì không cho chuyển sang `pending_approval`, `in_progress`, `resolved`. Nhân viên vẫn có thể tiếp nhận và xác minh để giải quyết phần thiếu. Với ca mâu thuẫn hoặc thiếu thời gian, sau khi kiểm chứng mô phỏng, ghi mã căn cứ và nhận định ở bước `verifying`:

```text
/xacminh C002 5 DEMO-E1 Đã đối chiếu thông tin mô phỏng, cần người xử lý, chưa kết luận bên có lỗi
```

Lệnh tăng version; đọc số mới trước `/capnhat`. Ghi nhận xác minh không sửa snapshot hoặc cho phép voucher khi dữ kiện không đủ. Ở kịch bản C002 phần 3, sau `/capnhat C002 4 verifying ...`, ca là v5; `/xacminh` đưa lên v6.

`/nhac 30` trả các nháp ca chưa có kết quả chờ ít nhất 30 phút từ lần đổi trạng thái cuối. Ngưỡng nội bộ, không phải SLA hãng; không tự gửi hoặc chạy lịch nền. Xem lại trả cùng khóa nháp, không thêm sự kiện. Mới tạo ca sẽ chưa có nháp quá ngưỡng; unit test dùng đồng hồ giả để kiểm mà không sửa timestamp thật của ca.

Sau khi ca có kết quả:

```text
/khach demo
/phanhoi C001 unresolved Tôi vẫn chưa thấy vấn đề được xử lý
/nhanvien
/tonghop
/molai C001 6 Đã đọc phản hồi, cần xác minh tiếp
```

C001 ở kịch bản phần 2 là v5 sau khi có kết quả; phản hồi khách đưa lên v6. Đổi mã/version theo output khi chạy trên DB đã có ca. Phản hồi chỉ là lời khách chưa xác minh, không tự mở lại. Nhân viên mở lại thì về `verifying`; kiểm checklist và ghi căn cứ mới khi còn cảnh báo. Tổng hợp chỉ đếm phản hồi mới nhất mỗi ca, không hiển thị nội dung/định danh hoặc kết luận shop có lỗi.
