# Prototype README - VFCare

## 1) Mô tả prototype
VFCare là trợ lý AI hỗ trợ chủ xe VinFast chẩn đoán lỗi và gợi ý lịch bảo dưỡng theo mức độ ưu tiên (`critical`/`medium`/`low`).  
Prototype đã có AI call thật thông qua OpenAI function calling, cho phép mô phỏng đầy đủ flow: chẩn đoán -> gợi ý lịch -> kiểm tra slot -> đặt lịch.  
Hệ thống có thêm nhánh giải thích khuyến nghị (explainability) và ước tính chi phí để hỗ trợ người dùng ra quyết định.

## 2) Level prototype
**Working prototype (Bonus++)**

Lý do:
- Có AI xử lý hội thoại và tự quyết định tool call theo ngữ cảnh.
- Có logic nghiệp vụ được code thật (không chỉ mock giao diện).
- Có thể demo live trên Terminal hoặc Web UI (Streamlit).

## 3) Links
- Source code prototype: `VFCare/`
- Agent core: `VFCare/agent.py`
- Tool logic: `VFCare/tools.py`
- Web demo (Streamlit): `VFCare/app.py`
- Terminal demo: `VFCare/main.py`
- Flow tổng quan: `VFCare/FLOW.md`
- Sơ đồ flow: `VFCare/flow.mermaid`

## 4) Tools và API đã dùng

### Nền tảng/thư viện
- Python 3.10+
- `openai` (LLM + function calling)
- `streamlit` (Web demo UI)

### AI model
- Mặc định: `gpt-4o-mini` (có thể đổi bằng biến môi trường `OPENAI_MODEL`)

### Tool functions trong prototype
1. `get_user_info`
2. `get_vehicle_info`
3. `run_diagnostic`
4. `recommend_schedule`
5. `check_slot_availability`
6. `book_appointment`
7. `cancel_or_postpone`
8. `get_explainability`
9. `estimate_maintenance_cost`

## 5) Phân công


| Thành viên | Phần phụ trách | Output chính |
|-----------|----------------|--------------|
| Nguyễn Mai Phương | Code prototype | Mã nguồn prototype trong `VFCare/` |
| Chu Thị Ngọc Huyền | Code prototype mock | Phần mock prototype trong `VFCare/` |
| Chu Bá Tuấn Anh | Debug, UX, sketch | Các cập nhật debug, UX và sketch flow |
| Hứa Quang Linh | Feedback, slide thuyết trình | Nội dung feedback và demo slides |
| Nguyễn Văn Lĩnh | Spec final | Tài liệu `spec-final.md` |
| Nguyễn Thị Tuyết | Hoàn thiện tài liệu prototype | `prototype-readme.md` |

## 6) Cách chạy nhanh

```bash
cd VFCare
pip install -r requirements.txt
set OPENAI_API_KEY=sk-your-key
set OPENAI_MODEL=gpt-4o-mini
python main.py
```

Chạy web UI:

```bash
cd VFCare
streamlit run app.py
```

## 7) Giá trị demo và hạn chế hiện tại

### Giá trị demo
- Có thể trình bày được luồng nghiệp vụ AI rõ ràng (diagnostic -> scheduling -> booking).
- Có fallback và explainability để tăng độ tin cậy khi demo.
- Có nhiều case để test nhanh trên một bộ dữ liệu mock.

### Hạn chế hiện tại
- Dữ liệu đang là mock data (chưa kết nối backend/DB thật).
- Chưa tích hợp auth, logging và quản lý trạng thái booking đa người dùng.
- Chưa có test tự động cho các tool function.
