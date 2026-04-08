# 1. AI Product Canvas

**Đề tài:** `VFCare` - Trợ lý AI dự đoán và tự động đặt lịch bảo dưỡng xe VinFast cá nhân hóa.

## Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi guide** | User nào? Pain gì? AI giải quyết gì mà cách hiện tại không giải được? | Khi AI sai thì user bị ảnh hưởng thế nào? User biết AI sai bằng cách nào? User sửa bằng cách nào? | Cost bao nhiêu/request? Latency bao lâu? Risk chính là gì? |
| **Trả lời** | **User:** Chủ xe VinFast cá nhân (đặc biệt người đi làm bận rộn, chạy xe hằng ngày). **Pain:** Không biết chính xác khi nào cần bảo dưỡng, thường chỉ nhớ theo mốc km cố định hoặc khi xe có dấu hiệu bất thường -> phát sinh chờ đợi lâu và chi phí bất ngờ. **Value:** AI phân tích dữ liệu thời gian thực từ xe (pin, motor, hệ thống treo, điều hòa, quãng đường, thói quen lái, môi trường) để dự đoán thời điểm bảo dưỡng tối ưu, chủ động nhắc nhở và gợi ý khung giờ/xưởng gần nhất. | **Khi AI sai:** Có thể nhắc sớm (mất thời gian) hoặc nhắc muộn (tăng rủi ro hỏng hóc/chi phí). **User biết AI sai:** Đối chiếu với cảnh báo thực tế từ xe, lịch sử bảo dưỡng gần nhất, hoặc cảm nhận vận hành bất thường. **User sửa:** 1 chạm đổi thời gian đề xuất, chọn xưởng khác, hoặc bấm "chưa cần bảo dưỡng"; hệ thống ghi nhận phản hồi để học theo từng người dùng. | **Cost ước lượng:** ~`$0.005-0.02`/xe/ngày cho suy luận + đồng bộ dữ liệu (tùy tần suất). **Latency mục tiêu:** `<2s` cho gợi ý lịch trong app, `<200ms` cho scoring nền theo batch/stream. **Risk chính:** dự đoán sai dẫn tới mất niềm tin; thiên lệch theo kiểu lái hiếm; phụ thuộc chất lượng dữ liệu cảm biến; rủi ro quyền riêng tư dữ liệu hành vi và vị trí. |

---

## Automation hay augmentation?

☐ Automation - AI làm thay, user không can thiệp  
☑ Augmentation - AI gợi ý, user quyết định cuối cùng

**Justify:** Chọn **Augmentation** vì quyết định bảo dưỡng liên quan chi phí và an toàn; người dùng cần quyền xác nhận cuối. Cost of reject gần bằng 0 (từ chối gợi ý hoặc dời lịch rất nhanh), trong khi automation hoàn toàn khi AI sai có thể gây trải nghiệm tệ và mất trust.

---

## Learning signal

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | User correction đi vào đâu? | Mọi thao tác đổi lịch, từ chối lịch, đổi xưởng, đổi lý do bảo dưỡng được ghi vào `feedback log` gắn theo xe + ngữ cảnh (mốc km, thời tiết, kiểu lái), đưa vào pipeline tinh chỉnh mô hình dự đoán theo chu kỳ. |
| 2 | Product thu signal gì để biết tốt lên hay tệ đi? | **Implicit:** tỉ lệ chấp nhận lịch AI đề xuất, thời gian từ nhắc đến đặt lịch, tỉ lệ bỏ lỡ bảo dưỡng. **Explicit:** đánh giá "gợi ý hữu ích/không hữu ích", lý do từ chối. **Outcome:** giảm breakdown đột xuất, giảm chi phí bảo dưỡng ngoài kế hoạch, giảm thời gian chờ tại xưởng. |
| 3 | Data thuộc loại nào? | ☑ User-specific · ☑ Domain-specific · ☑ Real-time · ☑ Human-judgment · ☑ Khác: dữ liệu vận hành từ thiết bị xe/IoT |

**Có marginal value không?** Có. Dữ liệu vận hành theo từng xe, thói quen lái, điều kiện đường sá/môi trường địa phương và phản hồi đặt lịch là dữ liệu riêng, khó có sẵn trong model nền. Càng chạy lâu, hệ thống càng tạo lợi thế dự đoán cá nhân hóa và tối ưu công suất xưởng tốt hơn.
