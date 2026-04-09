"""Entry point for running LangGraph agent as a module"""

if __name__ == "__main__":
    from .agent import VFCareGraphAgent
    from .state import VFCareGraphState
    
    print("=" * 60)
    print("🚗 VFCare LangGraph Agent - Running Demo")
    print("=" * 60)
    print()
    
    try:
        # Create and run agent
        agent = VFCareGraphAgent()
        initial_state = VFCareGraphState()
        final_state = agent.run(initial_state)
        
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
            for issue in final_state.detected_issues:
                print(f"   - {issue['recommendation']} (Priority: {issue['priority']})")
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
        
        if final_state.workshops:
            print(f"🏪 Available Workshops: {len(final_state.workshops)}")
            for workshop in final_state.workshops[:3]:  # Show first 3
                print(f"   - {workshop['name']} (Rating: {workshop.get('rating', 'N/A')})")
            print()
        
        # Print conversation history
        if final_state.messages:
            print(f"💬 Conversation History ({len(final_state.messages)} messages):")
            for msg in final_state.messages[-3:]:  # Show last 3 messages
                role = msg.get("role", "unknown").upper()
                content = msg.get("content", "")[:80]
                print(f"   [{role}] {content}...")
            print()
        
        print("✅ Demo completed!")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
