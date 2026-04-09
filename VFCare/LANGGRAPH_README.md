# 🤖 VFCare LangGraph Agent

## Tổng quan

VFCare Agent đã được nâng cấp để sử dụng **LangGraph** - một framework mạnh mẽ để xây dựng agentic workflows với LLM. Hệ thống giờ kết hợp:

- **LangGraph**: Quản lý workflow theo node/edge
- **LLM Integration**: Sử dụng OpenAI, Anthropic, hoặc Ollama
- **Environment Variables**: Bảo vệ các giá trị nhạy cảm (API keys)
- **Persistent State**: Theo dõi state qua các nodes

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│         LangGraph State Machine                     │
│                                                     │
│  [load_vehicle]                                    │
│        ↓                                            │
│  [analyze_vehicle] ← LLM reasoning                 │
│        ↓                                            │
│  [detect_issues]                                   │
│        ↓                                            │
│  [calculate_priority]                              │
│        ↓                                            │
│  [generate_recommendations] ← LLM reasoning        │
│        ↓                                            │
│  [suggest_workshops]                               │
│        ↓                                            │
│  [handle_user_input] ← LLM confirmation            │
│        ↓                                            │
│  [book_appointment]                                │
│        ↓                                            │
│  [save_feedback]                                   │
│        ↓                                            │
│       [END]                                        │
│                                                     │
│  State flows through each node with context       │
└─────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
VFCare/
├── langgraph_agent/          # LangGraph version
│   ├── __init__.py
│   ├── agent.py              # Main LangGraph agent (entry point)
│   ├── config.py             # Configuration from .env
│   ├── llm_provider.py       # LLM abstraction layer
│   ├── nodes.py              # LangGraph nodes (with LLM)
│   ├── state.py              # State definition
│   └── tools.py              # Tool definitions
├── .env.example              # Environment variables template
├── requirements.txt          # Python dependencies
├── setup_langgraph.py        # Setup script
└── tools/                    # Existing tools (maintained)
    ├── issue_detector.py
    ├── priority_calculator.py
    ├── recommendation_engine.py
    ├── workshop_suggester.py
    ├── feedback_manager.py
    └── utils.py
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
cd /Users/huyenchu/Vinuni/day06/VFCare

# Run setup script (interactive)
python3 setup_langgraph.py
```

Hoặc tạo `.env` manually:

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Agent

```bash
# Run LangGraph agent
python3 langgraph_agent/agent.py
```

## 🔑 Environment Variables

### LLM Configuration

**OpenAI:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxxx...
OPENAI_MODEL=gpt-4o-mini
```

**Anthropic:**
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-xxxx...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**Ollama (Local):**
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

### VFCare Configuration

```env
VEHICLE_ID=VF_LAC_HONG_001
VEHICLE_NAME=VF Lạc Hồng

DATA_DIR=./data
FEEDBACK_DIR=./data
RULES_FILE=./data/maintenance_rules.json
WORKSHOPS_FILE=./data/workshops.json
VEHICLE_STATUS_FILE=./data/vehicle_status.json
FEEDBACK_FILE=./data/user_feedback.json
```

### Thresholds (Tunable)

```env
CRITICAL_RISK_THRESHOLD=75
MEDIUM_RISK_THRESHOLD=40
DEFER_DAYS_MEDIUM=5
DEFER_DAYS_LOW=30
```

## 🧠 Key Features

### 1. **LLM-Powered Nodes**

Mỗi node có thể sử dụng LLM để reasoning:

```python
# In analyze_vehicle_node:
analysis = call_llm(llm, vehicle_summary)
state.add_message("assistant", analysis)
```

### 2. **State Management**

State được duy trì qua các nodes:

```python
@dataclass
class VFCareGraphState:
    vehicle_data: dict
    detected_issues: list
    vehicle_priority: str
    risk_score: float
    messages: list  # Conversation history
    # ... more fields
```

### 3. **Environment Security**

Tất cả API keys và sensitive data được lưu trong `.env`:

```python
api_key = os.getenv("OPENAI_API_KEY")  # Protected
```

### 4. **Fallback Support**

Support cho nhiều LLM providers:

```python
if provider == "openai":
    return ChatOpenAI(...)
elif provider == "anthropic":
    return ChatAnthropic(...)
elif provider == "ollama":
    return ChatOllama(...)
```

## 💬 LLM Integration Points

LLM được gọi tại các điểm chính:

1. **analyze_vehicle**: Phân tích ban đầu về tình trạng xe
2. **detect_issues**: Tóm tắt các vấn đề được phát hiện
3. **calculate_priority**: Giải thích lý do prioritization
4. **generate_recommendations**: Tạo action items
5. **suggest_workshops**: Xếp hạng và gợi ý xưởng
6. **handle_user_input**: Xác nhận booking

## 📝 Configuration Files

### .env.example
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4o-mini
VEHICLE_ID=VF_LAC_HONG_001
VEHICLE_NAME=VF Lạc Hồng
DEBUG=false
LOG_LEVEL=INFO
...
```

### requirements.txt
```
langchain>=0.1.0
langgraph>=0.0.48
openai>=1.12.0
anthropic>=0.21.0
python-dotenv>=1.0.0
pydantic>=2.0.0
requests>=2.31.0
```

## 🔄 Workflow Flow

```
1. User runs: python3 langgraph_agent/agent.py
   ↓
2. Load environment from .env
   ↓
3. Initialize LLM based on LLM_PROVIDER
   ↓
4. Graph processes through nodes:
   - load_vehicle: Load data from JSON
   - analyze_vehicle: LLM analyzes status
   - detect_issues: Find issues using rules
   - calculate_priority: Compute priority & risk
   - generate_recommendations: LLM creates actions
   - suggest_workshops: Rank workshops
   - handle_user_input: LLM confirms choice
   - book_appointment: Save booking
   - save_feedback: Store to JSON
   ↓
5. Return final state with results
```

## 🛠️ API Reference

### VFCareGraphAgent

```python
from langgraph_agent import VFCareGraphAgent

# Create agent
agent = VFCareGraphAgent()

# Run demo
state = agent.run()
```

### Configuration Access

```python
from langgraph_agent.config import (
    get_llm_config,
    get_vfcare_config,
    get_threshold_config
)

llm_cfg = get_llm_config()  # LLM settings
vf_cfg = get_vfcare_config()  # VFCare settings
thresh_cfg = get_threshold_config()  # Thresholds
```

### LLM Provider

```python
from langgraph_agent.llm_provider import get_llm, call_llm

llm = get_llm()
response = call_llm(llm, "Your prompt here")
```

## 🧪 Testing

```bash
# Test LLM connection
python3 -c "
from langgraph_agent.llm_provider import get_llm
llm = get_llm()
print('✅ LLM initialized:', llm.model_name)
"

# Test configuration
python3 -c "
from langgraph_agent.config import get_llm_config
cfg = get_llm_config()
print('Provider:', cfg.provider)
print('Model:', cfg.model)
"

# Run full agent
python3 langgraph_agent/agent.py
```

## 🔐 Security Best Practices

1. **Never commit .env file**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use .env.example as template**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Rotate API keys regularly**
   ```
   Update OPENAI_API_KEY in .env when rotated
   ```

4. **Use minimal permissions**
   ```
   Only needed scopes in API keys
   ```

## 📊 Output Example

```
============================================================
🚗 VFCare LangGraph Agent - Running Demo
============================================================

... (processing nodes) ...

============================================================
📊 EXECUTION RESULTS
============================================================

🚗 Vehicle: VF Lạc Hồng
   Mileage: 45,230 km
   Battery Health: 88%

📈 Analysis:
   Priority: MEDIUM
   Risk Score: 16.8/100
   Issues Found: 6

💡 Recommendations:
   Urgency: SOON
   Message: Nên kiểm tra sớm...

✅ Booking:
   Workshop: VFCare Hà Nội - Hoàng Mai
   Date: 2026-04-09
   Time: 10:00-11:00
   Booking ID: FB_20260409...

✅ Demo completed!
============================================================
```

## 🚨 Troubleshooting

### Error: "API key not found"
```
Solution: Check .env file has OPENAI_API_KEY/ANTHROPIC_API_KEY set
```

### Error: "langgraph not installed"
```
Solution: Run: pip install -r requirements.txt
```

### Error: "Ollama connection failed"
```
Solution: Start Ollama: ollama serve
         Check OLLAMA_BASE_URL in .env
```

## 🔄 Comparison: Old vs New

| Feature | Original | LangGraph |
|---------|----------|-----------|
| Architecture | Modular functions | State machine |
| Reasoning | Rule-based | LLM-powered |
| API Keys | Hardcoded | .env protected |
| Conversation | None | Built-in history |
| Workflow | Sequential | Graph nodes |
| Extendability | Limited | Highly extensible |

## 📚 References

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents)
- [OpenAI API](https://platform.openai.com/docs/api-reference)
- [Anthropic API](https://docs.anthropic.com/)

## 🎯 Next Steps

1. Setup .env with your API key
2. Install dependencies
3. Run the agent
4. Extend with custom nodes
5. Add tool calling for more autonomy

---

**VFCare Agent LangGraph Version** - Ready to use! 🚀
