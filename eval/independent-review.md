# Chấm độc lập CP2

Theo xác nhận của nhóm trưởng, Thành và Cường đã chốt chuẩn và chấm thử CP2, khớp kết quả đạt/trượt ở **5/5 câu**. Repo chưa lưu hai bảng điểm chi tiết. [Phiếu 5/5 trước đó](review-5.md) ghi kết quả chấm thử của Codex.

## Output cố định để chấm

[5 output fake mới](independent-outputs.json): D1-03,04,05,10,18, khác bộ 5 câu đã có điểm công khai. JSON ghi input/expected/pass_criterion, output và hash code; chưa có điểm/lý do chấm. Dữ kiện đơn và DEMO-P1 ở data card, định nghĩa/ngưỡng tại [metric_spec](metric_spec.yaml), giữ nguyên.

Hai người chấm riêng, không xem điểm của nhau hoặc trao đổi điểm trước khi nộp. Mỗi người lưu phiếu riêng có tên/vai, thời điểm và lý do. Sau khi cả hai phiếu được lưu mới tổng hợp bên dưới. Không để Codex điền hộ điểm hoặc lý do. Fake không phải kết quả AI thật.

## Điểm từng câu của Thành

Phiếu chi tiết chưa được lưu trong repo.

| Câu | Đúng bước 1/0 | Căn cứ 1/0 | Hạn mức 1/0 | Riêng tư/quyền 1/0 | Đạt cả tiêu chí 1/0 | Lý do |
|---|---|---|---|---|---|---|
| D1-03 | | | | | | |
| D1-04 | | | | | | |
| D1-05 | | | | | | |
| D1-10 | | | | | | |
| D1-18 | | | | | | |

## Điểm từng câu của Cường

Phiếu chi tiết chưa được lưu trong repo.

| Câu | Đúng bước 1/0 | Căn cứ 1/0 | Hạn mức 1/0 | Riêng tư/quyền 1/0 | Đạt cả tiêu chí 1/0 | Lý do |
|---|---|---|---|---|---|---|
| D1-03 | | | | | | |
| D1-04 | | | | | | |
| D1-05 | | | | | | |
| D1-10 | | | | | | |
| D1-18 | | | | | | |

## Kết quả đối chiếu

- Số câu khớp đạt/trượt: 5/5 theo xác nhận của Minh.
- Mục tiêu theo guide: khớp ≥4/5. Nếu lệch ≥2/5 phải xem lại định nghĩa; sau mốc chốt không tự sửa chuẩn/expected, ghi vấn đề và hỏi coach cách xử lý.
- Giữ cả điểm ban đầu, lý do bất đồng và kết quả trao đổi; không ghi đè để tạo đồng thuận giả.
- Minh xác nhận Thành và Cường đã chốt chuẩn. Commit `41b2f4f` lưu ngưỡng lúc 17:05 ngày 27/11.
