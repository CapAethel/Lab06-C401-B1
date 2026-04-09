# Individual reflection — Nguyễn Mai Phương (2A202600175)

> Dự án: VFCare — AI Agent dự đoán & đặt lịch bảo dưỡng xe VinFast điện
> Nhóm: C401-B1 · Ngày 6 Hackathon · 09/04/2026

---

## 1. Role

UI programmer, agent programmer: Dựa trên mock prototype để build agent và UI. 

---

## 2. Đóng góp cụ thể

- Viết Top 3 failure modes (SPEC_draft Section 4) — Tập trung vào các lỗi mà user KHÔNG BIẾT bị sai: (1) AI báo đặt thành công nhưng xưởng không ghi nhận do thiếu đồng bộ realtime, (2) hệ thống tự hủy lịch khi GPS phản hồi chậm mà không thông báo user, (3) AI xếp lịch sửa phần cứng mà không check tồn kho phụ tùng → khách đến nơi mới biết phải "giam xe". Mỗi failure mode có mitigation cụ thể (2-way handshake, push notification trước khi hủy, cross-check API kho).
- Program agent dựa trên cấu trúc từ sketch và mock data
- Tạo UI cơ bản cho demo
- Hỗ trợ tạo sketch (Thảo luận cùng nhóm, chốt sketch và flow cuối cùng cho nhóm)
---

## 3. SPEC mạnh/yếu

- Mạnh nhất — Failure modes:
3 failure modes đều là loại "user không biết mình bị lỗi" — đây là loại nguy hiểm nhất trong AI product. Đặc biệt failure #1 (AI báo thành công nhưng xưởng không nhận) được peer feedback ghi nhận là insight tốt. Mitigation "2-way handshake" thay vì confirm ngay cũng phản ánh đúng thực tế hệ thống distributed.

- Yếu nhất — ROI:
Dù đã tách 3 kịch bản với assumption khác nhau, nhưng các con số benefit (giảm cuộc tổng đài, upsell rate) vẫn là ước lượng chủ quan, chưa có dữ liệu benchmark từ VinFast thật. Peer feedback cũng chỉ ra "chưa thể hiện rõ tính toán phức tạp cần tới AI" — nghĩa là phần ROI chưa thuyết phục được rằng AI tạo ra giá trị khác biệt so với hệ thống rule-based đơn giản.

---

## 4. Đóng góp khác

- Test agent flow end-to-end — Chạy thử VFCare agent với cả 3 test cases (xe lỗi nặng, xe lỗi nhẹ, xe không lỗi) để kiểm tra agent có follow đúng severity-based flow không. Phát hiện agent đôi khi bỏ qua bước hỏi user mà tự gọi `recommend_schedule` → báo lại cho team fix system prompt.

- Chuẩn bị demo script — Phân công phần trình bày cho nhóm: ai nói Problem, ai nói Solution, ai chạy Live demo, ai nói Lessons. Dry run 2 lần trước khi demo thật.

- Liên kết Day 5 analysis vào SPEC — Kinh nghiệm phân tích 4-path cho Moni AI (MoMo) ở Day 5 giúp viết failure modes sâu hơn: ở Day 5 đã phân tích "khi AI sai" và "khi user mất niềm tin" → áp dụng trực tiếp vào failure mode #1 (trust breakdown khi booking fail im lặng).

---

## 5. Điều học được

- Silent failure nguy hiểm hơn visible failure. Trước hackathon, khi nghĩ về "AI sai" thì chỉ nghĩ đến trường hợp AI trả lời sai rõ ràng (user thấy ngay). Nhưng khi thiết kế failure modes cho VFCare, nhận ra rằng lỗi nguy hiểm nhất là lỗi mà user tin là đúng — AI nói "đặt lịch thành công", user tin và lái xe đến xưởng, đến nơi mới biết không có lịch. Loại lỗi này phá hủy trust nhanh hơn bất kỳ lỗi nào khác, và cách duy nhất để phòng là thiết kế confirmation loop ở tầng system (2-way handshake), không phải ở tầng prompt.

---

## 6. Nếu làm lại

- Viết failure modes trước, SPEC khác sau. Thực tế là nhóm viết Canvas -> User Stories -> Eval -> Failure modes theo thứ tự template. Nhưng failure modes lại inform ngược lại eval metrics (ví dụ: failure #1 → cần metric "Slot Accuracy = 100%") và cả ROI (failure #3 thiếu phụ tùng → ảnh hưởng benefit calculation). Nếu làm lại, sẽ brainstorm failure modes đầu tiên, rồi dùng nó để define metrics và tính ROI — logic sẽ chặt chẽ hơn.

Cụ thể: dành 30 phút đầu để nhóm cùng brainstorm 5-7 failure modes → vote top 3 → rồi mới chia nhau viết các section khác.

---

## 7. AI giúp gì / AI sai gì

### AI giúp:
- Dùng Claude để brainstorm failure modes — nó gợi ý được case "hệ thống tự hủy lịch khi GPS chậm" mà nhóm không nghĩ ra. Từ gợi ý này phát triển thành failure #2
- Dùng ChatGPT để tính nhanh ROI 3 kịch bản — đưa assumption vào, nó giúp cross-check phép tính và phát hiện chỗ tính nhầm benefit từ upsell.

### AI sai/mislead:
- Claude gợi ý thêm failure mode "AI bias theo vùng miền" — nghe hợp lý nhưng không phù hợp với scope MVP (VFCare đang mock data 1 thành phố, chưa có multi-region). Suýt thêm vào SPEC một failure mode không relevant.
- ChatGPT lên một flow không phù hợp với dự tính của nhóm nhưng trông thuyết phục, tuy nhiên không thực tế.

---