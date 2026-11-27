# Data mining · D1 — Khiếu nại đơn giao đồ ăn

> Repo chưa lưu toàn bộ review gốc và bảng gắn nhãn từng dòng. Phụ lục lưu mã theo nhãn để người đọc kiểm lại phép đếm.

**Bước 1.2 · Bản lấy review trực tiếp từ Google Play, 27/11/2026**

Trong mẫu **400 review**, tín hiệu phù hợp nhất cho Canvas là **khách đã chờ lâu cần biết tình trạng đơn và bước xử lý tiếp theo**. Một review GrabFood mô tả cả hai việc: giờ giao dự kiến thay đổi nhiều lần và khách không gặp được chuyên viên khi nhắn hỗ trợ. Review phía quán bổ sung trường hợp đã làm xong món nhưng chưa có tài xế đến lấy hoặc đơn bị hủy, dẫn đến tranh chấp bồi hoàn.

## 1. Giả thuyết và cách lấy mẫu

**Giả thuyết.** Khi đơn giao đồ ăn chờ lâu, một số khách mất thêm thời gian tìm hỗ trợ để biết đơn còn được giao hay đã bị hủy và họ có thể làm gì tiếp theo. Dấu hiệu trực tiếp là một review vừa kể giao chậm hoặc chờ lâu, vừa nêu một trở ngại cụ thể khi tìm hoặc nhận hỗ trợ cho sự cố đó.

Lấy **100 review mới nhất Google Play trả về cho mỗi app** bằng `google-play-scraper==1.2.7`, với `lang="vi"`, `country="vn"`, `Sort.NEWEST` và mọi mức sao. Đếm theo review, bỏ ID trùng trong cùng app. Bốn nguồn có 100 review duy nhất mỗi nguồn. Ngày dưới đây là ngày hiển thị trong dữ liệu trả về.

| Mã | Nguồn Google Play | N | Khoảng ngày | Số review từ 1★ đến 5★ |
|---|---|---:|---|---|
| SF | [ShopeeFood](https://play.google.com/store/apps/details?id=com.deliverynow&hl=vi&gl=VN) | 100 | 16/11/2026–26/11/2026 | 26 / 4 / 2 / 5 / 63 |
| GF | [Grab](https://play.google.com/store/apps/details?id=com.grabtaxi.passenger&hl=vi&gl=VN) | 100 | 21/11/2026–26/11/2026 | 35 / 7 / 1 / 2 / 55 |
| SM | [ShopeeFood Merchant](https://play.google.com/store/apps/details?id=com.sea.foody.nowmerchant&hl=vi&gl=VN) | 100 | 19/08/2022–02/11/2026 | 59 / 3 / 1 / 1 / 36 |
| GM | [GrabMerchant](https://play.google.com/store/apps/details?id=com.grab.merchant&hl=vi&gl=VN) | 100 | 05/04/2026–25/11/2026 | 69 / 2 / 3 / 2 / 24 |

ChatGPT đã đọc nội dung cả 400 dòng và gắn nhãn theo nội dung review. Review mơ hồ, ví dụ chỉ nói ứng dụng chậm hoặc chỉ nói tài xế mà không rõ dịch vụ, được giữ trong mẫu gốc. Với app Grab, chỉ đưa vào tập con GrabFood khi có dấu hiệu rõ như tên GrabFood, món ăn, đơn đồ ăn hoặc cách mô tả luồng giao đồ ăn. Các review chỉ nói đặt xe, chuyển hàng chung chung hoặc lỗi nền tảng nằm ngoài tập con. Review có cả đặt xe và đồ ăn được tính cho GrabFood nếu phần đồ ăn đủ cụ thể để gắn nhãn.

## 2. Quy tắc gắn nhãn

| Mã | Dấu hiệu |
|---|---|
| G · Chờ/giao lâu | Khách mô tả đợi lâu để có tài xế hoặc nhận đồ ăn, giao muộn, hoặc giờ giao dự kiến bị lùi khiến phải chờ. |
| H · Vướng hỗ trợ | Khách mô tả một trở ngại cụ thể với đơn, như không liên hệ được, không nhận phản hồi, chatbot không xử lý được, hoặc thao tác hủy bị chặn. |
| C · Hủy đơn kèm vấn đề tiền | Đơn đã hủy nhưng người viết kể vẫn bị trừ tiền, bị yêu cầu thanh toán hoặc chưa nhận khoản hoàn. |
| S / M · Sai món / Thiếu món | Khách nói đã nhận món sai loại hoặc đã nhận đơn và thấy thiếu một món hay một phần. Đơn chưa đến hoặc bị hủy không được gắn M. |
| Q · Chậm hoặc trục trặc khâu giao nhận phía quán | Quán mô tả thiếu tài xế, lấy món chậm, trục trặc bàn giao, thông báo đơn muộn hoặc thời gian chuẩn bị không khớp. |
| K · Vướng xử lý hủy phía quán | Quán kể đơn bị hủy, việc hủy bị chặn, hoặc đơn không thể từ chối trong hoàn cảnh cụ thể. |
| B · Vướng bồi hoàn phía quán | Quán nêu vấn đề cụ thể với việc đề nghị bồi hoàn hoặc với khoản sàn hoàn cho khách. |
| E · Tranh chấp xác minh | Quán nêu việc thiếu bằng chứng hoặc cho rằng sàn hoàn tiền mà chưa đối chiếu sự cố. |

Một review có thể có nhiều nhãn. Nhãn Q, K, B và E chỉ áp dụng cho review phía quán. Với GrabMerchant, chỉ gắn khi nội dung cho thấy bối cảnh quán hoặc đơn món.

## 3. Kết quả

### Phía khách

| Hiện tượng | ShopeeFood · N=100 | Grab · N=100 | Tập con GrabFood · n=12 |
|---|---:|---:|---:|
| Chờ/giao lâu | 10/100 (10,0%) | 5/100 (5,0%) | 5/12 (41,7%) |
| Vướng hỗ trợ | 2/100 (2,0%) | 4/100 (4,0%) | 4/12 (33,3%) |
| Cả hai trong cùng review | 0/100 (0,0%) | 1/100 (1,0%) | 1/12 (8,3%) |
| Hủy đơn kèm vấn đề tiền | 2/100 (2,0%) | 1/100 (1,0%) | 1/12 (8,3%) |
| Sai món | 1/100 (1,0%) | 0/100 (0,0%) | 0/12 (0,0%) |
| Thiếu món | 0/100 (0,0%) | 0/100 (0,0%) | 0/12 (0,0%) |

Trong cột Grab N=100, tử số chỉ gồm các dòng xác định được là GrabFood. Cột n=12 mô tả riêng nhóm review nhận diện được dịch vụ này và có mẫu nhỏ. **SF054** cho thấy thời gian đợi 90 phút. **GF071** là trường hợp trực tiếp trong mẫu mới mô tả cả chờ/giao lâu lẫn vướng nhận hỗ trợ. Không có review nào từ phía khách đáp ứng tiêu chí thiếu món trong hai mẫu này.

### Phía quán

| Hiện tượng | ShopeeFood Merchant · N=100 | GrabMerchant · N=100 |
|---|---:|---:|
| Chậm hoặc trục trặc khâu giao nhận | 3/100 (3,0%) | 10/100 (10,0%) |
| Vướng xử lý hủy | 5/100 (5,0%) | 5/100 (5,0%) |
| Vướng bồi hoàn | 2/100 (2,0%) | 6/100 (6,0%) |
| Tranh chấp xác minh | 1/100 (1,0%) | 3/100 (3,0%) |

**GM029** là ví dụ cho thấy quyết định hủy và bồi hoàn có thể tác động đến quán đã làm món. **SM023** ghi nhận một tranh chấp về bằng chứng thiếu món từ phía quán. Review này cho thấy có tranh chấp xác minh, chưa thể xác định khách thực tế nhận thiếu món.

## 4. Ví dụ ẩn danh

Các dòng dưới đây được diễn giải từ review gốc. Mã là vị trí review trong bản lấy mẫu, theo từng app ở mục 1. Các trang nguồn có thể hiển thị review khác khi truy cập lại.

| Mã | Ngày | Sao | Nhãn | Ví dụ |
|---|---|---:|---|---|
| SF005 | 25/11/2026 | 1★ | G | Đơn đi khoảng 3 km nhưng mất hơn một tiếng để giao. |
| SF015 | 24/11/2026 | 1★ | H, C | Đơn bị hủy. Khách kể đã chờ hai tháng chưa thấy hoàn tiền và được yêu cầu cung cấp sao kê. |
| SF052 | 21/11/2026 | 1★ | H, S | Khách nói món thay thế không đúng loại đã đặt và không hủy được. |
| SF054 | 21/11/2026 | 1★ | G | Khách đặt lúc 10:37, nhận lúc 12:07, tổng thời gian 90 phút. Khách quy sự chậm trễ cho việc ghép đơn. |
| GF006 | 26/11/2026 | 1★ | H | Khách nhắc rõ GrabFood và kể chatbot không hiểu vấn đề, chưa xử lý được yêu cầu. |
| GF048 | 24/11/2026 | 1★ | G | Khách kể thời gian giao tăng từ 30 phút lên khoảng một tiếng dù không chọn giao tiết kiệm. |
| GF071 | 23/11/2026 | 1★ | G, H | Giờ giao ban đầu 11:42, sau đó đổi nhiều lần. Món tới lúc 12:04, muộn 22 phút so với giờ hiển thị ban đầu. Khách kể không gặp được chuyên viên khi nhắn hỗ trợ. |
| SM023 | 28/07/2024 | 1★ | E | Quán cho biết đã bị đánh giá thiếu đồ và cho rằng phía khách không đưa ra ảnh chứng minh. Đây là lời kể từ phía quán. |
| SM077 | 18/11/2022 | 1★ | K, B | Quán kể đã làm xong món thì đơn bị hủy. Khi xin bồi hoàn, quán cho biết hệ thống yêu cầu ảnh hóa đơn in trước khi hủy mà quán không có. |
| GM022 | 18/09/2026 | 5★ | Q | Quán kể món đã làm xong nhưng tài xế chưa đến lấy, trong khi tình trạng chậm lại được quy về phía quán. |
| GM029 | 12/09/2026 | 1★ | Q, K, B | Quán kể đã làm xong món, không có tài xế, đơn bị hủy và khiếu nại bồi hoàn chưa được xử lý. |

## 5. Kết luận cho Canvas và bảng impact

- **Giả thuyết có một ví dụ trực tiếp trong mẫu mới.** Dùng GF071 để minh họa khách vừa chờ vừa gặp khó khi tìm hỗ trợ. Các review khác cho thấy đơn chậm, hủy đơn và hoàn tiền có thể là những sự cố riêng biệt.
- **Lát cắt đề xuất.** Khi khách báo chờ lâu mà chưa nhận đồ ăn, AI tra trạng thái đơn và mốc giao dự kiến để quyết định hướng dẫn khách tiếp tục chờ, kiểm tra điều kiện hủy hoặc chuyển nhân viên, giúp khách biết bước tiếp theo.
- **Dữ liệu cần cho demo.** Giờ giao dự kiến ban đầu và cập nhật, thời điểm quán xác nhận hoặc làm xong, thời điểm có tài xế và lấy món, trạng thái hủy, trạng thái thanh toán. Chỉ đưa ra lý do cụ thể khi dữ liệu đơn xác nhận được.
- **Giới hạn.** Đây là tỷ lệ trong review do Google Play trả về, chưa đo tỷ lệ trên số đơn hay số lần mỗi khách gặp trong tháng. Các app có khoảng thời gian khác nhau, đặc biệt ShopeeFood Merchant có nhiều review cũ. Review tự thuật không xác nhận được bên nào có lỗi hay chính sách bồi hoàn đang áp dụng. ChatGPT hỗ trợ đọc và gắn nhãn từ nội dung review. Nhóm chưa kiểm lại độc lập.

## Phụ lục · Kiểm lại phép đếm

Mỗi mã dưới đây xuất hiện tối đa một lần trong một dòng nhãn. Tử số là số mã trong dòng. Với nhãn giao nhau, lấy số mã xuất hiện trong cả G và H cùng app. Mẫu số là 100 cho mỗi app hoặc 12 cho tập GF–F. Các mã không xuất hiện trong bảng vẫn nằm trong mẫu 100 của app tương ứng.

| App | Nhãn | Mã review |
|---|---|---|
| SF | G | SF005, SF018, SF026, SF030, SF039, SF053, SF054, SF070, SF082, SF083 |
| SF | H | SF015, SF052 |
| SF | C | SF015, SF016 |
| SF | S | SF052 |
| SF | M | — |
| GF | F | GF006, GF008, GF019, GF021, GF027, GF031, GF032, GF046, GF048, GF054, GF066, GF071 |
| GF | G | GF008, GF032, GF046, GF048, GF071 |
| GF | H | GF006, GF027, GF066, GF071 |
| GF | C | GF027 |
| GF | S | — |
| GF | M | — |
| SM | Q | SM012, SM079, SM080 |
| SM | K | SM012, SM077, SM079, SM080, SM086 |
| SM | B | SM012, SM077 |
| SM | E | SM023 |
| GM | Q | GM002, GM009, GM022, GM029, GM050, GM074, GM081, GM086, GM099, GM100 |
| GM | K | GM002, GM029, GM050, GM058, GM081 |
| GM | B | GM011, GM029, GM038, GM039, GM071, GM081 |
| GM | E | GM011, GM038, GM071 |

### Lấy lại mẫu theo cùng tiêu chí

Chạy đoạn dưới đây với `google-play-scraper==1.2.7`. Mẫu mới sẽ thay đổi theo ngày chạy. Bảng mã ở trên giữ kết quả đếm của bản chụp ngày 27/11/2026.

```python
from google_play_scraper import Sort, reviews

app_ids = [
    "com.deliverynow",
    "com.grabtaxi.passenger",
    "com.sea.foody.nowmerchant",
    "com.grab.merchant",
]

for app_id in app_ids:
    sample, _ = reviews(
        app_id, lang="vi", country="vn", sort=Sort.NEWEST, count=100
    )
    seen = set()
    for review in sample:
        review_id = review["reviewId"]
        if review_id in seen:
            continue
        seen.add(review_id)
        print(
            app_id,
            len(seen),
            review["at"].date(),
            review["score"],
            review["content"],
        )
```
