# Ngày 6 — Hackathon: SPEC → POC → Demo

> Không có lecture mới. Hôm nay = chứng minh. SPEC là hypothesis, POC là evidence, Demo là convince.

---

## Tổng quan

```text
SÁNG (9:00-13:00)              CHIỀU (14:00-16:00)            DEMO DAY (16:00-18:00)
┌────────────────────┐        ┌────────────────────┐         ┌────────────────────┐
│   BUILD POC         │        │   POLISH + PREP     │         │  GALLERY WALK +     │
│                     │        │                     │         │  DEMO ROUND         │
│  M1: Canvas check   │        │  Polish POC          │         │  60 phút             │
│  Build              │   →    │  Viết demo script    │    →    ├────────────────────┤
│  M2: Show 1 thứ     │        │  M4: Dry run + setup │         │  TOP TEAMS PRESENT  │
│  Build tiếp         │        │                     │         │  + TRAO GIẢI         │
│  M3: SPEC final     │        │                     │         │                     │
└────────────────────┘        └────────────────────┘         └────────────────────┘
```

---

## Timeline

| Giờ | Milestone | Nội dung | Ghi chú |
|-----|-----------|----------|---------|
| 9:00 | **M1** | Canvas check + SPEC draft review | Chưa có Canvas → bổ sung trước 9:30 |
| 9:15 | | **Build POC** | GV đi vòng: "Đang build gì? Stuck ở đâu?" |
| 11:00 | **M2** | **"Show 1 thứ chạy được"** — GV check từng nhóm | Chưa có gì → simplify scope / chuyển mock |
| 11:15 | | Build tiếp | |
| 13:00 | **M3** | **SPEC final + demo flow draft** | Trước nghỉ trưa — chiều chỉ polish |
| 13:00–14:00 | | Nghỉ trưa | |
| 14:00 | | Polish + chuẩn bị demo | 15:00: "1h nữa Demo. Freeze code, focus narrative." |
| 15:30 | **M4** | Demo prep done + dry run | Mỗi nhóm 1 bàn: laptop + poster/slides |
| **16:00** | **M5** | **Gallery walk + demo round (60 phút)** | 2-3 ở lại trình bày + 2-3 đi xem + feedback form |
| **17:00** | **M6** | **Top teams present + trao giải + closing** | |

---

## Deliverables

| # | Deliverable | Loại | Deadline |
|---|-------------|------|----------|
| 1 | **SPEC final** — Canvas + 6 phần đầy đủ | Nhóm | 13:00 Day 6 |
| 2 | **POC** — Option A (prompt demo), B (mock flow), hoặc C (working code) | Nhóm | 16:00 Day 6 |
| 3 | **Demo** — 2 phút trình bày tại bàn + poster/slides | Nhóm | 16:00 Day 6 |
| 4 | **Feedback forms** — đánh giá các team khác trong zone | Cá nhân | Cuối demo round |
| 5 | **Individual form** — role + reflection | Cá nhân | Sau Day 6 |

---

## SPEC — 6 phần

Dùng template: [`01-templates/spec-template.md`](01-templates/spec-template.md)

| # | Phần | Yêu cầu |
|---|------|---------|
| 1 | **AI Product Canvas** | 3 cột Value / Trust / Feasibility + learning signal. Auto hay aug? Data gì, loại gì, có marginal value? |
| 2 | **User Stories 4 paths** | 2–3 features × 4 paths: happy / low-confidence / failure / correction |
| 3 | **Eval metrics + threshold** | 3 metrics + threshold + red flag. Precision hay recall? Tại sao? |
| 4 | **Top 3 failure modes** | Mỗi failure: trigger → hậu quả → mitigation |
| 5 | **ROI 3 kịch bản** | Conservative / realistic / optimistic + kill criteria |
| 6 | **Mini AI spec** | 1 trang tóm tắt: giải gì, cho ai, auto/aug, quality, risk, data flywheel |

---

## POC — 3 options

| | Option A | Option B | Option C |
|---|---|---|---|
| **Gì** | Prompt-based demo | Mock flow | Working code |
| **Cách** | Agent/chatbot chạy 1 flow, dùng API có sẵn | Figma/slides + 1 prompt test thật | End-to-end |
| **Cho ai** | Mọi nhóm | Mọi nhóm | Nhóm mạnh (bonus) |

- Chọn A hoặc B. Bonus nếu làm được C.
- Option B vẫn **phải có ít nhất 1 prompt/AI call test thật** — không được 100% mock.
- **Vibe-coding rule:** không hiểu code = 0 điểm demo. Mỗi người giải thích được phần mình làm.

---

## Demo round (M5, 60 phút)

**Cách chơi:**

1. Mỗi nhóm cử 2-3 người **ở lại demo** tại bàn, 2-3 người **đi xem** nhóm khác
2. Đi xem + feedback **đủ** các team trong zone
3. Mỗi lần xem: nghe demo (~3-4 phút) + điền feedback form (~1-2 phút)

**3 tiêu chí feedback (chấm 1-5):**

| # | Tiêu chí | Hỏi |
|---|----------|-----|
| 1 | Problem-solution fit | Bài toán rõ? Giải pháp logic? |
| 2 | AI product thinking | Auto/aug rõ? Failure modes? Eval metrics? |
| 3 | Demo quality | Chạy được? Narrative rõ? |

Thêm: 1 điều làm tốt + 1 gợi ý cải thiện.

**Nộp đủ feedback forms** — chấm cả chất lượng review.

---

## Checklist trước demo (M4, 15:30)

- [ ] POC chạy được hoặc mock flow ready
- [ ] Demo script 2 phút: ai nói gì, show gì, thứ tự nào
- [ ] Poster/slides tóm tắt: Problem → Solution → Auto/Aug → Demo
- [ ] Mỗi người trả lời được: "Auto hay aug?", "Failure mode chính?", "Phần mình làm gì?"
- [ ] Feedback forms nhận đủ

---

## Scoring (chung Day 5 + Day 6 = 100 điểm)

| Hạng mục | Điểm | Loại | Khi nào |
|----------|------|------|---------|
| SPEC milestone | 25 | Nhóm + cá nhân | Draft midnight D5, final 13:00 D6 |
| POC milestone | 15 | Nhóm + cá nhân | 16:00 Day 6 |
| Demo Day | 25 | Nhóm | Demo round + top teams, chiều D6 |
| UX exercise | 10 | Cá nhân + bonus | UX workshop sáng D5 |
| Individual form (role + reflection) | 25 | Cá nhân | Sau D6 |
| **Tổng** | **100** | | |

---

## Tài liệu trong repo này

### Templates — [`01-templates/`](01-templates/)

| File | Dùng cho |
|------|----------|
| [`spec-template.md`](01-templates/spec-template.md) | SPEC 6 phần — template chính |
| [`canvas-template.md`](01-templates/canvas-template.md) | AI Product Canvas |
| [`user-stories-4path.md`](01-templates/user-stories-4path.md) | User stories × 4 paths |
| [`eval-metrics.md`](01-templates/eval-metrics.md) | Eval metrics + threshold |
| [`failure-modes.md`](01-templates/failure-modes.md) | Top 3 failure modes |
| [`roi-3-scenarios.md`](01-templates/roi-3-scenarios.md) | ROI 3 kịch bản |
| [`demo-script.md`](01-templates/demo-script.md) | Demo script 2 phút |
| [`poster-layout.md`](01-templates/poster-layout.md) | Poster/slides layout |

### Hướng dẫn công cụ — [`02-tools-guide/`](02-tools-guide/)

| File | Nội dung |
|------|----------|
| [`api-cheatsheet.md`](02-tools-guide/api-cheatsheet.md) | API key setup, model nào cho gì |
| [`prototyping-tools.md`](02-tools-guide/prototyping-tools.md) | Công cụ build POC nhanh |
| [`prompt-engineering-tips.md`](02-tools-guide/prompt-engineering-tips.md) | Prompt tips cho hackathon |

### Tham khảo — [`03-reference/`](03-reference/)

| File | Nội dung |
|------|----------|
| [`day5-cheatsheet.md`](03-reference/day5-cheatsheet.md) | Recap 1 trang các framework Day 5 |
| [`canvas-example.md`](03-reference/canvas-example.md) | Ví dụ Canvas hoàn chỉnh (AI Email Triage) |

### Luật chơi — [`04-rules/`](04-rules/)

| File | Nội dung |
|------|----------|
| [`hackathon-rules.md`](04-rules/hackathon-rules.md) | Rules, timeline, milestones, scoring, demo round |

---

*Ngày 6 — VinUni A20 — AI Thực Chiến · 2026*
