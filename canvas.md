# Canvas — Ishowspeed · Track D1 · thiết kế cập nhật 27/11/2026

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt | D · D1 · Tiếp nhận và xử lý ban đầu ca khiếu nại giao trễ, có nhân viên duyệt và khách theo dõi tiến độ. |
| 2 | Người dùng chính | Khách đang gặp đơn giao trễ/bất thường. Người phối hợp: nhân viên xử lý khiếu nại. |
| 3 | Pain một câu | Khi đơn giao trễ/bất thường, khách khó nhận được phương án xử lý rõ ràng và biết yêu cầu của mình đã được tiếp nhận đến đâu. |
| 4 | Bằng chứng đầu | Mẫu Google Play: 10/100 review ShopeeFood nói chờ/giao lâu; mẫu đối chiếu App Store: 2/31 nói cả chờ lâu lẫn vướng hỗ trợ. Chưa chứng minh đầy đủ việc kể lại nhiều lần hoặc thiếu theo dõi ca; chưa có bằng chứng cho nhu cầu ETA cá nhân hóa. Xem [summary](evidence/summary.md). |
| 5 | Lát cắt một câu | Một khách phản ánh một đơn giao trễ/bất thường → agent hỏi phần thiếu, đối chiếu dữ kiện và đề xuất phương án/hồ sơ → nhân viên phản hồi và duyệt → khách theo dõi tiến độ và kết quả có căn cứ trong cùng ca. |
| 6 | Mức tự động và lý do | Agent chọn công cụ đọc, làm rõ và soạn nháp; code kiểm chính sách, tiền, quyền và chuyển trạng thái. Nhân viên xác nhận lưu ca/duyệt phương án/cập nhật; không có giao dịch hoặc gửi tin ngoài hệ thống thật. Agent không tự phán quyết mâu thuẫn chưa xác minh. |
| 7 | Phân công có tên | Minh: agent/phiên/giao diện khách/tích hợp; Thành: công cụ/dữ liệu/hồ sơ/quyền duyệt/giao diện nhân viên; Quang: bằng chứng/data card/đặc tả lịch sử và màn hình ETA cùng Minh; Cường: đánh giá/chi phí/tính và đo ETA bằng code. Code khung mới do Codex triển khai; từng thành viên còn phải rà và xác nhận phần phụ trách. |

**Phần mở rộng:** Màn hình shop trước đặt hàng hiển thị khoảng thời gian giao từ lịch sử tất cả đơn hoàn tất, ưu tiên những lần khách đã đặt cùng shop nếu đủ mẫu. Khi thiếu dữ liệu thì lùi về thống kê shop hoặc báo thiếu cơ sở. Khiếu nại cung cấp ngữ cảnh riêng, không dùng làm mẫu duy nhất để dự báo. CP2 đã có `/shop` tính trên 120 đơn synthetic, đủ mẫu thì cá nhân hóa/fallback; chưa đánh giá độ chính xác, không thuộc chuẩn chấm chính CP2 v1.

**Đã đổi gì so với CP1:** CP1 chuyển từ thiếu món sang giao trễ theo review. Thiết kế mới nâng luồng hướng dẫn một lượt thành agent làm rõ, tổng hợp ca và phối hợp nhân viên đến kết quả. Bổ sung giả thuyết ETA từ lịch sử; giữ phạm vi chính là khiếu nại giao trễ. Không có bằng chứng mới hoặc kết quả model thật từ lần cập nhật tài liệu này.

**Hiện trạng CP2 mới:** CLI hai vai, planner fake/vòng công cụ, nhớ phiên, nháp/ca/sự kiện SQLite, nhân viên tiếp nhận/cập nhật và khách bổ sung/theo dõi; ETA từ 120 lịch sử synthetic. Chưa web, đăng nhập production hoặc AI thật. 20 câu/4 metric và phiếu 5/5 cũ giữ làm mốc; kiểm nâng cấp báo riêng.

**Chuẩn CP2 v1 giữ nguyên:** ≥80% câu đạt (ít nhất 16/20), 100% câu từ chối đạt và 100% câu đáp ứng điều kiện cứng về căn cứ, hạn mức, riêng tư và người duyệt; sự cố thực phẩm phải đề xuất chuyển người ngay. [Spec §7](spec.md) và [metric](eval/metric_spec.yaml) không đổi theo kết quả. Đánh giá phần mới tách riêng tại [upgrade-plan](eval/upgrade-plan.md).

Mốc, việc còn thiếu và đầu ra từng người: [phân công CP1–CP2](TEAMS.md).

**CP1 liên quan:** Canvas và spec đã đồng bộ pain, người dùng và lát cắt; không thay đổi lịch sử CP1 đã nộp. [Kịch bản CP2](docs/cp2-demo.md).
