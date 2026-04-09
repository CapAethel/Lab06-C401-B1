# Individual reflection — Chu Bá Tuấn Anh 2A202600012

## 1. Role

* UX Designer chính của sản phẩm
* Thiết kế toàn bộ user flow bằng mermaid
* Tham gia xây dựng system prompt cho AI Agent
* Debug flow cuối và align logic giữa các agent
* Cầu nối giữa phần business logic và trải nghiệm người dùng

## 2. Đóng góp cụ thể

* Thiết kế end-to-end flow: từ đọc log → đánh giá tình trạng → đề xuất bảo trì
* Chuẩn hóa các trạng thái xe: NORMAL / LOW / MEDIUM / CRITICAL
* Xây dựng luồng decision rõ ràng cho từng mức độ rủi ro
* Thiết kế flow tìm workshop theo constraint: khoảng cách, thời gian
* Đề xuất flow đặt lịch bảo trì tối giản bước nhưng vẫn đủ thông tin
* Viết và refine system prompt để agent phản hồi nhất quán
* Thiết kế fallback flow khi AI không chắc chắn
* Review và chỉnh sửa mermaid diagram để đảm bảo readable & scalable
* Debug logic chaining giữa các bước: phân tích → đề xuất → booking
* Đồng bộ wording UX với tone “trợ lý chăm sóc xe”

## 3. SPEC mạnh/yếu

**Mạnh:**

* Flow rõ ràng, có phân nhánh theo mức độ rủi ro
* UX logic bám sát use case thực tế của tài xế
* System prompt có cấu trúc tốt → dễ scale agent
* Có xử lý fallback và low-confidence scenario
* Tính nhất quán giữa các bước (diagnose → action)

**Yếu:**

* Chưa validate với dữ liệu log thực tế từ xe
* Một số flow còn linear, chưa tối ưu dynamic decision
* Chưa mô hình hóa đầy đủ hành vi user bất thường

## 4. Đóng góp khác

* Hỗ trợ team define AI Product Canvas
* Góp ý về cách chia agent role (diagnosis / planning / booking)
* Review nội dung và wording của các phần tài liệu
* Đề xuất cách tổ chức tài liệu để dễ đọc và trình bày

## 5. Điều học được

* Cách thiết kế UX cho AI Agent khác với app truyền thống
* Tầm quan trọng của system prompt trong việc định hình behavior
* Cách chuyển từ business requirement → conversational flow
* Hiểu rõ hơn về multi-step reasoning và tool chaining
* Nhận ra UX cần bao gồm cả “khi AI sai” chứ không chỉ “khi AI đúng”
* Cách thiết kế fallback và recovery flow hiệu quả
* Làm việc với mermaid giúp visualize logic nhanh và rõ

## 6. Nếu làm lại

* Bắt đầu từ real data (log xe) thay vì giả định
* Thiết kế metric ngay từ đầu để đo UX effectiveness
* Tách rõ hơn các agent và contract giữa chúng
* Làm prototype hội thoại sớm để test với user
* Đầu tư nhiều hơn vào workshop recommendation logic
* Chuẩn hóa system prompt theo template chặt chẽ hơn
* Giảm complexity ở một số flow để tăng tốc độ phản hồi

## 7. AI giúp gì / AI sai gì

**AI giúp:**

* Generate nhanh các version của system prompt
* Gợi ý flow và edge case mà mình chưa nghĩ tới
* Hỗ trợ viết và refine tài liệu
* Tăng tốc quá trình ideation và iteration
* Hỗ trợ debug logic ở mức high-level

**AI sai / hạn chế:**

* Đôi khi suy luận không sát với thực tế vận hành xe
* Gợi ý flow quá “lý tưởng”, thiếu constraint thực tế
* Không hiểu rõ context nếu prompt chưa đủ chặt
* Có lúc tạo ra logic mâu thuẫn giữa các bước
* Cần nhiều vòng refine để đạt chất lượng mong muốn
