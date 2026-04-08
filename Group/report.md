# 1. AI Product Canvas - Nguyễn Thị Tuyết -2A202600215

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

---

# 2. User Stories x 4 Paths

## 2.1 Happy Path (ideal flow)

**Goal:** User nhanh chóng chấp nhận gợi ý và đặt lịch thành công.

1. **Trigger:**
   Hệ thống phát hiện xe sắp đến ngưỡng bảo dưỡng tối ưu (dựa trên km + hành vi + môi trường).

2. **AI Suggestion:**
   App push notification:
   *“Xe của bạn nên bảo dưỡng trong 3 ngày tới. Đề xuất: Thứ 6, 9:00 tại VinFast Hai Bà Trưng.”*

3. **User Action:**

   * Mở app → xem chi tiết (lý do: hao mòn phanh + điều hòa giảm hiệu suất)
   * Xem slot thời gian + xưởng đề xuất

4. **Decision:**

   * User bấm **“Đặt lịch”**

5. **System Action:**

   * Gọi tool: `check_slot_availability`
   * Gọi tool: `book_appointment`

6. **Output:**

   * Hiển thị: “Đặt lịch thành công” + QR check-in + reminder

7. **Learning Signal:**

   * `accept_suggestion = true`
   * latency từ suggest → booking
   * không có chỉnh sửa

---

## 2.2 Low-confidence Path (user chưa chắc chắn)

**Goal:** User cần thêm thông tin trước khi quyết định.

1. **Trigger:**
   AI đề xuất giống Happy Path

2. **User Reaction:**

   * Không tin tưởng ngay
   * Click “Xem thêm”

3. **AI Support:**
   Hiển thị explainability:

   * So sánh với lịch bảo dưỡng trước
   * Dự đoán nếu trì hoãn: *“Sau 2 tuần, nguy cơ hao mòn tăng 18%”*
   * Confidence score (ví dụ: 78%)

4. **User Action:**

   * Xem thêm option:

     * Đổi xưởng gần hơn
     * Đổi ngày

5. **Decision:**

   * User chọn slot khác (ví dụ: Chủ nhật)

6. **System Action:**

   * Re-run: `recommend_schedule` với constraint mới
   * Book theo lựa chọn user

7. **Output:**

   * Booking thành công (customized)

8. **Learning Signal:**

   * `accept_with_modification = true`
   * loại modification (time/location change)
   * confidence threshold chưa đủ → cần tuning explainability

---

## 2.3 Failure Path (AI sai hoặc không khả dụng)

**Goal:** Xử lý khi AI hoặc hệ thống fail.

### Case A: AI dự đoán sai

1. **Trigger:**
   AI đề xuất bảo dưỡng

2. **User Reaction:**

   * User thấy xe vẫn bình thường
   * Hoặc vừa mới bảo dưỡng gần đây

3. **User Action:**

   * Bấm: “Chưa cần bảo dưỡng”

4. **System Response:**

   * Hỏi nhanh lý do:

     * “Mới bảo dưỡng”
     * “Xe chưa có dấu hiệu”
     * “Khác”

5. **Output:**

   * Dừng nhắc trong X ngày
   * Update model

6. **Learning Signal:**

   * `reject_suggestion = true`
   * reason label

---

### Case B: System/tool failure

1. **Trigger:**
   User bấm “Đặt lịch”

2. **System Issue:**

   * `check_slot_availability` timeout / lỗi API

3. **Fallback:**

   * Hiển thị:
     *“Không thể đặt lịch tự động. Bạn muốn gọi hotline hoặc thử lại?”*

4. **User Option:**

   * Retry
   * Call support
   * Manual booking

5. **Learning Signal:**

   * error rate per tool
   * drop-off sau lỗi

---

## 2.4 Correction Path (user chủ động sửa AI)

**Goal:** User actively override → hệ thống học mạnh nhất.

1. **Trigger:**
   AI đề xuất lịch

2. **User Action:**

   * Edit:

     * Đổi thời gian (từ sáng → tối)
     * Đổi xưởng (gần nhà hơn)
     * Đổi loại dịch vụ (chỉ kiểm tra điều hòa)

3. **System Behavior:**

   * Real-time update recommendation
   * Validate constraint (slot, capacity)

4. **Decision:**

   * User confirm lịch đã chỉnh

5. **Output:**

   * Booking thành công với custom config

6. **Learning Signal (quan trọng):**

   * `user_override_vector`:

     * preferred_time_slot
     * preferred_location
     * service_priority
   * Update profile cá nhân hóa

---

## Tổng kết mapping

| Path           | Đặc trưng chính    | Value                      |
| -------------- | ------------------ | -------------------------- |
| Happy          | Accept ngay        | UX nhanh, chứng minh value |
| Low-confidence | Cần explain        | Tăng trust                 |
| Failure        | Sai / lỗi hệ thống | Bảo vệ UX, giảm churn      |
| Correction     | User override      | Signal học mạnh nhất       |
