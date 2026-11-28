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

## Đối chiếu CP3 ngoài video

| Yêu cầu trong `02-guide.md` | Kết quả kiểm |
|---|---|
| Bằng chứng pain: ít nhất một nguồn đạt ngưỡng và ít nhất năm trích dẫn/ví dụ | Mẫu App Store 31 dòng có cách chọn, quy tắc nhãn, x/N và năm cụm nguyên văn đã đối chiếu lại trên trang nguồn ngày 28/11. Mẫu Google Play 400 review chưa lưu đủ review gốc và nhãn từng dòng; chưa có phỏng vấn hoặc khảo sát đủ ngưỡng. Mẫu App Store là mẫu lời phàn nàn, không đại diện mọi người dùng. |
| Bảng impact chọn trong ít nhất ba hướng, có số và nguồn/nhãn ước tính | `spec.md` §2 nay có ba hướng và phép tính impact cho mỗi hướng, toàn bộ đầu vào thiếu nguồn đều đánh dấu *tự ước tính*. Chưa đo impact thực tế hoặc đủ căn cứ để dự báo kinh tế. |
| Bộ 20–30 câu; ít nhất năm khó, hai từ chối; ít nhất 1/3 từ người dùng/data thật | `run.py check` qua: 20 câu, 12 khó, 3 từ chối, 7/20 gắn nhãn `data_that`. Nguồn của bảy câu còn cần kiểm độc lập nên tỷ lệ 1/3 dữ liệu thật chưa thể xác nhận chắc chắn. |
| Bản chạy thử dùng model thật, có dữ liệu/công cụ, chặn rủi ro | OpenAI `eval --try` qua 3/3 có token; `eval` qua 20/20 không lỗi. 25 test kỹ thuật qua. `simulate --try` qua 10/10; `simulate` qua 50/50 phiên với 0 lỗi và có token API thật. Cấu hình `cost/personas.yaml` còn persona, quy mô và bảng giá ví dụ, nên mô phỏng chỉ xác nhận luồng kỹ thuật, chưa phải kết luận chi phí CP4. |
| Lượt 1 có run ID, token, chấm `pass` và `score` | Cả `eval/run-1.csv` và `eval/run-2.csv` đã được Codex chấm hai cột được phép; `run.py score` lần lượt ra 13/20 và 18/20. Chưa có chấm độc lập của thành viên nhóm cho hai lượt AI thật. |
| `spec.md` §0–§7 đã commit | Có trong lịch sử Git; lần commit cuối của file là `354e6c6` ngày 28/11/2026 00:08 +07. |

Lượt tích hợp Ollama 19/20 trong [report.md](report.md) chạy ở commit `db2c7db`, khác commit của lượt OpenAI này; chênh lệch 19/20 và 18/20 chưa thể quy riêng cho model. Không sửa benchmark, metric hay chuẩn đạt; trong hai CSV đánh giá chỉ điền `pass` và `ghi_chu` theo quy định. [Lượt mô phỏng 50 phiên](../cost/simulate-1-summary.md) dùng cấu hình ví dụ, không dùng bảng chi phí đó để nộp CP4.

## Việc nhóm cần xác nhận hoặc tự nộp

- [Video CP3](../artifacts/cp3-demo-thuyet-minh.mp4) có trong repo. Nhóm cần tải lên YouTube ở chế độ Không công khai hoặc Drive cho người có link, thử mở khi đăng xuất và điền link vào Form 2; repo không xác nhận được trạng thái chia sẻ và nộp form.
- Ba tình huống benchmark dẫn từ Google Play thiếu bản lưu review gốc có thể tái kiểm. Nhóm cung cấp snapshot/nguồn từng dòng để xác nhận chắc chắn mốc ít nhất 1/3 câu từ dữ liệu thật; không sửa câu thử hoặc nhãn nguồn sau khi đã chạy để hợp thức hóa kết quả.
- Điểm hai lượt đã được Codex chấm; Thành và Cường cần đọc output và xác nhận nếu nhóm muốn có phiếu chấm độc lập. Các sửa đổi CP3 hiện tại cần được nhóm rà và commit trước khi nộp.
