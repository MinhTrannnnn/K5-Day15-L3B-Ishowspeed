# Hồ sơ chấm CP2 và phiếu độc lập còn thiếu

Theo xác nhận của nhóm trưởng, Thành và Cường đã chốt chuẩn và đồng ý với kết quả **5/5 câu đạt** do Codex chấm thử trong [phiếu trước đó](review-5.md). Repo không lưu hai bảng điểm của hai người trước khi họ xem hoặc trao đổi kết quả, nên chưa thể tự kiểm mức khớp của hai lượt chấm độc lập. Bộ 5 output dưới đây là bộ bổ sung và chưa được chấm.

## Output cố định để chấm

[5 output fake mới](independent-outputs.json): D1-03,04,05,10,18, khác bộ 5 câu đã có điểm công khai. JSON ghi input/expected/pass_criterion, output và hash code; chưa có điểm/lý do chấm. Dữ kiện đơn và DEMO-P1 ở data card, định nghĩa/ngưỡng tại [metric_spec](metric_spec.yaml), giữ nguyên.

Khi chấm bộ output bổ sung, hai người chấm riêng, không xem điểm của nhau hoặc trao đổi điểm trước khi nộp. Mỗi người lưu phiếu riêng có tên/vai, thời điểm và lý do. Chỉ tổng hợp sau khi cả hai phiếu được lưu. Không để Codex điền hộ điểm hoặc lý do. Fake không phải kết quả AI thật.

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

## Kết quả đối chiếu bộ output bổ sung

- Chưa có kết quả đối chiếu: hai bảng điểm phía trên chưa được điền. Xác nhận 5/5 của Minh nói về phiếu chấm thử trước đó, không chứng minh bộ output bổ sung đã được chấm độc lập.
- Mục tiêu theo guide: khớp ≥4/5. Nếu lệch ≥2/5 phải xem lại định nghĩa; sau mốc chốt không tự sửa chuẩn/expected, ghi vấn đề và hỏi coach cách xử lý.
- Giữ cả điểm ban đầu, lý do bất đồng và kết quả trao đổi; không ghi đè để tạo đồng thuận giả.
- Minh xác nhận Thành và Cường đã chốt chuẩn. Commit `41b2f4f` lưu ngưỡng lúc 17:05 ngày 27/11.
