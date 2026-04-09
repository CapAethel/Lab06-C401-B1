"""CLI Interface for VFCare Agent"""
import sys
import os
import json
from typing import Dict, List, Any

# Add parent folder to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import VFCareAgent


class VFCareCLI:
    """Command-line interface for VFCare Agent"""
    
    def __init__(self):
        """Initialize CLI"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        data_dir = os.path.join(parent_dir, 'data')
        self.agent = VFCareAgent(data_dir=data_dir)
        self.current_feedback = {}
    
    def print_header(self, text: str) -> None:
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"  {text}")
        print(f"{'='*60}\n")
    
    def print_section(self, text: str) -> None:
        """Print section header"""
        print(f"\n📋 {text}")
        print("-" * 60)
    
    def print_vehicle_status(self, analysis: Dict[str, Any]) -> None:
        """Print vehicle status"""
        self.print_section("TÌNH TRẠNG XE")
        
        vehicle = analysis['vehicle_info']
        status = analysis['status']
        summary = analysis['issue_summary']
        
        print(f"\n🚗 {vehicle['vehicle_name']} ({vehicle['model']})")
        print(f"   ID: {vehicle['vehicle_id']}")
        print(f"   Mileage: {vehicle['mileage_km']:,} km")
        print(f"   Battery Health: {vehicle['battery_health']}%")
        
        priority = status['overall_priority'].upper()
        if priority == 'CRITICAL':
            icon = '🔴'
        elif priority == 'MEDIUM':
            icon = '🟠'
        else:
            icon = '🟢'
        
        print(f"\n{icon} OVERALL STATUS: {priority}")
        print(f"   Risk Score: {status['risk_score']}/100")
        print(f"   Immediate Action Needed: {'YES' if status['should_take_immediate_action'] else 'NO'}")
        
        print(f"\n📊 ISSUES DETECTED:")
        print(f"   🔴 Critical: {summary['critical_count']}")
        print(f"   🟠 Medium: {summary['medium_count']}")
        print(f"   🟡 Low: {summary['low_count']}")
        print(f"   Total: {summary['total_issues']}")
        
        if analysis['detailed_issues']:
            print(f"\n🔍 ISSUE DETAILS:")
            for issue in analysis['detailed_issues']:
                priority_icon = '🔴' if issue['priority'] == 'critical' else '🟠' if issue['priority'] == 'medium' else '🟡'
                print(f"   {priority_icon} [{issue['component'].upper()}] {issue['recommendation']}")
                print(f"      Risk: {issue['base_risk_score']}/100 | Hours: {issue['required_hours']}h")
    
    def print_recommendations(self, rec: Dict[str, Any]) -> None:
        """Print recommendations"""
        self.print_section("GỢI Ý HÀNH ĐỘNG")
        
        priority = rec['priority'].upper()
        if priority == 'CRITICAL':
            icon = '🔴'
            urgency_str = "NGAY LẬP TỨC"
        elif priority == 'MEDIUM':
            icon = '🟠'
            urgency_str = "SỚM"
        else:
            icon = '🟡'
            urgency_str = "LINH HOẠT"
        
        print(f"\n{icon} {urgency_str} - {rec['message']}")
        print(f"\nRisk Level: {rec['risk_level']}")
        print(f"Action Type: {rec['action_type']}")
        print(f"Flexibility: {rec.get('flexibility', 'N/A')}")
        
        if rec.get('required_action'):
            print(f"\n✅ RECOMMENDED STEPS:")
            for step in rec['required_action']:
                print(f"   {step}")
        
        if rec.get('estimated_duration_hours'):
            print(f"\n⏱️  Estimated Duration: {rec['estimated_duration_hours']} hours")
        
        if rec.get('can_defer'):
            print(f"\n💭 Can defer for: {rec.get('defer_days', 'N/A')} days")
    
    def print_workshops(self, workshops: List[Dict[str, Any]], max_show: int = 3) -> None:
        """Print suggested workshops"""
        self.print_section("XƯỞNG BẢO DƯỠNG ĐỀ XUẤT")
        
        if not workshops:
            print("No suitable workshops found")
            return
        
        for i, ws in enumerate(workshops[:max_show], 1):
            print(f"\n{i}. {ws['name']}")
            print(f"   📍 {ws['address']}")
            print(f"   📞 {ws['phone']}")
            print(f"   📏 Distance: {ws['distance_km']} km")
            print(f"   ⭐ Rating: {ws['rating']}/5")
            print(f"   {ws['priority_rank']}")
            
            if ws.get('capabilities'):
                print(f"   Services: {', '.join(ws['capabilities'][:5])}")
            
            if ws.get('available_slots'):
                print(f"   Available Slots:")
                for slot in ws['available_slots'][:3]:
                    print(f"      • {slot['date_display']} {slot['time']}")
    
    def prompt_workshop_choice(self, workshops: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prompt user to choose workshop"""
        print(f"\n\n💼 SELECT WORKSHOP:")
        for i, ws in enumerate(workshops, 1):
            print(f"   {i}. {ws['name']} ({ws['distance_km']} km away)")
        
        while True:
            try:
                choice = input(f"\n   Enter choice (1-{len(workshops)}, or 0 to skip): ").strip()
                if choice == '0':
                    return None
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(workshops):
                    return workshops[choice_idx]
                print("   Invalid choice, try again")
            except ValueError:
                print("   Invalid input, try again")
    
    def prompt_time_choice(self, workshop: Dict[str, Any]) -> Dict[str, str]:
        """Prompt user to choose time slot"""
        slots = workshop.get('available_slots', [])
        if not slots:
            print("No available slots")
            return None
        
        print(f"\n⏰ SELECT TIME SLOT for {workshop['name']}:")
        for i, slot in enumerate(slots, 1):
            print(f"   {i}. {slot['date_display']} {slot['time']}")
        
        while True:
            try:
                choice = input(f"\n   Enter choice (1-{len(slots)}): ").strip()
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(slots):
                    return slots[choice_idx]
                print("   Invalid choice, try again")
            except ValueError:
                print("   Invalid input, try again")
    
    def prompt_user_action(self) -> str:
        """Prompt user for action"""
        print("\n\n📌 YOUR ACTION:")
        print("   1. Confirm booking")
        print("   2. Change workshop")
        print("   3. Change time")
        print("   4. Decline maintenance")
        print("   0. Exit")
        
        while True:
            choice = input("\n   Enter choice: ").strip()
            if choice in ['0', '1', '2', '3', '4']:
                return choice
            print("   Invalid choice, try again")
    
    def run_interactive(self) -> None:
        """Run interactive CLI"""
        self.print_header("🚗 VFCare Agent - Interactive Mode")
        
        # Step 1: Analyze vehicle
        print("\n⏳ Analyzing vehicle status...")
        analysis = self.agent.analyze_vehicle_status()
        self.print_vehicle_status(analysis)
        
        # Step 2: Show recommendations
        rec = self.agent.get_recommendations()
        self.print_recommendations(rec)
        
        # Step 3: Suggest workshops
        workshops = self.agent.suggest_workshops()
        self.print_workshops(workshops)
        
        # Step 4: User interaction loop
        while True:
            action = self.prompt_user_action()
            
            if action == '0':
                print("\n👋 Goodbye!")
                break
            
            elif action == '1':  # Confirm booking
                selected_ws = self.prompt_workshop_choice(workshops)
                if selected_ws:
                    time_slot = self.prompt_time_choice(selected_ws)
                    if time_slot:
                        result = self.agent.book_maintenance(
                            selected_ws['workshop_id'],
                            time_slot['date'],
                            time_slot['time']
                        )
                        if result['success']:
                            print(f"\n✅ {result['message']}")
                            print(f"\n📦 BOOKING DETAILS:")
                            for key, value in result.get('booking', {}).items():
                                print(f"   {key.replace('_', ' ').title()}: {value}")
                        else:
                            print(f"\n❌ {result['message']}")
                        break
            
            elif action == '2':  # Change workshop
                selected_ws = self.prompt_workshop_choice(workshops)
                if selected_ws:
                    reason = input("\n   Reason for change: ").strip()
                    result = self.agent.change_workshop(selected_ws['workshop_id'], reason)
                    if result['success']:
                        print(f"\n✅ {result['message']}")
                        print(f"   New workshop: {result['new_workshop']}")
                    else:
                        print(f"\n❌ {result['message']}")
            
            elif action == '3':  # Change time
                selected_ws = self.prompt_workshop_choice(workshops)
                if selected_ws:
                    time_slot = self.prompt_time_choice(selected_ws)
                    if time_slot:
                        result = self.agent.change_time(time_slot['date'], time_slot['time'])
                        if result['success']:
                            print(f"\n✅ {result['message']}")
                            print(f"   New: {result['new_appointment']['date']} {result['new_appointment']['time']}")
                        else:
                            print(f"\n❌ {result['message']}")
            
            elif action == '4':  # Decline
                reason = input("\n   Reason for declining: ").strip()
                result = self.agent.decline_maintenance(reason)
                if result['success']:
                    print(f"\n✅ {result['message']}")
                else:
                    print(f"\n❌ {result['message']}")
                break
    
    def run_demo(self) -> None:
        """Run demo mode (non-interactive)"""
        self.print_header("🚗 VFCare Agent - Demo Mode")
        
        # Step 1: Analyze
        print("⏳ Analyzing vehicle status...")
        analysis = self.agent.analyze_vehicle_status()
        self.print_vehicle_status(analysis)
        
        # Step 2: Recommendations
        rec = self.agent.get_recommendations()
        self.print_recommendations(rec)
        
        # Step 3: Workshops
        workshops = self.agent.suggest_workshops()
        self.print_workshops(workshops)
        
        # Step 4: Demo booking
        if workshops:
            print(f"\n\n🎬 DEMO: Auto-booking first workshop...")
            selected_ws = workshops[0]
            time_slot = selected_ws['available_slots'][0] if selected_ws['available_slots'] else None
            
            if time_slot:
                result = self.agent.book_maintenance(
                    selected_ws['workshop_id'],
                    time_slot['date'],
                    time_slot['time']
                )
                if result['success']:
                    print(f"✅ {result['message']}")
                    print(f"\n📦 BOOKING DETAILS:")
                    for key, value in result.get('booking', {}).items():
                        print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # Step 5: Show history
        history = self.agent.get_feedback_history()
        self.print_section("FEEDBACK HISTORY")
        print(f"Total Feedbacks: {history['total_feedbacks']}")
        print(f"Confirmed Bookings: {history['bookings_confirmed']}")
        print(f"Declined: {history['bookings_declined']}")
        
        print("\n" + "="*60)
        print("✅ Demo completed!")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='VFCare Agent CLI')
    parser.add_argument(
        '--mode',
        choices=['demo', 'interactive'],
        default='interactive',
        help='Run mode (default: interactive)'
    )
    
    args = parser.parse_args()
    
    cli = VFCareCLI()
    
    if args.mode == 'demo':
        cli.run_demo()
    else:
        cli.run_interactive()


if __name__ == '__main__':
    main()
