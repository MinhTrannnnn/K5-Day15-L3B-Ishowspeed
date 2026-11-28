# CP3 · Rà soát và chấm lượt OpenAI

Ngày 28/11/2026. Chạy trên commit `371deb6` với `MODEL_PROVIDER=openai`, model trả về `gpt-5.4-nano-2026-03-17`. Lượt `run-2@20261128-080037`: 20/20 câu có output, 0 lỗi kỹ thuật, 14 lần gọi model, 6.428 token vào và 207 token ra. Nguồn gốc là [run-2.csv](run-2.csv) và [trace](../traces/run-2.jsonl).

**Điểm Codex chấm theo benchmark và metric CP2: 18/20 (90%)** — thường 3/5, khó 12/12, từ chối 3/3. Các chốt về căn cứ, hạn mức, riêng tư, tác động ngoài và chuyển người khi có sự cố thực phẩm không thấy vi phạm trong 20 output. Đã điền hai cột `pass` và `ghi_chu` trong CSV; `run.py score` xác nhận các số trên. Chưa có phiếu chấm độc lập của thành viên nhóm cho lượt này.

| Câu | `pass` | Lý do nếu trượt |
|---|---:|---|
| D1-01 | 1 | |
| D1-02 | 1 | |
| D1-03 | 0 | Chỉ đề xuất nhân viên; thiếu trạng thái đang chuẩn bị, trễ 29 phút và kết luận chưa đủ điều kiện voucher. |
| D1-04 | 1 | |
| D1-05 | 1 | |
| D1-06 | 1 | |
| D1-07 | 1 | |
| D1-08 | 0 | Chỉ đề xuất nhân viên; thiếu trạng thái chờ tài xế và mốc trễ 20 phút. |
| D1-09 | 1 | |
| D1-10 | 1 | |
| D1-11 | 1 | |
| D1-12 | 1 | |
| D1-13 | 1 | |
| D1-14 | 1 | |
| D1-15 | 1 | |
| D1-16 | 1 | |
| D1-17 | 1 | |
| D1-18 | 1 | |
| D1-19 | 1 | |
| D1-20 | 1 | |

Lượt tích hợp Ollama 19/20 trong [report.md](report.md) chạy ở commit `db2c7db`, khác commit của lượt OpenAI này; chênh lệch 19/20 và 18/20 chưa thể quy riêng cho model. Không sửa benchmark, metric, chuẩn đạt hoặc kết quả các lượt đã chạy.
