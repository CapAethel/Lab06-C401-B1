# 🚀 VFCare Agent - Quick Start Guide

## Khởi động nhanh

### 1️⃣ Demo Mode (3 giây - Xem kết quả luôn)

```bash
cd /Users/huyenchu/Vinuni/day06/VFCare
python3 ui/cli_interface.py --mode demo
```

**Kết quả**: Hệ thống sẽ:
- 📊 Phân tích tình trạng xe VF Lạc Hồng
- 🔍 Phát hiện 6 vấn đề (4 medium, 2 low)
- 💡 Đưa ra gợi ý bảo dưỡng
- 🔧 Đề xuất 3 xưởng gần nhất
- 📝 Tự động đặt lịch và lưu feedback

---

### 2️⃣ Interactive Mode (Tương tác)

```bash
cd /Users/huyenchu/Vinuni/day06/VFCare
python3 ui/cli_interface.py --mode interactive
```

**Tính năng**:
```
1. Confirm booking (Xác nhận đặt lịch)
2. Change workshop (Đổi xưởng)
3. Change time (Đổi giờ)
4. Decline maintenance (Từ chối)
0. Exit (Thoát)
```

---

### 3️⃣ Run Agent Directly

```bash
cd /Users/huyenchu/Vinuni/day06/VFCare
python3 agent.py
```

---

## 📁 File Structure

```
VFCare/
├── 📋 README.md                   ← You are here
├── 🚀 agent.py                    ← Main agent
├── 📁 data/                       ← Mock data
│   ├── vehicle_status.json        ← Xe VF Lạc Hồng
│   ├── maintenance_rules.json     ← Rules phát hiện lỗi  
│   ├── workshops.json             ← 4 xưởng bảo dưỡng
│   └── user_feedback.json         ← Lịch sử booking ✅
├── 🛠️  tools/                      ← Core modules
│   ├── issue_detector.py          ← Phát hiện vấn đề
│   ├── priority_calculator.py     ← Tính priority
│   ├── recommendation_engine.py   ← Gợi ý hành động
│   ├── workshop_suggester.py      ← Đề xuất xưởng
│   ├── feedback_manager.py        ← Quản lý feedback
│   └── utils.py                   ← Tiện ích
└── 💻 ui/
    └── cli_interface.py           ← CLI (demo + interactive)
```

---

## 🎯 Use Cases

### Use Case 1: View Vehicle Status Only
```python
from agent import VFCareAgent

agent = VFCareAgent(data_dir='data')
analysis = agent.analyze_vehicle_status()

print(f"Status: {analysis['status']['overall_priority']}")
print(f"Risk Score: {analysis['status']['risk_score']}/100")
print(f"Issues: {analysis['issue_summary']['total_issues']}")
```

### Use Case 2: Get Recommendations
```python
recommendations = agent.get_recommendations()

print(f"Urgency: {recommendations['urgency']}")
print(f"Message: {recommendations['message']}")
for step in recommendations['required_action']:
    print(f"  → {step}")
```

### Use Case 3: Suggest Workshops
```python
workshops = agent.suggest_workshops()

for ws in workshops[:2]:
    print(f"{ws['name']} ({ws['distance_km']} km)")
    for slot in ws['available_slots'][:2]:
        print(f"  {slot['date_display']} {slot['time']}")
```

### Use Case 4: Book Maintenance
```python
result = agent.book_maintenance(
    workshop_id='WS_001',
    date='2026-04-09',
    time='10:00-11:00'
)

if result['success']:
    print(f"✅ Booking confirmed: {result['booking']['booking_id']}")
```

---

## 📊 Data Overview

### Current Vehicle Status
- **Vehicle**: VF Lạc Hồng (VF 8)
- **Mileage**: 45,230 km
- **Battery Health**: 88%
- **Issues Found**: 6 (4 medium, 2 low)

### Detected Issues
| Component | Issue | Priority | Risk | Action |
|-----------|-------|----------|------|--------|
| Brake | Pads worn | Medium | 65 | Replace |
| Brake Fluid | Low | Medium | 55 | Top up |
| Tire | Tread low | Medium | 60 | Replace |
| Air Filter | Dirty | Medium | 45 | Replace |
| Tire | Pressure low | Low | 25 | Inflate |
| Brake System | Overdue maintenance | Low | 30 | Check |

### Available Workshops
| Workshop | Distance | Rating | Slots | 
|----------|----------|--------|-------|
| Hoàng Mai | 3.2 km | 4.8/5 | 3+ |
| Ba Đình | 8.5 km | 4.6/5 | 3+ |
| Cầu Giấy | 12.3 km | 4.7/5 | 2+ |
| Tây Hồ | 15.7 km | 4.5/5 | 2+ |

---

## 🔍 Problem Diagnosis Rules

### Critical Issues 🔴
- Air Filter efficiency < 50%
- Brake pad thickness < 2.5mm (front) or 3.0mm (rear)

### Medium Issues 🟠  
- Brake pads: < 4.0mm (front) or < 4.5mm (rear)
- Brake fluid: < 80%
- Tire tread: < 5.0-5.5mm
- Air filter: < 70% efficiency
- Battery temp: > 45°C
- Motor efficiency: < 90%
- Overdue maintenance: > 10,000 km since last service

### Low Issues 🟡
- Tire pressure: < recommended psi
- Battery health: < 80%

---

## 💾 Feedback Storage

All user feedback is saved in `data/user_feedback.json`:

```json
{
  "vehicle_id": "VF_LAC_HONG_001",
  "feedbacks": [
    {
      "id": "FB_20260409105245_002",
      "type": "agree",
      "timestamp": "2026-04-09T10:52:45.243317",
      "details": {
        "workshop_id": "WS_001",
        "workshop_name": "VFCare Hà Nội - Hoàng Mai",
        "appointment_date": "2026-04-09",
        "appointment_time": "10:00-11:00",
        "status": "confirmed"
      }
    }
  ]
}
```

---

## 🎬 Flow Diagram

```
┌─────────────────────┐
│  Start Agent        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────┐
│  1. Analyze Vehicle Status      │
│  - Read vehicle_status.json     │
│  - Load maintenance_rules       │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  2. Detect Issues               │
│  - Critical: 0                  │
│  - Medium: 4                    │
│  - Low: 2                       │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  3. Calculate Priority          │
│  - Vehicle Status: MEDIUM       │
│  - Risk Score: 16.8/100         │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  4. Generate Recommendations    │
│  - Urgency: SOON (3-5 days)     │
│  - Action: Schedule maintenance │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  5. Suggest Workshops           │
│  - Hoàng Mai (3.2 km)  ← Best   │
│  - Ba Đình (8.5 km)            │
│  - Cầu Giấy (12.3 km)          │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  6. Display Available Slots     │
│  - Today: 10:00, 15:00, 16:00   │
│  - Tomorrow: 08:00, 09:00, etc. │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  7. User Choose Action          │
│  □ Confirm                      │
│  □ Change Workshop              │
│  □ Change Time                  │
│  □ Decline                      │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  8. Save Feedback               │
│  → user_feedback.json           │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  ✅ Complete                    │
└─────────────────────────────────┘
```

---

## 🆘 Troubleshooting

### Error: "python not found"
```bash
# Use python3 instead
python3 ui/cli_interface.py --mode demo
```

### Error: "FileNotFoundError: data/"
```bash
# Make sure you're in the VFCare directory
cd /Users/huyenchu/Vinuni/day06/VFCare
```

### Want to Reset Feedback?
```bash
# Clear user_feedback.json
echo '{"vehicle_id": "VF_LAC_HONG_001", "feedbacks": []}' > data/user_feedback.json
```

---

## 📚 Examples

### Example 1: Custom Vehicle Analysis
```python
from agent import VFCareAgent

agent = VFCareAgent()
analysis = agent.analyze_vehicle_status()

# Print detailed info
print(f"Vehicle: {analysis['vehicle_info']['vehicle_name']}")
for issue in analysis['detailed_issues']:
    print(f"  - {issue['recommendation']} (Priority: {issue['priority']})")
```

### Example 2: List All Available Workshops
```python
workshops = agent.suggest_workshops()

for ws in workshops:
    print(f"\n{ws['name']}")
    print(f"  Address: {ws['address']}")
    print(f"  Rating: {ws['rating']}/5")
    print(f"  Slots: {len(ws['available_slots'])} available")
```

### Example 3: Get Feedback History
```python
history = agent.get_feedback_history()

print(f"Total bookings: {history['bookings_confirmed']}")
if history['agree']:
    for booking in history['agree']:
        print(f"  - {booking['details']['workshop_name']}")
```

---

## 📞 Support

For issues or questions, check:
- `README.md` - Full documentation
- `data/` - Mock data files
- `tools/` - Implementation details
- Comments in source code

---

## ✨ Features Summary

✅ Vehicle status analysis
✅ Issue detection from rules
✅ Priority calculation (critical/medium/low)
✅ Risk scoring (0-100)
✅ Recommendation generation
✅ Workshop suggestion
✅ Time slot booking
✅ Feedback management
✅ Persistent storage (JSON)
✅ CLI interface (demo + interactive)
✅ End-to-end workflow

**Ready to use! 🚀**
