# SPEC — AI Product Hackathon

**Nhóm:** B1-C401
**Track:** ☑ VinFast · ☐ Vinmec · ☐ VinUni-VinSchool · ☐ XanhSM · ☐ Open
**Problem statement (1 câu):** Chủ xe VinFast không biết chính xác khi nào cần bảo dưỡng, thường chỉ nhớ theo mốc km cố định hoặc khi xe có dấu hiệu bất thường, dẫn đến chờ đợi lâu và chi phí bất ngờ. AI phân tích dữ liệu thời gian thực từ xe (pin, motor, hệ thống treo, điều hòa, quãng đường, thói quen lái, môi trường) để dự đoán thời điểm bảo dưỡng tối ưu, chủ động nhắc nhở và gợi ý khung giờ/xưởng gần nhất.

---

## 1. AI Product Canvas - Nguyễn Thị Tuyết -2A202600215

|             | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Trust                                                                                                                                                                                                                                                                                                                                                                         | Feasibility                                                                                                                                                                                                                                                                                                                                                          |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Câu hỏi** | User nào? Pain gì? AI giải gì?                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Khi AI sai thì sao? User sửa bằng cách nào?                                                                                                                                                                                                                                                                                                                                   | Cost/latency bao nhiêu? Risk chính?                                                                                                                                                                                                                                                                                                                                  |
| **Trả lời** | **User:** Chủ xe VinFast cá nhân (đặc biệt người đi làm bận rộn, chạy xe hằng ngày). **Pain:** Không biết chính xác khi nào cần bảo dưỡng, thường chỉ nhớ theo mốc km cố định hoặc khi xe có dấu hiệu bất thường -> phát sinh chờ đợi lâu và chi phí bất ngờ. **Value:** AI phân tích dữ liệu thời gian thực từ xe (pin, motor, hệ thống treo, điều hòa, quãng đường, thói quen lái, môi trường) để dự đoán thời điểm bảo dưỡng tối ưu, chủ động nhắc nhở và gợi ý khung giờ/xưởng gần nhất. | **Khi AI sai:** Có thể nhắc sớm (mất thời gian) hoặc nhắc muộn (tăng rủi ro hỏng hóc/chi phí). **User biết AI sai:** Đối chiếu với cảnh báo thực tế từ xe, lịch sử bảo dưỡng gần nhất, hoặc cảm nhận vận hành bất thường. **User sửa:** 1 chạm đổi thời gian đề xuất, chọn xưởng khác, hoặc bấm "chưa cần bảo dưỡng"; hệ thống ghi nhận phản hồi để học theo từng người dùng. | **Cost ước lượng:** ~`$0.005-0.02`/xe/ngày cho suy luận + đồng bộ dữ liệu (tùy tần suất). **Latency mục tiêu:** `<2s` cho gợi ý lịch trong app, `<200ms` cho scoring nền theo batch/stream. **Risk chính:** dự đoán sai dẫn tới mất niềm tin; thiên lệch theo kiểu lái hiếm; phụ thuộc chất lượng dữ liệu cảm biến; rủi ro quyền riêng tư dữ liệu hành vi và vị trí. |

**Automation hay augmentation?** ☐ Automation · ☑ Augmentation
Justify: Chọn **Augmentation** vì quyết định bảo dưỡng liên quan chi phí và an toàn; người dùng cần quyền xác nhận cuối. Cost of reject gần bằng 0 (từ chối gợi ý hoặc dời lịch rất nhanh), trong khi automation hoàn toàn khi AI sai có thể gây trải nghiệm tệ và mất trust.

**Learning signal:**

1. User correction đi vào đâu? Mọi thao tác đổi lịch, từ chối lịch, đổi xưởng, đổi lý do bảo dưỡng được ghi vào `feedback log` gắn theo xe + ngữ cảnh (mốc km, thời tiết, kiểu lái), đưa vào pipeline tinh chỉnh mô hình dự đoán theo chu kỳ.
2. Product thu signal gì để biết tốt lên hay tệ đi? **Implicit:** tỉ lệ chấp nhận lịch AI đề xuất, thời gian từ nhắc đến đặt lịch, tỉ lệ bỏ lỡ bảo dưỡng. **Explicit:** đánh giá "gợi ý hữu ích/không hữu ích", lý do từ chối. **Outcome:** giảm breakdown đột xuất, giảm chi phí bảo dưỡng ngoài kế hoạch, giảm thời gian chờ tại xưởng.
3. Data thuộc loại nào? ☑ User-specific · ☑ Domain-specific · ☑ Real-time · ☑ Human-judgment · ☑ Khác: dữ liệu vận hành từ thiết bị xe/IoT
   Có marginal value không? (Model đã biết cái này chưa?) Có. Dữ liệu vận hành theo từng xe, thói quen lái, điều kiện đường sá/môi trường địa phương và phản hồi đặt lịch là dữ liệu riêng, khó có sẵn trong model nền. Càng chạy lâu, hệ thống càng tạo lợi thế dự đoán cá nhân hóa và tối ưu công suất xưởng tốt hơn.

---

## 2. User Stories x 4 paths - Chu Bá Tuấn Anh - 2A202600012

Mỗi feature chính = 1 bảng. AI trả lời xong → chuyện gì xảy ra?

### Feature: Dự đoán và đặt lịch bảo dưỡng xe VinFast

**Trigger:** Hệ thống phát hiện xe sắp đến ngưỡng bảo dưỡng tối ưu (dựa trên km + hành vi + môi trường).

---

### 2.1 Happy Path (ideal flow)

**Goal:** User nhanh chóng chấp nhận gợi ý và đặt lịch thành công.

1. **Trigger:** Hệ thống phát hiện xe sắp đến ngưỡng bảo dưỡng tối ưu.

2. **System Action:** Gọi tool `get_user_info()` → Gọi tool `get_vehicle_info()` → Gọi tool `run_diagnostic()`.

3. **AI Analysis:** Phát hiện lỗi, tính severity, gọi `recommend_schedule(error_code)` với lỗi critical/medium/low.

4. **AI Suggestion:** App push notification: _"Xe của bạn nên bảo dưỡng trong 3 ngày tới. Đề xuất: Thứ 6, 9:00 tại VinFast Hai Bà Trưng."_

5. **User Action:** Mở app → xem chi tiết (lý do: hao mòn phanh + điều hòa giảm hiệu suất) → xem slot thời gian + xưởng đề xuất.

6. **Decision:** User bấm **"Đặt lịch"**.

7. **System Action:** Gọi tool `check_slot_availability(workshop_id)` → Gọi tool `book_appointment(workshop_id, slot_id, error_codes)`.

8. **Output:** Hiển thị: "Đặt lịch thành công" + QR check-in + reminder + Booking ID.

9. **Learning Signal:** `accept_suggestion = true`, latency từ suggest → booking, không có chỉnh sửa, save vào feedback log.

---

### 2.2 Low-confidence Path (user chưa chắc chắn)

**Goal:** User cần thêm thông tin trước khi quyết định.

1. **Trigger:** AI đề xuất giống Happy Path.

2. **User Reaction:** Không tin tưởng ngay → Click "Xem thêm".

3. **AI Support:** Gọi tool `get_explainability(error_code)` để hiển thị:
    - Confidence score (ví dụ: 78%)
    - Risk analysis: "RẤT CAO - 89% xe có lỗi tương tự gặp sự cố trong 7 ngày"
    - Vehicle history (ODO, lần bảo dưỡng cuối, pin health)
    - Similar cases: "Trong 1000 xe VF cùng model, 890 xe đã gặp sự cố khi trì hoãn"

4. **User Action:** Xem thêm option: Đổi xưởng gần hơn, Đổi ngày.

5. **Decision:** User chọn slot khác (ví dụ: Chủ nhật).

6. **System Action:** Gọi `check_slot_availability()` với constraint mới → Gọi `book_appointment()` theo lựa chọn user.

7. **Output:** Booking thành công (customized) + QR check-in.

8. **Learning Signal:** `accept_with_modification = true`, loại modification (time/location change), user_override_vector → save vào feedback log để improve prompts.

---

### 2.3 Failure Path (AI sai hoặc không khả dụng)

**Goal:** Xử lý khi AI hoặc hệ thống fail.

#### Case A: AI dự đoán sai (User reject suggestion)

1. **Trigger:** AI đề xuất bảo dưỡng.

2. **User Reaction:** User thấy xe vẫn bình thường hoặc vừa mới bảo dưỡng gần đây.

3. **User Action:** Bấm: "Chưa cần bảo dưỡng".

4. **System Action:** Gọi `cancel_or_postpone(error_code)` lần 1 (không có reason) → Hỏi nhanh lý do:
    - "Mới bảo dưỡng xong gần đây"
    - "Chưa cần thiết / chưa tiện"
    - "Lý do khác"

5. **User Answer:** Chọn reason.

6. **System Action:** Gọi `cancel_or_postpone(error_code, reason)` lần 2 → Xử lý theo severity:
    - **Critical**: Cảnh báo mạnh + hỏi xác nhận lần nữa (confirm_critical param)
    - **Medium**: Hỏi "Nhắc lại sau bao nhiêu ngày?" (3/5/7/14 days) → ghi nhận snooze_until
    - **Low**: Nhắn nhẹ "hãy đến sơm nhất có thể"

7. **Output:** Dừng nhắc trong X ngày → learning signal saved.

8. **Learning Signal:** `reject_suggestion = true`, reason label → update feedback log + model retraining.

#### Case B: System/tool failure (API error)

1. **Trigger:** User bấm "Đặt lịch".

2. **System Issue:** Tool `check_slot_availability()` hoặc `book_appointment()` timeout/API error.

3. **Fallback Response:** Tool tự động return fallback object:

    ```json
    {
        "error": "Không thể đặt lịch tự động",
        "fallback": {
            "hotline": "1900 23 23 89",
            "message": "Vui lòng gọi hotline để được hỗ trợ",
            "can_retry": true,
            "retry_suggestion": "Thử kiểm tra xưởng khác hoặc ngày khác"
        }
    }
    ```

4. **User Option:** Retry / Call hotline / Choose different workshop.

5. **Learning Signal:** error_rate per tool, drop-off sau lỗi, tool availability tracking.

---

### 2.4 Correction Path (user chủ động sửa AI)

**Goal:** User actively override → hệ thống học mạnh nhất.

1. **Trigger:** AI đề xuất lịch (từ Happy Path hoặc Low-confidence Path).

2. **User Action:** Edit: Đổi thời gian (từ sáng → tối), Đổi xưởng (gần nhà hơn).

3. **System Behavior:**
    - Nếu đổi xưởng: Gọi `recommend_schedule(error_code)` lại → hiển thị recommend mới cho xưởng khác
    - Gọi `check_slot_availability(new_workshop_id, preferred_date)` để validate slot
    - Validate constraint (slot khả dụng, workshop có khả năng xử lý)

4. **Decision:** User confirm lịch đã chỉnh.

5. **System Action:** Gọi `book_appointment(workshop_id, slot_id, error_codes)` với custom config.

6. **Output:** Booking thành công với custom config + QR check-in.

7. **Learning Signal (quan trọng):** `user_override_vector`:
    - `preferred_time_slot`: morning/afternoon/evening/weekend
    - `preferred_location`: workshop_id, distance_km
    - `service_type`: loại dịch vụ ưa thích
    - Save vào feedback log → cá nhân hóa recommendation cho lần sau

---

## Tổng kết mapping

| Path           | Đặc trưng chính    | Value                      |
| -------------- | ------------------ | -------------------------- |
| Happy          | Accept ngay        | UX nhanh, chứng minh value |
| Low-confidence | Cần explain        | Tăng trust                 |
| Failure        | Sai / lỗi hệ thống | Bảo vệ UX, giảm churn      |
| Correction     | User override      | Signal học mạnh nhất       |

---

## 3. Eval metrics + threshold

Đối với bài toán **AI Agent đặt lịch bảo trì VinFast**, câu trả lời ngắn gọn và chuẩn xác nhất là: **Optimize Precision.**

### ☑ Precision — khi AI nói "có" thì thực sự đúng (ít false positive)

**Tại sao?**
Trong dịch vụ đặt lịch (Booking), **sự tin cậy (Trust)** là yếu tố sống còn.

- **Precision cao** nghĩa là khi Agent xác nhận: _"Anh đã đặt lịch thành công lúc 9h sáng mai tại VinFast Landmark 81"_, thì chắc chắn 100% slot đó đã được giữ trên hệ thống và xưởng đã sẵn sàng đón khách.
- Khách hàng của VinFast (đặc biệt là dòng xe điện cao cấp) thường là những người bận rộn. Họ cần sự khẳng định tuyệt đối để sắp xếp công việc cá nhân.

---

**Nếu sai ngược lại thì sao? (Nếu ưu tiên Recall mà bỏ qua Precision)**

Nếu chọn **Recall**, AI sẽ cố gắng "vơ" hết mọi yêu cầu của khách để chốt lịch bằng được (giảm False Negative - không bỏ sót đơn hàng), nhưng dễ dẫn đến sai sót (False Positive - xác nhận bừa).

**Hậu quả khi Precision thấp (Sai ngược lại):**

1. **Trùng lịch (Double Booking):** Agent xác nhận lịch cho khách trong khi xưởng thực tế đã kín chỗ. Khách lái xe đến và bị từ chối phục vụ.
2. **Sai lệch thông tin:** Agent xác nhận sai gói bảo dưỡng hoặc sai địa điểm xưởng.
3. **Khủng hoảng niềm tin:** Chỉ cần **một lần** khách hàng đến xưởng mà không có tên trong danh sách do lỗi AI, họ sẽ không bao giờ sử dụng Agent nữa và quay lại gọi tổng đài truyền thống. Chi phí để khắc phục một lỗi "False Positive" (khách đến xưởng nhưng không được phục vụ) đắt hơn gấp nhiều lần so với việc Agent nói: _"Em không chắc chắn về lịch này, để em nối máy với nhân viên hỗ trợ"_ (một lỗi False Negative an toàn).

**Kết luận**: Trong các hệ thống AI giao dịch (Transactional AI), thà để Agent trả lời "Em không biết/Em chưa rõ" (giảm Recall) để chuyển cho người thật, còn hơn là đưa ra thông tin sai lệch nhưng khẳng định là đúng (thấp Precision). Precision là nền tảng của sự chuyên nghiệp trong dịch vụ hạng sang.

---

| Metric                          | Threshold                                         | Red flag (dừng khi)                                           |
| ------------------------------- | ------------------------------------------------- | ------------------------------------------------------------- |
| Booking Success Rate            | > 85% cuộc hội thoại chốt lịch thành công         | < 50%: Quy trình đang gây khó khăn cho khách                  |
| Slot Accuracy                   | 100% không trùng lịch (Double-booking)            | > 0%: Sai lệch dữ liệu giữa AI và thực tế xưởng               |
| Information Extraction Accuracy | > 95% nhận diện đúng biển số/số điện thoại/số ODO | < 80%: Agent liên tục hỏi lại các thông tin đã cung cấp       |
| Fallback Rate                   | < 10% cuộc gọi phải chuyển cho nhân viên thật     | > 25%: Khả năng xử lý ngôn ngữ tự nhiên của Agent kém         |
| Schedule Adherence Rate         | > 90% khách hàng đến đúng khung giờ AI đã đặt     | < 70%: Quy trình nhắc lịch (reminder) của Agent chưa hiệu quả |

---

## 4. Top 3 failure modes

_Liệt kê cách product có thể fail — không phải list features._
_"Failure mode nào user KHÔNG BIẾT bị sai? Đó là cái nguy hiểm nhất."_

| #   | Trigger                                                                                                                                                                                                               | Hậu quả                                                                                                                                                                                                                                | Mitigation                                                                                                                                                                                                                      |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | AI báo "Đặt lịch thành công" nhưng thực tế xưởng không ghi nhận hoặc đã quá tải: Hệ thống app đặt lịch không đồng bộ realtime với tình trạng thực tế tại xưởng (đặc biệt khi có lượng lớn xe Xanh SM đột xuất đổ về). | User KHÔNG BIẾT bị lỗi. Người dùng đinh ninh đã có lịch, chạy xe hàng chục km đến nơi mới bị xưởng báo "không có thông tin trên hệ thống" hoặc "xưởng đã kín chỗ", bắt buộc phải quay về.                                              | Thay vì báo thành công ngay, AI đưa vào trạng thái "Chờ xưởng xác nhận" (2-way handshake). Nếu API xưởng báo tải trọng >90%, AI tự động lock slot tại xưởng đó và chủ động gợi ý xưởng khác lân cận.                            |
| 2   | Hệ thống AI/App ghi nhận sai thời gian check-in: Người dùng mang xe đến xưởng đúng giờ đã hẹn nhưng hệ thống định vị của app phản hồi chậm hoặc lỗi đồng bộ.                                                          | Hệ thống tự động đánh dấu khách "đến trễ", âm thầm tự động hủy lịch. Người dùng không hề hay biết cho đến khi gặp lễ tân.                                                                                                              | Thiết lập tính năng chủ động Check-in bằng nút bấm trên app khi vào bán kính 500m của xưởng. Khi hệ thống đếm ngược hết giờ, AI phải gửi Push Notification "Bạn đã đến nơi chưa?" thay vì tự động hủy.                          |
| 3   | AI tiếp nhận lịch sửa chữa nhưng bỏ qua bước kiểm tra tồn kho phụ tùng / thời gian lưu xe: Người dùng nhập mô tả lỗi (VD: kẹt kính, hư mô tơ, lỗi túi khí), AI tự động xếp lịch vào một slot trống ngắn hạn.          | Đã xảy ra rồi mới biết. Người dùng mang xe đến xưởng kỳ vọng sửa nhanh rồi về, nhưng đến nơi mới vỡ lẽ xưởng không có sẵn phụ tùng thay thế hoặc lỗi phức tạp bắt buộc phải "giam xe" qua ngày, làm hỏng hoàn toàn lịch trình cá nhân. | Khi AI nhận diện các từ khóa báo lỗi phần cứng, hệ thống phải tự động cross-check với API kho phụ tùng. Nếu phát hiện thiếu linh kiện, cảnh báo ngay: "Lỗi này hiện cần chờ nhập linh kiện, AI đề xuất dời lịch sang tuần sau". |

---

**Lý do chọn 3 failure modes này:**
#1 và #2 là lỗi Silent Failure điển hình của hệ thống Automation. Máy móc tưởng là đúng nhưng thực tế sai, và khách hàng hoàn toàn không biết mình bị lỗi cho đến khi mất thời gian/công sức đến tận xưởng.
#3 là lỗi Delayed Realization, hệ thống augmentation thiếu data (không nối với API kho). AI đặt lịch rất trơn tru nhưng hệ quả (giam xe, thiếu đồ) thì khách hàng đến nơi mới chịu đựng.

---

## 5. ROI 3 kịch bản

|                | Conservative                                                                                                                                        | Realistic                                                                                                               | Optimistic                                                                                                                       |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Assumption** | 150 lượt/ngày qua AI (20% tổng); 58% tự động hoàn toàn; chủ yếu giờ hành chính                                                                      | 500 lượt/ngày (60% tổng); 75% tự động; hoạt động 24/7                                                                   | 1,200 lượt/ngày (full adoption); 88% tự động; tích hợp toàn hệ thống                                                             |
| **Cost**       | API: $0.8/ngày + Infra/maintain: $5.5/ngày = **$6.3/ngày**                                                                                          | API: $2.5/ngày + Infra/maintain: $7.5/ngày = **$10/ngày**                                                               | API: $6/ngày + Infra/maintain: $9/ngày = **$15/ngày**                                                                            |
| **Benefit**    | Giảm 87 cuộc tổng đài × 12 phút → tiết kiệm ~$14/ngày nhân lực; +8 booking ngoài giờ × $45 × 20% margin = $72; giảm no-show 2% = $6 → **~$92/ngày** | Giảm 375 cuộc → $60/ngày; +30 booking ngoài giờ = $300; upsell 4% × 375 × $18 = $270; no-show 2% = $15 → **~$645/ngày** | Giảm 1,056 cuộc → $169/ngày; +80 booking ngoài giờ = $880; upsell 8% × 1,056 × $22 = $1,859; no-show 2% = $33 → **~$2,941/ngày** |
| **Net**        | ~$86/ngày → **~$25,800/năm**                                                                                                                        | ~$635/ngày → **~$190,500/năm**                                                                                          | ~$2,926/ngày → **~$877,800/năm**                                                                                                 |

**Kill criteria:** Tỷ lệ tự động hoàn toàn < 40% sau 60 ngày vận hành → model kém hoặc luồng hội thoại cần thiết kế lại; Net/ngày âm liên tục 2 tháng, kể cả sau khi tối ưu prompt & infra; NPS khách hàng sau trải nghiệm AI < 30 (tức tệ hơn tổng đài truyền thống); Tỷ lệ booking thành công < 60% tổng lượt bắt đầu hội thoại (funnel vỡ ở bước nào đó)

---

## 6. Mini AI spec (1 trang)

**VFCare** là trợ lý AI dự đoán và tự động đặt lịch bảo dưỡng xe VinFast cá nhân hóa, dành cho chủ xe VinFast (đặc biệt người đi làm bận rộn, chạy xe hằng ngày) gặp pain không biết chính xác khi nào cần bảo dưỡng, thường chỉ nhớ theo mốc km cố định hoặc khi xe có dấu hiệu bất thường, dẫn đến chờ đợi lâu và chi phí bất ngờ.

**Architecture:** OpenAI function calling với 8 tools:

- `get_user_info()` / `get_vehicle_info()` / `run_diagnostic()` → Phân tích tình trạng xe
- `recommend_schedule(error_code)` → Gợi ý lịch theo severity (critical: xưởng gần nhất, medium: 3-5 ngày, low: linh hoạt)
- `check_slot_availability()` / `book_appointment()` → Quản lý slot & đặt lịch
- `cancel_or_postpone()` → Hoãn/từ chối (xử lý khác nhau per severity)
- `get_explainability()` → Giải thích confidence score & risk analysis

AI hoạt động theo mô hình **Augmentation** - AI gợi ý, user quyết định cuối cùng. Lý do: quyết định bảo dưỡng liên quan chi phí và an toàn; người dùng cần quyền xác nhận cuối. Cost of reject gần bằng 0 (từ chối gợi ý hoặc dời lịch rất nhanh), trong khi automation hoàn toàn khi AI sai có thể gây trải nghiệm tệ và mất trust.

**Severity-based logic:**

- **Critical 🔴**: Xưởng hỗ trợ critical GẦN NHẤT (sắp xếp km), slot sớm nhất, bắt buộc xác nhận hoãn, nhắc lại lần bật xe sau
- **Medium 🟠**: Xưởng gần, slot 3-5 ngày, user chọn ngày nhắc lại nếu hoãn (3/5/7/14 ngày)
- **Low 🟡**: Xưởng linh hoạt, weekend/afternoon slots ưu tiên, nhắn nhẹ nhàng khi hoãn

**Khi AI sai:** Có thể nhắc sớm (mất thời gian) hoặc nhắc muộn (tăng rủi ro hỏng hóc). User biết AI sai bằng cách xem `get_explainability()` (confidence score, risk analysis, lịch sử xe). User sửa bằng 1 chạm đổi thời gian, chọn xưởng khác, hoặc bấm "chưa cần bảo dưỡng"; hệ thống ghi nhận phản hồi → feedback log.

**Quality:** Ưu tiên **Precision** hơn Recall (false positive ít hơn false negative vì false positive là mất thời gian, false negative là hỏng hóc). Nhưng Recall quá thấp → user bỏ dùng nếu không được nhắc đúng lúc.

**Risk chính:** Dự đoán sai → mất niềm tin; double-booking slot; thiếu kiểm tra tồn kho phụ tùng; phụ thuộc dữ liệu cảm biến; quyền riêng tư dữ liệu vị trí/hành vi.

**Data flywheel:** Dữ liệu vận hành (thói quen lái, điều kiện đường), phản hồi đặt lịch (accept/reject/modify) được ghi vào feedback log → pipeline tinh chỉnh prompt & fine-tune model theo chu kỳ. Càng chạy lâu, hệ thống càng tạo lợi thế dự đoán cá nhân hóa per xe + tối ưu công suất xưởng.
