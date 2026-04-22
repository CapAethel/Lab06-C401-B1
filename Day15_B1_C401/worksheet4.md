# Worksheet 4 — Scaling & Reliability Tabletop

**Sản phẩm:** VFCare — AI dự đoán & đặt lịch bảo dưỡng xe VinFast
**Nhóm:** B1-C401
**Mục tiêu:** Luyện phản ứng khi hệ thống gặp tải tăng hoặc provider lỗi

---

## Nền tảng phân tích: Real-time vs Async

Trước khi vào tình huống, phân loại request theo độ trễ chấp nhận được:

| Loại request | Ví dụ | Chế độ | Latency target |
|---|---|---|---|
| User mở app chờ gợi ý | AI phân tích + suggest lịch | **Real-time** | < 2s (spec) |
| User bấm "Đặt lịch" | book_appointment() | **Real-time với confirm** | < 3s hoặc async + notify |
| Background fleet scoring | run_diagnostic() cho toàn fleet | **Async / Batch** | < 200ms per xe, chạy nền |
| Retraining model | Fine-tune từ feedback log | **Async / Scheduled** | Không giới hạn |

Phân loại này quyết định trực tiếp chiến lược fallback cho mỗi tình huống.

---

## Tình huống 1 — Traffic Tăng Đột Biến

### Mô tả

VinFast thông báo recall phần mềm hoặc có sự kiện lớn (ra mắt model mới, khuyến mãi bảo dưỡng) → hàng nghìn chủ xe đồng thời mở app kiểm tra. Hoặc đơn giản hơn: peak sáng 7–9h khi toàn bộ Conservative traffic (150 lượt) dồn vào 2 giờ thay vì phân bổ đều ngày.

### Tác động tới user

```
Request queue đầy
    → LLM API latency tăng từ <2s lên 8–15s
        → Spinner quay mãi không ra kết quả
            → User bấm thoát app
                → Booking rate giảm, drop-off tăng
                    → Fallback rate vượt ngưỡng red flag (>25%)
```

Trường hợp tệ hơn: `check_slot_availability()` bị timeout → app báo lỗi khi user đã chờ 10 giây → mất trust ngay lần đầu dùng.

### Phản ứng ngắn hạn

1. **Queue + async với notify:** Với booking request (không phải gợi ý lịch), chuyển sang async:
   - Hiển thị ngay: _"Đang xử lý, bạn sẽ nhận thông báo trong 1–2 phút"_
   - Khi xong: push notification kết quả
   - User không phải chờ màn hình, không bị drop

2. **Rate limiting có ưu tiên:**
   - Critical severity request → ưu tiên xử lý real-time
   - Low severity → đẩy vào queue, xử lý khi load giảm

3. **Trả về cached recommendation tạm thời:**
   - Nếu xe đã được scoring trong vòng 6 giờ → trả kết quả cũ kèm label _"Cập nhật lúc X"_
   - Không gọi LLM lại, giảm ngay tải tức thì

### Giải pháp dài hạn

1. **Auto-scaling app server** theo CPU/request queue depth (không theo lịch cố định vì không predict được recall/sự kiện)

2. **Pre-warming LLM context vào buổi sáng:** Batch scoring chạy lúc 6h (trước peak), kết quả cache sẵn. Khi user mở app 7–9h → đọc cache thay vì gọi LLM fresh

3. **Selective Inference (từ Worksheet 3) đặc biệt quan trọng ở đây:** Filter ngay những xe "all clear" để không chạm đến LLM pipeline trong lúc cao điểm

---

## Tình huống 2 — Provider Timeout (LLM API Down)

### Mô tả

Claude API hoặc OpenAI API trả về timeout / 503 liên tục trong 15–60 phút. Xảy ra do provider incident (không phải do lỗi của hệ thống VFCare). Đây là failure mode ngoài tầm kiểm soát của đội engineering.

### Tác động tới user

```
LLM API timeout
    → run_diagnostic() không có kết quả
        → Không có gợi ý lịch
            → User không biết xe có cần bảo dưỡng không
                → Xe critical severity không được nhắc
                    → Rủi ro an toàn nếu kéo dài
```

Đây là failure mode nguy hiểm nhất vì ảnh hưởng đến **toàn bộ user đồng thời**, không phải từng cá nhân.

### Phản ứng ngắn hạn — Circuit Breaker

```
Bình thường:     Request → LLM API → Response
Khi timeout:     Request → Circuit Breaker [OPEN] → Fallback ngay (không chờ timeout)
Sau 5 phút:      Circuit Breaker [HALF-OPEN] → Thử 1 request → Nếu OK → [CLOSED]
```

**Cấu hình circuit breaker:**
- Threshold mở: 5 lỗi liên tiếp trong 30 giây
- Timeout mặc định mỗi LLM call: 8 giây (không để user chờ hơn)
- Half-open probe: 1 request thử mỗi 60 giây

**Fallback theo tầng khi circuit breaker mở:**

| Tầng | Fallback | Áp dụng khi |
|---|---|---|
| 1 | Rule-based recommendation | LLM down < 30 phút |
| 2 | Cached result (nếu có trong 24h) | LLM down, chưa có rule |
| 3 | Human escalation (hotline) | LLM down > 30 phút, critical severity |

**Rule-based recommendation (Tầng 1) — không cần LLM:**

```python
if error_codes contains CRITICAL:
    → "Xe bạn cần bảo dưỡng sớm. Gọi 1900 23 23 89 để đặt lịch ngay."
elif odometer >= next_maintenance_threshold:
    → "Xe đã đến mốc bảo dưỡng định kỳ. Đặt lịch trong tuần này."
else:
    → "Xe bạn đang ổn. Chúng tôi sẽ kiểm tra lại vào ngày mai."
```

Rule-based không cá nhân hóa được nhưng đảm bảo **không có false silence** (xe critical không bị bỏ qua).

### Giải pháp dài hạn

1. **Multi-provider routing:** Primary = Claude Sonnet, Fallback = OpenAI GPT-4o, Emergency = Haiku self-hosted (nếu data sovereignty cho phép)

2. **Separate SLA cho critical vs non-critical:** Critical severity xe → luôn có path xử lý dù LLM down. Non-critical → queue lại khi LLM phục hồi

3. **Provider SLA monitoring:** Alert ngay khi p99 latency LLM API > 5s, không chờ đến khi user báo lỗi

---

## Tình huống 3 — Response Chậm (Degraded Performance)

### Mô tả

LLM API không down hoàn toàn nhưng trả về chậm: p50 = 4s, p95 = 12s (thay vì < 2s theo spec). Xảy ra khi provider throttle hoặc model đang tải cao. Đây là trường hợp khó phát hiện hơn timeout vì hệ thống "vẫn chạy".

### Tác động tới user

- Spinner quay 4–12 giây → **70% user mobile bỏ qua sau 4 giây** (theo industry benchmark)
- Tool chain (get_user_info → get_vehicle_info → run_diagnostic → recommend_schedule) gọi tuần tự → mỗi bước 4s → tổng >16s
- User không nhận được error, chỉ thấy chậm → không biết retry hay đợi
- Booking trong trạng thái intermediate: check_slot xong nhưng book_appointment chưa xong → slot bị hold nhưng không confirm

### Phản ứng ngắn hạn

1. **Streaming response + progressive disclosure:**
   - Không chờ toàn bộ LLM response xong mới hiển thị
   - Hiển thị từng phần khi có: "Đang kiểm tra xe... ✓ Pin: Tốt | Đang phân tích motor..."
   - User thấy tiến trình, không cảm giác bị treo

2. **Timeout cứng per tool call (8s) + retry 1 lần:**
   ```
   call tool → wait 8s → timeout → retry once → timeout → fallback
   ```
   Không để user chờ > 16s dù bất kỳ lý do gì.

3. **Parallel tool calls khi có thể:**
   - `get_user_info()` và `get_vehicle_info()` không phụ thuộc nhau → gọi song song
   - Giảm tổng latency từ 4 calls × 4s = 16s xuống còn 2 rounds × 4s = 8s

4. **Route sang Haiku cho non-critical:** Nếu detect p95 > 5s trên Sonnet → tự động route Low severity request sang Haiku (nhanh hơn ~3x, rẻ hơn)

### Giải pháp dài hạn

1. **SLO-based auto-routing:** Monitor p95 latency real-time. Nếu vượt 3s → tự động tăng tỷ lệ Haiku routing. Nếu về dưới 2s → trả về Sonnet

2. **Pre-compute background scoring:** Hầu hết gợi ý lịch có thể tính trước lúc 6h sáng. User mở app 7h chỉ đọc kết quả đã có → latency = 0

---

## Metrics cần Monitor

### Tier 1 — Alert ngay (page on-call)

| Metric | Ngưỡng alert | Lý do |
|---|---|---|
| LLM API error rate | > 5% trong 5 phút | Circuit breaker sắp mở |
| Booking success rate | < 60% | Funnel vỡ — kill criteria của spec |
| LLM p99 latency | > 8s | User experience phá vỡ hoàn toàn |
| Circuit breaker state | OPEN | Toàn bộ user đang dùng fallback |

### Tier 2 — Review hàng ngày

| Metric | Ngưỡng quan tâm | Lý do |
|---|---|---|
| Fallback rate | > 10% | Spec định nghĩa red flag |
| Queue depth (background scoring) | > 1,000 xe pending | Backlog tích lũy |
| LLM p95 latency | > 3s | Báo hiệu degradation sắp xảy ra |
| Slot accuracy | > 0% double-booking | Zero tolerance theo spec |
| Drop-off rate per step | Tăng > 20% so với baseline | Bước nào đó đang broken |

### Tier 3 — Review hàng tuần

| Metric | Mục đích |
|---|---|
| Cache hit rate (background scoring) | Đánh giá hiệu quả Semantic Caching |
| Rule-based fallback activation count | LLM down bao nhiêu lần/tuần |
| Human escalation rate | Xác định khi nào cần mở rộng team review |
| Tool call timeout rate per tool | Phát hiện tool nào đang có vấn đề API |

---

## Fallback Proposal

### Kiến trúc fallback 3 tầng

```
[User Request]
      │
      ▼
[Pre-filter: Selective Inference]
      │ All clear? → Rule-based response (không tốn LLM)
      │ Anomaly?
      ▼
[LLM Pipeline — Sonnet]
      │ OK (< 8s)? → Real-time response
      │ Slow (> 8s) hoặc p95 > 3s?
      ▼
[Tầng 1 Fallback: Model Routing → Haiku]
      │ OK? → Response với note "Phân tích rút gọn"
      │ Haiku cũng lỗi / circuit breaker OPEN?
      ▼
[Tầng 2 Fallback: Rule-based Engine]
      │ Có error code? → Template response theo severity
      │ Critical severity?
      ▼
[Tầng 3 Fallback: Human Escalation]
      └─ Push notification: "Gọi 1900 23 23 89 để được hỗ trợ ngay"
         + Booking thủ công qua tổng đài
```

### Nguyên tắc thiết kế fallback

| Nguyên tắc | Áp dụng |
|---|---|
| **Không có silent failure** | Mọi fallback phải thông báo user biết đang ở trạng thái nào |
| **Critical severity không được bỏ sót** | Dù LLM down, xe critical vẫn phải được cảnh báo qua rule-based hoặc hotline |
| **Async > timeout** | Booking có thể async + notify; gợi ý lịch mới cần real-time |
| **Fallback phải test định kỳ** | Chaos engineering: tắt LLM API định kỳ để verify fallback chain hoạt động |

### Retry Policy

| Loại call | Retry | Backoff | Max wait |
|---|---|---|---|
| LLM inference | 1 lần | Ngay lập tức | 8s + 8s = 16s |
| book_appointment() | 2 lần | Exponential (2s, 4s) | ~14s tổng |
| check_slot_availability() | 2 lần | Exponential (1s, 2s) | ~5s tổng |
| run_diagnostic() | 0 (dùng cached nếu có) | — | 8s rồi fallback |

---

## Tổng kết

| Tình huống | Rủi ro chính | Phản ứng ngắn hạn | Giải pháp dài hạn |
|---|---|---|---|
| Traffic đột biến | Drop-off, booking fail | Queue + async notify + cache | Pre-warming + auto-scaling + Selective Inference |
| Provider timeout | Toàn bộ user mất AI | Circuit breaker + rule-based fallback | Multi-provider + self-hosted emergency |
| Response chậm | User bỏ app, invisible failure | Streaming + parallel tools + hard timeout | SLO-based routing + pre-compute background |

> **Nguyên tắc chung:** Thiết kế cho failure, không thiết kế cho happy path. Mỗi tool call phải có timeout, mỗi LLM call phải có fallback, và xe critical severity phải luôn có ít nhất một đường thông báo đến user dù toàn bộ AI infrastructure down.
