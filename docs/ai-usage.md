# Khai báo dùng AI — CP1 và CP2

| Việc | Công cụ | AI làm gì | Người phụ trách kiểm | Trạng thái kiểm của nhóm |
|---|---|---|---|---|
| Workflow/demo | Codex | Viết agent, fake model và tích hợp CLI | Trần Quang Minh; Quang kiểm chéo | Demo đã chạy và cả nhóm đã kiểm tra bản CP2 |
| Công cụ và dữ liệu demo | Codex | Viết tools, generator, 10 fixtures seed 27112026, policy synthetic | Trần Duy Thành; Cường kiểm chéo | Test code đã qua; chưa có log kiểm tay của nhóm |
| Tài liệu review | Codex theo khai báo trong hồ sơ review | Tài liệu nguồn có phân tích review; lượt CP2 chỉ tích hợp | Trần Duy Thành đối chiếu ở CP1, Nguyễn Văn Cường rà bản tổng hợp, Nguyễn Hải Quang phụ trách data card CP2 | Tiến độ CP1 ghi đã đối chiếu nhãn. Repo chưa có bản lưu toàn mẫu |
| Benchmark | Codex | Diễn giải 7 tình huống từ tài liệu có dẫn mã, viết 13 tình huống từ lưới phủ | Nguyễn Văn Cường; Thành kiểm chéo | Không coi câu diễn giải là trích nguyên văn |
| Metric và phiếu 5 output | Codex | Soạn 4 metric, chuẩn đạt và xuất output fake để chấm | Thành và Cường chấm độc lập | Codex đã chấm thử, 5/5 câu đạt. Nhóm trưởng xác nhận Thành và Cường đồng ý với kết quả cả 5 câu. Phiếu lưu điểm đã xác nhận |
| Spec/canvas/data card | Codex | Soạn bản CP2 từ tài liệu được cung cấp và code đã chạy | Cả 4 cùng duyệt theo TEAMS.md | Cả nhóm đã kiểm tra bản CP2. Chưa xác nhận chốt chuẩn |
| Kiểm tra code | Codex | Chạy check BTC, 6 unit test, 20 nhánh fake và CLI | Cả 4 đọc và giải thích phần phụ trách | Chỉ kiểm luồng fake, không phải điểm AI thật |

Codex đã chấm thử 5 output từ model giả theo metric CP2. Chưa có điểm đánh giá CP3 trên model thật. Fake model không đọc benchmark/expected. Không ghi các việc chấm/duyệt người thật là đã hoàn tất khi chưa có kết quả. Sau khi chốt CP2 không sửa chuẩn đạt để khớp kết quả.


## Cập nhật thiết kế theo yêu cầu Minh — 27/11/2026

Codex cập nhật spec, canvas, README, kế hoạch CP2–CP4, phân công, giả thuyết, yêu cầu dữ liệu và kế hoạch đánh giá cho agent/hồ sơ/người duyệt/ETA. Minh chọn hướng sản phẩm trong trao đổi; chưa ghi nhận cả nhóm đã duyệt bản tài liệu mới. Lần này chưa viết code tính năng mới, chưa thu thập bằng chứng, chưa chấm model thật, không thay đổi chuẩn CP2 v1 hoặc kết quả fake cũ.


## Nâng khung CP1–CP2 theo yêu cầu tiếp theo của Minh

Codex triển khai CP2 fake nhiều lượt (cp2_demo.py, app.py, nhánh planner fake trong ai.py), SQLite lưu trạng thái local, generator 120 lịch sử synthetic và unit test cho quyền/chuyển bước/phiên/mâu thuẫn/ETA. Cập nhật lại hồ sơ CP1 và CP2 để khớp bản chạy, giữ lịch sử nộp/chuẩn/artifact cũ. Chưa nối API thật hoặc triển khai CP3; chưa có xác nhận các thành viên đã rà code mới.


## Rà và tinh gọn trước push

Minh xác nhận đã kiểm bản nâng cấp và OK. Gộp hai hướng dẫn trùng nội dung (`docs/cp1.md`, `docs/checkpoints.md`) vào canvas/spec, TEAMS và checklist README; giữ kịch bản CLI cần để demo. Chưa ghi nhận Thành, Quang, Cường đã rà bản nâng cấp.


## Hợp nhất lõi xử lý

Theo yêu cầu Minh, Codex bỏ luồng điều phối trùng, đưa hội thoại vào agent.py, quy tắc chung vào policy.py và kho ca/ETA vào cases.py. CLI và harness dùng cùng agent, bỏ lệnh quay về bản trước và sơ đồ thiết kế lỗi thời. Giữ chuẩn/bộ thử/kết quả lịch sử. Các tên module trong mục lịch sử phía trên được đối chiếu về tên hiện tại; không tuyên bố các lần chấm trước đã chạy trên code mới.


## Chốt phạm vi ETA theo Minh

Codex sửa spec §4.3/sơ đồ và tài liệu liên quan: ETA do app giao đồ ăn cung cấp; agent chỉ đọc/đối chiếu dữ kiện. Bỏ công cụ dự báo, /shop và dữ liệu/generator lịch sử, thay bằng /eta đọc snapshot. Cập nhật phân công và kiểm kỹ thuật, giữ chuẩn/bộ thử/artifact cũ. Các mô tả dự báo ở mục lịch sử phía trên không còn đại diện tính năng hiện tại. Đề xuất checklist/nhắc ca/phản hồi chỉ ghi kế hoạch, chưa triển khai.


## Rà góp ý và phần mở rộng CP2

Codex đối chiếu guide 2.1/2.2/2.4, bổ sung thiết kế và làm rõ thiếu mốc chốt/điểm độc lập/nguồn câu thử. Triển khai checklist, chặn chuyển duyệt, ghi căn cứ nhân viên, nháp nhắc, phản hồi/tổng hợp/mở lại; giữ ngưỡng/metric/benchmark và output đã lưu. Phiếu độc lập chỉ được tạo trống, không điền điểm hay xác nhận thay người thật.
