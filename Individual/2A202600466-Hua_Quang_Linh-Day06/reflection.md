# Individual Reflection — Hứa Quang Linh (2A202600466)

> Dự án: **VFCare** — AI Agent dự đoán & đặt lịch bảo dưỡng xe VinFast điện
> Nhóm: C401-B1 · Ngày 6 Hackathon · 09/04/2026

---

## 1. Role

**AI Engineer + Full-stack Developer.**
Đóng góp xây dựng prototype: backend AI agent (OpenAI function calling), tool functions với mock data, và Streamlit UI bao gồm booking flow end-to-end.

---

## 2. Đóng góp cụ thể

- **Xây dựng `agent.py`** — Streamlit app tích hợp OpenAI gpt-4o-mini với agentic loop (tool_calls), session state management, auto-diagnosis khi chọn xe, và booking confirmation flow 2 bước. Output: file chạy được với `python -m streamlit run agent.py`.

- **Xây dựng `tools.py`** — tool functions: `check_slot_availability`, `book_appointment`. Mock data xe VinFas với các mức sức khỏe khác nhau

- **Thiết kế UX booking flow** — Luồng 4 bước: dự đoán → 2 nút lựa chọn (Đặt ngay / Nhắc sau) → 3 thẻ workshop cards → booking dialog với slot selector và bảng tóm tắt. Intercept `book_appointment` để buộc user xác nhận thay vì agent tự đặt.

---

## 3. SPEC mạnh/yếu

**Mạnh nhất — AI Product Canvas & Augmentation design:**
Nhóm xác định rõ VFCare là **augmentation** (AI đề xuất, user quyết định), không phải automation. Thiết kế learning signals (implicit: booking rate, explicit: 👍👎, correction: user chỉnh lại lịch) phản ánh đúng triết lý trust-first. Phần này có cơ sở vững vì được implement thật trong code.

**Yếu nhất — Eval metrics & threshold:**
3 metrics được liệt kê (precision dự đoán, booking conversion rate, maintenance interval accuracy) nhưng threshold được chọn theo cảm tính, chưa có dữ liệu thật để calibrate. Ví dụ: đặt threshold "risk_score > 0.7 → cần bảo dưỡng" dựa trên logic, không phải từ historical data của VinFast. Nếu có access vào telemetry thật thì threshold này sẽ thay đổi đáng kể.

---

## 4. Đóng góp khác

- **Debug agentic loop** — Phát hiện và fix lỗi agent thông báo "đã đặt lịch thành công" trước khi user xác nhận. Root cause: `book_appointment` trả về status bình thường → agent hiểu đã xong. Fix: intercept tool call, trả về `"pending_user_selection"` kèm instruction rõ ràng không được confirm trước.

- **Viết `system-prompt.md` và vehicle health factors** — Tài liệu hóa 8 yếu tố đánh giá sức khỏe xe điện (Battery SoH, Motor efficiency, Brakes wear, Suspension, HVAC, Driving behavior, Environment, Maintenance history). Dùng làm nền cho logic mock data và system prompt của agent.

- **Tạo marketing deck `VFCare-Launch.pptx`** — 6 slides tiếng Việt : Hero, Pain points, Giải pháp, 3 tính năng cốt lõi, Đối tượng & tác động, CTA.

---

## 5. Điều học được

**Tool intercept pattern trong agentic loop** — Trước hackathon, tôi hiểu OpenAI function calling theo hướng đơn giản: model gọi tool → tool chạy → model nhận kết quả → trả lời. Nhưng khi cần UI confirmation trước khi book, tôi học được cách *intercept* tool call ở tầng application: thay vì gọi tool thật, trả về một response "pending" với instruction cho model. Pattern này cho phép inject UI/UX vào giữa agentic loop mà không phá vỡ conversation state — điều không có trong tutorial nào tôi đọc trước đó.

---

## 6. Nếu làm lại

**Build và test mock data trước, UI sau.** Thực tế là tôi build UI Streamlit song song với mock data, dẫn đến phải sửa data schema nhiều lần khi UI cần field mới (ví dụ: `available_slots` nested trong workshop object, `pad_wear_percent` thay vì `brake_wear`). Nếu dành 30 phút đầu để finalize JSON schema của tất cả tool responses rồi mới build UI, sẽ tiết kiệm khoảng 1-2 giờ refactor.

Cụ thể hơn: freeze `MOCK_VEHICLES`, `MOCK_WORKSHOPS` schema trước 10:00, sau đó UI và agent build song song mà không conflict.

---

## 7. AI giúp gì / AI sai gì

**AI giúp:**
- **Claude Code** giúp scaffold toàn bộ `agent.py` và `tools.py` boilerplate trong ~15 phút đầu. Việc generate TOOLS_SPEC (format OpenAI function calling) và mock data phong phú (3 xe với health scores khác nhau, 3 xưởng với slots) nhanh hơn tự viết tay ít nhất 2 giờ.
- Khi mô tả yêu cầu UX bằng ngôn ngữ tự nhiên ("user xác nhận trước khi agent đặt lịch"), Claude gợi ý đúng hướng intercept pattern mà không cần tôi biết trước solution.

**AI sai / mislead:**
- **Agent ban đầu tự confirm booking** — Dù đã viết trong system prompt "không đặt lịch khi chưa có xác nhận", agent vẫn thông báo "Tôi đã đặt lịch bảo dưỡng thành công" ngay sau khi tool trả về. Lý do: model không phân biệt được tool result là "pending" hay "confirmed" nếu response format không đủ explicit. **Bài học: không thể dùng prose instruction để kiểm soát behavior — phải enforce bằng code (intercept + return value cụ thể).**
- **Scope creep từ AI suggestions** — Claude liên tục gợi ý thêm features (export learning signals, demo scenarios, thông tin xe chi tiết). Nhiều thứ được implement rồi phải xóa đi vì clutters UI. AI brainstorm tốt nhưng không biết giới hạn scope của hackathon.

---

*Nộp: 23:59 · 09/04/2026 · Repo cá nhân: `2A202600466-HuaQuangLinh-Day06`*
