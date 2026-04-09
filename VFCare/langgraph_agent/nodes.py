"""LangGraph nodes for VFCare Agent"""
from typing import Any
from .state import VFCareGraphState, AgentState
from .tools import VFCareTools
from .config import get_vfcare_config


class VFCareNodes:
    """Node functions for LangGraph"""

    @staticmethod
    def load_vehicle_node(state: VFCareGraphState) -> VFCareGraphState:
        """Load vehicle data using tool"""
        print("[NODE] Loading vehicle...")

        config = get_vfcare_config()
        result = VFCareTools.load_vehicle_status(config.vehicle_id)

        if result["success"]:
            state.vehicle_data = result["data"]
            state.vehicle_id = config.vehicle_id
            state.add_message("system", f"✓ Vehicle loaded: {result['message']}")
            state.current_step = AgentState.DETECT_ISSUES
        else:
            state.error = result["message"]
            state.current_step = AgentState.END

        return state

    @staticmethod
    def detect_issues_node(state: VFCareGraphState) -> VFCareGraphState:
        """Detect issues using tools"""
        print("[NODE] Detecting issues...")

        # Tool 1: Load maintenance rules
        rules_result = VFCareTools.load_maintenance_rules()
        if not rules_result["success"]:
            state.error = rules_result["message"]
            state.current_step = AgentState.END
            return state

        rules = rules_result["data"]
        state.add_message("system", rules_result["message"])

        # Tool 2: Detect issues from vehicle data + rules
        issue_result = VFCareTools.detect_issues_from_log(state.vehicle_data, rules)
        if issue_result["success"]:
            state.detected_issues = issue_result["issues"]
            state.add_message("system", f"✓ Issues detected: {issue_result['message']}")
        else:
            state.error = issue_result["message"]

        state.current_step = AgentState.CALCULATE_PRIORITY
        return state

    @staticmethod
    def confirm_to_proceed_node(state: VFCareGraphState) -> VFCareGraphState:
        """Show detected issues and ask user to confirm booking"""
        print("[NODE] Confirming with user...")

        if not state.detected_issues:
            print("\n✓ No issues detected. Vehicle is in good condition!")
            state.user_action = "no_issues"
            state.current_step = AgentState.END
            return state

        # Display detected issues
        print()
        print("=" * 60)
        print("🔍 DETECTED ISSUES")
        print("=" * 60)
        print(f"\n🚗 Vehicle: {state.vehicle_data.get('vehicle_name', 'Unknown')}")
        print(f"Total Issues Found: {len(state.detected_issues)}\n")

        # Group by priority
        critical = [i for i in state.detected_issues if i['priority'] == 'critical']
        medium = [i for i in state.detected_issues if i['priority'] == 'medium']
        low = [i for i in state.detected_issues if i['priority'] == 'low']

        if critical:
            print("🔴 CRITICAL Issues:")
            for issue in critical:
                print(f"   - {issue['recommendation']} (Risk: {issue['base_risk_score']}/100)")
            print()

        if medium:
            print("🟡 MEDIUM Issues:")
            for issue in medium:
                print(f"   - {issue['recommendation']} (Risk: {issue['base_risk_score']}/100)")
            print()

        if low:
            print("🟢 LOW Issues:")
            for issue in low:
                print(f"   - {issue['recommendation']} (Risk: {issue['base_risk_score']}/100)")
            print()

        # Ask user confirmation
        print("=" * 60)
        try:
            response = input(
                "Do you want to proceed with booking maintenance? (yes/no): "
            ).strip().lower()
        except (EOFError, KeyboardInterrupt):
            response = "yes"
            print("(Auto-confirming due to input unavailable)")

        if response in ['yes', 'y']:
            state.user_action = "proceed"
            state.add_message("user", "Confirmed to proceed with maintenance booking")
            print("✅ Proceeding with maintenance booking...\n")
            state.current_step = AgentState.CALCULATE_PRIORITY
        else:
            state.user_action = "decline"
            state.add_message("user", "Declined to proceed with maintenance booking")
            print("❌ Booking cancelled\n")
            state.current_step = AgentState.END

        return state

    @staticmethod
    def calculate_priority_node(state: VFCareGraphState) -> VFCareGraphState:
        """Calculate vehicle priority using tool"""
        print("[NODE] Calculating priority...")

        # Tool: Calculate priority and risk score
        priority_result = VFCareTools.calculate_priority(state.detected_issues)

        if priority_result["success"]:
            state.vehicle_priority = priority_result["priority"]
            state.risk_score = priority_result["risk_score"]
            state.add_message("system", f"✓ {priority_result['message']}")
        else:
            state.error = priority_result["message"]

        state.current_step = AgentState.GENERATE_RECOMMENDATIONS
        return state

    @staticmethod
    def generate_recommendations_node(state: VFCareGraphState) -> VFCareGraphState:
        """Generate recommendations using tool"""
        print("[NODE] Generating recommendations...")

        # Tool: Generate recommendations
        rec_result = VFCareTools.generate_recommendations(
            state.detected_issues,
            state.vehicle_priority,
            state.risk_score
        )

        if rec_result["success"]:
            state.recommendations = rec_result["recommendations"]
            state.add_message("system", f"✓ {rec_result['message']}")
        else:
            state.error = rec_result["message"]

        state.current_step = AgentState.SUGGEST_WORKSHOPS
        return state

    @staticmethod
    def suggest_workshops_node(state: VFCareGraphState) -> VFCareGraphState:
        """Suggest workshops using tools"""
        print("[NODE] Suggesting workshops...")

        # Tool 1: Load workshops
        workshops_result = VFCareTools.load_workshops()
        if not workshops_result["success"]:
            state.error = workshops_result["message"]
            state.current_step = AgentState.END
            return state

        workshops = workshops_result["data"]
        state.add_message("system", workshops_result["message"])

        # Tool 2: Suggest workshops based on priority and services
        services = set()
        service_map = {
            'brake_system': 'brake',
            'tire': 'tire',
            'air_filter': 'filter',
            'cabin_filter': 'filter',
            'battery': 'battery',
            'motor': 'motor'
        }
        for issue in state.detected_issues:
            component = issue['component']
            if component in service_map:
                services.add(service_map[component])

        suggest_result = VFCareTools.suggest_workshops(
            workshops,
            state.vehicle_priority,
            list(services) if services else None
        )

        if suggest_result["success"]:
            state.available_workshops = suggest_result["workshops"]
            state.add_message("system", f"✓ {suggest_result['message']}")
        else:
            state.error = suggest_result["message"]

        state.current_step = AgentState.HANDLE_USER_INPUT
        return state

    @staticmethod
    def handle_user_input_node(state: VFCareGraphState) -> VFCareGraphState:
        """Handle user input/action"""
        print("[NODE] Handling user input...")

        if state.available_workshops:
            state.selected_workshop = state.available_workshops[0]
            if state.selected_workshop.get('available_slots'):
                state.selected_time_slot = state.selected_workshop['available_slots'][0]

                # Display workshop and ask for confirmation
                ws_name = state.selected_workshop.get('name', 'Unknown Workshop')
                distance = state.selected_workshop.get('distance_km', 'N/A')
                rating = state.selected_workshop.get('rating', 'N/A')
                time_slot = state.selected_time_slot.get('date', '') + ' ' + state.selected_time_slot.get('time', '')

                print()
                print("=" * 60)
                print("📋 WORKSHOP SUGGESTION")
                print("=" * 60)
                print(f"\nRecommended Workshop: {ws_name}")
                print(f"Location: {distance}km away")
                print(f"Rating: {rating}/5")
                print(f"Available Time: {time_slot}")
                print()

                # Ask user confirmation with error handling
                try:
                    user_response = input("Do you want to book this workshop? (yes/no): ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    # If can't read input, auto-confirm
                    user_response = "yes"
                    print("(Auto-confirming due to input unavailable)")

                if user_response in ['yes', 'y']:
                    state.user_action = "book"
                    state.add_message("user", f"Confirmed booking at {ws_name} at {time_slot}")
                    print("✅ Booking confirmed!")
                else:
                    state.user_action = "decline"
                    state.add_message("user", "Declined the workshop booking suggestion")
                    print("❌ Booking declined")

        state.current_step = AgentState.BOOK_APPOINTMENT
        return state
    
    @staticmethod
    def book_appointment_node(state: VFCareGraphState) -> VFCareGraphState:
        """Book appointment"""
        print("[NODE] Booking appointment...")
        
        if state.user_action == "book" and state.selected_workshop and state.selected_time_slot:
            issues_to_fix = [issue['recommendation'] for issue in state.detected_issues]
            
            feedback = {
                'type': 'agree',
                'details': {
                    'workshop_id': state.selected_workshop['workshop_id'],
                    'workshop_name': state.selected_workshop['name'],
                    'appointment_date': state.selected_time_slot['date'],
                    'appointment_time': state.selected_time_slot['time'],
                    'issues_to_fix': issues_to_fix,
                    'status': 'confirmed'
                }
            }
            
            state.user_feedback = feedback
            state.add_message("system", "Appointment ready to be saved")
            state.current_step = AgentState.SAVE_FEEDBACK
        else:
            state.current_step = AgentState.SAVE_FEEDBACK
        
        return state
    
    @staticmethod
    def save_feedback_node(state: VFCareGraphState) -> VFCareGraphState:
        """Save feedback to JSON"""
        print("[NODE] Saving feedback...")

        import sys
        import os as os_module
        sys.path.insert(0, os_module.path.join(os_module.path.dirname(__file__), '..'))
        from tools.feedback_manager import FeedbackManager
        from .config import get_data_file_path
        
        if state.user_feedback:
            feedback_file = get_data_file_path("user_feedback.json")
            manager = FeedbackManager(feedback_file)
            
            # Create feedback with proper structure
            if not state.user_feedback.get('id'):
                state.user_feedback = manager.create_booking_feedback(
                    workshop_id=state.selected_workshop.get('workshop_id', ''),
                    workshop_name=state.selected_workshop.get('name', ''),
                    date=state.selected_time_slot.get('date', ''),
                    time=state.selected_time_slot.get('time', ''),
                    issues=[issue['recommendation'] for issue in state.detected_issues]
                )
            
            save_result = VFCareTools.save_user_feedback(state.user_feedback)
            if save_result["success"]:
                state.add_message("system", f"Feedback saved: {save_result['message']}")
            else:
                state.add_message("system", f"Warning: {save_result['message']}")
        
        state.current_step = AgentState.END
        return state
