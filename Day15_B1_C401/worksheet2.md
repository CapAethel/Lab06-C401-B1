# Worksheet 2 — Cost Breakdown: AI System

**Sản phẩm:** VFCare — AI dự đoán & đặt lịch bảo dưỡng xe VinFast
**Nhóm:** B1-C401
**Mục tiêu:** Bóc tách cost của AI system thay vì chỉ nhìn vào token/API

---

## 1. Ước lượng traffic

### Số user / request / ngày

Lấy trực tiếp từ 3 kịch bản ROI trong spec (Section 5):

| Kịch bản | Lượt/ngày qua AI | % tự động hoàn toàn | Active AI conversations |
|---|---|---|---|
| Conservative | 150 | 58% | ~87 conversations |
| Realistic | 500 | 75% | ~375 conversations |
| Optimistic | 1,200 | 88% | ~1,056 conversations |

Ngoài conversations chủ động, hệ thống chạy **background batch scoring** liên tục cho toàn bộ fleet đang kết nối — đây là workload riêng biệt, độc lập với số người mở app.

### Peak traffic

Chủ xe kiểm tra app buổi sáng trước đi làm → peak **7:00–9:00** (2 giờ ≈ 30% daily traffic):

| Kịch bản | Peak requests/giờ |
|---|---|
| Conservative | ~22 req/h |
| Realistic | ~75 req/h |
| Optimistic | ~180 req/h |

Background scoring: phân bổ đều 24/7, không bị spike theo peak người dùng.

---

## 2. Ước lượng token nếu dùng LLM API

### Cấu trúc một conversation (Happy Path)

| Thành phần | Loại | Tokens ước tính |
|---|---|---|
| System prompt + tool definitions (8 tools) | Input | ~1,300 |
| get_user_info() + get_vehicle_info() response | Input | ~500 |
| run_diagnostic() response | Input | ~400 |
| User message | Input | ~50 |
| Tool call results tổng hợp | Input | ~500 |
| **Tổng Input** | | **~2,750** |
| AI phân tích + gợi ý lịch | Output | ~300 |
| Tool call JSON (book_appointment…) | Output | ~200 |
| **Tổng Output** | | **~500** |
| **Tổng / conversation** | | **~3,250** |

### Theo từng path

| Path | Tokens ước tính | Lý do tăng |
|---|---|---|
| Happy Path | ~3,250 | Luồng ngắn nhất |
| Low-confidence | ~4,500 | Thêm get_explainability() + risk analysis |
| Failure / Correction | ~5,000 | Multi-turn, tool retry, user override |
| **Trung bình có trọng số** | **~4,000** | 60% happy, 25% low-conf, 15% failure/correction |

### Chi phí token (Claude Sonnet 4.6)

- Input: $3 / 1M tokens → 2,750 tokens × $3/1M = **$0.0083/conv**
- Output: $15 / 1M tokens → 500 tokens × $15/1M = **$0.0075/conv**
- **Tổng: ~$0.016/conversation**

Tại 150 conv/ngày → **~$2.4/ngày token cost** *(spec ghi $0.8/ngày — xem mục 6)*

---

## 3. Các lớp cost đầy đủ

| # | Lớp cost | Mô tả | Loại |
|---|---|---|---|
| 1 | **Token / LLM API** | Claude/OpenAI API call mỗi conversation | Variable, scales với requests |
| 2 | **Compute — app server** | API gateway, app backend, orchestration layer | Semi-fixed, tăng bậc thang |
| 3 | **Compute — background ML** | Batch scoring fleet: dự đoán maintenance risk mỗi xe mỗi ngày | Fixed/ngày, tăng với fleet size |
| 4 | **Storage — telemetry** | Time-series DB lưu cảm biến xe (pin, motor, ODO…) theo thời gian thực | Variable, tăng liên tục |
| 5 | **Storage — audit & logging** | Mọi AI decision phải log đầy đủ (ràng buộc enterprise worksheet 1) | Variable, retention dài hạn |
| 6 | **Storage — feedback log** | accept/reject/modify của từng user per xe | Variable |
| 7 | **Human review** | Nhân sự xem xét AI errors, edge case, khiếu nại chủ xe | Semi-fixed, thường bị bỏ quên |
| 8 | **Maintenance — retraining pipeline** | Fine-tune model định kỳ từ feedback log | Periodic, tăng theo data volume |
| 9 | **Maintenance — integration** | Cập nhật khi VinFast thay đổi API xưởng, CRM, ERP | Không dự đoán được |
| 10 | **Monitoring & alerting** | CloudWatch / Datadog / PagerDuty theo dõi uptime, latency, error rate | Fixed/tháng |

---

## 4. Tính sơ bộ cost ở mức MVP

**Giả định MVP:** Conservative scenario (150 lượt/ngày), fleet 500 xe kết nối, 1 kỹ thuật viên part-time review.

| Lớp | Tính toán | Cost/ngày |
|---|---|---|
| Token API | 87 conv × $0.016 | **$1.40** |
| Compute app server | 1 small instance (t3.medium ~$30/tháng) | **$1.00** |
| Background ML inference | 500 xe × batch scoring nhẹ | **$0.50** |
| Storage telemetry | 500 xe × ~10KB/ngày × 90 days retention | **$0.30** |
| Storage audit/logging | 87 conv × logs + system events | **$0.20** |
| Monitoring | Datadog basic (~$15/tháng) | **$0.50** |
| Human review | 1 người part-time (2h/ngày × $15/h) | **$30.00** |
| Maintenance retraining | Amortize 1 retraining/tháng × $50 | **$1.70** |
| **Tổng MVP** | | **~$35.60/ngày** |

> **Lưu ý quan trọng:** Spec ghi $6.3/ngày (Conservative). Con số đó **không bao gồm human review và retraining** — hai khoản chiếm ~90% cost thực tế ở mức MVP. Xem mục 6.

---

## 5. Khi user tăng 5x hoặc 10x — phần nào tăng mạnh nhất?

| Lớp cost | Tăng 5x user | Tăng 10x user | Đặc điểm |
|---|---|---|---|
| Token API | **5x** | **10x** | Linear — dễ dự đoán, dễ kiểm soát |
| Compute app server | ~2x (scale bậc thang) | ~3x | Tăng khi vượt ngưỡng instance |
| Background ML | ~5x (theo fleet size) | ~10x | Linear với số xe, không với active users |
| Storage telemetry | **>10x** | **>20x** | Tích lũy theo thời gian, không reset — **nguy hiểm nhất về dài hạn** |
| Storage audit/log | 5x | 10x | Linear nhưng cần retention dài → tổng GB tăng nhanh |
| Human review | 2–3x (team chưa cần mở rộng) rồi **nhảy vọt** | **5–8x** | Sub-linear đến một điểm, sau đó phải thuê thêm người |
| Retraining pipeline | ~2x (nhiều data hơn nhưng 1 pipeline) | ~3x | Sub-linear — lợi thế scale |
| Monitoring | ~1.5x | ~2x | Gần fixed, tăng chậm |

**Kết luận scaling:**
- **Tăng nhanh nhất:** Storage telemetry (tích lũy vô hạn) + Human review (nhảy bậc khi team phải mở rộng)
- **Tăng có thể predict:** Token API (linear, dễ budget)
- **Tăng chậm nhất:** Monitoring, retraining pipeline

---

## 6. Ba câu hỏi nhóm phải trả lời

### Cost driver lớn nhất là gì?

**Ở MVP → Human review** (chiếm ~84% cost ngày khi mới launch).
**Ở scale lớn → Storage telemetry** (tích lũy không ngừng từ hàng nghìn xe × nhiều sensor × retention dài).

Token API trông như cost driver vì dễ nhìn thấy trên dashboard, nhưng thực ra là phần dễ kiểm soát nhất (có thể cache, batch, giảm call không cần thiết).

---

### Hidden cost nào dễ bị quên nhất?

**1. Human review** — Spec hoàn toàn không đề cập. Nhưng ở giai đoạn đầu khi model chưa được fine-tune theo xe VinFast thật, tỉ lệ AI sai cao hơn nhiều. Cần người xem xét các trường hợp reject/failure để tránh chủ xe khiếu nại.

**2. Retraining pipeline** — Spec đề cập "data flywheel" và fine-tune theo chu kỳ nhưng không đưa vào bất kỳ dòng cost nào trong bảng ROI. Mỗi lần retrain tốn compute (GPU), kỹ sư ML, và evaluation cost.

**3. Integration maintenance** — Khi VinFast upgrade CRM, thay API xưởng, hoặc thêm model xe mới, toàn bộ tool calls (get_vehicle_info, check_slot_availability…) phải cập nhật. Cost này không định kỳ và khó budget trước.

**4. Storage retention dài hạn** — Audit trail (ràng buộc enterprise) cần lưu nhiều năm. 500 xe × 3 năm × daily telemetry = lượng data lớn hơn nhiều so với tính năng core.

---

### Đội đang ước lượng quá lạc quan ở đâu?

| Điểm lạc quan | Vấn đề thực tế |
|---|---|
| API cost $0.8/ngày tại 150 lượt | Tính lại ra ~$1.4/ngày nếu dùng Claude Sonnet 4.6 với average 4,000 tokens/conv. Có thể spec dùng model rẻ hơn hoặc tính ít tokens hơn thực tế. |
| Infra/maintain $5.5/ngày (Conservative) | Không bao gồm human review (~$30/ngày) và retraining (~$1.7/ngày). Thực tế gần **$35/ngày**, cao hơn 5.5x. |
| 75% tự động ở Realistic sau khi launch | 75% automation rate đòi hỏi model đã được fine-tune tốt với dữ liệu xe VinFast thật. Ở early stage, tỉ lệ này có thể chỉ đạt 40–50%, đẩy Fallback Rate vượt ngưỡng red flag (>25%). |
| $0.005–0.02/xe/ngày cho inference | Con số này có thể đúng nếu chỉ tính token API. Nhưng không phải chi phí toàn hệ thống per xe. Nếu tính đủ thì cost/xe/ngày ở MVP gần $0.07. |

---

## Tổng kết

| | Spec (Section 5) | Thực tế ước lượng worksheet này |
|---|---|---|
| Cost/ngày (Conservative) | $6.3 | **~$35.60** |
| Cost driver được nhắc | API + Infra | Token + Compute + Storage + **Human review + Retraining** |
| Hidden cost | Không đề cập | Human review, retraining, integration maintenance, storage retention |
| Scaling risk | Không phân tích | Storage telemetry + Human review tăng mạnh nhất |

> **Bài học cốt lõi:** Token cost là phần dễ nhìn nhất nhưng không phải lớn nhất. Human review và storage là hai khoản dễ bị quên và tăng không kiểm soát được khi scale.
