# VFCare Agent - Hệ thống gợi ý bảo dưỡng xe ô tô điện thông minh

## 📋 Tổng quan

VFCare Agent là một hệ thống AI tự động phân tích tình trạng xe VF Lạc Hồng và đưa ra gợi ý bảo dưỡng/bảo trì phù hợp. Hệ thống sử dụng dữ liệu mock từ các file JSON local, không cần database thực.

## 🎯 Tính năng chính

### 1. **Phân tích trạng thái xe** 📊
- Đọc log trạng thái các component (pin, motor, hệ thống phanh, lốp, lọc, v.v.)
- So sánh với các rules bảo dưỡng định sẵn
- Phát hiện các vấn đề hiện tại

### 2. **Xác định mức độ ưu tiên** 🎚️
- **Critical (🔴)**: Nguy hiểm, cần xử lý ngay
- **Medium (🟠)**: Nên kiểm tra sớm  
- **Low (🟡)**: Theo dõi hoặc đặt lịch linh hoạt
- Tính risk_score từ 0 đến 100

### 3. **Sinh gợi ý hành động** 💡
- **Critical**: Liên hệ xưởng gần nhất để xử lý khẩn cấp
- **Medium**: Đề xuất xưởng phù hợp và các slot giờ trống
- **Low**: Hướng dẫn theo dõi, bảo dưỡng định kỳ

### 4. **Đề xuất xưởng bảo dưỡng** 🔧
- Lựa chọn xưởng gần nhất và thích hợp
- Hiển thị các slot thời gian trống
- Ưu tiên xưởng có đủ điều kiện xử lý các vấn đề

### 5. **Quản lý phản hồi người dùng** 📝
- Ghi nhận các lựa chọn: đồng ý, đổi xưởng, đổi giờ, từ chối
- Lưu lịch sử phản hồi vào file JSON
- Theo dõi lịch sử bảo dưỡng

## 📁 Cấu trúc dự án

```
VFCare/
├── data/                          # Dữ liệu mock
│   ├── vehicle_status.json        # Trạng thái hiện tại xe VF Lạc Hồng
│   ├── maintenance_rules.json     # Rules phát hiện lỗi
│   ├── workshops.json             # Danh sách xưởng bảo dưỡng
│   └── user_feedback.json         # Lịch sử phản hồi người dùng
├── tools/                         # Core modules
│   ├── utils.py                   # Hàm tiện ích
│   ├── issue_detector.py          # Phát hiện vấn đề từ log
│   ├── priority_calculator.py     # Tính mức độ ưu tiên
│   ├── recommendation_engine.py   # Sinh gợi ý hành động
│   ├── workshop_suggester.py      # Đề xuất xưởng
│   └── feedback_manager.py        # Quản lý phản hồi
├── ui/                            # Giao diện người dùng
│   └── cli_interface.py           # CLI interface (demo + interactive)
└── agent.py                       # Main agent orchestrator
```

## 🚀 Cách sử dụng

### 1. **Demo Mode (Không tương tác)**
```bash
cd /Users/huyenchu/Vinuni/day06/VFCare
python3 ui/cli_interface.py --mode demo
```

Demo sẽ:
- 📊 Phân tích tình trạng xe
- 💡 Hiển thị gợi ý hành động
- 🔧 Đề xuất xưởng bảo dưỡng
- 📝 Tự động đặt lịch (booking đầu tiên)
- 📋 Hiển thị lịch sử phản hồi

### 2. **Interactive Mode (Tương tác)**
```bash
cd /Users/huyenchu/Vinuni/day06/VFCare
python3 ui/cli_interface.py --mode interactive
```

Chế độ tương tác cho phép:
- ✅ Xác nhận lịch bảo dưỡng
- 🔧 Đổi xưởng
- ⏰ Đổi thời gian
- ❌ Từ chối gợi ý

### 3. **Chạy Agent trực tiếp**
```bash
cd /Users/huyenchu/Vinuni/day06/VFCare
python3 agent.py
```

## 📊 Quy luật xác định mức độ ưu tiên của toàn xe

| Điều kiện | Mức độ ưu tiên |
|-----------|---|
| Có ≥1 issue **critical** | **CRITICAL** 🔴 |
| Không có critical, nhưng có ≥1 issue **medium** | **MEDIUM** 🟠 |
| Chỉ có **low** hoặc không có issue | **LOW** 🟡 |

## 🎛️ Các loại issue được phát hiện

### Critical Issues 🔴
- **Air Filter Critical**: Hiệu suất < 50%
- **Brake Pads Critical**: Độ dày < 2.5-3.0mm

### Medium Issues 🟠
- **Brake Pads Worn**: Độ dày < 4.0-4.5mm
- **Brake Fluid Low**: Mức dưới 80%
- **Tire Tread Low**: Độ sâu lốp < 5.0-5.5mm
- **Air Filter Dirty**: Hiệu suất < 70%
- **Battery Temperature High**: Trên 45°C
- **Motor Efficiency Low**: < 90%
- **Brake System Overdue**: Quá 10,000 km kể từ bảo dưỡng cuối

### Low Issues 🟡
- **Tire Pressure Low**: Áp suất thấp hơn mức chuẩn
- **Battery Health Degraded**: Sức khỏe < 80%
- **Maintenance Overdue**: Hơn 10,000 km

## 📈 Risk Score Calculation

Risk Score được tính trên thang điểm 0-100:
- Mỗi issue có base risk score
- Áp dụng trọng số dựa trên priority:
  - Critical: 1.0x
  - Medium: 0.67x
  - Low: 0.33x
- Tổng hợp từ tất cả issues, normalize thành 0-100

### Ví dụ:
- Nếu có 1 issue critical (85 points) → Risk Score ≈ 85/100
- Nếu có 3 issue medium (65, 60, 55) → Risk Score ≈ 47/100
- Nếu không có issue → Risk Score = 0

## 🔧 Đề xuất xưởng

### Cho lỗi CRITICAL 🔴
- Chỉ đề xuất xưởng gần nhất (có khả năng xử lý khẩn cấp)
- Hiển thị 2 slot trống gần nhất
- Ưu tiên slot trong cùng ngày nếu có

### Cho lỗi MEDIUM/LOW 🟠🟡
- Đề xuất 3-4 xưởng gần nhất thích hợp
- Sắp xếp theo: khoảng cách → rating
- Hiển thị 3 slot trống soonest
- Cho phép người dùng chọn xưởng và giờ

## 📝 Quản lý Feedback

Hệ thống lưu lại các loại feedback:

### 1. **Agree (Đồng ý)** ✅
```json
{
  "type": "agree",
  "details": {
    "workshop_id": "WS_001",
    "appointment_date": "2026-04-09",
    "appointment_time": "10:00-11:00",
    "issues_to_fix": [...],
    "status": "confirmed"
  }
}
```

### 2. **Change Workshop (Đổi xưởng)** 🔧
```json
{
  "type": "change_workshop",
  "details": {
    "new_workshop_id": "WS_002",
    "reason": "Gần nhà hơn"
  }
}
```

### 3. **Change Time (Đổi giờ)** ⏰
```json
{
  "type": "change_time",
  "details": {
    "new_appointment_date": "2026-04-10",
    "new_appointment_time": "14:00-15:00",
    "reason": "Rảnh giờ này"
  }
}
```

### 4. **Decline (Từ chối)** ❌
```json
{
  "type": "decline",
  "details": {
    "reason": "Sẽ kiểm tra sau"
  }
}
```

Tất cả feedback được lưu vào `data/user_feedback.json` với timestamp.

## 🔄 Workflow End-to-End

```
1. INITIALIZE AGENT
   ↓
2. ANALYZE VEHICLE STATUS
   - Đọc vehicle_status.json
   - Phát hiện issues từ rules
   ↓
3. CALCULATE PRIORITY & RISK
   - Xác định priority từng issue
   - Tính overall priority của xe
   - Tính risk_score
   ↓
4. GENERATE RECOMMENDATIONS
   - Tạo gợi ý hành động dựa trên priority
   ↓
5. SUGGEST WORKSHOPS
   - Đề xuất xưởng phù hợp
   - Lấy available slots
   ↓
6. USER INTERACTION
   - Người dùng chọn xưởng/giờ hoặc từ chối
   ↓
7. SAVE FEEDBACK & BOOKING
   - Lưu phản hồi vào user_feedback.json
   - Cập nhật lịch sử
   ↓
8. COMPLETE
```

## 📊 Ví dụ dữ liệu

### Vehicle Status (vehicle_status.json)
```json
{
  "vehicle_id": "VF_LAC_HONG_001",
  "vehicle_name": "VF Lạc Hồng",
  "model": "VF 8",
  "total_mileage_km": 45230,
  "battery": { "level_percent": 42, "health_percent": 88, ... },
  "brake_system": { "front_pad_thickness_mm": 3.2, ... },
  "tire": { "front_left_pressure_psi": 31.5, ... },
  ...
}
```

### Maintenance Rules (maintenance_rules.json)
```json
{
  "rules": [
    {
      "rule_id": "BR_001",
      "component": "brake_system",
      "issue_type": "brake_pads_worn",
      "condition": "front_pad_thickness_mm < 4.0 OR rear_pad_thickness_mm < 4.5",
      "priority": "medium",
      "base_risk_score": 65,
      "recommendation": "Thay má phanh trước và sau"
    },
    ...
  ]
}
```

### Workshops (workshops.json)
```json
{
  "workshops": [
    {
      "workshop_id": "WS_001",
      "name": "VFCare Hà Nội - Hoàng Mai",
      "address": "123 Lạc Long Quân, Hoàng Mai",
      "distance_km": 3.2,
      "capabilities": ["battery", "motor", "brake", "tire", "filter"],
      "available_slots": [
        {
          "date": "2026-04-09",
          "time_slots": [
            { "time": "10:00-11:00", "available": true },
            ...
          ]
        }
      ]
    }
  ]
}
```

## 🧪 Test Results

### Demo Run Output
```
1. VỀ XE: VF Lạc Hồng
   - Overall Priority: MEDIUM
   - Risk Score: 16.8/100

2. PHÁT HIỆN VẤN ĐỀ:
   - Critical: 0
   - Medium: 4 (brake pads, brake fluid, tire tread, air filter)
   - Low: 2 (tire pressure, maintenance overdue)

3. ĐỀ XUẤT XƯỞNG:
   - VFCare Hà Nội - Hoàng Mai (3.2 km, 4.8/5)
   - Available slots today: 10:00, 15:00, 16:00

4. BOOKING CONFIRMATION:
   ✅ Lịch bảo dưỡng đã được xác nhận
   ID: FB_20260409105245_002
```

## 🛠️ Các module chính

### `issue_detector.py`
- **Chức năng**: Phát hiện issues từ vehicle status
- **Phương thức chính**:
  - `detect_all_issues()`: Phát hiện tất cả issues
  - `get_critical_issues()`: Lấy critical issues
  - `get_issues_by_priority()`: Lọc theo priority

### `priority_calculator.py`
- **Chức năng**: Tính priority và risk score
- **Phương thức chính**:
  - `calculate_overall_priority()`: Xác định priority của xe
  - `calculate_risk_score()`: Tính risk score 0-100
  - `get_issue_summary()`: Tóm tắt issues theo priority

### `recommendation_engine.py`
- **Chức năng**: Sinh gợi ý hành động
- **Phương thức chính**:
  - `generate_recommendations()`: Tạo recommendations dựa trên priority
  - `get_issue_summary_text()`: Tóm tắt text của issues

### `workshop_suggester.py`
- **Chức năng**: Đề xuất xưởng thích hợp
- **Phương thức chính**:
  - `suggest_workshops()`: Đề xuất danh sách xưởng
  - `_get_available_slots()`: Lấy available slots
  - `_calculate_priority_rank()`: Tính priority rank

### `feedback_manager.py`
- **Chức năng**: Quản lý phản hồi người dùng
- **Phương thức chính**:
  - `save_feedback()`: Lưu feedback
  - `create_booking_feedback()`: Tạo booking feedback
  - `get_feedback_summary()`: Tóm tắt feedback

### `agent.py`
- **Chức năng**: Orchestrator chính
- **Phương thức chính**:
  - `analyze_vehicle_status()`: Phân tích tình trạng
  - `get_recommendations()`: Lấy gợi ý
  - `suggest_workshops()`: Đề xuất xưởng
  - `book_maintenance()`: Đặt lịch bảo dưỡng

## 💻 Yêu cầu hệ thống

- Python 3.7+
- Không cần cài đặt thêm thư viện (sử dụng built-in modules)

## 📝 Ghi chú

- Tất cả dữ liệu là mock, không kết nối database thực
- Timestamp trong feedback sử dụng ISO format
- Risk Score được normalize thành 0-100
- Xưởng được sắp xếp theo khoảng cách và rating
- Feedback được lưu dưới dạng JSON append-only

## 🔮 Tương lai mở rộng

Có thể mở rộng thêm:
- Kết nối real database
- Gửi thông báo qua email/SMS
- Tích hợp thanh toán online
- AI/ML để dự đoán maintenance trước
- Mobile app
- Real-time monitoring
- Integrations với VF cloud

