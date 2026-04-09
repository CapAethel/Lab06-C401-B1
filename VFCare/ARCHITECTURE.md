# VFCare Agent - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VFCare Agent System                      │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │         User Interface Layer (CLI)                │   │
│  │  ┌──────────────────┐    ┌──────────────────┐    │   │
│  │  │  Demo Mode       │    │ Interactive Mode │    │   │
│  │  │  (Automated)     │    │  (User Control)  │    │   │
│  │  └──────────────────┘    └──────────────────┘    │   │
│  └────────────────────────────────────────────────────┘   │
│                          ▲                                  │
│                          │                                  │
│  ┌────────────────────────────────────────────────────┐   │
│  │      Agent Orchestration Layer (agent.py)         │   │
│  │  - analyze_vehicle_status()                       │   │
│  │  - get_recommendations()                          │   │
│  │  - suggest_workshops()                            │   │
│  │  - book_maintenance()                             │   │
│  │  - change_workshop()                              │   │
│  │  - change_time()                                  │   │
│  │  - decline_maintenance()                          │   │
│  └────────────────────────────────────────────────────┘   │
│                          ▲                                  │
│         ┌────────────────┼────────────────┐               │
│         │                │                │               │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐       │
│  │   Issue     │  │  Priority   │  │Recommendation
│  │  Detector   │  │ Calculator  │  │   Engine    │       │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤       │
│  │ - Rules     │  │ - Level     │  │ - Critical  │       │
│  │ - Detect    │  │ - Hierarchy │  │ - Medium    │       │
│  │ - Issues    │  │ - Risk      │  │ - Low       │       │
│  │   (6 found) │  │   (16.8/100)│  │ - Steps     │       │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │
│         │                │                │               │
│         │       ┌────────▼───────┐       │               │
│         │       │ Workshop       │◄──────┘               │
│         │       │ Suggester      │                        │
│         │       ├────────────────┤                        │
│         │       │ - Suggest (4)  │                        │
│         │       │ - Sort by dist │                        │
│         │       │ - Show slots   │                        │
│         │       └────────┬───────┘                        │
│         │                │                                 │
│         └────────┬───────▼──────┬────────┐               │
│                  │              │        │               │
│           ┌──────▼──────┐ ┌─────▼────┐  │               │
│           │  Feedback   │ │ Utils    │  │               │
│           │  Manager    │ │ Module   │  │               │
│           ├─────────────┤ ├──────────┤  │               │
│           │ - Save      │ │ - JSON   │  │               │
│           │ - History   │ │- Parse   │  │               │
│           │ - Types (4) │ │ - Flatten│  │               │
│           └──────┬──────┘ └──────────┘  │               │
│                  │                       │               │
│                  ▼                       ▼               │
│         ┌────────────────────────────────────────┐      │
│         │        Data Storage Layer              │      │
│         │  vehicle_status.json                   │      │
│         │  maintenance_rules.json                │      │
│         │  workshops.json                        │      │
│         │  user_feedback.json ◄─ (updates)     │      │
│         └────────────────────────────────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

```
1. INITIALIZATION
   ↓
   Load: vehicle_status.json
         maintenance_rules.json
         workshops.json

2. ISSUE DETECTION
   Vehicle Status + Rules → Issue Detector
   ↓
   Detected Issues (6): critical=0, medium=4, low=2
   
3. PRIORITY CALCULATION
   Issues → Priority Calculator
   ↓
   Vehicle Priority: MEDIUM
   Risk Score: 16.8/100
   
4. RECOMMENDATION GENERATION
   Priority → Recommendation Engine
   ↓
   Action: schedule_maintenance
   Urgency: SOON (3-5 days)
   Steps: 1. Schedule bảo dưỡng
          2. Chọn xưởng phù hợp
          3. Lựa chọn slot thời gian
   
5. WORKSHOP SUGGESTION
   Required Services + Priority → Workshop Suggester
   ↓
   Suggestions (sorted by distance):
   - WS_001: Hoàng Mai (3.2 km) - 4.8/5 ⭐
   - WS_002: Ba Đình (8.5 km) - 4.6/5 ⭐
   - WS_003: Cầu Giấy (12.3 km) - 4.7/5 ⭐
   
6. USER INTERACTION
   User selects: Workshop + Time Slot
   ↓
   4 Action Types:
   - Agree (confirm booking)
   - Change Workshop
   - Change Time
   - Decline

7. FEEDBACK STORAGE
   Action → Feedback Manager
   ↓
   Save to user_feedback.json with:
   - Unique ID
   - Timestamp
   - Details
   - Status
```

## Component Interaction

```
┌──────────────────┐
│   CLI Interface  │
│  cli_interface   │
│       .py        │
└────────┬─────────┘
         │ user_input
         ▼
┌──────────────────┐
│  VFCare Agent    │
│   agent.py       │
└────────┬─────────┘
         │
    ┌────┴────┬─────────┬──────────┬──────────┐
    │          │         │          │          │
    ▼          ▼         ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Issue  │ │Priority│ │Rec.    │ │Workshop│ │Feedback│
│Detector│ │Calc.   │ │Engine  │ │Suggst. │ │Manager │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘
    │          │         │          │          │
    └──────────┴─────────┴──────────┴──────────┘
                    │
                    └─ utils.py (shared)
                    
                    ▼
              ┌──────────────┐
              │ user_feedback│
              │   .json      │
              └──────────────┘
```

## State Transitions

```
                  USER RECEIVES RECOMMENDATION
                            │
                            ▼
                  ┌────────────────────┐
                  │ What will you do?  │
                  └────────────────────┘
                    │        │        │
          ┌─────────┘        │        └─────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │ 1.AGREE  │      │ 2.CHANGE │      │ 3.DECLINE│
    │ (Confirm)│      │ (Options)│      │ (Reject) │
    └────┬─────┘      └────┬─────┘      └────┬─────┘
         │                 │                  │
         │             ┌───┴───┐             │
         │             │       │             │
         │             ▼       ▼             │
         │        ┌────────┐ ┌─────────┐     │
         │        │Workshop│ │  Time   │     │
         │        │ Change │ │ Change  │     │
         │        └────────┘ └─────────┘     │
         │             │            │        │
         └─────────┬───┴─── ────────┘        │
                   │                         │
                   ▼                         │
         ┌──────────────────┐               │
         │ SAVE FEEDBACK    │◄──────────────┘
         │ - type: agree    │
         │ - type: change   │
         │ - type: decline  │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │  COMPLETE ✅     │
         └──────────────────┘
```

## Module Dependencies

```
agent.py (main)
    │
    ├─→ IssueDetector
    │   └─→ utils.py
    │
    ├─→ PriorityCalculator
    │   └─→ (no dependencies)
    │
    ├─→ RecommendationEngine
    │   └─→ (no dependencies)
    │
    ├─→ WorkshopSuggester
    │   └─→ (no dependencies)
    │
    └─→ FeedbackManager
        └─→ utils.py

cli_interface.py
    │
    └─→ agent.py (all of above)
```

## Critical vs Medium vs Low vs Low Flow

```
Vehicle Status Analysis
        │
        ▼
Issue Detection (Check all rules)
        │
        ├─ Critical: 0 issues
        │   └─ IF >= 1: Mark vehicle CRITICAL 🔴
        │
        ├─ Medium: 4 issues
        │   └─ IF >= 1 AND no critical: Mark vehicle MEDIUM 🟠
        │
        └─ Low: 2 issues
            └─ ELSE: Mark vehicle LOW 🟡

        │
        ▼
VEHICLE PRIORITY DETERMINED
        │
        ├─ CRITICAL → Emergency action
        │   ├─ Show ONLY closest workshop
        │   ├─ Force selection (full slot OK)
        │   └─ Urgent message
        │
        ├─ MEDIUM → Normal maintenance
        │   ├─ Show 3-4 workshops
        │   ├─ Flexible time selection
        │   └─ Schedule in 3-5 days
        │
        └─ LOW → Flexible
            ├─ Show all suitable workshops
            ├─ Very flexible time
            └─ Can defer 30 days
```

## Risk Score Calculation

```
For Each Issue:
    base_risk_score × priority_weight
    
Where priority_weight:
    - Critical: 1.0x
    - Medium: 0.67x
    - Low: 0.33x

Example Current Vehicle:
    Issue 1: 65 × 0.67 = 43.55
    Issue 2: 55 × 0.67 = 36.85
    Issue 3: 25 × 0.33 = 8.25
    Issue 4: 60 × 0.67 = 40.20
    Issue 5: 45 × 0.67 = 30.15
    Issue 6: 30 × 0.33 = 9.90
    ─────────────────────────────
    Total: 168.9
    
Normalize to 0-100:
    168.9 / 10 = 16.89 → 16.8/100 ✓
```

## File Read/Write Operations

```
INITIALIZATION PHASE:
    os.path ← Get script directory
        │
        ├─ Read: vehicle_status.json
        ├─ Read: maintenance_rules.json
        ├─ Read: workshops.json
        └─ Read: user_feedback.json (existing)

OPERATION PHASE:
    Analysis runs in memory (no disk I/O)

USER INTERACTION PHASE:
    User chooses action
        │
        ├─ IF agree/change/decline:
        │  └─ Write: user_feedback.json (append)
        │
        └─ Done

QUERY PHASE:
    Agent can read user_feedback.json anytime
    to generate history reports
```

## JSON Data Schema

```
vehicle_status.json
├─ vehicle_id: string
├─ vehicle_name: string
├─ total_mileage_km: integer
├─ battery: { level_percent, health_percent, ... }
├─ brake_system: { status, front_pad_thickness_mm, ... }
├─ tire: { status, pressure_psi, tread_mm, ... }
└─ air_filter: { efficiency_percent, ... }

maintenance_rules.json
├─ rules: [
  {
    rule_id: string,
    component: string,
    condition: string (evaluable),
    priority: "critical|medium|low",
    base_risk_score: number (0-100),
    recommendation: string,
    action: string,
    required_hours: number
  },
  ...
]

workshops.json
├─ workshops: [
  {
    workshop_id: string,
    name: string,
    distance_km: number,
    capabilities: [string],
    rating: number (0-5),
    available_slots: [
      {
        date: string (YYYY-MM-DD),
        time_slots: [
          { time: string, available: boolean }
        ]
      }
    ]
  },
  ...
]

user_feedback.json
├─ vehicle_id: string
└─ feedbacks: [
  {
    id: string (FB_YYYYMMDDhhmmss_nnn),
    type: "agree|change_workshop|change_time|decline",
    timestamp: string (ISO format),
    details: {
      ... (varies by type)
    }
  },
  ...
]
```

---

This visualization helps understand how all components work together in the VFCare Agent system.
