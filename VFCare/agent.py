"""VFCare Agent - Main orchestrator for vehicle maintenance recommendations"""
import sys
import os
from typing import Dict, Any, List

# Add tools folder to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))

from tools.utils import load_json, save_json
from tools.issue_detector import IssueDetector
from tools.priority_calculator import PriorityCalculator
from tools.recommendation_engine import RecommendationEngine
from tools.workshop_suggester import WorkshopSuggester
from tools.feedback_manager import FeedbackManager


class VFCareAgent:
    """Main VFCare Agent for vehicle maintenance recommendations"""
    
    def __init__(self, data_dir: str = 'data'):
        """Initialize VFCareAgent
        
        Args:
            data_dir: Directory containing data files
        """
        self.data_dir = data_dir
        
        # Load data files
        self.vehicle_status = load_json(os.path.join(data_dir, 'vehicle_status.json'))
        self.rules = load_json(os.path.join(data_dir, 'maintenance_rules.json'))
        self.workshops = load_json(os.path.join(data_dir, 'workshops.json'))['workshops']
        
        # Initialize managers
        self.issue_detector = IssueDetector(
            self.vehicle_status,
            os.path.join(data_dir, 'maintenance_rules.json')
        )
        self.feedback_manager = FeedbackManager(
            os.path.join(data_dir, 'user_feedback.json')
        )
        
        # Current state
        self.detected_issues = []
        self.overall_priority = 'low'
        self.risk_score = 0.0
        self.recommendations = {}
        self.suggested_workshops = []
    
    def analyze_vehicle_status(self) -> Dict[str, Any]:
        """Analyze current vehicle status and detect issues
        
        Returns:
            Analysis result with issues and priorities
        """
        # Detect all issues
        self.detected_issues = self.issue_detector.detect_all_issues()
        
        # Calculate priorities
        priority_calc = PriorityCalculator(self.detected_issues)
        self.overall_priority = priority_calc.calculate_overall_priority()
        self.risk_score = priority_calc.calculate_risk_score()
        issue_summary = priority_calc.get_issue_summary()
        
        # Get vehicle info
        vehicle_info = {
            'vehicle_id': self.vehicle_status['vehicle_id'],
            'vehicle_name': self.vehicle_status['vehicle_name'],
            'model': self.vehicle_status['model'],
            'mileage_km': self.vehicle_status['total_mileage_km'],
            'battery_health': self.vehicle_status['battery']['health_percent']
        }
        
        analysis_result = {
            'vehicle_info': vehicle_info,
            'status': {
                'overall_priority': self.overall_priority,
                'risk_score': self.risk_score,
                'should_take_immediate_action': priority_calc.should_take_immediate_action()
            },
            'issue_summary': issue_summary,
            'detailed_issues': self.detected_issues,
            'analysis_timestamp': self.vehicle_status['last_update']
        }
        
        return analysis_result
    
    def get_recommendations(self) -> Dict[str, Any]:
        """Get maintenance recommendations based on analysis
        
        Returns:
            Recommendations with action items
        """
        if not self.detected_issues or self.overall_priority == 'low':
            priority_calc = PriorityCalculator(self.detected_issues)
            overall_priority = priority_calc.calculate_overall_priority()
            risk_score = priority_calc.calculate_risk_score()
        else:
            overall_priority = self.overall_priority
            risk_score = self.risk_score
        
        # Generate recommendations
        rec_engine = RecommendationEngine(
            self.detected_issues,
            overall_priority,
            risk_score
        )
        self.recommendations = rec_engine.generate_recommendations()
        
        return self.recommendations
    
    def suggest_workshops(self) -> List[Dict[str, Any]]:
        """Suggest suitable workshops for maintenance
        
        Returns:
            Ordered list of suggested workshops with available slots
        """
        # Get services from issues
        services = set()
        for issue in self.detected_issues:
            component = issue['component']
            # Map components to services
            service_map = {
                'brake_system': 'brake',
                'tire': 'tire',
                'air_filter': 'filter',
                'cabin_filter': 'filter',
                'battery': 'battery',
                'motor': 'motor'
            }
            if component in service_map:
                services.add(service_map[component])
        
        # Suggest workshops
        suggester = WorkshopSuggester(self.workshops, self.overall_priority)
        self.suggested_workshops = suggester.suggest_workshops(list(services) if services else None)
        
        return self.suggested_workshops
    
    def book_maintenance(
        self,
        workshop_id: str,
        date: str,
        time: str
    ) -> Dict[str, Any]:
        """Book maintenance appointment
        
        Args:
            workshop_id: ID of selected workshop
            date: Selected date
            time: Selected time slot
            
        Returns:
            Booking confirmation
        """
        # Find workshop
        workshop = None
        for ws in self.suggested_workshops:
            if ws['workshop_id'] == workshop_id:
                workshop = ws
                break
        
        if not workshop:
            return {'success': False, 'message': 'Workshop not found'}
        
        # Extract issues to fix
        issues_to_fix = [issue['recommendation'] for issue in self.detected_issues]
        
        # Create booking feedback
        booking_feedback = self.feedback_manager.create_booking_feedback(
            workshop_id=workshop_id,
            workshop_name=workshop['name'],
            date=date,
            time=time,
            issues=issues_to_fix
        )
        
        # Save feedback
        if self.feedback_manager.save_feedback(booking_feedback):
            return {
                'success': True,
                'message': 'Lịch bảo dưỡng đã được xác nhận',
                'booking': {
                    'workshop': workshop['name'],
                    'address': workshop['address'],
                    'phone': workshop['phone'],
                    'date': date,
                    'time': time,
                    'booking_id': booking_feedback['id']
                }
            }
        else:
            return {'success': False, 'message': 'Lỗi khi lưu thông tin đặt lịch'}
    
    def change_workshop(self, new_workshop_id: str, reason: str = "User preference") -> Dict[str, Any]:
        """Change selected workshop
        
        Args:
            new_workshop_id: ID of new workshop
            reason: Reason for change
            
        Returns:
            Change confirmation
        """
        # Find workshop
        new_workshop = None
        for ws in self.suggested_workshops:
            if ws['workshop_id'] == new_workshop_id:
                new_workshop = ws
                break
        
        if not new_workshop:
            return {'success': False, 'message': 'Workshop not found'}
        
        # Create change feedback
        change_feedback = self.feedback_manager.create_workshop_change_feedback(
            new_workshop_id=new_workshop_id,
            new_workshop_name=new_workshop['name'],
            reason=reason
        )
        
        # Save feedback
        if self.feedback_manager.save_feedback(change_feedback):
            return {
                'success': True,
                'message': 'Đã đổi xưởng',
                'new_workshop': new_workshop['name']
            }
        else:
            return {'success': False, 'message': 'Lỗi khi lưu thay đổi'}
    
    def change_time(self, new_date: str, new_time: str, reason: str = "User preference") -> Dict[str, Any]:
        """Change appointment time
        
        Args:
            new_date: New appointment date
            new_time: New appointment time
            reason: Reason for change
            
        Returns:
            Change confirmation
        """
        # Create change feedback
        change_feedback = self.feedback_manager.create_time_change_feedback(
            new_date=new_date,
            new_time=new_time,
            reason=reason
        )
        
        # Save feedback
        if self.feedback_manager.save_feedback(change_feedback):
            return {
                'success': True,
                'message': 'Đã cập nhật thời gian',
                'new_appointment': {
                    'date': new_date,
                    'time': new_time
                }
            }
        else:
            return {'success': False, 'message': 'Lỗi khi lưu thay đổi'}
    
    def decline_maintenance(self, reason: str = "User declined") -> Dict[str, Any]:
        """Decline maintenance recommendation
        
        Args:
            reason: Reason for declining
            
        Returns:
            Decline confirmation
        """
        # Create decline feedback
        decline_feedback = self.feedback_manager.create_decline_feedback(reason=reason)
        
        # Save feedback
        if self.feedback_manager.save_feedback(decline_feedback):
            return {
                'success': True,
                'message': 'Bạn đã từ chối gợi ý bảo dưỡng',
                'reason': reason
            }
        else:
            return {'success': False, 'message': 'Lỗi khi lưu phản hồi'}
    
    def get_feedback_history(self) -> Dict[str, Any]:
        """Get feedback and booking history
        
        Returns:
            Summary of all feedbacks and bookings
        """
        return self.feedback_manager.get_feedback_summary()


def main():
    """Main entry point"""
    # Initialize agent
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    
    agent = VFCareAgent(data_dir=data_dir)
    
    # Demo: Analyze vehicle
    print("🚗 VFCare Agent - Demo Flow\n")
    print("=" * 60)
    
    analysis = agent.analyze_vehicle_status()
    print(f"\n1. VỀ XE: {analysis['vehicle_info']['vehicle_name']}")
    print(f"   - Mileage: {analysis['vehicle_info']['mileage_km']} km")
    print(f"   - Battery Health: {analysis['vehicle_info']['battery_health']}%")
    print(f"   - Overall Priority: {analysis['status']['overall_priority'].upper()}")
    print(f"   - Risk Score: {analysis['status']['risk_score']}/100")
    
    print(f"\n2. PHÁT HIỆN VẤN ĐỀ:")
    print(f"   - Critical: {analysis['issue_summary']['critical_count']}")
    print(f"   - Medium: {analysis['issue_summary']['medium_count']}")
    print(f"   - Low: {analysis['issue_summary']['low_count']}")
    
    for issue in analysis['issue_summary']['critical']:
        print(f"     ⚠️  {issue['recommendation']}")
    for issue in analysis['issue_summary']['medium']:
        print(f"     ⚠  {issue['recommendation']}")
    
    print(f"\n3. GỢI Ý HÀNH ĐỘNG:")
    rec = agent.get_recommendations()
    print(f"   - Urgency: {rec['urgency']}")
    print(f"   - Message: {rec['message']}")
    
    print(f"\n4. ĐỀ XUẤT XƯỞNG BẢOỸNG:")
    workshops = agent.suggest_workshops()
    for i, ws in enumerate(workshops[:2], 1):
        print(f"\n   Xưởng {i}: {ws['name']}")
        print(f"   - Địa chỉ: {ws['address']}")
        print(f"   - Khoảng cách: {ws['distance_km']} km")
        print(f"   - Rating: {ws['rating']}/5")
        print(f"   - Slots trống:")
        for slot in ws['available_slots'][:3]:
            print(f"     • {slot['date_display']} {slot['time']}")
    
    print("\n" + "=" * 60)
    print("✅ Demo flow hoàn tất!")


if __name__ == '__main__':
    main()
