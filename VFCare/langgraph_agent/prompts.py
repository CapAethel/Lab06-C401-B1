"""System prompts for VFCare Agent - Vietnamese vehicle maintenance advisor"""

# Main system prompt for OpenAI
SYSTEM_PROMPT = """Bạn là cố vấn bảo dưỡng xe chuyên nghiệp, thân thiện.
Giải thích vấn đề xe rõ ràng, không kỹ thuật quá.
Đưa lời khuyên trực tiếp, không bán quá mức.
Nói chuyện tự nhiên như một người bạn đáng tin cậy."""

# System prompt for vehicle analysis and issue presentation
VEHICLE_ANALYSIS_PROMPT = """Phân tích tình trạng xe một cách rõ ràng, ngắn gọn:
1. Tóm tắt chi tiết xe và các vấn đề theo ưu tiên
2. Giải thích tại sao cần sửa, không quá kỹ thuật
3. Đề xuất hành động tiếp theo
Nhấn mạnh vấn đề cấp bách nhưng không gây hoảng sợ."""

# System prompt for workshop suggestion and booking
WORKSHOP_SUGGESTION_PROMPT = """Gợi ý xưởng bảo dưỡng phù hợp ngắn gọn:
1. Giới thiệu xưởng: tên, khoảng cách, đánh giá
2. Giải thích tại sao phù hợp cho vấn đề này
3. Hỏi có muốn đặt lịch hẹn không
Tập trung vào cách tiếp cận trực tiếp, không bao nhất."""

# System prompt for handling customer concerns and follow-up
CUSTOMER_CARE_PROMPT = """Trả lời câu hỏi chủ xe chính xác, thân thiện, không dài dòng.
Lắng nghe lo lắng, đưa giải pháp thực tế.
Nếu không chắc chắn, nói thẳng.
Respect ngân sách và ưu tiên của họ."""

# Get prompts by context
def get_system_prompt(context: str = "main") -> str:
    """Get system prompt based on context
    
    Args:
        context: Type of prompt needed - 'main', 'analysis', 'workshop', 'care'
    
    Returns:
        System prompt string
    """
    prompts = {
        "main": SYSTEM_PROMPT,
        "analysis": VEHICLE_ANALYSIS_PROMPT,
        "workshop": WORKSHOP_SUGGESTION_PROMPT,
        "care": CUSTOMER_CARE_PROMPT
    }
    
    return prompts.get(context, SYSTEM_PROMPT)


# Specific prompt templates for different scenarios
def create_analysis_prompt(vehicle_name: str, mileage_km: int, issues_text: str) -> str:
    """Create a prompt for vehicle analysis
    
    Args:
        vehicle_name: Name/model of vehicle
        mileage_km: Current mileage in km
        issues_text: Formatted list of detected issues
    
    Returns:
        Formatted prompt
    """
    return f"""Phân tích xe: {vehicle_name} ({mileage_km:,} km)

Vấn đề:
{issues_text}

Hãy:
1. Tóm tắt tình hình xe (ngắn gọn, không kỹ thuật)
2. Giải thích từng vấn đề tại sao cần sửa
3. Hỏi có muốn đặt lịch bảo dưỡng không

Nói ngắn gọn, tự nhiên."""


def create_workshop_prompt(workshop_name: str, distance_km: float, 
                          rating: float, time_slot: str, issues_str: str) -> str:
    """Create a prompt for workshop suggestion
    
    Args:
        workshop_name: Name of the workshop
        distance_km: Distance from customer in km
        rating: Workshop rating
        time_slot: Available appointment time
        issues_str: List of issues to be fixed
    
    Returns:
        Formatted prompt
    """
    return f"""Gợi ý xưởng: {workshop_name}
Cách: {distance_km}km | Đánh giá: {rating}/5
Thời gian: {time_slot}
Sửa: {issues_str}

Giải thích vì sao phù hợp, hỏi có muốn đặt không.
Trực tiếp, ngắn gọn."""


def create_issue_summary(issues: list[dict]) -> str:
    """Create a formatted summary of issues for prompts
    
    Args:
        issues: List of issue dictionaries
    
    Returns:
        Formatted string
    """
    lines = []
    for issue in issues:
        component = issue.get('component', 'Unknown')
        recommendation = issue.get('recommendation', 'Kiểm tra')
        priority = issue.get('priority', 'low')
        risk = issue.get('base_risk_score', 0)
        
        # Translate priority to Vietnamese
        priority_text = {
            'critical': 'Cấp bách',
            'medium': 'Trung bình',
            'low': 'Thấp'
        }.get(priority, priority)
        
        lines.append(f"- {recommendation} ({component})")
        lines.append(f"  • Mức độ ưu tiên: {priority_text}")
        lines.append(f"  • Điểm rủi ro: {risk}/100")
    
    return "\n".join(lines) if lines else "Không phát hiện vấn đề đáng kể"
