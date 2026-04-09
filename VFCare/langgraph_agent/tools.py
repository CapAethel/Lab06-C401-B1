"""Tool definitions for LangGraph Agent"""
from typing import Any
import json
import os
from datetime import datetime

# Try to import from parent tools package with fallback
try:
    from tools.utils import load_json, save_json
except ImportError:
    # Fallback: add parent to path and try again
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from tools.utils import load_json, save_json

from .config import get_data_file_path


class VFCareTools:
    """Tools available to LangGraph Agent"""
    
    @staticmethod
    def load_vehicle_status(vehicle_id: str) -> dict[str, Any]:
        """Load vehicle status from JSON"""
        try:
            vehicle_file = get_data_file_path("vehicle_status.json")
            data = load_json(vehicle_file)
            return {
                "success": True,
                "data": data,
                "message": f"Loaded vehicle: {data.get('vehicle_name', 'Unknown')}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to load vehicle data: {e}"
            }
    
    @staticmethod
    def load_maintenance_rules() -> dict[str, Any]:
        """Load maintenance rules from JSON"""
        try:
            rules_file = get_data_file_path("maintenance_rules.json")
            data = load_json(rules_file)
            return {
                "success": True,
                "data": data.get("rules", []),
                "count": len(data.get("rules", [])),
                "message": f"Loaded {len(data.get('rules', []))} maintenance rules"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to load rules: {e}"
            }
    
    @staticmethod
    def load_workshops() -> dict[str, Any]:
        """Load available workshops from JSON"""
        try:
            workshops_file = get_data_file_path("workshops.json")
            data = load_json(workshops_file)
            workshops = data.get("workshops", [])
            return {
                "success": True,
                "data": workshops,
                "count": len(workshops),
                "message": f"Loaded {len(workshops)} workshops"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to load workshops: {e}"
            }
    
    @staticmethod
    def detect_issues_from_log(vehicle_data: dict, rules: list) -> dict[str, Any]:
        """Detect issues from vehicle log using rules"""
        import sys
        import os as os_module
        sys.path.insert(0, os_module.path.join(os_module.path.dirname(__file__), '..'))
        from tools.issue_detector import IssueDetector
        import tempfile
        
        try:
            # Create temporary rules file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump({"rules": rules}, f)
                temp_file = f.name
            
            detector = IssueDetector(vehicle_data, temp_file)
            issues = detector.detect_all_issues()
            
            # Clean up
            os.unlink(temp_file)
            
            return {
                "success": True,
                "issues": issues,
                "count": len(issues),
                "message": f"Detected {len(issues)} issues"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to detect issues: {e}"
            }
    
    @staticmethod
    def calculate_priority(issues: list) -> dict[str, Any]:
        """Calculate priority and risk score"""
        import sys
        import os as os_module
        sys.path.insert(0, os_module.path.join(os_module.path.dirname(__file__), '..'))
        from tools.priority_calculator import PriorityCalculator
        
        try:
            calc = PriorityCalculator(issues)
            priority = calc.calculate_overall_priority()
            risk_score = calc.calculate_risk_score()
            summary = calc.get_issue_summary()
            
            return {
                "success": True,
                "priority": priority,
                "risk_score": risk_score,
                "summary": summary,
                "message": f"Vehicle priority: {priority}, Risk score: {risk_score}/100"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to calculate priority: {e}"
            }
    
    @staticmethod
    def generate_recommendations(issues: list, priority: str, risk_score: float) -> dict[str, Any]:
        """Generate recommendations based on priority"""
        import sys
        import os as os_module
        sys.path.insert(0, os_module.path.join(os_module.path.dirname(__file__), '..'))
        from tools.recommendation_engine import RecommendationEngine
        
        try:
            engine = RecommendationEngine(issues, priority, risk_score)
            recommendations = engine.generate_recommendations()
            
            return {
                "success": True,
                "recommendations": recommendations,
                "urgency": recommendations.get("urgency", "UNKNOWN"),
                "message": recommendations.get("message", "")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to generate recommendations: {e}"
            }
    
    @staticmethod
    def suggest_workshops(workshops: list, priority: str, required_services: list = None) -> dict[str, Any]:
        """Suggest suitable workshops"""
        import sys
        import os as os_module
        sys.path.insert(0, os_module.path.join(os_module.path.dirname(__file__), '..'))
        from tools.workshop_suggester import WorkshopSuggester
        
        try:
            suggester = WorkshopSuggester(workshops, priority)
            suggestions = suggester.suggest_workshops(required_services)
            
            return {
                "success": True,
                "workshops": suggestions,
                "count": len(suggestions),
                "message": f"Suggested {len(suggestions)} workshops"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to suggest workshops: {e}"
            }
    
    @staticmethod
    def save_user_feedback(feedback: dict) -> dict[str, Any]:
        """Save user feedback to JSON"""
        import sys
        import os as os_module
        sys.path.insert(0, os_module.path.join(os_module.path.dirname(__file__), '..'))
        from tools.feedback_manager import FeedbackManager
        
        try:
            feedback_file = get_data_file_path("user_feedback.json")
            manager = FeedbackManager(feedback_file)
            
            if manager.save_feedback(feedback):
                return {
                    "success": True,
                    "feedback_id": feedback.get("id"),
                    "message": "Feedback saved successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to save feedback",
                    "message": "Feedback save failed"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to save feedback: {e}"
            }
    
    @staticmethod
    def get_feedback_history() -> dict[str, Any]:
        """Get feedback history"""
        import sys
        import os as os_module
        sys.path.insert(0, os_module.path.join(os_module.path.dirname(__file__), '..'))
        from tools.feedback_manager import FeedbackManager
        
        try:
            feedback_file = get_data_file_path("user_feedback.json")
            manager = FeedbackManager(feedback_file)
            summary = manager.get_feedback_summary()
            
            return {
                "success": True,
                "history": summary,
                "message": f"Retrieved {summary.get('total_feedbacks', 0)} feedback records"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get feedback history: {e}"
            }
