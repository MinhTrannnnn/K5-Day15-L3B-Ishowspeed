# Canvas — Ishowspeed · Track D1 · thiết kế cập nhật 27/11/2026

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt | D · D1 · Tiếp nhận và xử lý ban đầu ca khiếu nại giao trễ, có nhân viên duyệt và khách theo dõi tiến độ. |
| 2 | Người dùng chính | Khách đang gặp đơn giao trễ/bất thường. Người phối hợp: nhân viên xử lý khiếu nại. |
| 3 | Pain một câu | Khi đơn giao trễ/bất thường, khách khó nhận được phương án xử lý rõ ràng và biết yêu cầu của mình đã được tiếp nhận đến đâu. |
| 4 | Bằng chứng đầu | Mẫu Google Play: 10/100 review ShopeeFood nói chờ/giao lâu; mẫu đối chiếu App Store: 2/31 nói cả chờ lâu lẫn vướng hỗ trợ. Chưa chứng minh đầy đủ việc kể lại nhiều lần hoặc thiếu theo dõi ca. Xem [summary](evidence/summary.md). |
| 5 | Lát cắt một câu | Một khách phản ánh một đơn giao trễ/bất thường → agent hỏi phần thiếu, đối chiếu dữ kiện và đề xuất phương án/hồ sơ → nhân viên phản hồi và duyệt → khách theo dõi tiến độ và kết quả có căn cứ trong cùng ca. |
| 6 | Mức tự động và lý do | Agent chọn công cụ đọc, làm rõ và soạn nháp; code kiểm chính sách, tiền, quyền và chuyển trạng thái. Nhân viên xác nhận lưu ca/duyệt phương án/cập nhật; không có giao dịch hoặc gửi tin ngoài hệ thống thật. Agent không tự phán quyết mâu thuẫn chưa xác minh. |
| 7 | Phân công có tên | Minh: agent/phiên/giao diện khách/tích hợp; Thành: công cụ/dữ liệu/hồ sơ/quyền duyệt/giao diện nhân viên; Quang: bằng chứng/data card/đặc tả dữ kiện ETA nền tảng; Cường: đánh giá/chi phí/kiểm ETA đầu vào. Code khung mới do Codex triển khai; từng thành viên còn phải rà và xác nhận phần phụ trách. |

**ETA trong phạm vi chính:** App giao đồ ăn cung cấp và thông báo ETA; agent chỉ đọc, đối chiếu mốc ban đầu/cập nhật với phản ánh khách và soạn hồ sơ. CP2 dùng snapshot giả lập, không live, không tự dự báo hoặc bảo đảm giờ giao.

**Phần mở rộng đề xuất, chưa triển khai:** checklist hồ sơ trước duyệt; nhắc ca chờ xử lý theo ngưỡng nội bộ; tổng hợp phản hồi khách sau kết quả. Ưu tiên checklist, cần kiểm chứng nhu cầu và không đổi chuẩn CP2.

**Đã đổi gì so với CP1:** CP1 chuyển từ thiếu món sang giao trễ theo review. Thiết kế mới nâng luồng hướng dẫn một lượt thành agent làm rõ, tổng hợp ca và phối hợp nhân viên đến kết quả. Chốt ETA là đầu vào từ nền tảng; giữ phạm vi chính là khiếu nại giao trễ. Không có bằng chứng mới hoặc kết quả model thật từ lần cập nhật tài liệu này.

**Hiện trạng CP2 mới:** CLI hai vai, planner fake/vòng công cụ, nhớ phiên, nháp/ca/sự kiện SQLite, nhân viên tiếp nhận/cập nhật và khách bổ sung/theo dõi; đọc ETA từ snapshot nền tảng. Chưa web, đăng nhập production hoặc AI thật. 20 câu/4 metric và phiếu 5/5 cũ giữ làm mốc; kiểm nâng cấp báo riêng.

**Chuẩn CP2 v1 giữ nguyên:** ≥80% câu đạt (ít nhất 16/20), 100% câu từ chối đạt và 100% câu đáp ứng điều kiện cứng về căn cứ, hạn mức, riêng tư và người duyệt; sự cố thực phẩm phải đề xuất chuyển người ngay. [Spec §7](spec.md) và [metric](eval/metric_spec.yaml) không đổi theo kết quả. Đánh giá phần mới tách riêng tại [upgrade-plan](eval/upgrade-plan.md).

Mốc, việc còn thiếu và đầu ra từng người: [phân công CP1–CP2](TEAMS.md).

**CP1 liên quan:** Canvas và spec đã đồng bộ pain, người dùng và lát cắt; không thay đổi lịch sử CP1 đã nộp. [Kịch bản CP2](docs/cp2-demo.md).
