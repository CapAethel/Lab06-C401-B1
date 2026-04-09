"""Feedback Manager - Manages user feedback and booking confirmations"""
from typing import Dict, Any, List
from utils import load_json, save_json
from datetime import datetime


class FeedbackManager:
    """Manages user feedback for maintenance recommendations"""
    
    FEEDBACK_TYPES = ['agree', 'change_workshop', 'change_time', 'decline']
    
    def __init__(self, feedback_file: str):
        """Initialize FeedbackManager
        
        Args:
            feedback_file: Path to feedback JSON file
        """
        self.feedback_file = feedback_file
        try:
            self.feedback_data = load_json(feedback_file)
        except:
            self.feedback_data = {'vehicle_id': '', 'feedbacks': []}
    
    def save_feedback(self, feedback: Dict[str, Any]) -> bool:
        """Save user feedback
        
        Args:
            feedback: Feedback object with user choice and details
            
        Returns:
            True if successfully saved
        """
        try:
            # Add timestamp if not present
            if 'timestamp' not in feedback:
                feedback['timestamp'] = datetime.now().isoformat()
            
            self.feedback_data['feedbacks'].append(feedback)
            save_json(self.feedback_file, self.feedback_data)
            return True
        except Exception as e:
            print(f"Error saving feedback: {e}")
            return False
    
    def get_feedback_summary(self) -> Dict[str, Any]:
        """Get summary of all feedbacks
        
        Returns:
            Summary dictionary with feedback counts and details
        """
        feedbacks = self.feedback_data.get('feedbacks', [])
        
        summary = {
            'total_feedbacks': len(feedbacks),
            'agree': [],
            'change_workshop': [],
            'change_time': [],
            'decline': [],
            'bookings_confirmed': 0,
            'bookings_declined': 0
        }
        
        for feedback in feedbacks:
            feedback_type = feedback.get('type')
            if feedback_type in summary:
                summary[feedback_type].append(feedback)
            
            if feedback_type == 'agree':
                summary['bookings_confirmed'] += 1
            elif feedback_type == 'decline':
                summary['bookings_declined'] += 1
        
        return summary
    
    def create_feedback(self, feedback_type: str, details: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create feedback object
        
        Args:
            feedback_type: Type of feedback (agree, change_workshop, change_time, decline)
            details: Additional details for the feedback
            
        Returns:
            Feedback object
        """
        if feedback_type not in self.FEEDBACK_TYPES:
            raise ValueError(f"Invalid feedback type. Must be one of {self.FEEDBACK_TYPES}")
        
        feedback = {
            'id': self._generate_feedback_id(),
            'type': feedback_type,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        
        return feedback
    
    def _generate_feedback_id(self) -> str:
        """Generate unique feedback ID
        
        Returns:
            Feedback ID
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        count = len(self.feedback_data.get('feedbacks', [])) + 1
        return f"FB_{timestamp}_{count:03d}"
    
    def get_latest_booking(self) -> Dict[str, Any]:
        """Get latest confirmed booking
        
        Returns:
            Latest booking feedback or None
        """
        feedbacks = self.feedback_data.get('feedbacks', [])
        confirmed = [f for f in feedbacks if f.get('type') == 'agree']
        
        if confirmed:
            return confirmed[-1]
        return None
    
    def create_booking_feedback(
        self, 
        workshop_id: str, 
        workshop_name: str, 
        date: str, 
        time: str,
        issues: List[str] = None
    ) -> Dict[str, Any]:
        """Create a booking confirmation feedback
        
        Args:
            workshop_id: Selected workshop ID
            workshop_name: Selected workshop name
            date: Appointment date
            time: Appointment time
            issues: List of issues to be fixed
            
        Returns:
            Booking feedback object
        """
        return self.create_feedback(
            'agree',
            {
                'workshop_id': workshop_id,
                'workshop_name': workshop_name,
                'appointment_date': date,
                'appointment_time': time,
                'issues_to_fix': issues or [],
                'status': 'confirmed'
            }
        )
    
    def create_workshop_change_feedback(
        self,
        new_workshop_id: str,
        new_workshop_name: str,
        reason: str = "User preference"
    ) -> Dict[str, Any]:
        """Create feedback for workshop change
        
        Args:
            new_workshop_id: New workshop ID
            new_workshop_name: New workshop name
            reason: Reason for change
            
        Returns:
            Change workshop feedback object
        """
        return self.create_feedback(
            'change_workshop',
            {
                'new_workshop_id': new_workshop_id,
                'new_workshop_name': new_workshop_name,
                'reason': reason,
                'status': 'pending_new_slot'
            }
        )
    
    def create_time_change_feedback(
        self,
        new_date: str,
        new_time: str,
        reason: str = "User preference"
    ) -> Dict[str, Any]:
        """Create feedback for time change
        
        Args:
            new_date: New appointment date
            new_time: New appointment time
            reason: Reason for change
            
        Returns:
            Change time feedback object
        """
        return self.create_feedback(
            'change_time',
            {
                'new_appointment_date': new_date,
                'new_appointment_time': new_time,
                'reason': reason,
                'status': 'time_updated'
            }
        )
    
    def create_decline_feedback(
        self,
        reason: str = "User declined"
    ) -> Dict[str, Any]:
        """Create feedback for declined recommendation
        
        Args:
            reason: Reason for declining
            
        Returns:
            Decline feedback object
        """
        return self.create_feedback(
            'decline',
            {
                'reason': reason,
                'decline_time': datetime.now().isoformat(),
                'status': 'maintenance_declined'
            }
        )
