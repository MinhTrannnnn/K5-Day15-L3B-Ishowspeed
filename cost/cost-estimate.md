# Chi phí khi dùng thật · kịch bản pilot CP4

Kết quả này là **mô phỏng theo giả định được ghi rõ**, không phải chi phí hoặc lợi ích thực tế của ShopeeFood. Số token được đo bằng API thật; quy mô và tần suất chưa được khảo sát. [Cấu hình đầu vào](personas.yaml) · [CSV 50 phiên](simulate-2.csv) · [bảng do harness sinh](simulate-2-summary.md).

## 1. Đầu vào và nguồn

- **Persona:** dùng ít 70% × 1 phiên/người/tháng × 1 lượt hỏi/phiên; dùng vừa 25% × 2 × 2; dùng nhiều 5% × 4 × 3. Mọi tỷ lệ và tần suất đều *(tự ước tính)*, chưa có phỏng vấn hoặc log sử dụng để kiểm. Không lấy quy mô lớp học track A làm quy mô ứng dụng giao đồ ăn.
- **Quy mô pilot:** thấp **100**, cơ sở **300**, cao **1.000** người dùng mục tiêu/tháng; tất cả *(tự ước tính)*, không phải số người dùng của hãng.
- **Giá Standard USD/1 triệu text token, xem 28/11/2026:** model thực đo `gpt-5.4-nano-2026-03-17` **$0.20 vào, $1.25 ra** theo [OpenAI Docs nano](https://developers.openai.com/api/docs/models/gpt-5.4-nano); mức so sánh `gpt-5.4-mini-2026-03-17` **$0.75 vào, $4.50 ra** theo [OpenAI Docs mini](https://developers.openai.com/api/docs/models/gpt-5.4-mini). Trang nano hiện ghi *Deprecated*; đã chạy được bằng key nhóm trong lượt này, nhưng cần kiểm lại khả dụng trước khi triển khai.
- **Tỷ lệ đạt dùng để tính:** [lượt OpenAI](../eval/run-2.csv) `run-2@20261128-080037`, **18/20 = 90%** theo chuẩn đã chốt. Đây là tỷ lệ đạt theo **câu thử**, được dùng như đại diện cho xác suất một phiên thành công; giả định này chưa được kiểm bằng đánh giá phiên nhiều lượt. Không giả định đạt 100%.

## 2. Kết quả mô phỏng

Lượt `simulate-2@20261128-092013`, seed **42**, **50/50 phiên không lỗi**. Đo được **23.377 token vào, 755 token ra, 51 lượt gọi model và 228 lượt gọi công cụ**. Model đo token là `gpt-5.4-nano-2026-03-17`. Số liệu dưới đây chép từ [bảng kết quả do harness sinh](simulate-2-summary.md), được tính lại từ [CSV](simulate-2.csv).

| Mức giá model | USD/phiên | USD/task thành công | USD/tháng: 100 người | USD/tháng: 300 người | USD/tháng: 1.000 người | USD/người/tháng ở mức 300 |
|---|---:|---:|---:|---:|---:|---:|
| Nano, đã đo token và đánh giá chất lượng | $0.00011 | $0.00012 | $0.0189 | $0.0567 | $0.1888 | $0.00019 |
| Mini, **chỉ giả lập giá trên token nano** | $0.00042 | $0.00047* | $0.0703 | $0.2110 | $0.7034 | $0.00070 |

Chi phí/task thành công = chi phí trung bình mỗi phiên ÷ **0,90**. *Dòng mini còn giả định mini dùng cùng lượng token và cũng đạt 90%; nhóm chưa chạy hoặc chấm model mini, nên đây chỉ là phép tính nhạy cảm theo giá, không phải dự báo chất lượng/chi phí thực đo của mini.* Không tính cache, Batch, lưu trữ, hạ tầng web, người duyệt hoặc phí thanh toán. Số thực tế có thể cao hơn.

## 3. So với impact

Ở mức cơ sở 300 người, [bảng impact](../spec.md#2-impact--quyết-định-chọn-guide-13) giả định **10 khách gặp vấn đề/tháng × 1 lần × 5 phút tìm hỗ trợ = 50 phút/tháng**. Đây là thời gian *có thể* giảm tối đa nếu công cụ giải quyết hoàn toàn phần tìm hỗ trợ; chưa đo được phút tiết kiệm. Chia trên 300 người là **0,167 phút/người/tháng** *(tự ước tính từ kịch bản)*. Giá token nano là **$0.00019/người/tháng**; để bù riêng $0.0567 token/tháng, 50 phút giả định cần có giá trị ít nhất **$0.00113/phút**. Chi phí nhân viên và hạ tầng sẽ tăng điểm hòa vốn.

**Kết luận:** Đáng thử pilot giới hạn vì chi phí token dự kiến thấp theo kịch bản này; **chưa đủ căn cứ nói triển khai thật có lợi** trước khi đo thời gian tiết kiệm, tỷ lệ phiên xử lý được và công duyệt hồ sơ.

## 4. Giới hạn và lượt cũ

[Lượt simulate-1](simulate-1-summary.md) dùng persona và bảng giá ví dụ, chỉ kiểm kỹ thuật, không dùng để kết luận CP4. Lượt mới thay toàn bộ giá trị ví dụ bằng giả định có nhãn hoặc giá có nguồn; 50 phiên là mô phỏng theo benchmark và persona, không phải log của khách thật. Quy mô 100/300/1.000 chưa có nguồn vận hành; nếu có dữ liệu thật, cập nhật [cấu hình](personas.yaml) và chạy một lượt mới, giữ nguyên CSV cũ.
