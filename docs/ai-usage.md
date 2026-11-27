# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | | | | |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Tài liệu review tham khảo | ChatGPT Codex (theo khai báo tài liệu CP1-D1) | Tài liệu nguồn khai báo đã lấy review và gắn nhãn; lượt tích hợp này chỉ đọc và kiểm tính nhất quán của tài liệu | Chưa kiểm lại review gốc; chưa có bản lưu toàn mẫu trong repo | Trần Quang Minh phụ trách xác minh |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Văn bản CP1 | ChatGPT Codex | Soạn bản nháp Canvas, spec và tổng hợp bằng chứng | Chờ Trần Quang Minh kiểm và duyệt nội dung; chưa duyệt số liệu nguồn | Trần Quang Minh |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
