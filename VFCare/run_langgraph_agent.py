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
