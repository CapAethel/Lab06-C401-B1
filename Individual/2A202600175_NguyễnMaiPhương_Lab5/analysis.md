# Product : Moni AI from MOMO
## Phân tích 4 path :
1. Khi AI đúng (High confidence)

- User thấy gì?

UI rất ít friction:

Suggestion rõ ràng: “Thanh toán điện tháng này – 350k”

CTA mạnh: “Thanh toán ngay”

Có thể auto-fill gần như toàn bộ thông tin

- Hệ thống confirm thế nào?

Implicit confirmation (ngầm):

Hiển thị summary trước khi execute (amount, người nhận)

Với giao dịch nhạy cảm:

Explicit confirm nhẹ (1 tap / FaceID)

- Nguyên tắc:

“Correct → phải nhanh hơn manual”

Không hỏi lại nếu confidence cao (tránh annoying)

2. Khi AI không chắc (Medium confidence)

- Hệ thống xử lý thế nào?

Có 3 chiến lược chính:

(1) Ask clarification (hỏi lại)

“Bạn muốn thanh toán điện hay nước?”

Dùng khi ambiguity cao

(2) Show alternatives (đưa lựa chọn)

“Bạn có muốn:

Điện EVN

Nước

Internet”

- Nguyên tắc:
Không đoán

Luôn giữ user trong control

AI là assistant, không phải decision maker

3.  Khi AI sai (Low confidence nhưng vẫn trả lời sai)

- User biết bằng cách nào?

So với expectation:

Sai người nhận

Sai số tiền

UI nên:

Highlight thông tin quan trọng

Cho user review trước khi confirm

- Sửa bằng cách nào?

Ví dụ:

“Sai người nhận?” → tap → chọn lại

“Sai số tiền?” → edit inline

- Nguyên tắc:

“Error recovery > Error prevention”

4. Khi user mất niềm tin (Trust breakdown)

Có exit không?

Có

“Nhập thủ công”

“Chuyển sang flow truyền thống”

Có fallback không?

Human support (CSKH)

FAQ / hướng dẫn
