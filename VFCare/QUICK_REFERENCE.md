# VFCare OpenAI System Prompt - Quick Reference

## 📋 Summary
Updated VFCare agent's system prompts to OpenAI with Vietnamese language support for natural, human-like communication with vehicle owners.

## 🎯 What Changed

### Before ❌
- English system prompts
- Technical, robot-like tone
- Generic LLM instructions
- No context-awareness in prompts

### After ✅
- Vietnamese system prompts
- Friendly, trusted advisor tone  
- Context-specific prompts (analysis, workshop, care)
- SystemMessage integration with OpenAI

## 📁 Files Created/Updated

### ✨ NEW: `langgraph_agent/prompts.py`
```python
# Main prompts for OpenAI
SYSTEM_PROMPT  # Core, friendly advisor tone
VEHICLE_ANALYSIS_PROMPT  # For analyzing vehicle issues
WORKSHOP_SUGGESTION_PROMPT  # For recommending workshops
CUSTOMER_CARE_PROMPT  # For customer support

# Helper functions
get_system_prompt(context)
create_analysis_prompt(...)
create_workshop_prompt(...)
create_issue_summary(...)
```

### 🔄 UPDATED: `langgraph_agent/nodes.py`
```python
# Added imports from prompts
from .prompts import (
    get_system_prompt,
    create_analysis_prompt,
    create_workshop_prompt,
    create_issue_summary
)

# Updated these nodes with Vietnamese + SystemMessage:
- confirm_to_proceed_node()  # Uses analysis prompt
- handle_user_input_node()   # Uses workshop prompt
- All other nodes messages in Vietnamese
```

### 🔧 UPDATED: `langgraph_agent/llm_provider.py`
```python
# Enhanced call_llm() function
- Now handles SystemMessage objects
- Proper LangChain message formatting
- Works with OpenAI, Anthropic, Ollama
```

### 📚 DOCUMENTATION: `SYSTEM_PROMPT_UPDATE.md`
Complete guide with examples and customization instructions.

## 🇻🇳 Vietnamese Communication Examples

### Vehicle Analysis Response
```
Chiếc VF Lạc Hồng của bạn đang chạy được 240,000 km,
hiện tại có một số vấn đề cần xử lý:

1. 🔴 Pin yếu - cần thay thế sớm
   - Rủi ro: 65/100 (Trung bình)
   - Ước tính: 1 tiếng sửa

2. 🟠 Làm sạch bộ lọc không khí
   - Rủi ro: 40/100 (Thấp)
   - Ước tính: 30 phút

Bạn muốn tiếp tục đặt lịch hẹn bảo dưỡng không?
```

### Workshop Suggestion Response
```
Tôi tìm thấy một xưởng thích hợp cho bạn:

🏪 Trung tâm bảo dưỡng Lạc Hồng
   📍 3 km từ vị trí của bạn
   ⭐ 4.8/5 sao
   ⏰ Có sẵn hôm nay lúc 14:00

Xưởng này chuyên sửa chữa pin và bộ lọc,
đúng những vấn đề chiếc xe bạn cần.
Bạn có muốn đặt lịch hẹn không?
```

## 🚀 How It Works

```python
# System message setup for OpenAI
from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(
        content=get_system_prompt("analysis")  # Vietnamese instructions for OpenAI
    ),
    HumanMessage(
        content=create_analysis_prompt(
            vehicle_name="VF Lạc Hồng",
            mileage_km=240000,
            issues_text="..."
        )
    )
]

# OpenAI now responds with:
# - Vietnamese language
# - Friendly, natural tone
# - Clear, non-technical explanations
response = openai_llm.invoke(messages)
```

## 💡 Key Features

| Feature | Before | After |
|---------|--------|-------|
| **Language** | English | Vietnamese 🇻🇳 |
| **Tone** | Technical/Formal | Friendly/Natural |
| **Prompts** | Generic | Context-specific |
| **System Msgs** | Inline strings | Structured prompts |
| **Customer Feel** | Bot-like | Human-like friend |

## 🔍 Testing

Run the agent to see updates:
```bash
cd /Users/huyenchu/Vinuni/day06/VFCare
python -m langgraph_agent
```

Expected output:
✅ All Vietnamese  
✅ Friendly tone  
✅ System prompts applied  
✅ Natural recommendations  

## 📚 Customization

To modify prompts:
1. Edit `langgraph_agent/prompts.py`
2. Update SYSTEM_PROMPT or create new functions
3. Re-run agent
4. Test with sample vehicle data

Example:
```python
SYSTEM_PROMPT = """Bạn là một chuyên gia tư vấn bảo dưỡng xe...
[YOUR CUSTOM INSTRUCTIONS HERE]
"""
```

## ✨ Benefits

✅ **Better Customer Experience** - Feels like talking to a friend
✅ **Increased Conversions** - Natural tone leads to more bookings  
✅ **Reduced Anxiety** - Calm, supportive tone reassures customers
✅ **Clear Communication** - Complex issues explained simply
✅ **Cultural Relevance** - Vietnamese language respected
✅ **Flexible** - Easy to customize prompts per need

## 📦 Module Organization

```
langgraph_agent/
├── prompts.py          ← NEW (Vietnamese prompts)
├── nodes.py            ← UPDATED (uses prompts)
├── llm_provider.py     ← UPDATED (SystemMessage support)
├── config.py           ← No changes needed
├── state.py            ← No changes needed
└── tools.py            ← No changes needed
```

---

**Status**: ✅ Complete and Ready for Testing
**Last Update**: 2026-04-09
**Language Support**: Vietnamese (English templates available if needed)
