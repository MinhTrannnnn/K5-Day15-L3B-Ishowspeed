> Repo nộp bài của nhóm Ishowspeed, phát triển từ khung BTC. Các chỗ `____` còn chờ bổ sung.
> Giờ, mốc, luật, rubric: xem `README.md`, `02-guide.md`, `03-rubric.md` trong repo đề (bộ đề BTC phát).

# Ishowspeed — Trợ lý AI xử lý khiếu nại giao trễ

## Chạy ứng dụng CP3 bằng Docker

Mở Docker Desktop hoặc Docker Engine, rồi chạy trong thư mục repo:

```sh
docker compose up --build
```

Mở [ứng dụng local](http://localhost:8080). FastAPI phục vụ bản build React/TypeScript từ Vite, SQLite lưu hồ sơ và Ollama chạy `qwen2.5:1.5b` trên máy. Compose tự tải model ở lần đầu và giữ lại trong volume. Xem [hướng dẫn eval và video CP3](docs/cp3.md).

Để dùng key OpenAI của nhóm, đặt `CP3_PROVIDER=openai`, `OPENAI_MODEL=gpt-5.4-nano` và `OPENAI_API_KEY` trong `.env`. Chạy `docker compose up -d --build` để nạp cấu hình. Xem [cấu hình OpenAI](docs/cp3.md#dùng-key-openai).

**Thành viên, lớp, track:** xem [TEAMS.md](TEAMS.md). **Điền TEAMS.md đúng format**: khi chấm và đánh giá, BTC quét file này để ghép điểm cho từng người.

*Lát cắt = phần nhỏ nhất làm xong được trong hackathon: một người dùng · một việc · một quyết định AI · một kết quả.*

---

## Đề tài — Track D · D1

**Pain chính đề xuất:** Khi đơn giao trễ/bất thường, khách khó nhận được phương án xử lý rõ ràng và biết yêu cầu đã được tiếp nhận đến đâu. Review hiện có hỗ trợ sơ bộ việc giao trễ và khó nhận hỗ trợ; việc phải kể lại, thiếu hồ sơ và thiếu theo dõi ca còn cần kiểm chứng.

**Lát cắt đích:** Khách phản ánh một đơn → một agent làm rõ, đối chiếu dữ kiện/mâu thuẫn, đề xuất phương án và tổng hợp hồ sơ → nhân viên phản hồi, duyệt và cập nhật → khách theo dõi từng bước. Mọi giao dịch chỉ mô phỏng, không kết nối hãng.

**ETA:** do app giao đồ ăn cung cấp. Agent đọc ETA ban đầu/cập nhật, trạng thái và thời điểm dữ liệu để hỗ trợ ca; không tự dự báo giờ đến. CP2 dùng snapshot giả lập, chưa có API hãng. CP2 đã có checklist trước duyệt, nháp nhắc ca chờ lâu, phản hồi/mở lại và tổng hợp sau xử lý; xem spec §4.5. Không gửi tin tự động hoặc giao dịch thật.

- **[Kịch bản CP2 mới](docs/cp2-demo.md)**
- [Canvas](canvas.md) · [Phân công](TEAMS.md) · [Thiết kế và hiện trạng](spec.md)
- [Bằng chứng và giới hạn](evidence/summary.md) · [Giả thuyết cần kiểm](evidence/hypothesis.md)
- [Kế hoạch đánh giá bổ sung](eval/upgrade-plan.md)

**Khung CP2 đã triển khai:** fake planner gọi công cụ trong vòng giới hạn, nhớ phiên, hồ sơ SQLite, bàn CLI khách/nhân viên, duyệt/cập nhật và theo dõi ca, đọc ETA nền tảng giả lập. Khung CLI mô phỏng dùng dữ liệu synthetic. [Báo cáo kiểm kỹ thuật](eval/cp2-upgrade-check.md).

Bản CP2 chạy được workflow D1 bằng model giả, không cần key; đã có 4 thành viên và phân công chung/kiểm chéo trong `TEAMS.md`. Có 20 câu thử, 4 metric, data card và 10 đơn synthetic; chính sách DEMO-P1 là quy tắc dựng, không phải chính sách của hãng.

```bash
python3 run.py check
MODEL_PROVIDER=fake python3 run.py
MODEL_PROVIDER=fake python3 -m unittest discover -s tests -v
```

Thử `D004 tôi chờ lâu` rồi `Tôi muốn hủy` để thấy nhớ phiên; `/nhanvien` → `/tiepnhan` để nhận ca; `/trangthai C001` để xem tiến độ. `/eta D004` xem ETA nền tảng từ snapshot. `/help` xem cú pháp. [Kịch bản đầy đủ](docs/cp2-demo.md). Dữ liệu synthetic/snapshot, không live. Trên PowerShell đặt `$env:MODEL_PROVIDER="fake"` rồi chạy `python run.py`.

**CP3** bổ sung web local dùng cùng agent và SQLite với CLI. Docker Compose hỗ trợ Ollama và OpenAI. [Hướng dẫn CP3](docs/cp3.md).

**Tiến độ lịch sử khung CP2 v1:** Nhóm trưởng đã nộp CP1. Cả nhóm đã kiểm tra bản CP2. Lượt chấm thử của Codex đạt 5/5 output từ model giả. Thành và Cường đã rà soát và đồng ý với kết quả 5/5 theo xác nhận của nhóm trưởng. Xem [phiếu chấm](eval/review-5.md).

---

## Kiểm trước khi nộp CP2

- [x] Canvas/spec đồng bộ đề tài mới; khung fake nhiều lượt, hồ sơ/duyệt và đọc ETA demo chạy được.
- [x] Minh đã kiểm bản lõi; 22 test lõi/mở rộng do Codex chạy đã qua, xem [báo cáo kiểm](eval/cp2-upgrade-check.md).
- [ ] Nhóm rà phần mở rộng mới: checklist, nháp nhắc và phản hồi/mở lại.
- [ ] Thành, Quang, Cường rà và xác nhận phần phụ trách trong [TEAMS](TEAMS.md).
- [x] Thành và Cường đã chốt chuẩn và chấm thử, đồng thuận 5/5 theo xác nhận của nhóm trưởng.
- [ ] Lưu bảng điểm từng câu và xác minh nguồn của 7 câu `data_that`.
- [x] Minh xác nhận đã nộp form CP2.

## Nhóm làm gì, khung làm gì

| Nhóm quyết định và viết | Khung làm sẵn (không cần sửa) |
|---|---|
| Người dùng, pain, bằng chứng, impact (`evidence/`, `spec.md` §1–§2) | — |
| Hình dạng giải pháp, công cụ, prompt, luồng (`spec.md` §4, `codebase/agent.py`, `tools.py`, `ai.py`) | Ghi mọi lần gọi model / công cụ vào trace, cộng token (`codebase/tracing.py`) |
| Bộ câu thử, metric, chuẩn "đạt" (`eval/benchmark.csv`, `eval/metric_spec.yaml`, `spec.md` §7) | Kiểm đủ cột, đủ câu `kho` / `tu_choi`, đủ ≥1/3 câu từ người dùng / data thật (`run.py check`) |
| Chấm cột `pass` theo metric spec | Chạy cả bộ một lệnh, có run ID, model, token từng câu (`run.py eval`) · tính % đạt (`run.py score`) |
| Persona, số người dùng thật, giá model (`cost/personas.yaml`) | Sinh ~50 phiên, chạy thật qua bản chạy thử, tính chi phí / phiên, / task thành công, / tháng 3 kịch bản (`run.py simulate`) |

*Ví dụ track A (ví dụ cỡ, không phải lời giải):* nhóm viết công cụ `search_lesson` tra bài pre-class đã đánh mã đoạn, luồng "tra đoạn → model trả lời kèm mã đoạn, không có thì nói không có", metric "mọi khẳng định có mã đoạn đúng", persona "ôn dồn trước kiểm tra". Khung chạy 25 câu thử ra `run-1.csv`, nhóm chấm `pass`, `score` in % đạt; `simulate` chạy 50 phiên ra chi phí / task thành công cho hai model.

## Chạy trong 3 phút

Bộ khung cần **Python 3.10 trở lên** (Python 3.9 có sẵn trên macOS vẫn chạy được, chỉ in một dòng nhắc). **Không cần `pip install`.**

**Bước 1 — Mở cửa sổ lệnh ngay trong thư mục repo**

| Windows (PowerShell) | macOS |
|---|---|
| Mở thư mục repo bằng File Explorer → bấm vào thanh địa chỉ → gõ `powershell` → Enter | Mở **Terminal** (Cmd + Space, gõ "Terminal") → gõ `cd ` (có dấu cách) → kéo thả thư mục repo vào → Enter |

Gõ `dir` (Windows) hoặc `ls` (macOS / Linux): thấy `run.py` và `README.md` là đang đứng đúng chỗ.

**Bước 2 — Kiểm Python và chạy thử**

| Việc | Windows (PowerShell) | macOS / Linux |
|---|---|---|
| Kiểm Python | `python --version` (không được thì `py --version`) | `python3 --version` |
| Chạy bản chạy thử (chế độ giả, chưa gọi model) | `python run.py` | `python3 run.py` |
| Kiểm bộ câu thử | `python run.py check` | `python3 run.py check` |
| Tạo file `.env` để nối model | `copy .env.example .env` | `cp .env.example .env` |

- Windows: gõ `python` mà mở Microsoft Store hoặc báo không có lệnh → dùng `py`. Chưa có Python: cài từ python.org, **tick "Add python.exe to PATH"**, mở lại PowerShell.
- macOS: báo `command not found: python` là bình thường → dùng `python3`.
- `python run.py` hiện trả hướng dẫn có nhãn DEMO; model fake có token 0. Chưa có AI thật trong bản CP2. Nối model thật: [docs/connect-model.md](docs/connect-model.md).

Trong README này lệnh viết là `python …`; máy nhóm cần `python3` hay `py` thì gõ thay.

## Lệnh

| Lệnh | Làm gì |
|---|---|
| `python run.py` | Chạy bản chạy thử (gõ đầu vào, nhận kết quả, kèm số lần gọi model / token) |
| `python run.py check` | Kiểm `eval/benchmark.csv` (6 cột, số câu, `kho` / `tu_choi`, mã `source`, ô trống, dòng mẫu) `eval/metric_spec.yaml` (≥3 metric điền đủ) và `TEAMS.md` (đúng format để BTC quét). Chỉ cảnh báo, không sửa file |
| `python run.py eval --try` | **Thử nối model:** chạy 3 câu đầu (`--try 5` = 5 câu) → `eval/run-try.csv`. Thấy "Nối model được" là xong. Không tính là một lượt |
| `python run.py eval` | Chạy cả bộ qua `codebase/agent.py` → `eval/run-1.csv` (lần sau `run-2.csv`…) + `traces/run-1.jsonl`. Mỗi dòng có run ID, model, số lần gọi model / công cụ, token. Model còn giả → chỉ ghi `run-mock.csv`; mọi câu lỗi → `run-error.csv`; Ctrl+C → `run-stopped.csv` — đều **không** được đánh số |
| `python run.py eval --fake` | Thử riêng bộ chạy, không gọi agent → `eval/run-fake.csv` |
| `python run.py score eval/run-1.csv` | Sau khi điền cột `pass` (1 / 0): in % đạt tổng và theo `type`. Còn ô trống → "CHƯA CHẤM XONG", không in % |
| `python run.py simulate --try` | Thử mô phỏng chi phí 10 phiên (làm trước CP3) → `cost/simulate-try.csv` |
| `python run.py simulate` | Mô phỏng chi phí khi dùng thật theo `cost/personas.yaml` (≥50 phiên) → `cost/simulate-N.csv` + `cost/simulate-N-summary.md` |
| `python run.py simulate --rate-from eval/run-2.csv` | Như trên, lấy tỉ lệ đạt từ đúng lượt chỉ định. Không ghi thì khung lấy lượt `run-N` mới nhất đã chấm, cùng model, và ghi rõ đã lấy lượt nào trong bản tóm tắt |

Gói miễn phí báo hết lượt: thêm `--wait 4` sau `eval` hoặc `simulate` (nghỉ 4 giây giữa hai lượt gọi). Sửa CSV bằng Excel: *File → Save As → CSV UTF-8*; Google Sheets: *Tệp → Tải xuống → CSV*.

**Lượt có lỗi kỹ thuật** (cột `error` có chữ): không sửa tay file đó, chạy lại thành lượt mới và ghi vào bảng các lượt ở `eval/README.md`. Không xoá file lượt nào.

Nhóm dùng stack khác (Node, Streamlit, notebook…): sửa hàm `run_app()` trong `run.py` để `python run.py` vẫn chạy được bản chạy thử, và giữ `answer()` trong `codebase/agent.py` để `eval`, `simulate` chạy được.

## Bản chạy thử — viết ở đâu

| File | Viết gì | Bước guide |
|---|---|---|
| `codebase/agent.py` | `Agent.chat` là lõi chung cho CLI và `answer(text)`; quy tắc ở `policy.py`, lưu ca/đọc ETA ở `cases.py` | 3.2 |
| `codebase/tools.py` | Công cụ của bài toán, mỗi công cụ một hàm có `@tool` | 2.2, 3.2 |
| `codebase/ai.py` | `call_model(system, user)` — chỗ duy nhất gọi model. Chưa điền `.env` thì chạy **chế độ giả** | 3.3 |

- **Trước CP2:** để chế độ giả, công cụ trả dữ liệu giả — `python run.py` đi hết luồng là đủ.
- **Trước CP3:** nối model thật theo [docs/connect-model.md](docs/connect-model.md), `eval --try` thấy token > 0 rồi mới `eval`.
- Bộ chạy gửi **nguyên ô `input`** của câu thử vào `answer(text)`. Dữ liệu nền (bài học, thông báo, lịch…) để trong `data/`, đọc qua công cụ.

**Lưu trạng thái demo:** `data/runtime/cp2.sqlite3` được gitignore. Hai vai CLI do người vận hành chuyển, chưa xác thực tài khoản; không dùng dữ liệu cá nhân thật.

## Phần nào thật, phần nào giả

| Thành phần | Thật / Giả | Ghi chú |
|---|---|---|
| Lời gọi AI ở quyết định trung tâm | **Cấu hình được** | Ollama, OpenAI hoặc OpenRouter trả số token thực tế. Chế độ fake mặc định khi CLI chưa cấu hình. |
| Dữ liệu và chính sách demo | **Synthetic** | 10 đơn, 1 chính sách DEMO-P1; seed 27112026 |
| Tra dữ liệu, kiểm tiền và trace | Code chạy thật | Không kết nối sàn hoặc thao tác tiền thật |

## Dùng AI vào việc gì

2–3 dòng (bắt buộc): nhóm dùng công cụ AI nào để làm gì, người kiểm lại phần nào. Chi tiết: [docs/ai-usage.md](docs/ai-usage.md). Coding agent đọc [AGENTS.md](AGENTS.md).

Nhóm dùng Codex để soạn hồ sơ, code workflow/fake model, fixtures, câu thử và metric CP2; Codex chạy kiểm tra cấu trúc, luồng và chốt an toàn. Cả 4 thành viên đã kiểm tra bản CP2. Thành và Cường đã rà soát và xác nhận kết quả chấm thử, theo thông tin từ nhóm trưởng. CP2 chưa thu thập thêm phỏng vấn hoặc khảo sát.

## File mẫu — điền ở bước nào

| File | Điền ở bước guide | Mốc |
|---|---|---|
| `TEAMS.md` | 1.0 | CP1 · **đúng format**, BTC quét khi chấm |
| `canvas.md` | 1.4 | CP1, cập nhật CP2 |
| `evidence/hypothesis.md` | 1.1 | trước khi tìm bằng chứng |
| `evidence/data-mining.md` · `evidence/interviews/TEMPLATE.md` → `P1.md`… · `evidence/survey/TEMPLATE.md` | 1.2 | bắt đầu sau Zoom, xong CP3 |
| `evidence/summary.md` | 1.2 | CP3 |
| `spec.md` | §0–§2: 1.1–1.3 · §3–§5: 2.1–2.3 · §7: 2.4 · §8: 4.2 · §10: suốt | §7 chốt CP2 · §0–§7 CP3 · đủ CP4 |
| `data/DATA_CARD.md` | 2.4 | bản đầu CP2 |
| `eval/benchmark.csv` · `eval/metric_spec.yaml` | 2.4 | ≥10 câu + metric chốt CP2 · 20–30 câu CP3 |
| `codebase/` | 3.2, 3.3 | khung CP2 · AI thật CP3 |
| `eval/report.md` · `eval/README.md` | 4.1 (README mục 1–4 từ 2.4) | CP4 |
| `cost/personas.yaml` · `cost/cost-estimate.md` | 4.2 | thử 10 phiên CP3 · đủ CP4 |
| `validation/log.md` *(bonus)* | 4.3 | CP4 |
| `slides/outline.md` → `demo-slides.pdf` | 5.1 | CP4 |
| `reflection/TEMPLATE.md` → `reflection/<ten>.md` | 5.3 | 23:59 Thứ Bảy 28/11 |
| `AGENTS.md` · `docs/ai-usage.md` | khi dùng coding agent / AI | suốt |

## Bảy hạng mục bắt buộc — nằm ở file nào

| # | Hạng mục | File |
|---|---|---|
| 1 | Bằng chứng pain | `evidence/` (tổng hợp ở `evidence/summary.md`) |
| 2 | Impact có số | `spec.md` §2 |
| 3 | Thiết kế giải pháp | `spec.md` §4 |
| 4 | Bản chạy thử làm trọn lát cắt | `codebase/` · lệnh ở mục "Lệnh" |
| 5 | Định nghĩa "tốt" + bộ câu thử | `data/DATA_CARD.md` · `eval/` |
| 6 | Mô phỏng chi phí khi dùng thật | `cost/` |
| 7 | Slide + demo + video dự phòng | [Slide CP4 bản chi tiết V2](artifacts/cp4-slides-v2.html) · [bản đầu](artifacts/cp4-slides.html) · [video đã ghi](artifacts/cp3-demo-thuyet-minh.mp4); nhóm cần kiểm link chia sẻ ngoài repo khi nộp form. |
