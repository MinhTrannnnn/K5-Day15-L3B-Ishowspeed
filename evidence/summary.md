# Tổng hợp bằng chứng · D1

> Nguồn chuyển vào repo: tài liệu `CP1-D1/` do nhóm cung cấp ngày 27/11/2026. Chưa có bản lưu đầy đủ review gốc và bảng gắn nhãn từng dòng cho mẫu Google Play trong repo; chưa đối chiếu độc lập. Các số dưới đây là số liệu tài liệu tham khảo báo cáo, không phải kết quả thu thập mới trong repo này.

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
