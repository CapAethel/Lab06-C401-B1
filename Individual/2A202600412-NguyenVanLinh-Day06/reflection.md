# Individual reflection — Nguyễn Văn Lĩnh (2A202600412)

## 1. Role

**LLM/Prompt Engineer** — Phụ trách tối ưu hóa LLM integration, system prompt, function calling design, và end-to-end workflow của agent.

## 2. Đóng góp cụ thể

### Core contribution:

- **Thiết kế 8 tools function calling** cho VFCare Agent:
    - `get_user_info()` → Lấy info chủ xe
    - `get_vehicle_info()` → Chi tiết xe VF
    - `run_diagnostic()` → Phát hiện tất cả lỗi (critical/medium/low)
    - `recommend_schedule(error_code)` → Gợi ý lịch bảo dưỡng
    - `check_slot_availability()` → Kiểm tra slot xưởng
    - `book_appointment()` → Đặt lịch
    - `cancel_or_postpone()` → Hoãn/từ chối (3 severity level, hành vi khác nhau)
    - `get_explainability()` → Giải thích confidence score & risk analysis

    → Mỗi tool có logic phức tạp: critical→xưởng gần nhất, medium→linh hoạt, low→dễ dàng hoãn

- **Thiết kế severity-based interaction flows**:
    - **Critical** (🔴): Cảnh báo mạnh, xưởng gần nhất, bắt buộc xác nhận
    - **Medium** (🟠): Gợi ý 3-5 ngày, user chọn xưởng/giờ tùy ý
    - **Low** (🟡): Hoãn linh hoạt, chỉ nhắc nhẹ

    → Implement trong `cancel_or_postpone()` với multi-step confirmation

- **Xây dựng TOOL_DEFINITIONS & TOOL_MAP** cho OpenAI function calling:
    - JSON schema cho mỗi tool (parameters, descriptions)
    - Callable map giúp LLM gọi tool → execute → trả kết quả

### Secondary contribution:

- **Mock data orchestration**: Kết hợp với Data Engineer để design structure của `vehicle_status.json`, `maintenance_rules.json`, `workshops.json`
- **CLI interface design**: Collaborate với UI designer để đảm bảo tools trả về data format phù hợp cho demo mode + interactive mode

## 3. SPEC mạnh/yếu theo từng thành phần

### VFCare SPEC mạnh nhất:

- **End-to-end workflow**: Từ detection → priority → recommendation → booking → feedback — tất cả đều connected via tools
- **Severity-based behavior**: Logic khác nhau cho critical/medium/low làm cho agent "smart" (không generic)
- **Explainability**: Tool `get_explainability()` giúp user tin tưởng AI (transparency)

### VFCare SPEC yếu nhất:

- **Learning loop**: Chỉ ghi nhận feedback vào JSON, chưa có fine-tune model. Feedback chỉ là "signal" chứ không refine behavior
- **Multi-error handling**: Khi xe có 4+ lỗi medium, gợi ý hành động chưa clear (ưu tiên cái nào trước? hay fix all once?)
- **Cost/Latency chưa validate**: Mock data không có real latency, chưa test với real vehicle data streams

## 4. Challenges gặp phải

1. **Tool design complexity**: Decide parameter signature cho `cancel_or_postpone()` khó — phải capture 2-step flow (hỏi lý do, rồi xử lý theo severity). Ban đầu muốn gom vào 1 call, nhưng LLM không sao theo multi-step được → phải split logic

2. **Severity logic trong tools**: Critical vs Medium có hành vi rất khác, viết trong 1 function hoặc tách 3 function? Cuối cùng chọn gom vào 1 function có if-elif-else vì LLM dễ call sai tool nếu có 3 tool tương tự

3. **JSON schema validation**: Tay viết TOOL_DEFINITIONS phải match actual function parameters, dễ miss hoặc typo

## 5. Key learnings

1. **Function calling là contract giữa LLM & backend**: Phải very clear & specific. Ambiguous parameter name → LLM gọi sai hoặc miss
2. **Severity-based design scales**: Thay vì hard-code "recommend_schedule_critical" + "recommend_schedule_medium" riêng, dùng 1 function + severity logic làm code cleaner
3. **Explainability tool không phải luxury**: Nó là essential cho trust. Nếu không có `get_explainability()`, user bị từ chối gợi ý không biết tại sao
4. **Mock data structure matters**: Cách organize workshop slots (WORKSHOP_SLOTS dict by workshop_id) ảnh hưởng interface của tools. Design tool-first → mock data structure, không ngược lại

## 6. Nếu làm lại / Suggestions for improvement

1. **Test tool schemas early** — Viết mock LLM caller (hardcode tool calls) vào D5 tối, tìm lỗi sớm. Không nên tới D6 sáng mới validate

2. **Add streaming support** — Hiện tools trả JSON sync. Để scale thành real agent, nên support streaming responses (critical error → stream warning ngay, không chờ toàn bộ analysis)

3. **Design feedback loop properly** — Hiện chỉ save feedback vào JSON. Nên design: feedback → label dataset → curate → retrain. Mà hackathon scope không cho phép, nhưng concept quan trọng

4. **Handle error gracefully in tools** — Hiện tools trả error message trong JSON. Nên có try-catch structure để backend không crash nếu tool fail

## 7. AI (Claude/ChatGPT) giúp gì / sai gì

### Giúp:

- **Brainstorm tool design**: Dùng Claude để idea tất cả cases của `cancel_or_postpone()` — nó suggest multi-step flow rất tự nhiên
- **Generate JSON schema boilerplate**: ChatGPT generate TOOL_DEFINITIONS template nhanh, chỉ cần customize parameters
- **Test mock data**: Dùng Claude để validate logic (VD: "Nếu critical thì luôn recommended xưởng gần nhất?" → Claude confirm đúng)

### Sai/Mislead:

- **Over-engineering suggestions**: Claude suggest "thêm rate limiting" cho tools — hay nhưng out of scope cho hackathon. Phải stop scope creep
- **Generic function names**: ChatGPT first suggestion là `get_recommendations()` generic, tôi phải push back để tách thành `recommend_schedule()` + `get_explainability()` → clearer

## 8. Metrics để biết VFCare tốt/xấu

**Nếu có dữ liệu thực:**

- **Tool success rate**: % tool calls LLM gọi đúng parameter (expect >90%)
- **Booking conversion**: % user receive suggestion → actually book (target >40%)
- **Cancellation rate**: % user decline suggestion (track by severity: critical should <5%, medium ~20%, low ~40%)
- **Time to decision**: Từ suggestion → user decision (target <2 min for critical, <10 min for medium)
- **Explainability impact**: A/B test: with `get_explainability()` vs without → conversion rate difference
