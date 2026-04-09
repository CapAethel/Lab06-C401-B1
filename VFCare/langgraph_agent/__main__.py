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
        print("✅ Đặt lịch thành công thôi")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
