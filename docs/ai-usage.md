# Khai báo dùng AI — CP1 và CP2

| Việc | Công cụ | AI làm gì | Người phụ trách kiểm | Trạng thái kiểm của nhóm |
|---|---|---|---|---|
| Workflow/demo | Codex | Viết agent, fake model và tích hợp CLI | Trần Quang Minh; Quang kiểm chéo | Demo đã chạy và cả nhóm đã kiểm tra bản CP2 |
| Công cụ và dữ liệu demo | Codex | Viết tools, generator, 10 fixtures seed 27112026, policy synthetic | Trần Duy Thành; Cường kiểm chéo | Test code đã qua; chưa có log kiểm tay của nhóm |
| Tài liệu review | Codex theo khai báo tài liệu CP1-D1 | Tài liệu nguồn có phân tích review; lượt CP2 chỉ tích hợp | Trần Duy Thành đối chiếu ở CP1, Nguyễn Văn Cường rà bản tổng hợp, Nguyễn Hải Quang phụ trách data card CP2 | Tiến độ CP1 ghi đã đối chiếu nhãn. Repo chưa có bản lưu toàn mẫu |
| Benchmark | Codex | Diễn giải 7 tình huống từ tài liệu có dẫn mã, viết 13 tình huống từ lưới phủ | Nguyễn Văn Cường; Thành kiểm chéo | Không coi câu diễn giải là trích nguyên văn |
| Metric và phiếu 5 output | Codex | Soạn 4 metric, chuẩn đạt và xuất output fake để chấm | Thành và Cường chấm độc lập | Chưa chấm, chưa ghi số khớp |
| Spec/canvas/data card | Codex | Soạn bản CP2 từ tài liệu được cung cấp và code đã chạy | Cả 4 cùng duyệt theo TEAMS.md | Cả nhóm đã kiểm tra bản CP2. Chưa xác nhận chốt chuẩn |
| Kiểm tra code | Codex | Chạy check BTC, 6 unit test, 20 nhánh fake và CLI | Cả 4 đọc và giải thích phần phụ trách | Chỉ kiểm luồng fake, không phải điểm AI thật |

Chưa dùng LLM chấm điểm, chưa tạo phỏng vấn/khảo sát, chưa gọi API thật hoặc đưa key vào repo. Fake model không đọc benchmark/expected. Không ghi các việc chấm/duyệt người thật là đã hoàn tất khi chưa có kết quả. Sau khi chốt CP2 không sửa chuẩn đạt để khớp kết quả.
