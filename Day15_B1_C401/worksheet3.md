# Worksheet 3 — Cost Optimization Debate

**Sản phẩm:** VFCare — AI dự đoán & đặt lịch bảo dưỡng xe VinFast
**Nhóm:** B1-C401
**Mục tiêu:** Chọn đúng chiến lược tối ưu thay vì tối ưu theo phong trào

---

## Bối cảnh trước khi chọn chiến lược

Từ Worksheet 2, cost thực tế của hệ thống:

| Lớp | Cost/ngày (MVP) | % tổng |
|---|---|---|
| Human review | $30.00 | 84% |
| Token API (LLM) | $1.40 | 4% |
| Retraining pipeline | $1.70 | 5% |
| Compute + Storage + Monitoring | $2.50 | 7% |
| **Tổng** | **$35.60** | 100% |

**Quan sát quan trọng:** Token API chỉ chiếm 4% tổng cost. Tối ưu token mà bỏ qua human review là tối ưu sai chỗ. Tuy nhiên ở scale lớn (10x user), token cost tăng linear và trở thành đáng kể. Chiến lược phải phục vụ cả hai giai đoạn.

---

## 3 Chiến lược được chọn

---

### Chiến lược 1 — Selective Inference (Phân tầng request trước khi gọi LLM)

#### Tiết kiệm phần nào

Loại bỏ LLM call hoàn toàn cho các xe không cần phân tích. Phần lớn xe trong fleet mỗi ngày đều "bình thường" — không có lỗi, chưa đến ngưỡng bảo dưỡng. Hiện tại hệ thống vẫn tốn token để xác nhận điều này.

```
[Xe kết nối] → Rule-based filter → "All clear" → Không gọi LLM
                                 → Anomaly detected → Gọi LLM để phân tích
```

**Rule-based filter (không cần LLM):**
- ODO < ngưỡng bảo dưỡng tiếp theo AND
- Không có error code nào từ run_diagnostic() AND
- Lần bảo dưỡng cuối < 6 tháng
→ Kết quả: push "Xe bạn đang ổn, không cần hành động" — không tốn token

#### Lợi ích

- Giảm 50–65% số LLM calls (ước tính phần lớn xe mỗi ngày không có lỗi)
- Latency background scoring giảm từ ~2s xuống ~50ms cho phần lớn fleet
- Giảm surface area bảo mật: ít data hơn được gửi lên cloud API

#### Trade-off

- Rule-based filter có thể bỏ sót lỗi tinh tế (false negative) nếu threshold cài không đúng
- Cần maintain song song 2 hệ thống: rule engine + LLM pipeline
- Khi VinFast thêm sensor mới, phải update rule engine

#### Thời điểm áp dụng

**Làm ngay từ MVP.** Không cần infrastructure mới, chỉ cần thêm một lớp pre-filter trước khi gọi `run_diagnostic()`. Risk thấp, impact cao nhất trong 3 chiến lược.

---

### Chiến lược 2 — Model Routing (Dùng model phù hợp với độ phức tạp request)

#### Tiết kiệm phần nào

Không phải mọi bước trong conversation đều cần model mạnh và đắt. Phân loại:

| Bước xử lý | Độ phức tạp | Model phù hợp | Cost/1K tokens |
|---|---|---|---|
| get_explainability() — phân tích risk, lịch sử xe | Cao | Claude Sonnet 4.6 | $3 input / $15 output |
| run_diagnostic() — phân tích error code phức tạp | Cao | Claude Sonnet 4.6 | $3 input / $15 output |
| recommend_schedule() — gợi ý lịch theo severity | Trung bình | Claude Haiku 4.5 | $0.8 input / $4 output |
| check_slot_availability() → book_appointment() | Thấp | Claude Haiku 4.5 | $0.8 input / $4 output |
| cancel_or_postpone() — ghi nhận từ chối | Thấp | Claude Haiku 4.5 | $0.8 input / $4 output |

Ước tính: ~60% token consumption có thể routing sang Haiku → tiết kiệm ~55% token cost.

```
Request đến → Classifier (rule-based, không tốn LLM) → Sonnet / Haiku
```

#### Lợi ích

- Token cost giảm ~55% khi đã có usage data để route đúng
- Haiku latency thấp hơn → Happy Path nhanh hơn (booking xong < 1.5s thay vì < 2s)
- Không cần thay đổi product logic, chỉ thay đổi ở orchestration layer

#### Trade-off

- Cần đánh giá kỹ: nếu route sai (Haiku làm việc của Sonnet), quality giảm → user reject nhiều hơn → tăng human review cost (phản tác dụng)
- Phải benchmark chất lượng Haiku trên bộ test case VinFast trước khi deploy
- Thêm complexity vào orchestration layer

#### Thời điểm áp dụng

**Làm sau MVP, khi đã có 4–6 tuần usage data thực tế.** Cần biết phân phối thực tế của các path (bao nhiêu % happy, low-confidence, failure) trước khi routing. Tối ưu sai route giai đoạn đầu có thể làm mất trust người dùng — chi phí khắc phục cao hơn tiết kiệm được.

---

### Chiến lược 3 — Semantic Caching cho Background Scoring

#### Tiết kiệm phần nào

Background batch scoring chạy hàng nghìn xe mỗi ngày. Nhiều xe cùng model (VF8, VF9), cùng mốc ODO, cùng error code → recommendation là giống nhau. Thay vì gọi LLM cho mỗi xe, cache kết quả theo key:

```
cache_key = hash(vehicle_model + error_codes + odometer_range + severity)
```

Ví dụ: 200 xe VF8 có `error_code: BRAKE_WEAR_MEDIUM` tại ODO 40,000–45,000km → cùng 1 recommendation → chỉ gọi LLM 1 lần, 199 xe còn lại đọc cache.

Cache invalidation: TTL 24 giờ (đủ cho batch scoring ngày), hoặc khi có firmware update thay đổi ngưỡng cảm biến.

#### Lợi ích

- Background scoring cost giảm 40–70% tùy mức độ trùng lặp trong fleet
- Latency batch scoring giảm mạnh → có thể tăng tần suất scoring mà không tăng cost
- Cache lưu on-prem → không gửi data lên cloud lặp lại → giảm privacy exposure

#### Trade-off

- Caching phù hợp cho recommendation chung, **không phù hợp** cho phần cá nhân hóa (thói quen lái, lịch user prefer)
- Nếu cache quá coarse-grained → recommendation thiếu cá nhân hóa, mất value proposition
- Cần infrastructure cache (Redis/Memcached) và logic invalidation

#### Thời điểm áp dụng

**Làm sau MVP, khi fleet đủ lớn (>200 xe cùng model).** Ở Conservative scenario (150 lượt/ngày, fleet nhỏ), cache hit rate thấp → không đáng đầu tư. Ở Realistic/Optimistic với hàng nghìn xe, cache trở nên rất hiệu quả.

---

## Quyết định: Làm ngay vs Để sau

| Chiến lược | Quyết định | Lý do |
|---|---|---|
| **Selective Inference** | ✅ **Làm ngay** | Không cần infra mới, risk thấp, tiết kiệm 50–65% LLM calls từ ngày đầu |
| **Model Routing** | ⏳ **Để sau (sau 4–6 tuần)** | Cần usage data thực để route đúng; route sai giai đoạn đầu tăng human review cost |
| **Semantic Caching** | ⏳ **Để sau (khi fleet >200 xe)** | Cache hit rate quá thấp ở MVP scale; cần đầu tư infra không xứng với Conservative scenario |

---

## Tại sao không chọn các chiến lược còn lại?

### Prompt Compression — Không ưu tiên

Tool definitions (8 tools × ~100 tokens) là phần không thể nén nhiều vì LLM cần đọc schema để gọi đúng function. Nén system prompt tiết kiệm ~200–300 tokens/conv → ~$0.001/conv → không đáng đầu tư engineering time ở giai đoạn này.

### Smaller/Self-hosted Model — Quá sớm

Self-hosting cần GPU on-prem, đội ML riêng để vận hành, và fine-tuning data đủ lớn. Ở MVP 150 conv/ngày, break-even so với cloud API là sau nhiều năm. Chỉ xem xét khi volume đạt >5,000 conv/ngày hoặc khi data sovereignty buộc phải inference on-prem hoàn toàn.

---

## Kết luận: Cost driver thực sự và chiến lược đúng

```
Giai đoạn MVP:
├── Cost driver #1: Human review (84%) → Giải pháp: Selective Inference
│   giảm LLM calls → giảm AI errors → giảm cần human review
└── Cost driver #2: Token API (4%) → Acceptable, chưa cần optimize

Giai đoạn Scale (5–10x):
├── Cost driver #1: Storage telemetry (tăng mạnh nhất, không dừng)
│   → Cần retention policy, cold storage tier (không phải LLM optimization)
├── Cost driver #2: Token API (tăng linear) → Model Routing
└── Cost driver #3: Background scoring → Semantic Caching
```

> **Bài học chốt:** Tối ưu token trước khi tối ưu human review là tối ưu 4% và bỏ qua 84%. Selective Inference không phải là "giảm token" mà là "đừng gọi LLM khi không cần" — đây là chiến lược đúng cho giai đoạn đầu.
