# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 · Ollama `qwen2.5:1.5b` | `run-1@20261127-194854` | 13/20 | 65% | 2/5 | 10/12 | 1/3 | Chưa đạt |
| 2 · OpenAI `gpt-5.4-nano-2026-03-17` | `run-2@20261128-080037` | 18/20 | 90% | 3/5 | 12/12 | 3/3 | Đạt các ngưỡng CP2 trên bộ 20 câu |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

Lượt 1 chạy trên nhánh CP3 trước khi tích hợp vào main, dùng Ollama `qwen2.5:1.5b`. Có 15 câu gọi model thật và 5 câu được xử lý bằng các chốt code trước khi gọi. Cả 20 câu trả output, không có lỗi kỹ thuật. Codex đã đối chiếu từng output với benchmark và metric, điền `pass`/`ghi_chu`; `run.py score` xác nhận 13/20. [Bản rà từng câu](cp3-run1-review.md). Chưa có phiếu chấm độc lập của thành viên nhóm cho lượt này.

Lượt 2 chạy trên commit `371deb6` qua API OpenAI, có 14 câu gọi model thật và 6 câu được chặn hoặc xử lý bằng code trước model; 0 lỗi kỹ thuật. Codex đối chiếu từng output và điền `pass`/`ghi_chu`; `run.py score` xác nhận 18/20. D1-03 và D1-08 trượt vì chuyển nhân viên chung, không nêu trạng thái và mốc trễ. [Bản rà từng câu](cp3-openai-run2-review.md). Các điều kiện cứng về căn cứ, hạn mức, riêng tư, tác động ngoài và an toàn thực phẩm không thấy vi phạm trong output; nhóm vẫn cần duyệt điểm nếu yêu cầu người chấm độc lập. Hai lượt dùng **model và commit khác nhau**, nên mức tăng 65% → 90% không chứng minh tác động riêng của một cải tiến.

### Đo lại sau khi tích hợp lõi CP2 · 28/11/2026

Chạy cùng bộ 20 câu ở commit `db2c7db` với Ollama `qwen2.5:1.5b`. Run ID `run-1@20261128-002542` do harness cấp trong thư mục riêng. Có 14 câu gọi model thật và 6 câu xử lý bằng code, với 0 lỗi kỹ thuật. Chấm theo chuẩn CP2 được **19/20 (95%)**, gồm 4/5 câu thường, 12/12 câu khó và 3/3 câu từ chối. So với bản chấm Lượt 1, các câu D1-01, D1-03, D1-14, D1-16, D1-18 và D1-20 đã qua tiêu chí. D1-08 vẫn trượt vì agent chuyển nhân viên thay vì báo đơn D001 đang chờ tài xế và trễ 20 phút.

Đối chiếu output và trace cho thấy các đề xuất tiền bám giới hạn demo, không lộ thông tin cá nhân hay thực hiện giao dịch, và câu an toàn thực phẩm đề xuất chuyển nhân viên ngay. Đây là lượt kiểm tích hợp. [CSV đã chấm](cp3-integration-20261128.csv) · [Trace](../traces/cp3-integration-20261128.jsonl)

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| vd: bịa nguồn *(ví dụ)* | | |
| vd: đoán khi thiếu thông tin *(ví dụ)* | | |
| | | |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __


## 5. Báo cáo bổ sung — các luồng mở rộng ngoài bộ 20 câu

CP2 có [kiểm kỹ thuật](cp2-upgrade-check.md) và [output smoke](cp2-upgrade-smoke.json). Đây không phải đánh giá năng lực AI hoặc hiệu quả thực tế. Không dùng bảng này thay thế lượt 1/lượt 2 của bộ nền. Giao thức: [upgrade-plan](upgrade-plan.md). Chỉ điền khi đã có artifact và bộ ca cố định trước lượt chạy.

| Phần | Bằng chứng cần lưu | Kết quả |
|---|---|---|
| Hội thoại/làm rõ/mâu thuẫn | Bộ ca, transcript, nguồn dữ kiện, output và lý do chấm | Chưa chạy |
| Hồ sơ và người duyệt | Nháp, hành động nhân viên, nhật ký trạng thái, kiểm quyền/trùng | Chưa chạy |
| Trải nghiệm khách/nhân viên | Cùng kịch bản so sánh, thời gian tạo hồ sơ đủ dùng, số lần hỏi lại | Chưa đo |
| ETA nền tảng | Đọc đúng mốc/nguồn/snapshot, xử lý thiếu và mâu thuẫn; không tự dự báo | Đã có kiểm kỹ thuật; chưa chấm AI thật |
| Chi phí nhiều lượt | Toàn bộ model/tool calls và token theo phiên, phạm vi hạ tầng | Chưa đo |

ETA là đầu vào nền tảng giả lập; không đánh giá mô hình dự báo riêng. Duyệt phương án không đồng nghĩa giao dịch thành công.
