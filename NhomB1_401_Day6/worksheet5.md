# Worksheet 5 — Skills Map & Track Direction

**Sản phẩm:** VFCare — AI dự đoán & đặt lịch bảo dưỡng xe VinFast
**Nhóm:** B1-C401
**Mục tiêu:** Kết nối dự án với năng lực hiện tại và hướng đi Phase 2

---

## Thang điểm tự chấm

| Điểm | Mô tả |
|---|---|
| 1 | Chưa biết / chưa làm bao giờ |
| 2 | Biết lý thuyết, chưa thực hành |
| 3 | Đã làm được trong môi trường học tập / dự án nhỏ |
| 4 | Làm được độc lập trong dự án thực tế |
| 5 | Có thể dẫn dắt người khác, xử lý được edge case phức tạp |

---

## 1. Bảng tự chấm từng thành viên

### Ba mảng đánh giá

**Business / Product**
Hiểu vấn đề người dùng, định nghĩa giá trị sản phẩm, phân tích ROI, viết spec, thiết kế UX flow, đánh giá thị trường.

**Infra / Data / Ops**
Thiết kế hạ tầng (cloud/on-prem/hybrid), xử lý dữ liệu pipeline, logging, monitoring, deployment, SLA, bảo mật dữ liệu.

**AI Engineering / Application**
Dùng LLM API, prompt engineering, function calling, eval metrics, fine-tuning, RAG, agent design, cost optimization.

---

### Thành viên 1 — Nguyễn Thị Tuyết (2A202600215)

*Phụ trách: AI Product Canvas (Section 1 spec)*

| Mảng | Tự chấm (1–5) | Ghi chú / Bằng chứng |
|---|---|---|
| Business / Product | ___ | |
| Infra / Data / Ops | ___ | |
| AI Engineering / Application | ___ | |

**Nhận xét từ output dự án:**
Phần AI Product Canvas (Value / Trust / Feasibility) được xây dựng rất có cấu trúc — xác định đúng user, pain, value; thiết kế learning signal đa tầng (implicit/explicit/outcome); phân tích marginal value của data. Cho thấy năng lực **Business/Product** ở mức ít nhất 3–4.

---

### Thành viên 2 — Chu Bá Tuấn Anh (2A202600012)

*Phụ trách: User Stories × 4 Paths (Section 2 spec)*

| Mảng | Tự chấm (1–5) | Ghi chú / Bằng chứng |
|---|---|---|
| Business / Product | ___ | |
| Infra / Data / Ops | ___ | |
| AI Engineering / Application | ___ | |

**Nhận xét từ output dự án:**
4 paths (Happy / Low-confidence / Failure / Correction) được thiết kế chi tiết với tool call cụ thể, JSON fallback object, và learning signal per path. Phần failure mode phân tích "silent failure" vs "delayed realization" — tư duy này thuộc về giao điểm **Product + AI Engineering**.

---

### Thành viên 3 — Nguyễn Văn Lĩnh (2A202600412)

*Phụ trách: Tổng hợp / Spec Final*

| Mảng | Tự chấm (1–5) | Ghi chú / Bằng chứng |
|---|---|---|
| Business / Product | ___ | |
| Infra / Data / Ops | ___ | |
| AI Engineering / Application | ___ | |

**Nhận xét từ output dự án:**
Spec-final tổng hợp được ROI 3 kịch bản với con số cụ thể, kill criteria định lượng, và mini AI spec 1 trang có kiến trúc rõ ràng (8 tools, severity-based logic, data flywheel). Cho thấy khả năng nhìn toàn bộ hệ thống — năng lực **Business/Product** kết hợp hiểu biết **AI Engineering** ở mức conceptual.

---

*(Thêm dòng nếu nhóm có thành viên thứ 4+)*

---

## 2. Tổng hợp điểm mạnh nhóm

*(Điền sau khi tất cả tự chấm xong)*

| Mảng | Điểm TB nhóm | Nhận xét |
|---|---|---|
| Business / Product | ___ / 5 | |
| Infra / Data / Ops | ___ / 5 | |
| AI Engineering / Application | ___ / 5 | |

### Điểm mạnh có thể quan sát được từ spec và worksheets

Không cần chờ tự chấm, output dự án đã cho thấy:

**Mạnh rõ ràng:**
- Tư duy sản phẩm: xác định đúng user pain, chọn Augmentation thay vì Automation với lý do cụ thể
- Phân tích failure mode: phân biệt silent failure vs delayed realization — đây là kỹ năng product nâng cao
- Cost thinking: ROI 3 kịch bản, kill criteria, nhận ra token cost không phải cost driver lớn nhất (Worksheet 2)
- Thiết kế fallback: 3-tầng fallback trong Worksheet 4, không để critical severity bị bỏ sót

**Cần kiểm chứng thêm:**
- Infra/Ops: Hybrid architecture được chọn đúng (Worksheet 1) nhưng chưa rõ nhóm có tự implement được không
- AI Engineering: Function calling design tốt nhưng chưa có bằng chứng đã build thực tế

---

## 3. Chọn Track Phase 2

### Các track có thể chọn

| Track | Mô tả | Phù hợp khi |
|---|---|---|
| **A — Product Depth** | Nghiên cứu user thật, prototype UX, validate với chủ xe VinFast thực tế | Nhóm mạnh Business/Product, muốn validate trước khi build |
| **B — Technical Build** | Implement prototype có thật: function calling với mock data, demo booking flow | Nhóm mạnh AI Engineering, muốn có sản phẩm chạy được |
| **C — Data & Ops** | Thiết kế data pipeline telemetry, logging, monitoring, đánh giá compliance | Nhóm mạnh Infra/Data, muốn giải quyết bottleneck enterprise |
| **D — Go-to-Market** | Pitch tới VinFast/XanhSM, xây dựng business case, tìm pilot partner | Nhóm mạnh cả Product và Communication, muốn tiến đến thị trường |

---

### Khuyến nghị dựa trên profile dự án

**Track được khuyến nghị: B — Technical Build kết hợp A — Product Depth**

**Lý do:**

Nhóm đã có spec chất lượng cao — đây là tài sản lớn nhất. Rủi ro lớn nhất hiện tại là spec đẹp nhưng chưa được validate bởi user thật và chưa có code chạy được. Phase 2 nên giải quyết đồng thời cả hai:

1. **Product Depth (A):** Phỏng vấn 3–5 chủ xe VinFast thật để validate pain và willingness-to-use. Câu hỏi quan trọng nhất chưa được trả lời: *"Bạn có trust AI đủ để đặt lịch bảo dưỡng không?"*

2. **Technical Build (B):** Implement demo với mock data: Claude API + 3 tool calls cơ bản (get_vehicle_info, recommend_schedule, book_appointment). Không cần tích hợp VinFast thật — demo với data giả đủ để prove feasibility và pitch.

**Không nên chọn C ngay:** Data pipeline và compliance là bottleneck enterprise — nhưng nếu chưa validate product-market fit, giải quyết infra là đầu tư sai thứ tự.

**Không nên chọn D ngay:** Pitch tới VinFast/XanhSM mà không có demo chạy được sẽ không hiệu quả.

---

### Track đã chọn (nhóm điền)

> **Track Phase 2:** _______________
>
> **Lý do nhóm chọn:** _______________

---

## 4. Kỹ năng cần bù để tiếp tục dự án

### Nếu chọn Track B (Technical Build)

| # | Kỹ năng cần bù | Tại sao cần | Cách học nhanh nhất |
|---|---|---|---|
| 1 | **Function calling / Tool use với Claude API** | Toàn bộ kiến trúc VFCare dựa trên 8 tool calls — đây là kỹ năng core để implement | Anthropic docs + build 1 toy agent với 2–3 tools trong 1 buổi |
| 2 | **Eval & testing AI responses** | Cần biết khi nào recommendation của AI là "đủ tốt" trước khi deploy, tránh trust mù | Viết 10 test case theo 4 paths trong spec, đo precision thủ công |
| 3 | **Mock API design** | Để demo mà không cần VinFast API thật, cần biết mock get_vehicle_info(), run_diagnostic() trả về data hợp lý | FastAPI + Pydantic để tạo mock endpoint trong < 2h |

### Nếu chọn Track A (Product Depth)

| # | Kỹ năng cần bù | Tại sao cần | Cách học nhanh nhất |
|---|---|---|---|
| 1 | **User interview kỹ thuật** | Phỏng vấn chủ xe để tìm pain thật, không bị confirmation bias | Đọc "The Mom Test" — 1 buổi, áp dụng ngay vào 3 buổi phỏng vấn |
| 2 | **Prototype no-code / low-code** | Tạo mockup UX để user phản hồi mà không cần code | Figma hoặc v0.dev — đủ để test booking flow |
| 3 | **Trust calibration trong AI product** | Biết đặt câu hỏi đúng: user trust AI đến mức nào, điểm nào họ muốn override | Nghiên cứu case study: Google Maps rerouting, Spotify Discover Weekly |

### Kỹ năng bù áp dụng cho cả hai track

| # | Kỹ năng | Lý do |
|---|---|---|
| 1 | **Prompt engineering có cấu trúc** | Spec định nghĩa severity-based logic — cần biết encode logic này vào system prompt hiệu quả, không phải viết lại mỗi lần |
| 2 | **Cost monitoring cơ bản** | Worksheet 2 và 3 phân tích cost tốt về lý thuyết — cần biết đọc dashboard thực tế (LangSmith hoặc Anthropic Console) để verify |

---

## Tổng kết

| Hạng mục | Kết quả |
|---|---|
| Điểm mạnh nhóm | Business/Product (observable từ spec) |
| Điểm cần phát triển | AI Engineering implementation + User validation |
| Track Phase 2 khuyến nghị | B + A (Technical Build + Product Depth song song) |
| Kỹ năng cần bù ưu tiên | Function calling, User interview, Eval/testing |
| Câu hỏi quan trọng nhất chưa trả lời | User có trust AI để đặt lịch bảo dưỡng không? |

> **Lời nhắc:** Spec tốt là điều kiện cần, không phải điều kiện đủ. Phase 2 cần chuyển từ "chúng tôi nghĩ user cần cái này" sang "user nói họ cần cái này và đã dùng thử".
