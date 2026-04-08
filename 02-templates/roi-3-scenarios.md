# ROI 3 kịch bản — VinFast AI Agent Đặt Lịch Bảo Trì

**Bài toán:** Khách hàng VinFast khó đặt lịch bảo trì vì phụ thuộc tổng đài & thao tác thủ công. AI Agent tự động kiểm tra lịch trống, gợi ý xưởng/khung giờ, chốt lịch trong một luồng hội thoại.

---

|   | Thận trọng | Thực tế | Lạc quan |
|   | Conservative | Realistic | Optimistic |
|---|-------------|-----------|------------|
| **Assumption** | 150 lượt/ngày qua AI (20% tổng); 58% tự động hoàn toàn; chủ yếu giờ hành chính | 500 lượt/ngày (60% tổng); 75% tự động; hoạt động 24/7 | 1,200 lượt/ngày (full adoption); 88% tự động; tích hợp toàn hệ thống |
| **Cost** | API: $0.8/ngày + Infra/maintain: $5.5/ngày = **$6.3/ngày** | API: $2.5/ngày + Infra/maintain: $7.5/ngày = **$10/ngày** | API: $6/ngày + Infra/maintain: $9/ngày = **$15/ngày** |
| **Benefit** | Giảm 87 cuộc tổng đài × 12 phút → tiết kiệm ~$14/ngày nhân lực; +8 booking ngoài giờ × $45 × 20% margin = $72; giảm no-show 2% = $6 → **~$92/ngày** | Giảm 375 cuộc → $60/ngày; +30 booking ngoài giờ = $300; upsell 4% × 375 × $18 = $270; no-show 2% = $15 → **~$645/ngày** | Giảm 1,056 cuộc → $169/ngày; +80 booking ngoài giờ = $880; upsell 8% × 1,056 × $22 = $1,859; no-show 2% = $33 → **~$2,941/ngày** |
| **Net** | ~$86/ngày → **~$25,800/năm** | ~$635/ngày → **~$190,500/năm** | ~$2,926/ngày → **~$877,800/năm** |

> 💡 Chi phí nhân lực tổng đài tính theo mức thực tế VN: $0.80/giờ. Revenue trung bình/booking: $45–55 (quy đổi từ gói bảo dưỡng 800K–2M VNĐ). Cost inference giảm nhanh (~100x trong 2 năm) — worst case hôm nay ≠ worst case 6 tháng sau.

**Kill criteria:**
- Tỷ lệ tự động hoàn toàn < 40% sau 60 ngày vận hành → model kém hoặc luồng hội thoại cần thiết kế lại
- Net/ngày âm liên tục 2 tháng, kể cả sau khi tối ưu prompt & infra
- NPS khách hàng sau trải nghiệm AI < 30 (tức tệ hơn tổng đài truyền thống)
- Tỷ lệ booking thành công < 60% tổng lượt bắt đầu hội thoại (funnel vỡ ở bước nào đó)
