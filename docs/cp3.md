# CP3 · Chạy và nộp bản thử D1

## Ứng dụng

Chạy `docker compose up --build` rồi mở [localhost:8080](http://localhost:8080). FastAPI phục vụ React y như bản build Vite, SQLite giữ hồ sơ và mặc định Ollama chạy `qwen2.5:1.5b` tại máy. Lần đầu chạy local cần Internet để tải image và trọng số model. Model và hồ sơ được giữ trong volume khi dùng `docker compose down`. Cấu hình mẫu nằm ở `.env.example`.

- **Khách hàng** chọn **D007 · Đã giao, chưa nhận** rồi bấm **Chưa nhận món** khi app hỏi. Khách thấy tóm tắt yêu cầu và trạng thái. Hồ sơ chi tiết giữ riêng trạng thái đơn ghi đã giao và lời khách báo chưa nhận ở bàn nhân viên.
- Nếu chọn **Đã nhận món**, app xác nhận đã giao. Bạn có thể dừng ở đây hoặc chọn **Tiếp tục nhờ nhân viên** nếu còn vấn đề cần xử lý.
- Chọn vai **Nhân viên mô phỏng** rồi bấm **Tiếp nhận hồ sơ** để tạo mã ca. Chọn **Đang xác minh**, nhập phản hồi cho khách và bấm **Cập nhật ca**. Quay lại vai khách hàng và bấm **Xem ca** để đọc trạng thái mới.
- Hai vai là mô phỏng cho người vận hành trên máy local. Mã đơn là synthetic. Không nhập thông tin cá nhân hoặc mở cổng demo ra mạng.

Code tra đơn, chính sách và mốc ETA. Model chọn hướng xử lý trong tối đa một lời gọi mỗi lượt đủ dữ kiện. Code kiểm trạng thái, giới hạn và dựng hồ sơ. `run.py eval` đo 20 câu trên cùng agent với web. Vòng đời hồ sơ nhiều lượt được kiểm riêng qua giao diện và unit test.

## Dùng key OpenAI

Thêm hoặc thay ba dòng dưới đây trong `.env` ở thư mục gốc. Điền key OpenAI thật ở máy của bạn.

```dotenv
CP3_PROVIDER=openai
OPENAI_MODEL=gpt-5.4-nano
OPENAI_API_KEY=
```

Chạy `docker compose up -d --build` để nạp `.env` rồi mở [ứng dụng](http://localhost:8080). Nhãn ở góc trên hiển thị `openai · gpt-5.4-nano`. Chọn D007 và bấm **Chưa nhận món** để thử gọi model. Có thể đổi `OPENAI_MODEL` sang model hỗ trợ Structured Outputs mà dự án OpenAI được cấp quyền sử dụng. Đổi `CP3_PROVIDER=ollama` để chạy lại bằng model local. Khi chạy Python ngoài Docker, chọn `MODEL_PROVIDER=openai`, `OPENAI_MODEL` và `OPENAI_API_KEY`.

## Lượt 1 và bằng chứng

Mở terminal khác trong repo khi app đã chạy:

```sh
docker compose exec app python run.py check
docker compose exec app python run.py eval --try
docker compose exec app python run.py eval
```

Lượt 1 đính kèm được chạy trên nhánh CP3 trước khi tích hợp vào main. File `eval/run-N.csv` và `traces/run-N.jsonl` được ghi về repo trên máy. `--try` kiểm kết nối và token, còn lượt đầy đủ mới có Run ID. Chấm theo [`metric_spec.yaml`](../eval/metric_spec.yaml), chỉ điền `pass` và `ghi_chu`, rồi chạy `docker compose exec app python run.py score eval/run-1.csv` với đúng tên CSV. Ghi `x/N`, Run ID và tên model vào báo cáo. Giữ nguyên câu thử, tiêu chí và ngưỡng CP2.

Bằng chứng pain cùng 5 đoạn trích ẩn tên nằm ở [tổng hợp nguồn](../evidence/summary.md). Bộ 20 câu hiện có 12 câu khó và 3 câu từ chối.

## Video 30 giây

[Bản ghi CP3 có thuyết minh](../artifacts/cp3-demo-thuyet-minh.mp4) dùng Ollama `qwen2.5:1.5b` với tình huống D007. Video ghi liền mạch thao tác con trỏ, hiển thị số token, có lời đọc Hải Đăng và phụ đề tiếng Việt. Xem [kịch bản thao tác và lời đọc](cp3-demo-script.md).

Nhóm tải video lên YouTube Unlisted hoặc Drive công khai, kiểm tra link khi đăng xuất và điền Form 2 nhánh CP3.

## Chạy ngoài Docker

Build frontend với `npm ci` và `npm run build` trong `frontend`. Tại thư mục gốc, chạy `python -m pip install -r requirements.txt`, đặt `MODEL_PROVIDER=ollama` cùng `OLLAMA_URL` nếu cần, rồi chạy `python -m uvicorn api:app --app-dir codebase --port 8080`. CLI chạy `python run.py`. Dùng `MODEL_PROVIDER=fake` để kiểm tra luồng giả, `MODEL_PROVIDER=openai` theo mục trên hoặc `MODEL_PROVIDER=openrouter` cùng key OpenRouter.
