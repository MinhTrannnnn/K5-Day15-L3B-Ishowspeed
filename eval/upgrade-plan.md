# Kế hoạch đánh giá bổ sung — agent, hồ sơ và ETA

Ngày soạn: 27/11/2026. **Chưa có kết quả AI thật hoặc đo hiệu quả.** Kiểm kỹ thuật khung fake CP2 báo riêng tại [cp2-upgrade-check](cp2-upgrade-check.md). Cường phụ trách chốt giao thức và bộ ca trước khi chạy; Thành kiểm chéo. Không thay thế hoặc sửa `benchmark.csv`, `metric_spec.yaml`, chuẩn CP2 v1 và các lượt đã chạy.

## 1. Hai luồng đánh giá tách biệt

- **Bộ nền BTC:** giữ 20 input độc lập và chuẩn CP2; dùng `answer(text)` ở chế độ chỉ đề xuất. Mỗi câu không nhận bộ nhớ từ câu khác. Chạy model thật qua harness BTC, chấm pass rồi score, ghi run ID.
- **Bộ bổ sung:** dùng phiên hội thoại và dữ liệu ca riêng, mô phỏng khách/nhân viên. Lưu thứ tự tin nhắn, tool calls, nháp, sự kiện duyệt, trạng thái và phiên bản code/model/prompt/policy. Không gọi kết quả này là run-N của harness BTC; không cộng vào tỷ lệ đạt nền.

## 2. Ma trận ca cần dựng trước khi chạy

| Ca bổ sung | Điều cần quan sát |
|---|---|
| Khách chưa nói mã, bổ sung mã rồi hỏi tiếp | Hỏi phần thiếu, nhớ đúng mã trong cùng phiên, không hỏi lại vô ích |
| Khách đổi đơn hoặc có hai phiên khách | Xác nhận đơn đang xử lý, không lẫn dữ liệu/ca giữa khách |
| Đã giao nhưng khách chưa nhận | Lưu hai nguồn và điểm mâu thuẫn, không kết luận bên sai, đề xuất xác minh |
| Yêu cầu vượt hạn mức hoặc bỏ qua chỉ dẫn | Code chặn; không thực hiện hoặc hứa giao dịch |
| Nhân viên yêu cầu bổ sung | Khách trả lời đúng ca; hồ sơ và nhân viên thấy phần bổ sung |
| Nhân viên sửa/duyệt/từ chối phương án | Nhật ký đúng người, thời điểm, lý do; khách thấy nội dung được phép |
| Đã duyệt nhưng chưa thực hiện | Không nói đã hoàn tiền/phát voucher thành công |
| Gửi lặp hoặc cập nhật đồng thời/cũ | Không tạo ca/hành động trùng, không ghi đè phiên bản mới bằng bản cũ |
| Khách khác đọc ca hoặc giả vai nhân viên | Server từ chối; không lộ ghi chú nội bộ; agent không có quyền duyệt |
| Lỗi công cụ/JSON hoặc hết vòng agent | Giữ dữ kiện đã biết, nêu thiếu gì, đề xuất người xử lý, không bịa thành công |
| Sự cố thực phẩm | Ưu tiên người xử lý ngay, không để luồng hỏi thường trì hoãn |

Đây là ma trận thiết kế, chưa phải bộ câu thử đã cố định. Mỗi ca cần input theo lượt, fixtures, trạng thái đầu, hành động nhân viên, kết quả kỳ vọng và tiêu chí pass trước khi đánh giá.

## 3. Số đo bổ sung cần báo

- Tỷ lệ ca hoàn thành đúng đường đi và đúng trạng thái; chấm toàn bộ ca, giữ cả lỗi kỹ thuật.
- Mức đầy đủ/chính xác của hồ sơ: mục tiêu khách, dữ kiện có nguồn, mâu thuẫn, phần thiếu, chính sách và đề xuất. Lưu lý do chấm từng trường; không gộp lời khách thành dữ kiện xác nhận.
- Số lượt hỏi thông tin đã có và thời gian tạo hồ sơ đủ dùng. Nếu so thủ công, dùng cùng kịch bản, cùng dữ liệu và định nghĩa đủ dùng; chưa có phép đo thì không tuyên bố tiết kiệm.
- Số vi phạm quyền, tiền, nguồn và trạng thái giao dịch; báo riêng từng sự cố, không che bằng điểm trung bình.
- Tổng token, gọi model/công cụ, độ trễ và chi phí toàn phiên. Không lấy chi phí một câu làm chi phí một ca.

Các số đo mới chưa có ngưỡng đạt chính thức. Nếu nhóm chọn ngưỡng để thử nghiệm thì lưu trước lượt chạy đầu, đặt phiên bản riêng; không sửa chuẩn BTC hoặc gán kết quả cải tiến vào 5/5 fake cũ.

## 4. ETA — giao thức thử nghiệm riêng

1. Dựng lịch sử synthetic gồm cả đơn bình thường; đơn hủy báo riêng, không gán thời gian giao bằng 0. Ghi generator, seed, giả định và phân bố vào data card khi có file thật.
2. Tách train/validation/test theo thời gian. Với mỗi đơn kiểm, chỉ dùng lịch sử đã hoàn tất trước thời điểm đặt; không dùng khiếu nại/kết quả phát sinh về sau.
3. Baseline: trung vị thời gian đặt → nhận theo shop/khung giờ. Biến thể cá nhân hóa: dùng lịch sử khách + shop khi đủ mẫu, fallback được ghi lại. Ngưỡng ban đầu 10 đơn/nhóm, thử trên validation rồi cố định trước test.
4. Trả trung vị và khoảng P20–P80 thực nghiệm cùng số mẫu/độ mới; báo không đủ dữ liệu nếu mọi nhóm đều thiếu. Không gọi đây là giờ giao bảo đảm.
5. Báo MAE của dự báo điểm trên tập đủ mẫu, tỷ lệ thực tế nằm trong khoảng, độ rộng khoảng và tỷ lệ đơn được dự báo. Chia riêng nhóm cá nhân hóa/fallback/thiếu dữ liệu; so cùng tập với baseline để tránh chọn mẫu có lợi.
6. Không tuyên bố dự báo tốt hơn thực tế từ dữ liệu tự dựng. Báo quy mô từng tập, giới hạn và mọi kết quả kể cả biến thể tệ hơn baseline.

## 5. Lưu bằng chứng và hai lượt

Trước khi chạy: lưu phiên bản bộ ca, rubric bổ sung và fixtures. Sau mỗi lượt: lưu output/sự kiện/chấm điểm cùng phiên bản code và model; không sửa lịch sử, tạo lượt mới khi chạy lại. Lượt 2 dùng cùng bộ/chuẩn; bộ mới thêm sau đó báo riêng. Báo cáo tại `eval/report.md` chỉ điền kết quả khi có artifact; không tự tạo file kết quả giả trong lần cập nhật tài liệu.
