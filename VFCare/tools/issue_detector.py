"""Issue Detector - Detects vehicle issues based on rules"""
from typing import List, Dict, Any
from .utils import load_json, evaluate_condition, get_nested_value
import os


class IssueDetector:
    def __init__(self, vehicle_status: Dict[str, Any], rules_path: str):
        """Initialize IssueDetector
        
        Args:
            vehicle_status: Current vehicle status data
            rules_path: Path to maintenance rules JSON file
        """
        self.vehicle_status = vehicle_status
        self.rules = load_json(rules_path)['rules']
        
    def detect_all_issues(self) -> List[Dict[str, Any]]:
        """Detect all issues in the vehicle
        
        Returns:
            List of detected issues with details
        """
        detected_issues = []
        
        for rule in self.rules:
            if self._check_rule(rule):
                issue = self._create_issue(rule)
                detected_issues.append(issue)
        
        return detected_issues
    
    def _check_rule(self, rule: Dict[str, Any]) -> bool:
        """Check if a rule condition is met
        
        Args:
            rule: Rule definition
            
        Returns:
            True if rule condition is met
        """
        condition = rule.get('condition', '')
        component = rule.get('component', '')
        
        # Get component data from vehicle status
        component_data = self.vehicle_status.get(component, {})
        
        # Handle special case for mileage-based rules
        if 'total_mileage' in condition:
            total_mileage = self.vehicle_status.get('total_mileage_km', 0)
            last_maint = component_data.get('last_maintenance_km', 0)
            return (total_mileage - last_maint) > 10000
        
        # Evaluate compound conditions (with OR)
        if ' OR ' in condition:
            conditions = condition.split(' OR ')
            # Build full condition string with actual values
            full_condition = self._build_condition_string(conditions, component)
            return evaluate_condition(full_condition, self.vehicle_status)
        else:
            full_condition = self._build_condition_string([condition], component)
            return evaluate_condition(full_condition, self.vehicle_status)
    
    def _build_condition_string(self, conditions: List[str], component: str) -> str:
        """Build evaluable condition string
        
        Args:
            conditions: List of conditions
            component: Component name
            
        Returns:
            Full condition string ready for eval
        """
        built_conditions = []
        component_data = self.vehicle_status.get(component, {})
        
        for cond in conditions:
            cond = cond.strip()
            # Extract field name and get value
            for field in component_data.keys():
                if field in cond:
                    value = component_data.get(field)
                    # Replace field name with actual value
                    cond = cond.replace(field, str(value))
                    break
            built_conditions.append(f"({cond})")
        
        return ' or '.join(built_conditions)
    
    def _create_issue(self, rule: Dict[str, Any]) -> Dict[str, Any]:
        """Create issue object from rule
        
        Args:
            rule: Rule definition
            
        Returns:
            Issue object with all details
        """
        return {
            'rule_id': rule.get('rule_id'),
            'component': rule.get('component'),
            'issue_type': rule.get('issue_type'),
            'priority': rule.get('priority'),
            'base_risk_score': rule.get('base_risk_score'),
            'recommendation': rule.get('recommendation'),
            'action': rule.get('action'),
            'required_hours': rule.get('required_hours'),
            'detected_at': self.vehicle_status.get('last_update', '')
        }
    
    def get_critical_issues(self) -> List[Dict[str, Any]]:
        """Get all critical issues"""
        all_issues = self.detect_all_issues()
        return [issue for issue in all_issues if issue['priority'] == 'critical']
    
    def get_issues_by_priority(self, priority: str) -> List[Dict[str, Any]]:
        """Get issues by priority level
        
        Args:
            priority: Priority level (critical, medium, low)
            
        Returns:
            List of issues with specified priority
        """
        all_issues = self.detect_all_issues()
        return [issue for issue in all_issues if issue['priority'] == priority]
