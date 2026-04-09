"""LangGraph nodes for VFCare Agent"""
from typing import Any
from .state import VFCareGraphState, AgentState
from .tools import VFCareTools
from .config import get_vfcare_config
from .llm_provider import get_llm, call_llm
from .prompts import (
    get_system_prompt,
    create_analysis_prompt,
    create_workshop_prompt,
    create_issue_summary
)


class VFCareNodes:
    """Node functions for LangGraph"""

    @staticmethod
    def load_vehicle_node(state: VFCareGraphState) -> VFCareGraphState:
        """Load vehicle data using tool"""
        print("[NODE] Đang tải thông tin xe...")

        config = get_vfcare_config()
        result = VFCareTools.load_vehicle_status(config.vehicle_id)

        if result["success"]:
            state.vehicle_data = result["data"]
            state.vehicle_id = config.vehicle_id
            state.add_message("system", f"✓ Xe đã được tải: {result['message']}")
            state.current_step = AgentState.DETECT_ISSUES
        else:
            state.error = result["message"]
            state.current_step = AgentState.END

        return state

    @staticmethod
    def detect_issues_node(state: VFCareGraphState) -> VFCareGraphState:
        """Detect issues using tools"""
        print("[NODE] Đang phát hiện các vấn đề...")

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
            state.add_message("system", f"✓ Các vấn đề đã được phát hiện: {issue_result['message']}")
        else:
            state.error = issue_result["message"]

        state.current_step = AgentState.CALCULATE_PRIORITY
        return state

    @staticmethod
    def confirm_to_proceed_node(state: VFCareGraphState) -> VFCareGraphState:
        """Show detected issues and ask user to confirm booking using LLM"""
        print("[NODE] Confirming with user...")

        if not state.detected_issues:
            print("\n✓ Không phát hiện vấn đề nào. Chiếc xe của bạn đang ở tình trạng tốt!")
            state.user_action = "no_issues"
            state.current_step = AgentState.END
            return state

        # Prepare issues summary for LLM
        issues_text = create_issue_summary(state.detected_issues)

        # Use LLM to analyze and present issues with Vietnamese system prompt
        llm = get_llm()
        
        vehicle_name = state.vehicle_data.get('vehicle_name', 'Xe của bạn')
        mileage_km = state.vehicle_data.get('total_mileage_km', 0)
        
        prompt = create_analysis_prompt(vehicle_name, mileage_km, issues_text)
        
        # Create messages with system message
        from langchain_core.messages import SystemMessage, HumanMessage
        messages = [
            SystemMessage(content=get_system_prompt("analysis")),
            HumanMessage(content=prompt)
        ]
        
        analysis = call_llm(llm, messages)
        state.add_message("assistant", analysis)

        # Display LLM analysis
        print()
        print("=" * 60)
        print("🔍 PHÂN TÍCH TÌNH TRẠNG XE")
        print("=" * 60)
        print(f"\n{analysis}\n")
        print("=" * 60)

        # Ask user confirmation
        try:
            response = input(
                "Bạn có muốn tiếp tục với việc đặt lịch hẹn bảo dưỡng không? (có/không): "
            ).strip().lower()
        except (EOFError, KeyboardInterrupt):
            response = "có"
            print("(Tự động xác nhận do không có đầu vào)")

        if response in ['có', 'yeah', 'yes', 'y']:
            state.user_action = "proceed"
            state.add_message("user", "Có, tôi muốn tiếp tục với việc đặt lịch hẹn bảo dưỡng")
            print("✅ Đang tiến hành đặt lịch hẹn...\n")
            state.current_step = AgentState.CALCULATE_PRIORITY
        else:
            state.user_action = "decline"
            state.add_message("user", "Không, tôi từ chối đặt lịch hẹn bảo dưỡng")
            print("❌ Đã hủy yêu cầu đặt lịch\n")
            state.current_step = AgentState.END

        return state

    @staticmethod
    def calculate_priority_node(state: VFCareGraphState) -> VFCareGraphState:
        """Calculate vehicle priority using tool"""
        print("[NODE] Đang tính toán mức độ ưu tiên...")

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
        print("[NODE] Đang tạo đề xuất bảo dưỡng...")

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
        print("[NODE] Đang gợi ý các xưởng bảo dưỡng...")

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
        """Handle user input/action with LLM assistance"""
        print("[NODE] Handling user input...")

        if state.available_workshops:
            state.selected_workshop = state.available_workshops[0]
            if state.selected_workshop.get('available_slots'):
                state.selected_time_slot = state.selected_workshop['available_slots'][0]

                # Display workshop and ask for confirmation
                ws_name = state.selected_workshop.get('name', 'Xưởng không xác định')
                distance = state.selected_workshop.get('distance_km', 'N/A')
                rating = state.selected_workshop.get('rating', 'N/A')
                time_slot = state.selected_time_slot.get('date', '') + ' ' + state.selected_time_slot.get('time', '')

                # Use LLM to present workshop option with Vietnamese system prompt
                issues_str = ", ".join([i['recommendation'] for i in state.detected_issues[:3]])
                llm = get_llm()
                
                prompt = create_workshop_prompt(ws_name, distance, rating, time_slot, issues_str)
                
                # Create messages with system message
                from langchain_core.messages import SystemMessage, HumanMessage
                messages = [
                    SystemMessage(content=get_system_prompt("workshop")),
                    HumanMessage(content=prompt)
                ]

                workshop_recommendation = call_llm(llm, messages)
                state.add_message("assistant", workshop_recommendation)

                print()
                print("=" * 60)
                print("📋 GỢI Ý XƯỞNG BẢO DƯỠNG")
                print("=" * 60)
                print(f"\n{workshop_recommendation}\n")
                print("=" * 60)

                # Ask user confirmation with error handling
                try:
                    user_response = input("Bạn có muốn đặt lịch hẹn tại xưởng này không? (có/không): ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    # If can't read input, auto-confirm
                    user_response = "có"
                    print("(Tự động xác nhận do không có đầu vào)")

                if user_response in ['có', 'yeah', 'yes', 'y']:
                    state.user_action = "book"
                    state.add_message("user", f"Xác nhận đặt lịch hẹn tại {ws_name} vào {time_slot}")
                    print("✅ Đã xác nhận đặt lịch hẹn!")
                else:
                    state.user_action = "decline"
                    state.add_message("user", "Từ chối gợi ý xưởng bảo dưỡng")
                    print("❌ Đã từ chối đặt lịch hẹn")

        state.current_step = AgentState.BOOK_APPOINTMENT
        return state
    
    @staticmethod
    def book_appointment_node(state: VFCareGraphState) -> VFCareGraphState:
        """Book appointment"""
        print("[NODE] Đang tiến hành đặt lịch hẹn...")
        
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
            state.add_message("system", "Lịch hẹn đã sẵn sàng để lưu")
            state.current_step = AgentState.SAVE_FEEDBACK
        else:
            state.current_step = AgentState.SAVE_FEEDBACK
        
        return state
    
    @staticmethod
    def save_feedback_node(state: VFCareGraphState) -> VFCareGraphState:
        """Save feedback to JSON"""
        print("[NODE] Đang lưu lại phản hồi...")

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
                state.add_message("system", f"Phản hồi đã được lưu: {save_result['message']}")
            else:
                state.add_message("system", f"Cảnh báo: {save_result['message']}")
        
        state.current_step = AgentState.END
        return state
