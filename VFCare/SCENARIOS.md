# 🧪 VFCare Agent - Example Scenarios & Test Cases

## Scenario 1: View Current Vehicle Status

### Command
```bash
python3 agent.py
```

### Expected Output
```
1. VỀ XE: VF Lạc Hồng
   - Mileage: 45,230 km
   - Battery Health: 88%
   - Overall Priority: MEDIUM
   - Risk Score: 16.8/100

2. PHÁT HIỆN VẤN ĐỀ:
   - Critical: 0
   - Medium: 4
   - Low: 2
     ⚠  Thay má phanh trước và sau
     ⚠  Kiểm tra và bổ sung dầu phanh
     ⚠  Thay lốp xe
     ⚠  Thay lọc không khí

3. GỢI Ý HÀNH ĐỘNG:
   - Urgency: SOON
   - Message: Nên kiểm tra sớm: Có một số vấn đề cần được giải quyết trong thời gian gần

4. ĐỀ XUẤT XƯỞNG:
   - VFCare Hà Nội - Hoàng Mai (3.2 km, 4.8/5)
   - VFCare Hà Nội - Ba Đình (8.5 km, 4.6/5)
   - VFCare Hà Nội - Cầu Giấy (12.3 km, 4.7/5)
```

---

## Scenario 2: Demo Mode (Auto-Booking)

### Command
```bash
python3 ui/cli_interface.py --mode demo
```

### What Happens
1. ✅ Analyzes vehicle status
2. ✅ Shows all detected issues
3. ✅ Displays recommendations
4. ✅ Lists available workshops
5. ✅ Auto-books first workshop (Hoàng Mai, 10:00-11:00)
6. ✅ Shows booking confirmation with ID
7. ✅ Displays feedback history

### Output Sample
```
============================================================
  🚗 VFCare Agent - Demo Mode
============================================================

⏳ Analyzing vehicle status...

📋 TÌNH TRẠNG XE
------------------------------------------------------------

🚗 VF Lạc Hồng (VF 8)
   ID: VF_LAC_HONG_001
   Mileage: 45,230 km
   Battery Health: 88%

🟠 OVERALL STATUS: MEDIUM
   Risk Score: 16.8/100
   Immediate Action Needed: NO

[... More details ...]

🎬 DEMO: Auto-booking first workshop...
✅ Lịch bảo dưỡng đã được xác nhận

📦 BOOKING DETAILS:
   Workshop: VFCare Hà Nội - Hoàng Mai
   Address: 123 Lạc Long Quân, Hoàng Mai, Hà Nội
   Phone: 024-3865-2500
   Date: 2026-04-09
   Time: 10:00-11:00
   Booking Id: FB_20260409105245_002

📋 FEEDBACK HISTORY
------------------------------------------------------------
Total Feedbacks: 2
Confirmed Bookings: 2
Declined: 0

============================================================
✅ Demo completed!
```

---

## Scenario 3: Interactive Mode - Confirm Booking

### Command
```bash
python3 ui/cli_interface.py --mode interactive
```

### User Interaction
```
📌 YOUR ACTION:
   1. Confirm booking
   2. Change workshop
   3. Change time
   4. Decline maintenance
   0. Exit

   Enter choice: 1

💼 SELECT WORKSHOP:
   1. VFCare Hà Nội - Hoàng Mai (3.2 km away)
   2. VFCare Hà Nội - Ba Đình (8.5 km away)
   3. VFCare Hà Nội - Cầu Giấy (12.3 km away)
   4. VFCare Hà Nội - Tây Hồ (15.7 km away)

   Enter choice (1-4, or 0 to skip): 1

⏰ SELECT TIME SLOT for VFCare Hà Nội - Hoàng Mai:
   1. Thu, 09/04/2026 10:00-11:00
   2. Thu, 09/04/2026 15:00-16:00
   3. Thu, 09/04/2026 16:00-17:00

   Enter choice (1-3): 1

✅ Lịch bảo dưỡng đã được xác nhận

📦 BOOKING DETAILS:
   Workshop: VFCare Hà Nội - Hoàng Mai
   Address: 123 Lạc Long Quân, Hoàng Mai, Hà Nội
   Phone: 024-3865-2500
   Date: 2026-04-09
   Time: 10:00-11:00
   Booking Id: FB_20260409105245_003
```

**Result**: Booking saved to `data/user_feedback.json` with type="agree"

---

## Scenario 4: Interactive Mode - Change Workshop

### User Interaction
```
📌 YOUR ACTION:
   1. Confirm booking
   2. Change workshop
   3. Change time
   4. Decline maintenance
   0. Exit

   Enter choice: 2

💼 SELECT WORKSHOP:
   1. VFCare Hà Nội - Hoàng Mai (3.2 km away)
   2. VFCare Hà Nội - Ba Đình (8.5 km away)
   3. VFCare Hà Nội - Cầu Giấy (12.3 km away)
   4. VFCare Hà Nội - Tây Hồ (15.7 km away)

   Enter choice (1-4, or 0 to skip): 3

   Reason for change: Gần nhà hơn

✅ Đã đổi xưởng
   New workshop: VFCare Hà Nội - Cầu Giấy
```

**Result**: Change feedback saved with type="change_workshop"

---

## Scenario 5: Interactive Mode - Change Time

### User Interaction
```
📌 YOUR ACTION:
   ...
   Enter choice: 3

💼 SELECT WORKSHOP:
   1. VFCare Hà Nội - Hoàng Mai (3.2 km away)
   ...

   Enter choice (1-4, or 0 to skip): 1

⏰ SELECT TIME SLOT for VFCare Hà Nội - Hoàng Mai:
   1. Thu, 09/04/2026 10:00-11:00
   2. Thu, 09/04/2026 15:00-16:00
   3. Thu, 09/04/2026 16:00-17:00

   Enter choice (1-3): 3

✅ Đã cập nhật thời gian
   New: 2026-04-09 16:00-17:00
```

**Result**: Time change feedback saved with type="change_time"

---

## Scenario 6: Interactive Mode - Decline

### User Interaction
```
📌 YOUR ACTION:
   ...
   Enter choice: 4

   Reason for declining: Sẽ xem xét sau tuần sau

✅ Bạn đã từ chối gợi ý bảo dưỡng
   reason: Sẽ xem xét sau tuần sau
```

**Result**: Decline feedback saved with type="decline"

---

## Scenario 7: Programmatic Usage - Get Issues Only

### Code
```python
from agent import VFCareAgent

agent = VFCareAgent()
analysis = agent.analyze_vehicle_status()

# Get critical issues only
critical_issues = analysis['issue_summary']['critical']
print(f"Critical issues: {len(critical_issues)}")
for issue in critical_issues:
    print(f"  - {issue['recommendation']}")

# Get risk score
risk = analysis['status']['risk_score']
print(f"Overall risk: {risk}/100")
```

### Expected Output
```
Critical issues: 0
Overall risk: 16.8/100
```

---

## Scenario 8: Programmatic Usage - Get Recommendations

### Code
```python
from agent import VFCareAgent

agent = VFCareAgent()
agent.analyze_vehicle_status()
rec = agent.get_recommendations()

print(f"Priority: {rec['priority']}")
print(f"Urgency: {rec['urgency']}")
print(f"Message: {rec['message']}")
print(f"\nSteps:")
for step in rec['required_action']:
    print(f"  {step}")
```

### Expected Output
```
Priority: medium
Urgency: SOON
Message: Nên kiểm tra sớm: Có một số vấn đề cần được giải quyết trong thời gian gần

Steps:
  1. Lên lịch bảo dưỡng trong 3-5 ngày tới
  2. Chọn xưởng có thể xử lý các vấn đề cần thiết
  3. Lựa chọn slot thời gian phù hợp với lịch của bạn
```

---

## Scenario 9: Programmatic Usage - Get Workshops

### Code
```python
from agent import VFCareAgent

agent = VFCareAgent()
agent.analyze_vehicle_status()
workshops = agent.suggest_workshops()

for ws in workshops[:2]:
    print(f"{ws['name']}")
    print(f"  Distance: {ws['distance_km']} km")
    print(f"  Rating: {ws['rating']}/5")
    print(f"  Available slots: {len(ws['available_slots'])}")
```

### Expected Output
```
VFCare Hà Nội - Hoàng Mai
  Distance: 3.2 km
  Rating: 4.8/5
  Available slots: 3

VFCare Hà Nội - Ba Đình
  Distance: 8.5 km
  Rating: 4.6/5
  Available slots: 3
```

---

## Scenario 10: Check Feedback History

### Code
```python
from agent import VFCareAgent

agent = VFCareAgent()
history = agent.get_feedback_history()

print(f"Total feedbacks: {history['total_feedbacks']}")
print(f"Bookings confirmed: {history['bookings_confirmed']}")
print(f"Declined: {history['bookings_declined']}")

# Show latest confirmed booking
if history['agree']:
    latest = history['agree'][-1]
    print(f"\nLatest booking:")
    print(f"  Workshop: {latest['details']['workshop_name']}")
    print(f"  Date: {latest['details']['appointment_date']}")
    print(f"  Time: {latest['details']['appointment_time']}")
```

### Expected Output (after demo run)
```
Total feedbacks: 2
Bookings confirmed: 2
Declined: 0

Latest booking:
  Workshop: VFCare Hà Nội - Hoàng Mai
  Date: 2026-04-09
  Time: 10:00-11:00
```

---

## Scenario 11: Custom Issue Simulation

### Code to Test Different Scenarios

#### Test Case A: No Issues
```python
# Modify vehicle_status.json to set all normal values
# Then run:
agent = VFCareAgent()
analysis = agent.analyze_vehicle_status()
print(f"Priority: {analysis['status']['overall_priority']}")  # Should be 'low'
print(f"Risk: {analysis['status']['risk_score']}")  # Should be 0.0
```

#### Test Case B: Multiple Critical Issues
```python
# Modify vehicle_status.json to trigger multiple critical rules:
# - air_filter.efficiency_percent = 40 (< 50)
# - brake_system.front_pad_thickness_mm = 2.0 (< 2.5)
# Then run:
agent = VFCareAgent()
analysis = agent.analyze_vehicle_status()
print(f"Priority: {analysis['status']['overall_priority']}")  # Should be 'critical'
print(f"Risk: {analysis['status']['risk_score']}")  # Should be high (>75)
```

---

## Test Matrix

| Scenario | Command | Expected Priority | Risk Score | Bookings |
|----------|---------|-------------------|-----------|----------|
| Default (Current) | `python3 agent.py` | MEDIUM | 16.8/100 | 0 |
| Demo Mode | `--mode demo` | MEDIUM | 16.8/100 | 1 |
| Interactive - Book | Interactive → 1 | MEDIUM | 16.8/100 | +1 |
| Interactive - Decline | Interactive → 4 | MEDIUM | 16.8/100 | 0 |

---

## Data Files Reference

### Current State After Demo

**vehicle_status.json**: Unchanged (same as initial)

**workshops.json**: Unchanged (same available slots)

**user_feedback.json**: After demo run
```json
{
  "vehicle_id": "VF_LAC_HONG_001",
  "feedbacks": [
    {
      "id": "FB_20260409105230_001",
      "type": "agree",
      "timestamp": "2026-04-09T10:52:30.927968",
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

## Key Takeaways

✅ **Vehicle Status**: Fixed at 45,230 km, MEDIUM priority, 6 issues found
✅ **Workflow**: Analyze → Detect Issues → Calculate Priority → Recommend → Book
✅ **Flexibility**: Supports multiple user choices via interactive mode
✅ **Storage**: All feedback persisted in user_feedback.json
✅ **Extensibility**: Easy to modify vehicle data to test different scenarios

