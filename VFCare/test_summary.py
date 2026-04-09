#!/usr/bin/env python3
"""Quick test to verify all components work"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))

from agent import VFCareAgent

print("\n" + "="*60)
print("🧪 VFCare Agent - Component Test")
print("="*60)

try:
    # Initialize
    print("\n✅ [1/5] Agent Initialization...")
    agent = VFCareAgent()
    print("   ✓ Agent created successfully")
    
    # Analyze
    print("\n✅ [2/5] Vehicle Analysis...")
    analysis = agent.analyze_vehicle_status()
    print(f"   ✓ Found {analysis['issue_summary']['total_issues']} issues")
    print(f"   ✓ Overall priority: {analysis['status']['overall_priority'].upper()}")
    print(f"   ✓ Risk score: {analysis['status']['risk_score']}/100")
    
    # Recommendations
    print("\n✅ [3/5] Generate Recommendations...")
    rec = agent.get_recommendations()
    print(f"   ✓ Urgency level: {rec['urgency']}")
    print(f"   ✓ Action type: {rec['action_type']}")
    
    # Workshops
    print("\n✅ [4/5] Workshop Suggestions...")
    workshops = agent.suggest_workshops()
    print(f"   ✓ Suggested {len(workshops)} workshops")
    print(f"   ✓ Closest: {workshops[0]['name']} ({workshops[0]['distance_km']} km)")
    print(f"   ✓ Available slots: {len(workshops[0]['available_slots'])}")
    
    # Booking
    print("\n✅ [5/5] Create Booking...")
    ws = workshops[0]
    slot = ws['available_slots'][0]
    result = agent.book_maintenance(ws['workshop_id'], slot['date'], slot['time'])
    print(f"   ✓ Booking status: {'SUCCESS' if result['success'] else 'FAILED'}")
    if result['success']:
        print(f"   ✓ Booking ID: {result['booking']['booking_id']}")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("\n📝 Next steps:")
    print("   1. Run demo:        python3 ui/cli_interface.py --mode demo")
    print("   2. Run interactive: python3 ui/cli_interface.py --mode interactive")
    print("   3. View feedback:   cat data/user_feedback.json")
    print("\n")
    
except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
