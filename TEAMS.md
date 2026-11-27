# TEAMS

> **Khi chấm và đánh giá, BTC dùng máy quét file này để ghép điểm cho từng người. Phải điền đúng format.**
> Giữ nguyên tên file `TEAMS.md` ở thư mục gốc repo, giữ nguyên các dòng `- Tên nhóm:` … và tiêu đề cột của bảng. Chỉ thay chỗ `____`.
> Kiểm bằng `python run.py check`: phần "Kiểm TEAMS.md" không báo gì là đúng format.

- Tên nhóm: Ishowspeed
- Lớp: L3B
- Track: D
- Link repo: https://github.com/MinhTrannnnn/K5-Day15-L3B-Ishowspeed

| STT | Họ và tên | Mã học viên | Vai trò | Phần việc chính |
|---|---|---|---|---|
| 1 | Trần Quang Minh | 2A202603929 | Đội trưởng | Agent, hội thoại, giao diện khách, tích hợp demo và nộp CP |
| 2 | Trần Duy Thành | 2A202603919 | Thành viên | Công cụ, dữ liệu, hồ sơ/trạng thái, quyền duyệt và giao diện nhân viên |
| 3 | Nguyễn Hải Quang | 2A202603936 | Thành viên | Bằng chứng, data card, canvas và đặc tả ETA nền tảng/nguồn dữ kiện |
| 4 | Nguyễn Văn Cường | 2A202603750 | Thành viên | Benchmark, metric, đánh giá/chi phí và kiểm ETA đầu vào |

**Quy tắc điền**
- **Lớp:** `L3A` hoặc `L3B`. **Track:** một chữ `A` (EdTech), `B` (Y tế), `C` (Du lịch), `D` (Thương mại điện tử), `E` (Tài chính) hoặc `F` (Làn khác). **Link repo:** link GitHub công khai của nhóm.
- Mỗi thành viên một dòng, nhóm **3–5 người**. Thiếu thì thêm dòng theo đúng mẫu, thừa thì xoá dòng.
- **Đội trưởng ở dòng 1**, cột Vai trò ghi đúng chữ `Đội trưởng`. Người khác ghi `Thành viên`.
- **Mã học viên** ghi đúng như trên hệ thống của khoá, không có khoảng trắng. Đội trưởng nộp các checkpoint bằng mã ở dòng 1.
- **Họ và tên** ghi đủ, có dấu.
- **Phần việc chính:** 1 dòng ngắn, khớp với phần có tên người đó trong repo.

## Phần việc — CP1

| Đầu việc | Người phụ trách | Trạng thái |
|---|---|---|
| Tạo repo và chọn Track D1 | Trần Quang Minh | Đã làm |
| Cung cấp tài liệu phân tích review | Nguyễn Hải Quang | Đã làm |
| Chuẩn bị khung repo, commit và push | Trần Quang Minh | Đã làm |
| Soạn README và canvas | Trần Quang Minh | Đã làm |
| Soạn spec và bảng so sánh 3 hướng | Trần Quang Minh | Đã làm |
| Tích hợp hồ sơ review, tổng hợp bằng chứng | Trần Quang Minh tích hợp, Nguyễn Văn Cường phụ trách duyệt | Đã làm |
| Đối chiếu review gốc và kiểm lại nhãn | Trần Duy Thành | Đã làm |
| Bổ sung thành viên và phân công | Trần Duy Thành | Đã làm |
| Xác nhận lát cắt | Nguyễn Hải Quang | Đã làm |
| Kiểm tra quyền xem repo công khai | Nguyễn Hải Quang | Đã làm |
| Nộp form CP1 | Trần Quang Minh | Đã nộp |


## Lịch sử phân công khung CP2 v1 — trước khi nâng thiết kế

Trần Quang Minh phụ trách chuẩn bị và tổng hợp bản CP2. Cả 4 thành viên cùng rà bài, thử demo và thống nhất chuẩn đạt. Mỗi người có hai phần phụ trách chính và kiểm chéo một phần của bạn khác.

| Thành viên | Hai phần phụ trách chính | Kiểm chéo | Trạng thái |
|---|---|---|---|
| Trần Quang Minh | Workflow `agent.py`; demo CLI và tích hợp spec | Data card/bằng chứng của Quang | Đã được cả nhóm kiểm tra |
| Trần Duy Thành | Công cụ `tools.py`; fixtures/chốt an toàn và test | Metric/câu thử của Cường; chấm độc lập 5 output | Đã rà soát và xác nhận 5/5 câu đạt theo xác nhận của nhóm trưởng |
| Nguyễn Hải Quang | Bằng chứng và data card; canvas và sơ đồ | Workflow/demo của Minh | Đã được cả nhóm kiểm tra phần hồ sơ. Chưa đối chiếu review gốc |
| Nguyễn Văn Cường | Benchmark; metric và hồ sơ đánh giá | Công cụ/fixtures của Thành; chấm độc lập 5 output | Đã rà soát và xác nhận 5/5 câu đạt theo xác nhận của nhóm trưởng |

Trần Quang Minh phụ trách nộp CP2 sau khi nhóm chốt chuẩn và hoàn tất chấm thử.


## Phân công rà bản CP1–CP2 nâng cấp — 27/11/2026

Đây là phân công theo hướng Minh chọn. Minh đã kiểm tra bản nâng cấp và xác nhận OK trong trao đổi; chưa có xác nhận các thành viên khác đã rà phần mới. Không dùng trạng thái kiểm khung fake cũ để xác nhận tính năng mới. Cả nhóm cùng rà và giải thích được phần có tên mình.

| Thành viên | Đầu ra phụ trách | Kiểm chéo | Trạng thái |
|---|---|---|---|
| Trần Quang Minh | CP1/canvas/spec; agent giả, nhớ phiên, CLI khách, tích hợp và nộp CP2 | Bằng chứng/data card của Quang | Khung fake do Codex triển khai; Minh đã kiểm tra và xác nhận OK |
| Trần Duy Thành | Công cụ, dữ liệu synthetic, lưu hồ sơ/nhật ký, quyền duyệt và giao diện nhân viên | Bộ kiểm bổ sung và hạn mức của Cường | Khung fake do Codex triển khai; chờ thành viên rà/xác nhận |
| Nguyễn Hải Quang | Kiểm chứng pain, nguồn chính sách, data card/canvas; đặc tả ETA nền tảng và nhu cầu nhân viên | Hội thoại/trải nghiệm khách của Minh | Kế hoạch; chưa có bằng chứng mới |
| Nguyễn Văn Cường | Giữ bộ chấm nền, thêm đánh giá nhiều lượt/hồ sơ, kiểm kỹ thuật CP2; kiểm nguồn ETA và chất lượng hồ sơ | Công cụ, trạng thái, quyền duyệt của Thành | Khung fake có kiểm tự động; chờ thành viên rà/xác nhận; chưa có AI thật |

Khung CP2 gồm luồng khiếu nại và đọc ETA nền tảng giả lập; chưa triển khai CP3. Hồ sơ [CP1 cập nhật](canvas.md) và [kịch bản CP2](docs/cp2-demo.md). Không thay đổi chuẩn CP2 v1 hoặc ghi lại lịch sử CP1 là đã làm theo thiết kế mới.


## Link phần việc và bằng chứng hiện có

Code/hồ sơ được soạn với Codex; bảng này chỉ ra phần mỗi người phụ trách và những xác nhận đã ghi nhận, không khẳng định mỗi người tự viết toàn bộ file.

| Thành viên | Phần phụ trách và link xem | Xác nhận đã có |
|---|---|---|
| Minh | [Spec](spec.md), [canvas](canvas.md), [hội thoại và hồ sơ](codebase/agent.py), [CLI/tích hợp](codebase/app.py) | CP1 đã nộp; bản CP2 nâng cấp đã kiểm và xác nhận OK trong trao đổi; chưa xác nhận đã nộp CP2 |
| Thành | [Công cụ/kiểm hạn mức](codebase/tools.py), [kho ca và trạng thái](codebase/agent.py), [fixtures đơn](data/demo_orders.json), [test](tests/test_agent.py) | Lịch sử CP1 ghi đối chiếu review/nhãn; đã đồng ý 5/5 output khung cũ theo nhóm trưởng. Chưa xác nhận rà code nâng cấp |
| Quang | [Bằng chứng](evidence/summary.md), [data card](data/DATA_CARD.md), [giả thuyết](evidence/hypothesis.md), [canvas](canvas.md) | Đã cung cấp tài liệu review, xác nhận lát cắt và kiểm quyền repo ở CP1 theo sổ phân công. Chưa kiểm độc lập toàn bộ review hoặc giả thuyết mở rộng |
| Cường | [Benchmark](eval/benchmark.csv), [metric](eval/metric_spec.yaml), [phiếu chấm cũ](eval/review-5.md), [kiểm CP2 mới](eval/cp2-upgrade-check.md) | Đã đồng ý 5/5 output khung cũ theo nhóm trưởng; kiểm kỹ thuật mới do Codex chạy. Chưa có lượt AI thật hoặc xác nhận rà bản nâng cấp |

CP2 còn cần nhóm rà/xác nhận, lưu mốc chốt chuẩn và nộp form. Không sửa chuẩn chấm theo output. CP3/CP4 để sau.
