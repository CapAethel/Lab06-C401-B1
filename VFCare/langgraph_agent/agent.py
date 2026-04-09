"""Main LangGraph Agent for VFCare"""
from langgraph.graph import StateGraph, END
from .state import VFCareGraphState, AgentState
from .nodes import VFCareNodes


class VFCareGraphAgent:
    """VFCare LangGraph Agent"""
    
    def __init__(self):
        """Initialize the graph"""
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        graph = StateGraph(VFCareGraphState)

        # Add nodes
        graph.add_node("load_vehicle", VFCareNodes.load_vehicle_node)
        graph.add_node("detect_issues", VFCareNodes.detect_issues_node)
        graph.add_node("confirm_to_proceed", VFCareNodes.confirm_to_proceed_node)
        graph.add_node("calculate_priority", VFCareNodes.calculate_priority_node)
        graph.add_node("generate_recommendations", VFCareNodes.generate_recommendations_node)
        graph.add_node("suggest_workshops", VFCareNodes.suggest_workshops_node)
        graph.add_node("handle_user_input", VFCareNodes.handle_user_input_node)
        graph.add_node("book_appointment", VFCareNodes.book_appointment_node)
        graph.add_node("save_feedback", VFCareNodes.save_feedback_node)

        # Define edges
        graph.add_edge("load_vehicle", "detect_issues")
        graph.add_edge("detect_issues", "confirm_to_proceed")

        # Conditional edge after confirm_to_proceed: route based on user decision
        def route_after_confirm(state):
            return "proceed" if state.user_action == "proceed" else "decline"

        graph.add_conditional_edges(
            "confirm_to_proceed",
            route_after_confirm,
            {
                "proceed": "calculate_priority",
                "decline": END
            }
        )

        # Continue with main flow
        graph.add_edge("calculate_priority", "generate_recommendations")
        graph.add_edge("generate_recommendations", "suggest_workshops")
        graph.add_edge("suggest_workshops", "handle_user_input")
        graph.add_edge("handle_user_input", "book_appointment")
        graph.add_edge("book_appointment", "save_feedback")
        graph.add_edge("save_feedback", END)

        # Set entry point
        graph.set_entry_point("load_vehicle")

        return graph.compile()
    
    def run(self) -> VFCareGraphState:
        """Run the agent"""
        print("\n" + "="*60)
        print("🚗 VFCare LangGraph Agent - Running Demo")
        print("="*60 + "\n")

        # Initialize state
        initial_state = VFCareGraphState()

        # Run graph
        final_state = self.graph.invoke(initial_state)

        # Convert dict to VFCareGraphState if needed
        if isinstance(final_state, dict):
            state_obj = VFCareGraphState()
            for key, value in final_state.items():
                if hasattr(state_obj, key):
                    setattr(state_obj, key, value)
            final_state = state_obj

        # Print results
        self._print_results(final_state)

        return final_state
    
    def _print_results(self, state: VFCareGraphState) -> None:
        """Print execution results"""
        print("\n" + "="*60)
        print("📊 EXECUTION RESULTS")
        print("="*60)
        
        if state.error:
            print(f"\n❌ Error: {state.error}")
            return
        
        # Print vehicle info
        print(f"\n🚗 Vehicle: {state.vehicle_data.get('vehicle_name', 'Unknown')}")
        print(f"   Mileage: {state.vehicle_data.get('total_mileage_km', 0)} km")
        print(f"   Battery Health: {state.vehicle_data.get('battery', {}).get('health_percent', 0)}%")
        
        # Print analysis results
        print(f"\n📈 Analysis:")
        print(f"   Priority: {state.vehicle_priority.upper()}")
        print(f"   Risk Score: {state.risk_score}/100")
        print(f"   Issues Found: {len(state.detected_issues)}")
        
        # Print issues
        if state.detected_issues:
            print(f"\n🔍 Issues:")
            for issue in state.detected_issues[:5]:
                print(f"   - {issue['recommendation']} ({issue['priority']}, {issue['base_risk_score']}/100)")
        
        # Print recommendations
        if state.recommendations:
            print(f"\n💡 Recommendations:")
            print(f"   Urgency: {state.recommendations.get('urgency', 'N/A')}")
            print(f"   Message: {state.recommendations.get('message', 'N/A')}")
        
        # Print workshops
        if state.available_workshops:
            print(f"\n🔧 Available Workshops:")
            for ws in state.available_workshops[:3]:
                print(f"   - {ws['name']} ({ws['distance_km']} km, {ws['rating']}/5)")
        
        # Print booking
        if state.selected_workshop and state.user_feedback.get('id'):
            print(f"\n✅ Booking:")
            print(f"   Workshop: {state.selected_workshop.get('name', 'N/A')}")
            print(f"   Date: {state.selected_time_slot.get('date', 'N/A')}")
            print(f"   Time: {state.selected_time_slot.get('time', 'N/A')}")
            print(f"   Booking ID: {state.user_feedback.get('id', 'N/A')}")
        elif state.user_action == "decline":
            print(f"\n❌ Booking Declined")
            print(f"   User did not confirm the workshop suggestion")
        
        # Print LLM conversation
        print(f"\n💬 LLM Conversation:")
        print("   " + "-"*56)
        for msg in state.messages[-6:]:  # Show last 6 messages
            role = msg['role'].upper()
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            print(f"   [{role}] {content}")
        print("   " + "-"*56)
        
        print("\n" + "="*60)
        print("✅ Demo completed!")
        print("="*60 + "\n")


if __name__ == "__main__":
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Run agent
    agent = VFCareGraphAgent()
    agent.run()
