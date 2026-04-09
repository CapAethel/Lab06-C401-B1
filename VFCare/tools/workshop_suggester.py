"""Workshop Suggester - Suggests suitable workshops and time slots"""
from typing import List, Dict, Any
from datetime import datetime


class WorkshopSuggester:
    """Suggests most suitable workshops and available time slots"""
    
    def __init__(self, workshops: List[Dict[str, Any]], vehicle_priority: str):
        """Initialize WorkshopSuggester
        
        Args:
            workshops: List of available workshops
            vehicle_priority: Vehicle priority level (critical, medium, low)
        """
        self.workshops = workshops
        self.vehicle_priority = vehicle_priority
    
    def suggest_workshops(self, required_services: List[str] = None) -> List[Dict[str, Any]]:
        """Suggest suitable workshops based on priority and capabilities
        
        Args:
            required_services: List of required services (e.g., ['brake', 'tire'])
            
        Returns:
            Sorted list of recommended workshops with details
        """
        if self.vehicle_priority == 'critical':
            return self._suggest_critical_workshops(required_services)
        else:
            return self._suggest_normal_workshops(required_services)
    
    def _suggest_critical_workshops(self, required_services: List[str] = None) -> List[Dict[str, Any]]:
        """For critical issues: return closest emergency-capable workshop
        
        Args:
            required_services: List of required services
            
        Returns:
            List with closest emergency-capable workshop
        """
        # Filter workshops that can handle emergency
        emergency_workshops = [w for w in self.workshops if w.get('emergency_capable', False)]
        
        if not emergency_workshops:
            # Fallback to closest workshop if no emergency capable
            emergency_workshops = self.workshops
        
        # Sort by distance (closest first)
        sorted_workshops = sorted(emergency_workshops, key=lambda w: w.get('distance_km', 999))
        
        # Return top 1-2 closest workshops
        result = []
        for ws in sorted_workshops[:2]:
            result.append({
                'workshop_id': ws['workshop_id'],
                'name': ws['name'],
                'address': ws['address'],
                'phone': ws['phone'],
                'distance_km': ws['distance_km'],
                'rating': ws['rating'],
                'emergency_capable': ws['emergency_capable'],
                'available_slots': self._get_immediate_slots(ws),
                'priority_rank': 'EMERGENCY - CLOSEST'
            })
        
        return result
    
    def _suggest_normal_workshops(self, required_services: List[str] = None) -> List[Dict[str, Any]]:
        """For normal issues: suggest multiple workshops with available slots
        
        Args:
            required_services: List of required services
            
        Returns:
            Sorted list of suitable workshops with available slots
        """
        suitable_workshops = []
        
        for workshop in self.workshops:
            # Check if workshop has required capabilities
            if required_services:
                capabilities = workshop.get('capabilities', [])
                if not any(service in capabilities for service in required_services):
                    continue
            
            # Get available slots
            available_slots = self._get_available_slots(workshop)
            
            if available_slots:
                suitable_workshops.append({
                    'workshop_id': workshop['workshop_id'],
                    'name': workshop['name'],
                    'address': workshop['address'],
                    'phone': workshop['phone'],
                    'distance_km': workshop['distance_km'],
                    'rating': workshop['rating'],
                    'emergency_capable': workshop['emergency_capable'],
                    'capabilities': workshop['capabilities'],
                    'available_slots': available_slots,
                    'priority_rank': self._calculate_priority_rank(workshop)
                })
        
        # Sort by priority: closest first, then by rating
        suitable_workshops.sort(key=lambda w: (w['distance_km'], -w['rating']))
        
        return suitable_workshops
    
    def _get_available_slots(self, workshop: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all available time slots for a workshop
        
        Args:
            workshop: Workshop data
            
        Returns:
            List of available slots (max 3 nearest slots)
        """
        available_slots = []
        
        for day_schedule in workshop.get('available_slots', []):
            date = day_schedule['date']
            for slot in day_schedule.get('time_slots', []):
                if slot.get('available', False):
                    available_slots.append({
                        'date': date,
                        'time': slot['time'],
                        'date_display': self._format_date(date),
                        'available': True
                    })
        
        # Return max 3 nearest slots
        return available_slots[:3]
    
    def _get_immediate_slots(self, workshop: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get immediate slots (same day if possible) for emergency cases
        
        Args:
            workshop: Workshop data
            
        Returns:
            List of immediate available slots
        """
        immediate_slots = []
        today = self._get_today_date()
        
        for day_schedule in workshop.get('available_slots', []):
            date = day_schedule['date']
            # Prioritize today's slots
            for slot in day_schedule.get('time_slots', []):
                if slot.get('available', False):
                    immediate_slots.append({
                        'date': date,
                        'time': slot['time'],
                        'date_display': self._format_date(date),
                        'available': True,
                        'is_today': date == today
                    })
        
        # Sort by today first, then by time
        immediate_slots.sort(key=lambda s: (not s['is_today'], s['time']))
        
        return immediate_slots[:2]  # Return top 2 immediate slots
    
    def _calculate_priority_rank(self, workshop: Dict[str, Any]) -> str:
        """Calculate priority rank for workshop recommendation
        
        Args:
            workshop: Workshop data
            
        Returns:
            Priority rank string
        """
        distance = workshop['distance_km']
        rating = workshop['rating']
        
        if distance < 5:
            return "★★★ GẦN NHẤT + RATING CAO"
        elif distance < 10:
            return "★★ GẦN + HỢP LÝ"
        else:
            return "★ KHÁC"
    
    def _format_date(self, date_str: str) -> str:
        """Format date string
        
        Args:
            date_str: Date in YYYY-MM-DD format
            
        Returns:
            Formatted date string
        """
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            return dt.strftime('%a, %d/%m/%Y')
        except:
            return date_str
    
    def _get_today_date(self) -> str:
        """Get today's date in YYYY-MM-DD format"""
        return datetime.now().strftime('%Y-%m-%d')
