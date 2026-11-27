# AI SPEC — Hỗ trợ khách chờ đơn giao đồ ăn · Nhóm Ishowspeed

Track: [x] D — D1, khiếu nại đơn giao đồ ăn.
Dữ liệu tham khảo (nguồn CP1-D1 do nhóm cung cấp; chưa đối chiếu độc lập review gốc): review công khai, gồm dữ liệu Google Play lấy trực tiếp và mẫu đối chiếu nguồn App Store.

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*

1. Khách đặt món và xem giờ giao dự kiến.
2. Khi đã chờ lâu, khách mở Chi tiết đơn để xem trạng thái và giờ giao cập nhật.
3. Khách kiểm tra khả năng tự hủy hoặc mở Trung tâm Trợ giúp từ màn hình đơn.
4. Nếu đã hủy, với đơn trả trước khách còn cần biết khoản hoàn đang ở bước nào.

Các bước hỗ trợ và hủy đơn tham chiếu tài liệu công khai của ShopeeFood. Bản demo dùng dữ liệu đơn giả lập. [Hướng dẫn khiếu nại](https://help.shopee.vn/portal/4/article/79520-) · [Hướng dẫn hủy đơn](https://help.shopee.vn/portal/4/article/79383-)

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*

- **Người dùng chính:** Khách tự đặt món qua app, đang đợi nhận và trực tiếp kiểm tra hoặc yêu cầu hỗ trợ cho đơn của mình.
- **Việc họ muốn làm:** Xác định đơn còn được giao hay đã hủy để quyết định chờ tiếp hoặc yêu cầu xử lý khi đã đợi lâu.
- **Họ đang xử lý thế nào:** Mở Chi tiết đơn, xem giờ dự kiến và trạng thái, rồi vào trợ giúp hoặc tìm nút hủy. Khi giờ dự kiến thay đổi nhiều lần hoặc phản hồi hỗ trợ chưa giải quyết được, họ vẫn chưa biết có nên chờ. Chi tiết đơn và trợ giúp trong app là các kênh khách có thể tìm ngay từ chính đơn đang chờ. [Quy trình ShopeeFood](https://help.shopee.vn/portal/4/article/79520-) · [Ví dụ GF071](evidence/data-mining.md#4-ví-dụ-ẩn-danh)
- **Bài toán:** Khách đặt đồ ăn qua app kiểm tra đơn khi đã chờ lâu nhưng có lúc vẫn chưa rõ đơn còn được giao hay đã bị hủy. Họ có thể mất thêm thời gian tìm hỗ trợ trước khi biết nên chờ tiếp, hủy hay yêu cầu xử lý.
- **Bằng chứng sơ bộ theo tài liệu CP1-D1, chưa đối chiếu nguồn gốc:** Trong 100 review ShopeeFood trên Google Play, 10 nói chờ lâu hoặc giao muộn. Trong 12 review nhận diện là GrabFood từ 100 review app Grab, 1 vừa nói chờ lâu vừa kể khó nhận hỗ trợ. Mẫu đối chiếu có 2/31 lời phàn nàn ShopeeFood mô tả cả hai. [Tổng hợp bằng chứng](evidence/summary.md)
- **Tình huống cá nhân để thảo luận:** Đặt bữa trưa qua app, thấy giờ giao dự kiến là 12:00. Đến 12:15 vẫn chưa nhận món; giờ dự kiến đổi thành 12:30 nhưng màn hình không nói rõ tài xế đã nhận đơn hay chưa. Mở Chi tiết đơn, tìm nút hủy rồi vào Trợ giúp để hỏi có nên chờ tiếp. Sau khoảng 10 phút tìm và gửi yêu cầu thì vẫn chưa biết đơn còn được giao hay có thể hủy, nên chưa thể quyết định đặt món khác.

## §2. Impact & quyết định chọn *(guide 1.3)*

| Hướng | Dấu hiệu trong review | Số lần/người/tháng | Mỗi lần tốn gì | Impact/tháng | Làm kịp? | Quyết định dự kiến |
|---|---|---|---|---|---|---|
| **Chờ lâu, chưa rõ trạng thái đơn** | Google Play: ShopeeFood 10/100 nói chờ/giao lâu, GrabFood 1/12 nói cả chờ lâu lẫn khó nhận hỗ trợ. Mẫu đối chiếu: 2/31 nói cả hai. | [NHÓM ĐIỀN số có nguồn hoặc tự ước tính] | SF054 kể tổng thời gian chờ 90 phút. GF071 kể giao muộn 22 phút so với mốc ban đầu, chưa đo thời gian tìm hỗ trợ riêng. | Xem công thức bên dưới. | Có thể demo bằng đơn giả lập và vài trạng thái đơn. | **Chọn dự kiến** |
| **Thiếu món** | 0/100 review khách ShopeeFood và 0/12 review GrabFood nói đã nhận đơn thiếu món. Có một tranh chấp xác minh từ phía quán, SM023. | Chưa đo | Có thể cần giao bù hoặc hoàn tiền phần thiếu. Chưa đo thời gian xử lý. | Chưa tính | Có thể demo, nhưng cần dữ liệu món và quy tắc bồi hoàn rõ. | Chưa chọn vì mẫu hiện tại thiếu trường hợp trực tiếp từ phía khách. |
| **Sai món** | 1/100 review ShopeeFood nêu nhận sai loại món, SF052. Trong tập GrabFood là 0/12. | Chưa đo | SF052 kể món giao sai loại và không hủy được đơn. Chưa đo thời gian xử lý hay chi phí. | Chưa tính | Có thể demo nếu có dữ liệu món đã đặt và món nhận được. | Chưa chọn vì bằng chứng trực tiếp ít hơn hướng chờ lâu. |

**Công thức impact/tháng cho hướng chọn** = số khách gặp vấn đề trong phạm vi nhóm chọn × số lần mỗi khách gặp/tháng × số phút tìm hỗ trợ mỗi lần. Nhóm xác nhận ba đầu vào trước khi dùng làm dự báo. Ví dụ minh họa cách tính, **toàn bộ đầu vào là tự ước tính**: 10 khách × 1 lần/tháng × 5 phút = **50 phút tìm hỗ trợ/tháng**. Số 10 khách ở ví dụ độc lập với 10/100 review, và 90 phút chờ giao không được dùng làm số phút tìm hỗ trợ.

**Tần suất cho persona:** [NHÓM ĐIỀN theo dữ kiện hoặc đánh dấu tự ước tính khi chốt phạm vi mô phỏng].

Chi tiết nguồn và mã review ở [bản Google Play](evidence/data-mining.md) và [bản đối chiếu](evidence/data-mining-app-store-31.md).

**Tình trạng kiểm chứng:** Chưa có bản lưu đầy đủ review gốc hoặc bảng gắn nhãn toàn mẫu Google Play trong repo; các ví dụ Google Play là diễn giải, không phải trích dẫn nguyên văn. Chưa tuyên bố đạt ngưỡng bằng chứng CP3.

## §3. Giải pháp tương tự *(guide 2.1)*
- [sản phẩm / tính năng gần giống]: một điều đáng học · một điều đáng né · mình khác gì

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt dự kiến:** Khi khách báo đã chờ lâu mà chưa nhận đồ ăn, AI tra trạng thái đơn và giờ giao dự kiến để quyết định hướng dẫn khách chờ tiếp, kiểm tra khả năng hủy hoặc chuyển nhân viên, giúp khách biết bước tiếp theo.
- Không làm (≥3 điều):
- **Sơ đồ** (ảnh / Mermaid / draw.io): [chèn ở đây]
- **Hình dạng:** [ ] workflow cố định · [ ] một agent · [ ] nhiều agent — 2 dòng lý do, và vì sao **không** chọn hình dạng phức tạp hơn:
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  |  |  |  |  |

- **Mức tự động dự kiến:** AI tự tra cứu và soạn hướng dẫn từ trạng thái đơn; hủy đơn, hoàn tiền, gửi yêu cầu và chuyển ca ra ngoài cần người phụ trách duyệt. Hủy sai có thể làm quán mất đơn đã chuẩn bị, hoàn sai làm quán hoặc khách mất tiền.
- **Chỗ chặn rủi ro dự kiến:** code kiểm điều kiện và hạn mức theo chính sách dựng có nguồn rõ; không suy ra lý do chậm khi dữ liệu không có; thiếu hoặc mâu thuẫn trạng thái thì đề xuất chuyển nhân viên; không coi mốc giao dự kiến là bảo đảm.
- **Chỗ người duyệt:** mọi thao tác hủy đơn, hoàn tiền hoặc tác động ra ngoài; không hứa bồi thường vượt chính sách.
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc |  |
  |  |  |
  |  |  |

- Phần còn giả: repo hiện vẫn là khung BTC, chưa triển khai luồng D1; demo dự kiến dùng đơn, quán, thanh toán và chính sách dựng có seed, không có giao dịch thật.

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
|  |  |  |  |
| *(tấn công)* |  |  |  |
| *(tấn công)* |  |  |  |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: · Không chắc (lớp 2): · Không có căn cứ (lớp 1): · Người dùng sửa:
- Bị đòi ngoài phạm vi (lớp 3): · Trường hợp đặc thù lĩnh vực (lớp 4):

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — __ câu (thuong __ · kho __ · tu_choi __) · metric: `eval/metric_spec.yaml` (__ metric)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ __% câu qua, và __"
- Kết quả: lượt 1 __/__ (__%) · lượt 2 __/__ (__%) — run ID: __ / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: đã ẩn danh gì, không thu gì, không đưa gì vào model gói miễn phí:
- AI **không được** tự hủy hoặc hoàn tiền; bồi thường vượt hạn mức; tiết lộ địa chỉ, số điện thoại hai bên; coi lời dọa là căn cứ. Nghi ngộ độc, dị ứng hoặc dị vật phải đề xuất chuyển người ngay.
- Ai có thể bị hại nếu AI sai, và nhóm chặn thế nào:

## §10. Phân công & changelog
- Phân công: Trần Quang Minh điều phối nhóm, quản lý repo và nộp checkpoint; các thành viên khác chờ bổ sung, khớp TEAMS.md.
- Dùng AI: Codex đối chiếu tài liệu CP1-D1 do nhóm cung cấp và soạn bản đầu canvas, spec, tổng hợp bằng chứng. Chưa đối chiếu độc lập review gốc; Trần Quang Minh cần kiểm lại nội dung trước khi dùng số liệu làm kết luận. Chi tiết: `docs/ai-usage.md`.
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
|  |  |  |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
