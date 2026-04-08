# AI Product Canvas — template

Điền Canvas cho product AI của nhóm. Mỗi ô có câu hỏi guide — trả lời trực tiếp, xóa phần in nghiêng khi điền.

---

## Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi guide** | User nào? Pain gì? AI giải quyết gì mà cách hiện tại không giải được? | Khi AI sai thì user bị ảnh hưởng thế nào? User biết AI sai bằng cách nào? User sửa bằng cách nào? | Cost bao nhiêu/request? Latency bao lâu? Risk chính là gì? |
| **Trả lời** | **User**: Người dùng Việt Nam (học sinh, sinh viên, người dùng thông thường) muốn hỏi câu hỏi đơn giản, cần trả lời nhanh, rõ ràng kiểu **Có/Không**.<br><br>**Ví dụ pain**:<br>• User hỏi: “Hải Dương có biển không?” → Mong đợi trả lời ngắn: “Không” (vì Hải Dương là tỉnh đất liền hoàn toàn).<br>• User yêu cầu: “Đào sâu thêm nhưng trả lời ngắn gọn, không giải thích dài”.<br><br>**Pain hiện tại**: V-AI vẫn trả lời dài dòng, loằng ngoằng, đưa thông tin thừa dù user đã yêu cầu ngắn gọn.<br><br>**Giải pháp của V-AI**: Hiểu ý định user (ngắn gọn / Có-Không), trả lời đúng trọng tâm trước, chỉ mở rộng khi user chủ động yêu cầu. | **Khi AI sai (trả lời dài dòng)**:<br>• User bị ảnh hưởng: Mất thời gian đọc, không nắm được thông tin chính nhanh chóng, trải nghiệm kém, dễ bỏ qua chatbot.<br><br>**User biết AI sai**: So sánh với kiến thức cá nhân hoặc câu trả lời mong đợi (ví dụ: rõ ràng là “Không” nhưng AI giải thích dài).<br>**User sửa**: Like/Dislike + comment feedback (“Quá dài”, “Trả lời ngắn thôi”), hoặc dùng lệnh nhanh như “/ngắn”. | **Cost**: Thấp (~0.2–0.8 cent/request nếu không search nhiều). Tăng nhẹ khi cần search real-time.<br>**Latency**: 1–3 giây.<br>**Risk chính**: <br>• Tốn token và chi phí nếu user spam hỏi lặp lại.<br>• AI không tuân thủ instruction “ngắn gọn” → giảm lòng tin người dùng. |

---

## Automation hay augmentation?

**☑ Augmentation** — AI hỗ trợ trả lời, nhưng vẫn cần user dẫn dắt và feedback để cải thiện độ ngắn gọn & chính xác.

**Gợi ý cải thiện**:
- Chỉnh **system prompt** mạnh: “Luôn ưu tiên trả lời ngắn gọn, đúng trọng tâm theo yêu cầu của user. Nếu user hỏi Có/Không hoặc yêu cầu ngắn gọn → chỉ trả lời 1–2 câu tối đa, không giải thích thêm trừ khi user yêu cầu rõ ràng.”
- Hỗ trợ lệnh nhanh: `/ngắn`, `/chi tiết`, `/có_không`.
- Cho phép user chỉnh sửa trực tiếp câu trả lời hoặc vote dislike + lý do.

---

## Learning signal

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | User correction đi vào đâu? | Like/Dislike + comment tự do (“Quá dài”, “Cần ngắn hơn”, “Trả lời sai trọng tâm”) → lưu vào dataset để refine prompt hoặc fine-tune. |
| 2 | Product thu signal gì để biết tốt lên hay tệ đi? | Binary like/dislike + qualitative feedback + tỷ lệ follow-up (user có hỏi thêm không) + thời gian đọc trả lời (nếu dài quá thì user bỏ qua nhanh). |
| 3 | Data thuộc loại nào? | ✓ Domain-specific (cách trả lời ngắn gọn, hiểu ý định user) · ✓ Real-time · ✓ Human-judgment · ☐ User-specific |

**Có marginal value không?**  
Có. Model lớn thường hay “giải thích dài” theo bản năng, ít dữ liệu chất lượng cao về việc **tuân thủ nghiêm ngặt yêu cầu ngắn gọn** của người dùng Việt. Dữ liệu feedback từ user thực tế sẽ giúp V-AI khác biệt rõ rệt ở khả năng kiểm soát độ dài và độ chính xác theo ý người dùng.

---

## Cách dùng

1. Điền Value trước — chưa rõ pain thì chưa điền Trust/Feasibility  
2. Trust: trả lời 4 câu UX (đúng → sai → không chắc → user sửa)  
3. Feasibility: ước lượng cost theo order of magnitude  
4. Learning signal: nghĩ về vòng lặp dài hạn (prompt engineering + fine-tuning)  
5. Đánh [?] cho chỗ chưa biết — Canvas là hypothesis, không phải đáp án

---

*AI Product Canvas — Ngày 5 — VinUni A20 — AI Thực Chiến · 2026*