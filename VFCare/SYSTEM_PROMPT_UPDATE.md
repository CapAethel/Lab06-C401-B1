# VFCare System Prompt - Vietnamese Update

## Overview
Updated the VFCare agent's system prompt configuration to enable natural, human-like communication with Vietnamese vehicle owners (chủ xe). The agent now communicates as a trusted friend and expert advisor rather than a technical bot.

## Changes Made

### 1. New Prompts Module (`langgraph_agent/prompts.py`)
Created a comprehensive prompts module with context-aware Vietnamese system prompts:

#### Main System Prompt
- **Purpose**: Core instruction for all agent interactions
- **Tone**: Professional yet friendly, like a trusted vehicle advisor
- **Key Features**:
  - Non-technical explanations for complex issues
  - Empathetic and solution-focused approach
  - Balanced between expertise and approachability
  - Builds customer confidence

#### Vehicle Analysis Prompt (`analysis`)
- Used when presenting vehicle inspection results
- Makes complex technical information understandable
- Explains urgency without causing unnecessary panic
- Helps car owners make informed decisions

#### Workshop Suggestion Prompt (`workshop`)
- Used when recommending repair workshops
- Presents workshop as a trusted solution
- Highlights relevant features (distance, rating, expertise)
- Encourages confident booking decision

#### Customer Care Prompt (`care`)
- Used for handling customer concerns and questions
- Emphasizes empathy and customer-centric approach
- Builds long-term relationships
- Respects customer budget and priorities

### 2. Updated LLM Provider (`langgraph_agent/llm_provider.py`)
Enhanced to properly handle system messages:
- Support for `SystemMessage` objects from LangChain
- Proper message format conversion
- Maintains compatibility with OpenAI, Anthropic, and Ollama

### 3. Updated Agent Nodes (`langgraph_agent/nodes.py`)
Integrated Vietnamese system prompts throughout the agent workflow:

#### Workflow Changes
1. **`confirm_to_proceed_node`**
   - Uses `VEHICLE_ANALYSIS_PROMPT`
   - Formats issues using `create_issue_summary()`
   - All interactions in Vietnamese
   
2. **`handle_user_input_node`**
   - Uses `WORKSHOP_SUGGESTION_PROMPT`
   - Presents workshops naturally and confidently
   - Vietnamese prompts for all user inputs

3. **All System Messages**
   - Node log messages in Vietnamese
   - User prompts in Vietnamese
   - Feedback messages in Vietnamese
   - Status indicators in Vietnamese

### 4. Prompt Helper Functions
Created template functions for dynamic prompt generation:

```python
create_analysis_prompt(vehicle_name, mileage_km, issues_text)
create_workshop_prompt(workshop_name, distance_km, rating, time_slot, issues_str)
create_issue_summary(issues)
```

## Key Vietnamese Communication Features

### Language & Tone
- 🇻🇳 Fully Vietnamese interface
- Natural conversational style
- Friendly and trustworthy
- Professional without being cold
- Technical explanations made simple

### Examples of Improved Communication

**Before (English, Technical):**
```
"Vehicle: Unknown (0km)
Detected Issues:
- Battery voltage low (Priority: medium, Risk: 45/100)"
```

**After (Vietnamese, Natural):**
```
"🚗 VF Lạc Hồng (240,000 km)

Mức độ ưu tiên ⭐: Trung bình
Điểm rủi ro: 45/100

Các vấn đề phát hiện được:
- Pin yếu (cần kiểm tra), độ lo lắng: Trung bình"
```

### User Interaction
- **Issue Analysis**: "Hãy để tôi giải thích tình hình của chiếc xe bạn..."
- **Workshop Suggestion**: "Tôi tìm thấy một xưởng thích hợp cho bạn..."
- **Confirmation**: "Bạn có muốn tiếp tục không?" (instead of "Do you want to proceed?")

## System Prompt Configuration

### How to Use Different Prompts

```python
from langgraph_agent.prompts import get_system_prompt

# Get main system prompt
main_prompt = get_system_prompt("main")

# Get specific prompts
analysis_prompt = get_system_prompt("analysis")
workshop_prompt = get_system_prompt("workshop")
care_prompt = get_system_prompt("care")
```

### Integration with LLM

```python
from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(content=get_system_prompt("analysis")),
    HumanMessage(content=user_query)
]

response = llm.invoke(messages)
```

## Configuration Options

### Environment Variables
To customize behavior, use OpenAI environment variables:

```bash
export OPENAI_API_KEY=your_key
export OPENAI_MODEL=gpt-4o-mini  # or other OpenAI models
export LLM_PROVIDER=openai
```

### Temperature Settings
Default temperature: **0.7**
- Balances between consistency and creativity
- Maintains professional tone while sounding natural

### Alternative Models
The system works with:
- ✅ OpenAI (gpt-4o-mini, gpt-4o, gpt-4-turbo)
- ✅ Anthropic Claude
- ✅ Ollama local models

## Benefits of Updated Prompts

1. **More Human-Like Interaction**: Customers feel they're talking to a friend, not a bot
2. **Better Understanding**: Complex technical issues explained simply
3. **Increased Confidence**: Customer feels assured about decisions
4. **Higher Conversion**: Natural recommendations lead to more bookings
5. **Reduced Anxiety**: Calm, supportive tone reduces concerns about repairs
6. **Cultural Relevance**: Vietnamese language and business practices respected

## Testing the Updated Prompts

### Run the Agent with Vietnamese Prompts
```bash
cd VFCare
python -m langgraph_agent
```

### Expected Output
- ✅ All agent messages in Vietnamese
- ✅ Natural, conversational tone
- ✅ System prompts properly applied
- ✅ LLM responses influenced by context-aware prompts

## Files Modified

- ✅ `langgraph_agent/prompts.py` - NEW (comprehensive prompt templates)
- ✅ `langgraph_agent/nodes.py` - Updated (integrated Vietnamese prompts)
- ✅ `langgraph_agent/llm_provider.py` - Updated (enhanced message handling)
- ✅ `ui/cli_interface.py` - Already bilingual (Vietnamese labels exist)

## Next Steps

1. **Test Prompts**: Run the agent and verify natural communication
2. **Fine-tune Templates**: Adjust prompts based on user feedback
3. **Add More Scenarios**: Create prompts for edge cases
4. **Multilingual Support**: Add English, Chinese templates if needed
5. **Monitor Quality**: Track LLM response quality metrics

## Customization Guide

To modify prompts for your needs:

1. Edit `langgraph_agent/prompts.py`
2. Update the prompt strings
3. Re-run the agent
4. Test with sample inputs

Example customization:
```python
SYSTEM_PROMPT = """Bạn là một chuyên gia tư vấn bảo dưỡng xe ô tô [YOUR CUSTOM INSTRUCTION]"""
```

