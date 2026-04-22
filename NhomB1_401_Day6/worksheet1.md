# Worksheet 1 — Deploy Demo vs Deploy Enterprise

**Sản phẩm:** VFCare — AI dự đoán & đặt lịch bảo dưỡng xe VinFast
**Nhóm:** B1-C401
**Mục tiêu:** Hiểu vì sao deploy demo và deploy enterprise là hai bài toán khác nhau

---

## 1. Bối cảnh tổ chức / khách hàng sử dụng hệ thống

| Tầng | Tổ chức | Vai trò trong hệ thống |
|---|---|---|
| **Owner dữ liệu xe** | VinFast (OEM) | Kiểm soát telemetry API, CRM, hệ thống xưởng |
| **Operator fleet** | XanhSM | Vận hành hàng nghìn xe tập trung — khách hàng enterprise điển hình nhất |
| **Doanh nghiệp B2B** | Công ty có đội xe VinFast (logistics, taxi địa phương) | Dùng như SaaS fleet management |
| **End user cá nhân** | Chủ xe VinFast bận rộn | Tương tác qua app, không tiếp xúc hạ tầng |

**Khác biệt demo vs enterprise ở tầng này:**
Demo chỉ cần 1 user test với dữ liệu giả. Enterprise phải phục vụ đồng thời nhiều tổ chức với dữ liệu xe thật, mỗi tổ chức có policy riêng về ai được xem dữ liệu gì.

---

## 2. Dữ liệu mà hệ thống sẽ động đến

| Loại dữ liệu | Nguồn | Mô tả |
|---|---|---|
| Telemetry cảm biến xe | IoT / VinFast Connect | Pin health, motor status, hệ thống treo, điều hòa, ODO |
| Vị trí GPS | App / xe | Vị trí thời gian thực để gợi ý xưởng gần nhất |
| Hành vi lái xe | Telemetry | Thói quen tăng tốc, phanh, quãng đường hằng ngày |
| Thông tin định danh | CRM VinFast | Biển số, số điện thoại, tên chủ xe |
| Lịch sử bảo dưỡng | CRM / ERP xưởng | Các lần vào xưởng trước, hạng mục đã làm |
| Slot & booking | Hệ thống đặt lịch xưởng | Lịch trống, booking ID, trạng thái xác nhận |
| Feedback log | App | Accept / reject / modify của từng lần AI gợi ý |
| Tồn kho phụ tùng | ERP xưởng | Cross-check khi AI phát hiện lỗi phần cứng |
| Dữ liệu môi trường | API thời tiết | Nhiệt độ, độ ẩm, điều kiện đường ảnh hưởng dự đoán |

---

## 3. Đánh giá mức độ nhạy cảm của dữ liệu

| Dữ liệu | Mức độ nhạy cảm | Lý do |
|---|---|---|
| Vị trí GPS liên tục | **Rất cao** | Biết chủ xe đang ở đâu, đi đâu, lúc nào — có thể bị lạm dụng để theo dõi |
| Hành vi lái xe | **Cao** | Profiling cá nhân; có thể dùng để đánh giá bảo hiểm hoặc rủi ro tín dụng |
| Thông tin định danh (SĐT, biển số) | **Cao** | PII trực tiếp, thuộc phạm vi Nghị định 13/2023/NĐ-CP |
| Feedback log | **Trung bình** | Gián tiếp phản ánh lịch trình và thói quen cá nhân |
| Lịch sử bảo dưỡng | **Trung bình** | Kết hợp với định danh → tiết lộ tình trạng tài sản |
| Telemetry kỹ thuật (pin, motor) | **Thấp** | Dữ liệu kỹ thuật thuần túy, nhưng nhạy cảm khi kết hợp với vị trí |
| Tồn kho phụ tùng | **Thấp** | Dữ liệu vận hành nội bộ xưởng |

**Gợi ý thảo luận — nếu trả lời sai thì ai bị ảnh hưởng đầu tiên?**
- AI nhắc sai (false positive): chủ xe mất thời gian, tốn tiền vào xưởng không cần thiết
- AI bỏ sót (false negative): xe hỏng giữa đường, chủ xe chịu rủi ro an toàn và chi phí đột xuất
- Dữ liệu vị trí bị lộ: chủ xe và gia đình bị ảnh hưởng trực tiếp
- Slot booking sai: cả chủ xe lẫn xưởng bị ảnh hưởng (chủ xe đến không có chỗ, xưởng mất slot)

---

## 4. Ba ràng buộc enterprise lớn nhất

### Ràng buộc 1 — Data sovereignty (Dữ liệu không được rời lãnh thổ)
Luật An ninh mạng 2018 và Nghị định 13/2023/NĐ-CP yêu cầu dữ liệu cá nhân của người dùng Việt Nam (vị trí, hành vi, định danh) phải được lưu trữ trên hạ tầng đặt tại Việt Nam. Nếu dùng cloud API nước ngoài (OpenAI, Claude) và truyền raw PII lên đó là vi phạm.

> **Tác động:** Không thể dùng cloud API trực tiếp với dữ liệu thô. Phải anonymize/tách PII trước khi gọi LLM inference.

### Ràng buộc 2 — Audit trail bắt buộc
Mỗi quyết định AI (nhắc bảo dưỡng, xác nhận slot, hủy lịch) phải có log đầy đủ: timestamp, input data, output, user action. Lý do: nếu xe hỏng sau khi AI báo "chưa cần bảo dưỡng", VinFast cần bằng chứng để xử lý khiếu nại.

> **Tác động:** Phải thiết kế logging pipeline từ đầu, không thể thêm sau. Tăng chi phí lưu trữ và đặt ra yêu cầu về retention policy.

### Ràng buộc 3 — Tích hợp hệ thống cũ (Legacy integration)
VinFast đã có CRM, hệ thống đặt lịch xưởng, ERP phụ tùng vận hành từ trước. Hệ thống mới phải gọi được các API này (check_slot_availability, book_appointment, kho phụ tùng) mà không thể yêu cầu VinFast rebuild toàn bộ. Đồng thời, quy trình phê duyệt booking tại xưởng hiện tại vẫn cần được tôn trọng (2-way handshake).

> **Tác động:** Phải có integration layer, xử lý API timeout/error, và không thể assume hệ thống xưởng luôn sẵn sàng realtime.

---

## 5. Lựa chọn mô hình triển khai

**☑ Hybrid** (On-prem + Public Cloud)

| Layer | Mô hình | Lý do |
|---|---|---|
| Lưu trữ dữ liệu nhạy cảm (GPS, PII, feedback log) | On-prem / Private cloud tại VN | Tuân thủ Luật An ninh mạng |
| AI inference (LLM calls) | Public cloud API | Không giữ PII, chỉ truyền anonymized sensor data |
| Push notification, app backend | Public cloud | Không chứa PII, cần scale toàn cầu |
| Audit log | On-prem | Cần retention dài hạn, không muốn phụ thuộc vendor |

---

## 6. Hai lý do chọn Hybrid

**Lý do 1 — Tuân thủ pháp lý mà không từ bỏ khả năng AI**
Dữ liệu vị trí và hành vi lái xe là PII theo Nghị định 13/2023 — phải lưu tại Việt Nam. Nhưng chạy LLM inference on-prem đòi hỏi GPU infrastructure đắt tiền và khó maintain. Hybrid giải quyết bằng cách: anonymize/tách PII tại on-prem, sau đó chỉ gửi feature vector kỹ thuật (không có PII) lên cloud API để inference. Dữ liệu nhạy cảm không rời khỏi tổ chức; khả năng AI vẫn được tận dụng.

**Lý do 2 — Workload không đều, cloud giúp auto-scale đúng lúc**
Phần lớn người dùng kiểm tra app vào buổi sáng trước khi đi làm → traffic AI inference có peak rõ ràng. Nếu dùng on-prem hoàn toàn, phải overspec phần cứng cho peak nhưng idle phần lớn thời gian — lãng phí. Public cloud cho phép scale up trong giờ cao điểm và scale down khi nhàn, phù hợp với cost model $0.005–0.02/xe/ngày mà spec đề ra.

---

## Tổng kết: Demo vs Enterprise

| Khía cạnh | Demo | Enterprise |
|---|---|---|
| Dữ liệu | Giả, không nhạy cảm | Thật, có PII, phải tuân thủ luật |
| Hạ tầng | Laptop / free tier cloud | Hybrid, có SLA, có DR plan |
| Audit | Không cần | Bắt buộc, retention dài hạn |
| Tích hợp | Mock API | Phải nối CRM, ERP, hệ thống xưởng thật |
| Scale | 1 user test | Hàng nghìn xe đồng thời |
| Rủi ro khi sai | Restart lại | Khiếu nại pháp lý, mất niềm tin khách hàng |
