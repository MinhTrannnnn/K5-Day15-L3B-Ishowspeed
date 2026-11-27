# Tổng hợp bằng chứng · D1

> Hai mẫu bên dưới được phân tích riêng. Repo chưa lưu toàn bộ review gốc và bảng gắn nhãn từng dòng của mẫu Google Play để người đọc tái kiểm toàn mẫu.

| Nguồn | Cách dùng | Kết quả chính |
|---|---|---|
| [400 review Google Play](data-mining.md) | Mẫu chính, 100 review mỗi app. Giữ mẫu khách và quán riêng. App Grab có 12 review xác định được là GrabFood trong 100 review. | ShopeeFood có 10/100 chờ lâu hoặc giao muộn, 2/100 vướng hỗ trợ và 0/100 có cả hai. GrabFood có 5/12 chờ lâu hoặc giao muộn và 1/12 có cả hai. |
| [31 lời phàn nàn ShopeeFood có nguồn từ App Store](data-mining-app-store-31.md) | Mẫu đối chiếu từ trang tổng hợp, nghiêng về phản hồi tiêu cực. | 14/31 chờ lâu hoặc giao muộn, 6/31 vướng hỗ trợ, 2/31 có cả hai. |

### Ví dụ có thể dùng trong Canvas hoặc khi giải thích

- **GF071.** Khách GrabFood kể giờ giao dự kiến thay đổi nhiều lần, từ mốc đầu 11:42 đến các mốc muộn hơn. Đơn đến 12:04, và khách cho biết không gặp được chuyên viên khi nhắn hỗ trợ. [Bảng ví dụ Google Play](data-mining.md#4-ví-dụ-ẩn-danh)
- **SF054.** Khách ShopeeFood kể đặt lúc 10:37 và nhận lúc 12:07, tổng thời gian chờ 90 phút. [Bảng ví dụ Google Play](data-mining.md#4-ví-dụ-ẩn-danh)
- **GM029.** Quán kể đã làm xong món, không có tài xế, đơn bị hủy và khiếu nại bồi hoàn chưa được xử lý. [Bảng ví dụ Google Play](data-mining.md#4-ví-dụ-ẩn-danh)
- **R16 và R18.** Hai review trong mẫu đối chiếu kể chờ hoặc giao lâu kèm khó nhận hỗ trợ. R16 vẫn trước giờ dự kiến khi khách liên hệ, còn R18 mô tả đơn đã giao trễ. [Bảng gắn nhãn mẫu đối chiếu](data-mining-app-store-31.md#phụ-lục--bảng-đánh-nhãn-có-thể-kiểm-lại)

**Kết luận sơ bộ.** Có ví dụ trực tiếp về khách chờ lâu và chưa nhận được hỗ trợ cho cùng một đơn. Có thể dùng làm cơ sở cho lát cắt giúp khách biết trạng thái và bước tiếp theo. Số liệu mô tả review đã đọc, chưa đo được tần suất trên số đơn, thời gian tìm hỗ trợ hay tác động theo tháng. Tần suất review từ hai mẫu được giữ riêng vì khác cách chọn mẫu và phạm vi.

## Tiến độ chuẩn bị CP2

Đã tích hợp hai tài liệu và đưa 7 tình huống nguồn (SF054, GF071, GF006, R16, R18, R07, R24) thành 7 câu diễn giải trong bộ 20 câu thử. Mọi mã đơn và snapshot dùng để chạy là synthetic. Sổ phân công CP1 ghi Thành đã đối chiếu review gốc và rà nhãn. Repo chưa có bản lưu toàn mẫu để tái kiểm độc lập. CP2 chưa thu thập thêm review, phỏng vấn hoặc khảo sát. Quang phụ trách hồ sơ nguồn và data card, Cường kiểm chéo.


## Giả thuyết mở rộng sau khi Minh chọn thiết kế mới — 27/11/2026

Không có bằng chứng mới được thu thập trong lần sửa tài liệu này. Review hiện có chỉ hỗ trợ sơ bộ giao trễ và khó nhận hỗ trợ; chưa xác nhận đầy đủ nhu cầu dưới đây.

| Giả thuyết | Cần kiểm trước khi kết luận | Phụ trách |
|---|---|---|
| Khách phải kể lại sự việc và chưa biết ca được xử lý đến đâu | Hỏi về lần gần nhất, các bước đã làm, thông tin phải lặp lại và kết quả; ghi cả trường hợp không gặp trở ngại | Quang |
| Nhân viên cần hồ sơ có căn cứ và điểm mâu thuẫn | Trao đổi với người có trải nghiệm xử lý khiếu nại; kiểm họ có thể quyết định gì từ hồ sơ và còn thiếu gì. Chưa tiếp cận được thì ghi chưa xác minh | Quang, Minh |
| Khách muốn xem thời gian giao từ lịch sử trước khi chọn shop | Hỏi lần chọn shop gần nhất, ETA đã ảnh hưởng quyết định thế nào, họ xử lý khi ETA không đáng tin ra sao; tránh chỉ hỏi có thích tính năng không | Quang |

Không suy từ tổng thời gian giao ra thời gian tìm hỗ trợ; không dùng số review để suy ra tần suất theo đơn. Kế hoạch kiểm trước thu thập: [hypothesis](hypothesis.md). Việc ETA cần dữ liệu tất cả đơn hoàn tất là yêu cầu dữ liệu, không phải kết quả nghiên cứu người dùng.

## CP3 · Năm đoạn trích nguyên văn, ẩn tên

Đối chiếu ngày 27/11/2026 tại mục **Chính các đánh giá** của [bản lưu công khai review ShopeeFood từ App Store](https://opportunitymarket.org/vi/ung-dung/shopeefood-food-delivery). Mỗi dòng trích một cụm chữ nguyên văn từ một review khác nhau. Mã khớp [bảng mẫu 31 review](data-mining-app-store-31.md). Bản lưu tập trung vào lời phàn nàn nên chỉ dùng để xác định tình huống gặp phải.

| Mã | Trích nguyên văn | Điều khách mô tả |
|---|---|---|
| R03 | “gần 2 tiếng” | Đợi gần hai tiếng mới nhận đơn. |
| R07 | “ko có bất kì 1 ai hỗ trợ” | Không nhận được hỗ trợ qua chat sau khi đơn báo hủy. |
| R13 | “1 đến 3 tiếng” | Khách mô tả thời gian chậm của các đơn được ghép. |
| R16 | “chưa có tài xế” | Khách xem đơn hơn một tiếng sau khi đặt, lúc đó chưa đến giờ giao dự kiến. |
| R24 | “7-30 ngày mới hoàn” | Khách kể mốc hoàn cho đơn trả trước đã bị hủy. |
