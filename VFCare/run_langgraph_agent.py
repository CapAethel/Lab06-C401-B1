#!/usr/bin/env python3
"""
VFCare LangGraph Agent - Entry point script
Run: python3 run_langgraph_agent.py
"""

import sys
import os

# Add the current directory to Python path so langgraph_agent is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    try:
        from langgraph_agent.agent import VFCareGraphAgent
        
        # Create and run agent
        agent = VFCareGraphAgent()
        final_state = agent.run()
        
        print()
        print("=" * 60)
        print("📊 EXECUTION RESULTS")
        print("=" * 60)
        print()
        
        # Print results
        if final_state.vehicle_data:
            print(f"🚗 Vehicle: {final_state.vehicle_data.get('vehicle_name', 'Unknown')}")
            print(f"   Mileage: {final_state.vehicle_data.get('total_mileage_km', 0)} km")
            print(f"   Battery Health: {final_state.vehicle_data.get('battery', {}).get('health_percent', 0)}%")
            print()
        
        if final_state.detected_issues:
            print(f"📈 Issues Detected: {len(final_state.detected_issues)}")
            for issue in final_state.detected_issues[:5]:  # Show first 5
                print(f"   - {issue['recommendation']} (Priority: {issue['priority']})")
            if len(final_state.detected_issues) > 5:
                print(f"   ... and {len(final_state.detected_issues) - 5} more")
            print()
        
        if final_state.vehicle_priority:
            print(f"📊 Analysis:")
            print(f"   Priority: {final_state.vehicle_priority}")
            print(f"   Risk Score: {final_state.risk_score:.1f}/100")
            print()
        
        if final_state.recommendations:
            print(f"🎯 Recommendations:")
            rec = final_state.recommendations
            print(f"   Urgency: {rec.get('urgency', 'UNKNOWN')}")
            print(f"   Action: {rec.get('action_type', 'UNKNOWN')}")
            print(f"   Duration: {rec.get('estimated_duration_hours', 0)} hours")
            print()
        
        if final_state.available_workshops:
            print(f"🏪 Available Workshops: {len(final_state.available_workshops)}")
            for workshop in final_state.available_workshops[:3]:
                print(f"   - {workshop['name']} (Rating: {workshop.get('rating', 'N/A')}/5)")
            print()
        
        # Print last few messages
        if final_state.messages:
            print(f"💬 Last Messages:")
            for msg in final_state.messages[-2:]:
                role = msg.get("role", "unknown").upper()
                content = msg.get("content", "")[:100]
                if len(msg.get("content", "")) > 100:
                    content += "..."
                print(f"   [{role}] {content}")
            print()
        
        print("✅ Demo completed successfully!")
        
    except ModuleNotFoundError as e:
        print(f"❌ Missing module: {e}")
        print("\nPlease install dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
