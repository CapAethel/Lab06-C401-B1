# Individual reflection — Chu Thị Ngọc Huyền (2A202600015)

## 1. Role
Documentation: Xây dựng file roi-3-scenarios, slide trình chiếu và poster giới thiệu 
Prompt engineer: Thiết kế flow chatbot và review tool.

## 2. Đóng góp cụ thể
- Xây dựng file roi-3-scenarios, slide trình chiếu và poster giới thiệu 
- Viết và test 3 phiên bản system prompt, chọn v3 vì recall tốt nhất trên 10 test cases
- Thiết kế flow chatbot và review các tool.

## 3. SPEC mạnh/yếu
- **Mạnh nhất:** SPEC đã thu hẹp scope khá tốt cho bối cảnh hackathon. Nhóm không cố làm một hệ thống bảo dưỡng xe hoàn chỉnh mà chỉ tập trung vào 1 xe mẫu (VF Lạc Hồng), dùng dữ liệu log mock, rule đơn giản và luồng gợi ý lịch bảo dưỡng rõ ràng. Điều này giúp bài toán đủ cụ thể để demo end-to-end và dễ giải thích với người xem.
- **Mạnh tiếp theo:** Rule nghiệp vụ cho mức độ ưu tiên được định nghĩa rõ. Đặc biệt, case `critical` có hành vi rất cụ thể: chọn xưởng gần nhất và không bị chặn bởi trạng thái full slot. Đây là điểm giúp sản phẩm có logic thực tế hơn thay vì chỉ dừng ở mức “gợi ý chung chung”.
- **Yếu nhất:** Phần đánh giá `risk_score` hiện vẫn còn đơn giản, chủ yếu dựa vào rule tĩnh và mapping theo lỗi. Cách này phù hợp để demo nhưng chưa phản ánh đầy đủ độ phức tạp thật của bài toán bảo trì xe điện, nơi nhiều tín hiệu cần được kết hợp theo thời gian.
- **Yếu tiếp theo:** Dữ liệu đầu vào còn hẹp, mới dừng ở một số log mẫu và chưa có nhiều variation để test các tình huống biên. Nếu có thêm thời gian, nên mở rộng test case cho low/medium/critical và thêm các trường hợp thiếu dữ liệu hoặc lỗi mơ hồ.

## 4. Đóng góp khác
- Hoàn thiện phần narrative cho slide và poster để bài toán được trình bày dễ hiểu hơn với người nghe không chuyên sâu kỹ thuật.
- Hỗ trợ chuẩn hóa cách mô tả flow của agent VFCare theo hướng ngắn gọn: đọc log, đánh giá mức độ rủi ro, gợi ý xưởng, gợi ý slot và lưu feedback người dùng.
- Đề xuất cách hạ scope bài toán để phù hợp thời gian hackathon, từ một ý tưởng khá rộng xuống bản demo đủ chạy được với mock JSON.
- Rà soát lại wording của system prompt để output của agent bám nghiệp vụ hơn, tránh trả lời lan man hoặc đi xa khỏi dữ liệu đầu vào.

## 5. Điều học được
Qua bài này, em học rõ hơn rằng một bài toán AI tốt không chỉ nằm ở model hay prompt, mà nằm rất nhiều ở việc định nghĩa scope và rule nghiệp vụ đủ rõ. Khi scope mơ hồ, AI có thể nghe “thông minh” nhưng rất khó demo và khó đánh giá đúng sai.

Em cũng hiểu hơn vai trò của prompt trong sản phẩm. Prompt không chỉ để làm chatbot trả lời hay hơn, mà còn giúp giữ agent đi đúng vai trò, đúng giới hạn và đúng format mong muốn. Với bài toán VFCare, prompt tốt là prompt biết ưu tiên kết luận, hành động đề xuất và cảnh báo trường hợp critical thay vì diễn giải dài.

Ngoài ra, em nhận ra rằng phần trình bày sản phẩm rất quan trọng. Một flow kỹ thuật nếu không được diễn đạt đơn giản thì người nghe khó nắm được giá trị. Việc làm slide và poster giúp em luyện cách chuyển một bài toán kỹ thuật thành câu chuyện dễ hiểu, có logic và có điểm nhấn.

## 6. Nếu làm lại
Nếu làm lại, em sẽ chốt bộ test case sớm hơn ngay từ lúc viết SPEC, thay vì hoàn thiện phần mô tả trước rồi mới quay lại test prompt. Làm như vậy sẽ giúp prompt và rule được kiểm chứng sớm hơn, tránh việc đến gần cuối mới phát hiện các case chưa ổn.

Em cũng sẽ tách rõ hai chế độ demo ngay từ đầu: một case `critical` để thể hiện logic ưu tiên khẩn, và một case `medium` để thể hiện khả năng chọn slot phù hợp. Như vậy phần demo sẽ trực quan hơn và không bị lệ thuộc vào một bộ log duy nhất.

Cuối cùng, nếu có thêm thời gian, em sẽ đầu tư hơn vào phần đánh giá kết quả đầu ra theo checklist cụ thể, ví dụ: có xác định đúng priority không, có chọn đúng xưởng không, có trả về slot hợp lý không, có lưu feedback đúng không. Điều đó sẽ giúp phần demo chặt chẽ hơn và dễ thuyết phục hơn.

## 7. AI giúp gì / AI sai gì
- **Giúp:** dùng Claude để brainstorm failure modes — nó gợi ý được "drug interaction" mà nhóm không nghĩ ra. Dùng Gemini để test prompt nhanh qua AI Studio.
- **Sai/mislead:** Claude gợi ý thêm nhiều thông tin trong log sensor, nghe hay nhưng scope quá lớn cho hackathon. Suýt bị scope creep nếu không dừng lại.
  Bài học: AI brainstorm tốt nhưng không biết giới hạn scope.
