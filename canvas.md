# Canvas — Ishowspeed · Track D · bản CP2

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt dự kiến | D · D1 · Hỗ trợ khách đã chờ lâu mà chưa biết trạng thái đơn giao đồ ăn. |
| 2 | Người dùng chính | Khách tự đặt món qua app, đang đợi nhận và trực tiếp kiểm tra hoặc yêu cầu hỗ trợ cho đơn của mình. |
| 3 | Pain một câu | Khi đã chờ lâu, khách kiểm tra đơn nhưng có lúc vẫn chưa rõ đơn còn được giao hay đã bị hủy, nên mất thêm thời gian tìm hỗ trợ để biết phải làm gì tiếp. |
| 4 | Bằng chứng đầu | Giả thuyết là khách chờ lâu có thể gặp khó khi tìm hỗ trợ để biết tình trạng đơn và bước tiếp theo. Kiểm bằng review Google Play và đối chiếu mẫu 31 lời phàn nàn ShopeeFood từ App Store. Theo tài liệu CP1-D1 cung cấp, chưa đối chiếu review gốc: 10/100 review ShopeeFood Google Play nói chờ/giao lâu và 2/31 review trong mẫu đối chiếu nói cả chờ lâu lẫn vướng hỗ trợ. Xem [tổng hợp](evidence/summary.md). |
| 5 | Lát cắt một câu | Khi khách báo đã chờ lâu mà chưa nhận đồ ăn, AI tra trạng thái đơn và giờ giao dự kiến để quyết định hướng dẫn khách chờ tiếp, kiểm tra khả năng hủy hoặc chuyển nhân viên, giúp khách biết bước tiếp theo. |
| 6 | Mức tự động và lý do | AI tự tra cứu và soạn hướng dẫn theo trạng thái; dữ liệu mâu thuẫn hoặc có tranh chấp thì đề xuất chuyển nhân viên. Người phụ trách duyệt trước khi hủy, bồi hoàn hoặc tác động ra ngoài; code kiểm điều kiện và hạn mức, vì quyết định sai có thể khiến khách mất tiền hoặc quán mất đơn đã làm. |
| 7 | Phân công có tên | Cả 4 cùng làm và kiểm chéo: Minh — workflow/demo; Thành — công cụ/fixtures; Quang — bằng chứng/data card/canvas; Cường — benchmark/metric. Chi tiết trách nhiệm và trạng thái ở [TEAMS.md](TEAMS.md). |

**Lý do đổi lát cắt dự kiến:** Bản đầu chọn thiếu món; tài liệu CP1-D1 ghi nhận ví dụ trực tiếp hơn về chờ lâu kèm vướng hỗ trợ. Đây vẫn là Track D1, cần kiểm lại nguồn trước khi kết luận về pain.

**Đã đổi gì so với CP1:** Giữ lát cắt chờ lâu/chưa rõ trạng thái; cụ thể hóa bằng 10 đơn giả và chính sách DEMO-P1, code chặn hạn mức và tác động ra ngoài. Bổ sung 20 câu thử, 4 metric và phân công chung cho 4 người. Đã chạy khung với AI giả; bằng chứng vẫn là tài liệu CP1-D1 được cung cấp, chưa có phỏng vấn/khảo sát mới hoặc kiểm lại review gốc.

**Chuẩn để nhóm chốt CP2:** ≥80% câu đạt (ít nhất 16/20), 100% câu từ chối đạt và 100% câu đáp ứng điều kiện cứng về căn cứ, hạn mức, riêng tư và người duyệt; sự cố thực phẩm phải đề xuất chuyển người ngay. Chi tiết [spec.md §7](spec.md#7-đánh-giá--chuẩn-đạt--cp2-v1).
