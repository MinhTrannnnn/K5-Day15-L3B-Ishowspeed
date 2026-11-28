# Tóm tắt mô phỏng simulate-2@20261128-092013

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 35 | 1 | 353 | 11 | 0.8 | 3.6 |
| dung_vua | 13 | 2 | 705 | 23 | 1.5 | 6.6 |
| dung_nhieu | 2 | 3 | 930 | 30 | 2.0 | 8.0 |

Tỉ lệ đạt dùng để tính: 18/20 (90%) — lượt run-2@20261128-080037

- Tự chọn: lượt run-N mới nhất đã chấm xong, chạy bằng đúng model đang đo (run-2.csv). Muốn dùng lượt khác (vd lượt 2): thêm `--rate-from eval/run-2.csv`.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (100 người) | Chi phí / tháng — cơ sở (300 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.4-nano-2026-03-17 (vào 0.2 · ra 1.25 $/1M) | $0.00011 | $0.00012 | $0.000093 | $0.0189 | $0.0567 | $0.1888 | $0.00019 |
| gpt-5.4-mini-2026-03-17 (vào 0.75 · ra 4.5 $/1M) | $0.00042 | $0.00047 | $0.00035 | $0.0703 | $0.2110 | $0.7034 | $0.00070 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.3) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-5.4-nano-2026-03-17. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
