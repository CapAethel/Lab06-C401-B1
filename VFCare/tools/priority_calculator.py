"""Priority Calculator - Calculates overall vehicle priority and risk score"""
from typing import List, Dict, Any, Tuple


class PriorityCalculator:
    """Calculates vehicle overall priority and risk score based on detected issues"""
    
    # Priority hierarchy
    PRIORITY_HIERARCHY = {
        'critical': 3,
        'medium': 2,
        'low': 1
    }
    
    def __init__(self, issues: List[Dict[str, Any]]):
        """Initialize PriorityCalculator
        
        Args:
            issues: List of detected issues
        """
        self.issues = issues
    
    def calculate_overall_priority(self) -> str:
        """Calculate overall vehicle priority
        
        Returns:
            Overall priority level (critical, medium, or low)
        """
        if not self.issues:
            return 'low'
        
        # Check for critical issues
        critical_issues = [i for i in self.issues if i['priority'] == 'critical']
        if critical_issues:
            return 'critical'
        
        # Check for medium issues
        medium_issues = [i for i in self.issues if i['priority'] == 'medium']
        if medium_issues:
            return 'medium'
        
        return 'low'
    
    def calculate_risk_score(self) -> float:
        """Calculate overall risk score (0-100)
        
        Returns:
            Risk score between 0 and 100
        """
        if not self.issues:
            return 0.0
        
        # Calculate weighted risk score
        total_score = 0.0
        
        for issue in self.issues:
            base_score = issue.get('base_risk_score', 0)
            priority = issue.get('priority', 'low')
            
            # Apply priority weight
            priority_weight = self.PRIORITY_HIERARCHY.get(priority, 1)
            weighted_score = base_score * (priority_weight / 3.0)
            
            total_score += weighted_score
        
        # Normalize to 0-100 scale
        # Assume max 10 issues max score is 100
        risk_score = min(total_score / 10.0, 100.0)
        
        return round(risk_score, 1)
    
    def get_issue_summary(self) -> Dict[str, Any]:
        """Get summary of all issues by priority
        
        Returns:
            Dictionary with counts and details by priority
        """
        summary = {
            'total_issues': len(self.issues),
            'critical': [],
            'medium': [],
            'low': []
        }
        
        for issue in self.issues:
            priority = issue['priority']
            summary[priority].append(issue)
        
        summary['critical_count'] = len(summary['critical'])
        summary['medium_count'] = len(summary['medium'])
        summary['low_count'] = len(summary['low'])
        
        return summary
    
    def should_take_immediate_action(self) -> bool:
        """Determine if immediate action is needed
        
        Returns:
            True if there are critical issues or high risk score
        """
        critical_issues = [i for i in self.issues if i['priority'] == 'critical']
        risk_score = self.calculate_risk_score()
        
        return len(critical_issues) > 0 or risk_score >= 75
