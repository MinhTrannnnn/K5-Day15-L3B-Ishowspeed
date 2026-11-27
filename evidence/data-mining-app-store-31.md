# Đào dữ liệu công khai · D1 — Khiếu nại đơn giao đồ ăn

> Nguồn chuyển vào repo: tài liệu `CP1-D1/` do nhóm cung cấp ngày 27/11/2026. Chưa có bản lưu đầy đủ review gốc và bảng gắn nhãn từng dòng cho mẫu Google Play trong repo; chưa đối chiếu độc lập. Các số dưới đây là số liệu tài liệu tham khảo báo cáo, không phải kết quả thu thập mới trong repo này.

Ngày xem 27/11/2026. Đây là phần 1.2 theo hướng đào review công khai.

## Giả thuyết cần kiểm

Khi nhận đơn thiếu một món, khách có thể gặp khó khi tìm kênh hỗ trợ, cung cấp bằng chứng hoặc biết khi nào phần tiền tương ứng được hoàn. Dấu hiệu trực tiếp là một review vừa mô tả món bị thiếu trong đơn đã nhận, vừa kể rõ một vướng mắc khi xin xử lý.

## 1. Cách chọn mẫu và đếm

- Lấy toàn bộ nhận xét tại mục **Chính các đánh giá** trên bản trang OpportunityMarket đọc được, theo thứ tự hiển thị từ trên xuống. Trang này tập hợp phàn nàn về ứng dụng ShopeeFood từ App Store, nên mẫu đã nghiêng về phản hồi tiêu cực. Giữ cả dòng không liên quan tới D1. Bỏ các bản lặp ở phần tổng hợp phía trên. [Trang lấy mẫu](https://opportunitymarket.org/vi/ung-dung/shopeefood-food-delivery)
- Đơn vị đếm là **một review**, mẫu số **N = 31**. Khoảng ngày của bản trang đối chiếu được là **15/09/2026–20/11/2026**. Một số dòng chỉ hiện ngày tương đối, được giữ dưới dạng đó trong bảng. Bản trích xuất hiển thị biểu tượng sao không đủ rõ để xác minh số sao từng dòng, nên không phân nhóm theo sao. [Trang App Store gốc](https://apps.apple.com/vn/app/shopeefood-food-delivery/id1137866760?see-all=reviews)
- Đọc thử khoảng 30 dòng rồi áp dụng các nhãn dưới đây cho toàn bộ 31 dòng. Một dòng có thể có nhiều nhãn. Đếm bằng số dòng có nhãn, chia cho 31 rồi nhân 100. Có thể kiểm lại trong Sheets bằng `=COUNTIF(C2:C32,"*G*")/COUNTA(A2:A32)` sau khi dán bốn cột của phụ lục vào A–D, rồi định dạng phần trăm. Thay G bằng mã nhãn cần kiểm. 

| Nhãn | Quy tắc gắn |
|---|---|
| M | Khách nói đã nhận đơn đồ ăn và thiếu ít nhất một món hoặc một phần của món. |
| K | Cùng review có nhãn M và mô tả một trở ngại cụ thể khi tìm hỗ trợ hoặc xin hoàn tiền. |
| S | Khách nói món nhận được khác món đã đặt. |
| G | Thân review nói khách thực tế chờ lâu, nhận muộn, hoặc mô tả thời gian giao/chờ mà họ thấy quá lâu. Chỉ đổi giờ giao dự kiến ngay sau khi đặt chưa đủ để gắn nhãn. |
| H | Mô tả trở ngại cụ thể khi tìm hoặc nhận hỗ trợ, như chat không có người trả lời, khó gọi, bằng chứng gửi lên không được xem, hoặc đã liên hệ mà chưa được giải quyết. |
| T | Đơn bị hủy và review nêu một thời gian chờ hoàn tiền. Trường hợp chưa rõ đã được hoàn hay chưa vẫn có thể gắn nhãn nếu review nêu thời gian được báo. |

## 2. Kết quả

| Nội dung | x/N | Tỷ lệ trong mẫu |
|---|---:|---:|
| Thiếu món (M) | 0/31 | 0,0% |
| Thiếu món kèm vướng hỗ trợ (K) | 0/31 | 0,0% |
| Sai món (S) | 0/31 | 0,0% |
| Chờ/giao lâu (G) | 14/31 | 45,2% |
| Vướng khi tìm hỗ trợ (H) | 6/31 | 19,4% |
| Được báo phải chờ hoàn tiền sau khi hủy (T) | 1/31 | 3,2% |

Mẫu cho thấy các vướng mắc về chờ giao và hỗ trợ xuất hiện lặp lại. Các trường hợp giao trễ có thể kiểm được giờ đặt, thời điểm khách liên hệ và trạng thái đơn trong review. Riêng giả thuyết về khó khiếu nại đơn đã nhận thiếu món chưa được kiểm chứng trong mẫu này.

## 3. Năm ví dụ ẩn danh

| Mã | Trích đoạn | Ngữ cảnh |
|---|---|---|
| R03 | “gần 2 tiếng” | Khách kể phải đợi gần hai tiếng mới được giao. |
| R07 | “Khi chat support” | Đơn báo hủy sau khi trừ tiền, khách kể không có người hỗ trợ qua chat. |
| R13 | “1 đến 3 tiếng” | Khách nói nhiều đơn ghép mất từ một đến ba tiếng theo lời kể. |
| R16 | “chưa có tài xế” | Hơn một tiếng sau khi đặt vẫn chưa có tài xế, nhân viên chưa giúp xử lý được. |
| R24 | “7-30 ngày mới hoàn” | Quán hủy đơn trả trước. Đây là thời gian khách kể ứng dụng báo sẽ hoàn. |

Nguồn của cả năm trích đoạn là mục **Chính các đánh giá** trên [trang tổng hợp nhận xét ShopeeFood](https://opportunitymarket.org/vi/ung-dung/shopeefood-food-delivery).

## 4. Nguồn bổ sung cho lát cắt thiếu món

- Grab công bố ngày 14/08/2026 rằng khoảng **20% trong số các báo cáo thiếu món** ở thử nghiệm của hãng là **thiếu một phần món**. Ví dụ gồm thiếu món tráng miệng trong combo, thiếu một miếng trong suất nhiều miếng, hoặc thiếu nước dùng đóng riêng. Grab mô tả hai khó khăn từng gặp là hoàn cả món gây chi phí cho quán và chuyển mọi ca thiếu một phần sang nhân viên làm khách chờ lâu. Đây là dữ liệu Grab tự công bố ở phạm vi khu vực, không công bố số tuyệt đối x/N hoặc số riêng cho Việt Nam. [Bài viết của Grab Support](https://www.grab.com/inside-grab/stories/how-we-taught-llms-to-solve-the-missing-muffins-mystery/)
- Điều khoản ShopeeFood dành cho người bán cũng liệt kê **sai hoặc thiếu nguyên món** trong phạm vi khiếu nại có quy trình xác minh bằng chứng. Tài liệu này xác nhận loại sự cố có trong quy trình, còn tần suất và trải nghiệm khách phải tìm từ nguồn khác. [Điều khoản ShopeeFood Merchant](https://resource.foody.vn/web/merchant-private-policy.html)

## 5. Giới hạn và kết luận sơ bộ

Tỷ lệ trong bảng chỉ áp dụng cho 31 lời phàn nàn đã thu thập. Các review tự thuật, thiếu số đơn dùng app, thiếu thông tin về số lượt trao đổi và thường không kể kết quả sau cùng. Ngày tương đối trên trang có thể thay đổi. Bảng dưới đây giữ thứ tự và tóm tắt của bản đã đọc để kiểm lại phép đếm.

**Kết luận về giả thuyết:** chưa đủ bằng chứng để kết luận khách ShopeeFood nhận thiếu món phải qua nhiều lượt hỗ trợ. Grab cho thấy bài toán định mức bồi thường khi thiếu một phần có thật trong vận hành. Nếu giữ lát cắt **thiếu một món**, đây là bằng chứng bối cảnh để trình bày ở CP1. Trong mẫu ShopeeFood, tình huống **chờ giao lâu kèm vướng hỗ trợ** có các ví dụ trực tiếp hơn (R16, R18).

## Phụ lục · Bảng đánh nhãn có thể kiểm lại

Mỗi dòng là một review được diễn giải ngắn và ẩn tên. Nguồn chung là mục **Chính các đánh giá** tại [trang ShopeeFood trên OpportunityMarket](https://opportunitymarket.org/vi/ung-dung/shopeefood-food-delivery).

| Mã | Ngày theo nguồn | Nhãn | Diễn giải |
|---|---|---|---|
| R01 | 20/11/2026 | G | Đơn giao lâu, người viết quy cho ghép đơn. |
| R02 | 20/11/2026 | H | Khách cho biết bằng chứng đã gửi không được xem và họ mất tiền. Loại sự cố ban đầu chưa rõ. |
| R03 | 3 ngày trước | G | Khách kể đơn mất gần hai tiếng mới giao. |
| R04 | 3 ngày trước | G | Sau khi lấy đồ uống, thời gian giao dự kiến là 45 phút cho 700 m. Khách cho biết tổng thời gian của tài xế hơn một tiếng. |
| R05 | 4 ngày trước | G | Khách chờ hai tiếng mà chưa nhận đồ ăn. |
| R06 | 18/11/2026 | G | Quãng đường khoảng 3 km nhưng sau hơn 50 phút đơn vẫn chưa đến. |
| R07 | 18/11/2026 | H | Đơn báo hủy sau khi trừ tiền thẻ. Khách chat nhưng không gặp người hỗ trợ, kết quả hoàn tiền chưa rõ. |
| R08 | 5 ngày trước | — | Định vị sai khiến tài xế đi xa và khó tìm điểm giao. |
| R09 | 5 ngày trước | G | Khách chờ khoảng một tiếng mà chưa có đồ. |
| R10 | 5 ngày trước | — | Khách kể không nhận được cuộc gọi và bị yêu cầu trả thêm phí giao lại. |
| R11 | 6 ngày trước | — | Người viết cho biết giao diện mới khiến tài xế không xem được ghi chú. |
| R12 | 16/11/2026 | — | Nhiều tài xế hủy và khách không tự hủy được đơn ưu tiên. |
| R13 | 16/11/2026 | G | Khách phàn nàn các đơn ghép giao chậm từ một đến ba tiếng theo lời kể. |
| R14 | 7 ngày trước | — | Gặp lỗi thao tác chỉnh địa chỉ và phải đặt lại khi quay về màn trước lúc thanh toán. |
| R15 | 7 ngày trước | — | Ứng dụng yêu cầu đăng nhập lại dù đã báo thành công. |
| R16 | 7 ngày trước | G, H | Đặt lúc 13:56, đến 15:00 vẫn chưa có tài xế, giờ giao dự kiến là 15:10. Khách cho biết nhân viên chưa giải quyết được. |
| R17 | 18/09/2026 | — | Không nhập được mã OTP khi xác minh tài khoản. |
| R18 | 18/09/2026 | G, H | Đơn giao sau giờ đã đặt. Khách không liên hệ được tài xế hay hotline. |
| R19 | 17/09/2026 | — | Tài xế gọi số cũ dù khách đã cập nhật số trên app rồi hủy đơn. |
| R20 | 17/09/2026 | G | Chờ hai tiếng chưa có đồ. Người viết nhắc đến việc ghép đơn. |
| R21 | 17/09/2026 | G | Đến giờ giao mà quán chưa làm món, khách kể mình không tự hủy được đơn. |
| R22 | 16/09/2026 | — | Chê khâu hỗ trợ khiếu nại nhưng không mô tả trở ngại cụ thể. |
| R23 | 16/09/2026 | — | Phàn nàn về thái độ tài xế và định vị. |
| R24 | 16/09/2026 | T | Quán hủy đơn bánh đã trả trước. Khách kể được báo thời gian hoàn là 7–30 ngày. |
| R25 | 16/09/2026 | G | Khách than chờ lâu, chưa thấy giao và không hủy được đơn ghép. |
| R26 | 16/09/2026 | G | Khách đặt quán gần nhà nhưng khoảng một tiếng mới nhận. |
| R27 | 15/09/2026 | H | Khách kể chưa có tài xế nhận và không hủy được. Kênh hỗ trợ mà họ tìm được chỉ có trợ lý tự động. |
| R28 | 15/09/2026 | G | Khách kể đặt lúc 11 giờ, đến 13 giờ vẫn chưa giao. |
| R29 | 15/09/2026 | H | Giờ dự kiến tăng từ 50 phút lên 95 phút ngay sau khi đặt. Khách không hủy được và cho biết không được hỗ trợ. |
| R30 | 4 ngày trước | — | Phàn nàn chung về lỗi ứng dụng. |
| R31 | 16/09/2026 | — | Phàn nàn về mặt hàng không bán trên ứng dụng. |
