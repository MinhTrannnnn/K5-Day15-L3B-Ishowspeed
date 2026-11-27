# Data card — D1 · CP2 v1 · 27/11/2026

## 1. Bằng chứng tham khảo: review ứng dụng

| Thuộc tính | Nội dung |
|---|---|
| Mục đích | Khám phá pain và lấy tình huống cho câu thử; không đưa review vào công cụ tra đơn |
| Nguồn | Review công khai trên Google Play và mẫu đối chiếu từ App Store. Cách lấy mẫu và nguồn gốc được ghi trong [báo cáo Google Play](../evidence/data-mining.md) và [báo cáo App Store](../evidence/data-mining-app-store-31.md) |
| Quy mô tài liệu báo cáo | 400 review Google Play (100/app, 4 app) và mẫu đối chiếu 31 phàn nàn nguồn App Store; không cộng hai mẫu thành tỷ lệ chung |
| Xử lý đã ghi trong tài liệu | Google Play mới nhất, vi/VN, mọi sao; nhãn theo sự cố; tách khách/quán; GrabFood là tập con 12/100. Mẫu App Store từ trang tổng hợp thiên về phản hồi tiêu cực |
| Tình trạng xác minh | Lượt CP2 không thu thập review mới. Chưa có snapshot đủ 400 dòng, chưa đối chiếu độc lập nguồn; không tuyên bố đủ ngưỡng bằng chứng CP3 |
| Ẩn danh | Chỉ giữ mã review, ngày, nhãn và ví dụ; không tên, email, điện thoại, địa chỉ người viết |
| Giới hạn | Ví dụ Google Play là diễn giải. Tỷ lệ review không phải tỷ lệ người dùng hoặc số đơn; không suy ra số phút tìm hỗ trợ |

## 2. Dữ liệu chạy thử — synthetic

| Thuộc tính | Nội dung |
|---|---|
| File | `data/demo_orders.json` và `data/demo_policy.json` |
| Quy mô | 10 snapshot đơn giả, 1 chính sách dựng DEMO-P1; không dữ liệu cá nhân hoặc giao dịch thật |
| Nguồn | Nhóm tự dựng với Codex, không sao chép chính sách chính thức |
| Sinh lại | `python3 data/build_demo.py`; seed `27112026`, phiên bản `d1-cp2-v1` |
| Thời gian | Snapshot cố định tại 12:30 ngày 27/11/2026 UTC+07, không phải trạng thái live. `delay_minutes` tính so mốc giao ban đầu |
| Biến thể | Chờ tài xế, đang chuẩn bị, đang giao, đã giao, đã hủy; trễ 29/30/31 phút; thiếu dữ liệu; mâu thuẫn; khoản hoàn pending/completed |
| Chính sách | Trễ **quá** 30 phút mới đề xuất voucher, tối đa 50.000 VND; hủy chỉ đề xuất khi chờ tài xế và quán chưa làm món; mọi tác động chờ người duyệt |
| Kiểm | Codex chạy kiểm tra ranh giới bằng code và smoke test luồng. Chưa có log kiểm tay của thành viên |
| Giới hạn | Dữ liệu giả không làm bằng chứng pain; không xác thực tài khoản thật, không kết nối sàn, không thực hiện hủy/hoàn/gửi tin |

## 3. Bộ câu thử — `eval/benchmark.csv`

- Phiên bản CP2 v1: **20 câu**, 5 `thuong`, 12 `kho`, 3 `tu_choi` (3 tấn công).
- **7/20 câu `data_that`** dẫn xuất từ 7 tình huống trong tài liệu review cung cấp: SF054, GF071, GF006, R16, R18, R07, R24. Đây là diễn giải để thử trên demo, **không phải lời nguyên văn của khách**; nguồn gốc vẫn chờ kiểm lại.
- **13/20 câu `tu_viet`** do Codex soạn từ lưới phủ do thiết kế quy định trong `eval/README.md`. Không gán nhãn `nguoi_dung` cho câu tự viết.
- Mã đơn, trạng thái, số phút gắn vào mọi input đều là synthetic. Tình huống gốc và phần biến đổi được ghi trong cột `source`.
- Đây là bộ thiết kế nhìn thấy được, chưa có test holdout độc lập. Model/công cụ không đọc benchmark hoặc expected khi chạy.
- Người phụ trách kiểm nguồn: Nguyễn Hải Quang; kiểm chéo Nguyễn Văn Cường. Chưa ghi nhận kiểm độc lập đã hoàn tất.


## 4. Dữ liệu khung có phiên và ETA nền tảng giả lập

- Phiên, nháp, ca và sự kiện lưu tại `data/runtime/cp2.sqlite3` khi chạy CLI, được gitignore. Chỉ dùng mã khách/đơn giả; lời khách và dữ kiện snapshot giữ riêng. Chưa có ghi chú nội bộ hoặc nhiều loại ca độc lập cùng đơn.
- ETA lấy từ `data/demo_orders.json`: `original_eta`, `updated_eta`, `updated_at`, `delay_minutes` và `consistent`. Đây là dữ liệu mô phỏng nền tảng cung cấp, không phải đầu ra dự báo của nhóm.
- `order_timeline` chỉ đọc và gắn `eta_source=platform_demo_snapshot`, `live=False`; không điền giá trị thiếu. Độ trễ trong fixture so với ETA ban đầu, không tính lại theo giờ máy hiện tại.
- Không tạo mốc đổi ETA hoặc lý do chậm không tồn tại trong snapshot. Thiếu thời gian/mâu thuẫn chuyển nhân viên xác minh; không tự đưa giờ giao mới.
- Đã bỏ dữ liệu/generator 120 lịch sử đơn phục vụ hướng dự báo trước đây. Kết quả thử nghiệm đã lưu giữ nguyên làm lịch sử, không đại diện phạm vi hiện tại. Dữ liệu đơn, chính sách, benchmark và metric nền không đổi.

Quang kiểm nguồn/đặc tả; Thành kiểm công cụ đọc và kho ca; Cường kiểm thiếu/mâu thuẫn và đầu ra có căn cứ; Minh tích hợp hội thoại. [Spec §4.3](../spec.md), [kiểm bổ sung](../eval/upgrade-plan.md).


## 5. Trạng thái xác minh 7 câu gắn nhãn data_that

Máy check chỉ đếm nhãn; 7/20 không tự chứng minh nguồn thật. Các mã SF054, GF071, GF006, R16, R18, R07, R24 cần đối chiếu bảng nguồn, link, ngày lấy và đoạn gốc ẩn danh từng câu. Ví dụ Google Play hiện là diễn giải, toàn mẫu chưa lưu đủ; chưa xác nhận đạt yêu cầu ≥1/3 nguồn thật. Không đổi nhãn/expected hoặc bịa bản gốc để đạt tỷ lệ.

Phần mở rộng chỉ thêm trường hồ sơ `session_id`, `policy_version`, sự kiện nhân viên xác minh có `evidence_ref`, lời khách phản hồi `verified=False` và sự kiện mở lại. Nháp nhắc ca đọc timestamp sự kiện trạng thái, không dùng/đổi timestamp ETA, không ghi hoặc gửi nhắc tự động. Tất cả là dữ liệu demo, không bằng chứng pain.
