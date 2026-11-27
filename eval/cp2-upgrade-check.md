# Kiểm kỹ thuật CP2 nâng cấp — 27/11/2026

**Phạm vi:** khung fake/synthetic, chưa gọi AI thật. Không thay thế chuẩn CP2 v1, phiếu 5/5 cũ hoặc đánh giá run-N. Code mới do Codex kiểm, chưa có xác nhận các thành viên đã rà bản mới.

## Kết quả đã chạy

| Kiểm | Kết quả | Bằng chứng |
|---|---|---|
| Cấu trúc BTC | Không thấy vấn đề; 20 câu, 4 metric, 4 thành viên | `python3 run.py check` |
| Unit test cũ và mới | 14 test qua, gồm 6 test chốt cũ và 8 test hành vi mới | `MODEL_PROVIDER=fake python3 -m unittest discover -s tests -v`; `tests/test_d1.py`, `tests/test_agent.py` |
| Tích hợp CLI | Làm rõ → nhớ mục tiêu/đơn → nháp → nhân viên tiếp nhận → xác minh/duyệt/kết quả → khách xem → ETA | [Lệnh và output smoke](cp2-upgrade-smoke.json), chạy database tạm độc lập, không sửa trạng thái demo người dùng |

Test mới kiểm việc không tự lưu ca trước người duyệt, không tạo trùng, không cho lệnh khách duyệt hoặc đọc ca khác, chặn phiên bản cũ/bước sai, yêu cầu bổ sung và lưu lời khách riêng, hồ sơ còn sau mở lại DB, không lẫn mục tiêu khi đổi đơn. Kiểm fake planner không gọi được công cụ ghi hoặc kết thúc thiếu căn cứ. ETA có đủ mẫu cá nhân, fallback shop, thiếu mẫu và lọc thời điểm.

## Các giới hạn còn lại

- Fake planner dùng luật và thứ tự công cụ mô phỏng; không phải năng lực suy luận agent thật. Hồ sơ/lời hỏi dựng bằng code.
- CLI hai vai local do người vận hành chuyển, chưa có web, đăng nhập hoặc phân quyền production. Không có giao dịch, gửi tin, hủy/hoàn thật.
- Chống ca trùng hiện theo khách + đơn; chưa phân biệt nhiều loại khiếu nại độc lập cùng đơn.
- Timeline chỉ chứa mốc có trong snapshot; không bịa lịch sử đổi ETA chi tiết không tồn tại.
- ETA là phân vị thực nghiệm từ 120 đơn tự dựng, chưa xét khung giờ/khoảng cách, chưa có holdout/MAE hoặc bằng chứng cải thiện thực tế.
- Chưa có nghiên cứu bổ sung để xác nhận toàn bộ pain mới hoặc phép đo thời gian hỗ trợ tiết kiệm.

Cách tái kiểm và thao tác: [kịch bản CP2](../docs/cp2-demo.md). Chuẩn/benchmark/metric và artifact CP2 v1 giữ nguyên; CP3 chưa triển khai.


## Kiểm sau khi hợp nhất về một lõi

- `Agent.chat` trong `agent.py` phục vụ cả CLI và adapter `answer(text)`; không còn module điều phối riêng hoặc lệnh quay về bản trước.
- 15 test qua, gồm kiểm adapter tạo phiên độc lập và không ảnh hưởng ca CLI đã lưu. Quy tắc ở `policy.py`, lưu ca/ETA ở `cases.py`; tên test hiện tại là `tests/test_agent.py`.
- Tái chạy tích hợp CLI trên database tạm: làm rõ → nháp → nhân viên tiếp nhận/cập nhật → kết quả → khách xem → ETA, không có lỗi.
- Tái chạy trực tiếp 20 input benchmark: đều trả đúng hợp đồng, action khớp action kỳ vọng và `executed=False`. Đây chỉ là kiểm kỹ thuật fake, chưa chấm đầy đủ bốn metric hoặc AI thật.
- Output smoke liên kết phía trên thuộc lần chạy trước được giữ nguyên làm bằng chứng lịch sử, không sửa lại để giả thành lần chạy trên code hiện tại.
