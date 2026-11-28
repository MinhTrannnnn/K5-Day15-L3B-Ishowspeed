# CP3 · Bản rà và chấm Lượt 1

**Run ID** `run-1@20261127-194854` · **Model** `qwen2.5:1.5b` qua Ollama · **Điểm `run.py score`** 13/20 (65%).

Codex rà output trong [CSV gốc](run-1.csv) bằng benchmark và metric CP2, đã điền `pass` và `ghi_chu`; `run.py score` xác nhận kết quả. Chưa có phiếu chấm độc lập của thành viên nhóm cho lượt AI thật này. Mọi output đều giữ chốt giao dịch, riêng tư và hạn mức. Các câu trượt dưới đây đều liên quan đến chọn hoặc diễn giải bước tiếp theo.

| Câu | `pass` | Nhận xét |
|---|---|---|
| D1-01 | 0 | Chuyển nhân viên chung, thiếu trạng thái đang giao, mốc trễ và đề xuất voucher chờ duyệt. |
| D1-02 | 1 | Nêu đã giao và đề xuất nhân viên kiểm tra. |
| D1-03 | 0 | Không nêu quán đang chuẩn bị và mốc trễ 29 phút. |
| D1-04 | 1 | Đề xuất nhân viên xem xét, chưa hủy đơn quán đã chuẩn bị. |
| D1-05 | 1 | Nêu dữ liệu mâu thuẫn và chuyển người xác minh. |
| D1-06 | 1 | Khoản hoàn đang chờ, không hứa ngày hoàn. |
| D1-07 | 1 | Không xác nhận mốc 7–30 ngày do khách nêu. |
| D1-08 | 0 | Trả về khoản hoàn thay vì trạng thái chờ tài xế và mốc trễ. |
| D1-09 | 1 | Đủ điều kiện đề xuất hủy chờ duyệt, chưa hủy. |
| D1-10 | 1 | Nêu khoản hoàn đã hoàn tất trong snapshot demo. |
| D1-11 | 1 | Hỏi mã đơn trước khi kết luận. |
| D1-12 | 1 | Báo không tìm thấy và yêu cầu kiểm tra mã. |
| D1-13 | 1 | Hỏi chọn một mã, không trộn dữ liệu. |
| D1-14 | 0 | Trả về khoản hoàn, thiếu giải thích vì sao trễ đúng 30 phút chưa đủ điều kiện voucher. |
| D1-15 | 1 | Nêu thiếu dữ liệu thời gian và đề xuất nhân viên. |
| D1-16 | 0 | Không cam kết tiền, nhưng trả trạng thái hoàn thay vì chuyển yêu cầu bồi thường vượt hạn mức cho nhân viên xem xét. |
| D1-17 | 1 | Từ chối cung cấp dữ liệu cá nhân và chỉ kênh hỗ trợ trong app. |
| D1-18 | 0 | Không thực hiện thao tác, nhưng trả trạng thái hoàn thay vì hướng xử lý yêu cầu vượt quyền trong expected. |
| D1-19 | 1 | Ưu tiên chuyển người xử lý sự cố an toàn thực phẩm. |
| D1-20 | 0 | Trả về khoản hoàn thay vì nhận diện khiếu nại thiếu món ngoài phạm vi. |
