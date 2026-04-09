"""State definition for VFCare LangGraph Agent"""
from typing import Any
from dataclasses import dataclass, field
from enum import Enum


class AgentState(str, Enum):
    """Agent states"""
    START = "start"
    LOAD_VEHICLE = "load_vehicle"
    ANALYZE_VEHICLE = "analyze_vehicle"
    DETECT_ISSUES = "detect_issues"
    CALCULATE_PRIORITY = "calculate_priority"
    GENERATE_RECOMMENDATIONS = "generate_recommendations"
    SUGGEST_WORKSHOPS = "suggest_workshops"
    HANDLE_USER_INPUT = "handle_user_input"
    BOOK_APPOINTMENT = "book_appointment"
    SAVE_FEEDBACK = "save_feedback"
    END = "end"


@dataclass
class VFCareGraphState:
    """LangGraph state for VFCare Agent"""
    
    # Vehicle data
    vehicle_id: str = ""
    vehicle_data: dict[str, Any] = field(default_factory=dict)
    
    # Analysis results
    detected_issues: list[dict[str, Any]] = field(default_factory=list)
    vehicle_priority: str = "low"  # critical, medium, low
    risk_score: float = 0.0
    
    # Recommendations
    recommendations: dict[str, Any] = field(default_factory=dict)
    
    # Workshops
    available_workshops: list[dict[str, Any]] = field(default_factory=list)
    selected_workshop: dict[str, Any] = field(default_factory=dict)
    selected_time_slot: dict[str, str] = field(default_factory=dict)
    
    # User input
    user_action: str = ""  # "book", "change_workshop", "change_time", "decline"
    user_feedback: dict[str, Any] = field(default_factory=dict)
    
    # Messages for LLM
    messages: list[dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    current_step: AgentState = AgentState.START
    error: str | None = None
    iteration: int = 0
    
    def add_message(self, role: str, content: str) -> None:
        """Add message to conversation"""
        self.messages.append({
            "role": role,  # "user", "assistant", "system"
            "content": content
        })
    
    def get_llm_messages(self) -> list[dict[str, str]]:
        """Get messages formatted for LLM"""
        return self.messages
    
    def format_for_llm(self) -> str:
        """Get state formatted for LLM context"""
        return f"""
Current Vehicle Analysis State:
- Vehicle: {self.vehicle_data.get('vehicle_name', 'Unknown')}
- Mileage: {self.vehicle_data.get('total_mileage_km', 0)} km
- Priority: {self.vehicle_priority}
- Risk Score: {self.risk_score}/100
- Issues Found: {len(self.detected_issues)}
- Current Step: {self.current_step.value}

Recent Issues:
{chr(10).join(f"- {issue.get('recommendation', '')} ({issue.get('priority', '')})" for issue in self.detected_issues[:5])}

Available Workshops:
{chr(10).join(f"- {ws.get('name', '')} ({ws.get('distance_km', 0)} km)" for ws in self.available_workshops[:3])}
"""
