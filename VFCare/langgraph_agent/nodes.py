"""LangGraph nodes for VFCare Agent"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

from typing import Any
from langchain_core.messages import HumanMessage, SystemMessage
from state import VFCareGraphState, AgentState
from tools import VFCareTools
from llm_provider import get_llm, call_llm
from config import get_vfcare_config, get_threshold_config


class VFCareNodes:
    """Node functions for LangGraph"""
    
    @staticmethod
    def load_vehicle_node(state: VFCareGraphState) -> VFCareGraphState:
        """Load vehicle data"""
        print("[NODE] Loading vehicle...")
        
        config = get_vfcare_config()
        result = VFCareTools.load_vehicle_status(config.vehicle_id)
        
        if result["success"]:
            state.vehicle_data = result["data"]
            state.vehicle_id = config.vehicle_id
            state.add_message("system", f"Vehicle loaded: {result['message']}")
            state.current_step = AgentState.ANALYZE_VEHICLE
        else:
            state.error = result["message"]
            state.current_step = AgentState.END
        
        return state
    
    @staticmethod
    def analyze_vehicle_node(state: VFCareGraphState) -> VFCareGraphState:
        """Analyze vehicle using LLM"""
        print("[NODE] Analyzing vehicle with LLM...")
        
        llm = get_llm()
        
        # Prepare context
        vehicle_summary = f"""
Vehicle: {state.vehicle_data.get('vehicle_name', 'Unknown')}
Mileage: {state.vehicle_data.get('total_mileage_km', 0)} km
Battery Health: {state.vehicle_data.get('battery', {}).get('health_percent', 0)}%
Motor Efficiency: {state.vehicle_data.get('motor', {}).get('efficiency_percent', 0)}%
        """
        
        prompt = f"""You are a vehicle maintenance expert. Analyze this vehicle status and provide initial assessment:

{vehicle_summary}

Provide a brief analysis of the current state and what checks are needed. Be concise."""
        
        analysis = call_llm(llm, prompt)
        
        state.add_message("assistant", analysis)
        state.current_step = AgentState.DETECT_ISSUES
        
        return state
    
    @staticmethod
    def detect_issues_node(state: VFCareGraphState) -> VFCareGraphState:
        """Detect issues from rules"""
        print("[NODE] Detecting issues...")
        
        # Load rules
        rules_result = VFCareTools.load_maintenance_rules()
        if not rules_result["success"]:
            state.error = rules_result["message"]
            state.current_step = AgentState.END
            return state
        
        rules = rules_result["data"]
        
        # Detect issues
        issue_result = VFCareTools.detect_issues_from_log(state.vehicle_data, rules)
        if issue_result["success"]:
            state.detected_issues = issue_result["issues"]
            state.add_message("system", f"Issues detected: {issue_result['count']}")
            
            # Use LLM to summarize issues
            llm = get_llm()
            issues_text = "\n".join([
                f"- {i['recommendation']} (Priority: {i['priority']}, Risk: {i['base_risk_score']}/100)"
                for i in state.detected_issues
            ])
            
            prompt = f"""Summarize these vehicle issues and their urgency:

{issues_text}

Provide a professional summary focusing on the most critical items first."""
            
            summary = call_llm(llm, issues_text)
            state.add_message("assistant", f"Issue Summary:\n{summary}")
        else:
            state.error = issue_result["message"]
        
        state.current_step = AgentState.CALCULATE_PRIORITY
        return state
    
    @staticmethod
    def calculate_priority_node(state: VFCareGraphState) -> VFCareGraphState:
        """Calculate priority and risk score"""
        print("[NODE] Calculating priority...")
        
        priority_result = VFCareTools.calculate_priority(state.detected_issues)
        
        if priority_result["success"]:
            state.vehicle_priority = priority_result["priority"]
            state.risk_score = priority_result["risk_score"]
            
            state.add_message("system", priority_result["message"])
            
            # Use LLM to explain priority
            llm = get_llm()
            summary = priority_result["summary"]
            prompt = f"""Based on these vehicle issues, explain why the priority is "{state.vehicle_priority}":

Critical Issues: {len(summary.get('critical', []))}
Medium Issues: {len(summary.get('medium', []))}
Low Issues: {len(summary.get('low', []))}

Explain the reasoning briefly."""
            
            explanation = call_llm(llm, prompt)
            state.add_message("assistant", explanation)
        else:
            state.error = priority_result["message"]
        
        state.current_step = AgentState.GENERATE_RECOMMENDATIONS
        return state
    
    @staticmethod
    def generate_recommendations_node(state: VFCareGraphState) -> VFCareGraphState:
        """Generate recommendations"""
        print("[NODE] Generating recommendations...")
        
        rec_result = VFCareTools.generate_recommendations(
            state.detected_issues,
            state.vehicle_priority,
            state.risk_score
        )
        
        if rec_result["success"]:
            state.recommendations = rec_result["recommendations"]
            state.add_message("system", rec_result["message"])
            
            # Use LLM to enhance recommendations
            llm = get_llm()
            rec_data = state.recommendations
            prompt = f"""Based on this vehicle maintenance recommendation, provide actionable next steps:

Urgency: {rec_data.get('urgency')}
Message: {rec_data.get('message')}
Recommended Action: {rec_data.get('action_type')}
Estimated Duration: {rec_data.get('estimated_duration_hours')} hours

Provide 3-5 specific action items the vehicle owner should take. Be practical and direct."""
            
            action_items = call_llm(llm, prompt)
            state.add_message("assistant", f"Recommended Actions:\n{action_items}")
        else:
            state.error = rec_result["message"]
        
        state.current_step = AgentState.SUGGEST_WORKSHOPS
        return state
    
    @staticmethod
    def suggest_workshops_node(state: VFCareGraphState) -> VFCareGraphState:
        """Suggest suitable workshops"""
        print("[NODE] Suggesting workshops...")
        
        # Load workshops
        workshops_result = VFCareTools.load_workshops()
        if not workshops_result["success"]:
            state.error = workshops_result["message"]
            state.current_step = AgentState.END
            return state
        
        workshops = workshops_result["data"]
        
        # Extract required services
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
        
        # Suggest workshops
        suggest_result = VFCareTools.suggest_workshops(
            workshops,
            state.vehicle_priority,
            list(services) if services else None
        )
        
        if suggest_result["success"]:
            state.available_workshops = suggest_result["workshops"]
            state.add_message("system", suggest_result["message"])
            
            # Use LLM to rank workshops
            llm = get_llm()
            workshops_info = "\n".join([
                f"- {w['name']}: {w['distance_km']}km away, Rating: {w['rating']}/5"
                for w in state.available_workshops[:3]
            ])
            
            prompt = f"""Recommend the best workshop from these options for a {state.vehicle_priority.upper()} priority vehicle:

{workshops_info}

Explain which workshop is best and why (considering distance, rating, and urgency)."""
            
            recommendation = call_llm(llm, prompt)
            state.add_message("assistant", f"Workshop Recommendation:\n{recommendation}")
        else:
            state.error = suggest_result["message"]
        
        state.current_step = AgentState.HANDLE_USER_INPUT
        return state
    
    @staticmethod
    def handle_user_input_node(state: VFCareGraphState) -> VFCareGraphState:
        """Handle user input/action"""
        print("[NODE] Handling user input...")
        
        # For demo: auto-confirm first workshop if available
        if state.available_workshops:
            state.selected_workshop = state.available_workshops[0]
            if state.selected_workshop.get('available_slots'):
                state.selected_time_slot = state.selected_workshop['available_slots'][0]
                state.user_action = "book"
                
                llm = get_llm()
                ws_name = state.selected_workshop.get('name', 'Unknown Workshop')
                time_slot = state.selected_time_slot.get('date_display', '') + ' ' + state.selected_time_slot.get('time', '')
                
                prompt = f"Confirm this booking: {ws_name} at {time_slot}. Is this suitable?"
                confirmation = call_llm(llm, prompt)
                state.add_message("assistant", confirmation)
        
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
        
        from tools.feedback_manager import FeedbackManager
        from config import get_data_file_path
        
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
