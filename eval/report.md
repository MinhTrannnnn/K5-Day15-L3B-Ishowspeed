# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-194854` | 13/20 dự kiến | 65% dự kiến | 2/5 | 10/12 | 1/3 | Chưa đạt theo bản chấm nháp |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

Lượt 1 dùng Ollama `qwen2.5:1.5b`. Có 15 câu gọi model thật và 5 câu được xử lý bằng các chốt code trước khi gọi. Cả 20 câu trả output, không có lỗi kỹ thuật. Điểm trong bảng là [bản chấm nháp](cp3-run1-review.md) để người chấm duyệt. CSV gốc vẫn để trống cột `pass` và `ghi_chu`.

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
| ETA | Seed, tập tách theo thời gian, baseline, MAE/độ phủ/độ rộng khoảng/tỷ lệ đủ mẫu | Chưa có dữ liệu/chưa đo |
| Chi phí nhiều lượt | Toàn bộ model/tool calls và token theo phiên, phạm vi hạ tầng | Chưa đo |

Kết quả ETA trên dữ liệu synthetic chỉ kiểm cách tính và luồng demo, không chứng minh độ chính xác ngoài thực tế. Duyệt phương án không đồng nghĩa giao dịch thành công.
