"""Recommendation Engine - Generates maintenance recommendations"""
from typing import List, Dict, Any
from .priority_calculator import PriorityCalculator


class RecommendationEngine:
    """Generates maintenance recommendations based on issues and priorities"""
    
    def __init__(self, issues: List[Dict[str, Any]], overall_priority: str, risk_score: float):
        """Initialize RecommendationEngine
        
        Args:
            issues: List of detected issues
            overall_priority: Overall vehicle priority (critical, medium, low)
            risk_score: Overall risk score (0-100)
        """
        self.issues = issues
        self.overall_priority = overall_priority
        self.risk_score = risk_score
    
    def generate_recommendations(self) -> Dict[str, Any]:
        """Generate comprehensive maintenance recommendations
        
        Returns:
            Dictionary with recommendations and action items
        """
        if self.overall_priority == 'critical':
            return self._generate_critical_recommendations()
        elif self.overall_priority == 'medium':
            return self._generate_medium_recommendations()
        else:
            return self._generate_low_recommendations()
    
    def _generate_critical_recommendations(self) -> Dict[str, Any]:
        """Generate recommendations for critical status"""
        critical_issues = [i for i in self.issues if i['priority'] == 'critical']
        
        return {
            'priority': 'critical',
            'urgency': 'IMMEDIATE',
            'message': 'CẦN XỬ LÝ NGAY: Có vấn đề nguy hiểm cần khắc phục tức thì',
            'risk_level': f'Rủi ro cao ({self.risk_score}/100)',
            'issue_details': critical_issues,
            'action_type': 'emergency_maintenance',
            'required_action': [
                '1. Ngừng sử dụng xe nếu có thể',
                '2. Liên hệ xưởng bảo dưỡng gần nhất để xử lý khẩn cấp',
                '3. Chuẩn bị thông tin xe để xưởng tiếp nhận nhanh chóng'
            ],
            'estimated_duration_hours': sum(i.get('required_hours', 0) for i in critical_issues),
            'can_defer': False,
            'needs_emergency_slot': True
        }
    
    def _generate_medium_recommendations(self) -> Dict[str, Any]:
        """Generate recommendations for medium status"""
        medium_issues = [i for i in self.issues if i['priority'] == 'medium']
        
        recommendations = {
            'priority': 'medium',
            'urgency': 'SOON',
            'message': 'Nên kiểm tra sớm: Có một số vấn đề cần được giải quyết trong thời gian gần',
            'risk_level': f'Rủi ro vừa phải ({self.risk_score}/100)',
            'issue_details': medium_issues,
            'action_type': 'schedule_maintenance',
            'required_action': [
                '1. Lên lịch bảo dưỡng trong 3-5 ngày tới',
                '2. Chọn xưởng có thể xử lý các vấn đề cần thiết',
                '3. Lựa chọn slot thời gian phù hợp với lịch của bạn'
            ],
            'estimated_duration_hours': min(sum(i.get('required_hours', 0) for i in medium_issues), 4),
            'flexibility': 'medium',
            'can_defer': True,
            'defer_days': 5,
            'needs_emergency_slot': False
        }
        
        return recommendations
    
    def _generate_low_recommendations(self) -> Dict[str, Any]:
        """Generate recommendations for low status"""
        return {
            'priority': 'low',
            'urgency': 'FLEXIBLE',
            'message': 'Tình trạng bình thường: Xe đang hoạt động tốt, theo dõi thường xuyên',
            'risk_level': f'Rủi ro thấp ({self.risk_score}/100)',
            'issue_details': self.issues if self.issues else [],
            'action_type': 'monitor',
            'required_action': [
                '1. Tiếp tục theo dõi tình trạng xe',
                '2. Nếu có vấn đề mới xuất hiện, lên lịch bảo dưỡng',
                '3. Bảo dưỡng định kỳ theo hướng dẫn của nhà sản xuất'
            ],
            'estimated_duration_hours': 0,
            'flexibility': 'high',
            'can_defer': True,
            'defer_days': 30,
            'needs_emergency_slot': False
        }
    
    def get_issue_summary_text(self) -> str:
        """Get text summary of key issues
        
        Returns:
            Formatted text summary of issues
        """
        if not self.issues:
            return "Không phát hiện vấn đề"
        
        summary_lines = []
        
        critical = [i for i in self.issues if i['priority'] == 'critical']
        medium = [i for i in self.issues if i['priority'] == 'medium']
        low = [i for i in self.issues if i['priority'] == 'low']
        
        if critical:
            summary_lines.append(f"⚠️  CRITICAL ({len(critical)}):")
            for issue in critical:
                summary_lines.append(f"   - {issue['recommendation']}")
        
        if medium:
            summary_lines.append(f"⚠  MEDIUM ({len(medium)}):")
            for issue in medium:
                summary_lines.append(f"   - {issue['recommendation']}")
        
        if low:
            summary_lines.append(f"ℹ️  LOW ({len(low)}):")
            for issue in low:
                summary_lines.append(f"   - {issue['recommendation']}")
        
        return '\n'.join(summary_lines)
