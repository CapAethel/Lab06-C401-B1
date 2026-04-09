# 🚀 VFCare LangGraph Setup Guide

## Bước 1: Chuẩn bị môi trường

### 1a. Clone hoặc tập trung vào folder VFCare

```bash
cd /Users/huyenchu/Vinuni/day06/VFCare
```

### 1b. Kiểm tra Python version

```bash
python3 --version
# Cần Python 3.9+
```

## Bước 2: Cài đặt Dependencies

### Cách 1: Auto Setup (Recommended)

```bash
# Run interactive setup script
python3 setup_langgraph.py
```

**Điều này sẽ:**
- Hỏi LLM provider (openai/anthropic/ollama)
- Yêu cầu API key
- Tạo .env file tự động
- Kiểm tra dependencies

### Cách 2: Manual Setup

```bash
# Copy template
cp .env.example .env

# Edit .env với text editor
nano .env  # hoặc dùng editor yêu thích

# Cài dependencies
pip install -r requirements.txt
```

## Bước 3: Cấu hình API

### Option A: OpenAI (GPT-4o-mini)

1. Lấy API key từ https://platform.openai.com/api-keys
2. Edit `.env`:
   ```env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-xxxx...
   OPENAI_MODEL=gpt-4o-mini
   ```
3. Test:
   ```bash
   python3 -c "import openai; print('✅ OpenAI OK')"
   ```

### Option B: Anthropic (Claude)

1. Lấy API key từ https://console.anthropic.com
2. Edit `.env`:
   ```env
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=sk-ant-xxxx...
   ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
   ```
3. Test:
   ```bash
   python3 -c "import anthropic; print('✅ Anthropic OK')"
   ```

### Option C: Ollama (Local)

1. Install Ollama từ https://ollama.ai
2. Start Ollama:
   ```bash
   ollama serve
   ```
3. Tải model (trong terminal khác):
   ```bash
   ollama pull llama2
   ```
4. Edit `.env`:
   ```env
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   ```

## Bước 4: Kiểm tra Setup

```bash
# Test LLM provider
python3 -c "
from dotenv import load_dotenv
load_dotenv()
from langgraph_agent.config import get_llm_config
cfg = get_llm_config()
print(f'✅ LLM Provider: {cfg.provider}')
print(f'✅ Model: {cfg.model}')
"

# Test LLM initialization
python3 -c "
from dotenv import load_dotenv
load_dotenv()
from langgraph_agent.llm_provider import get_llm
llm = get_llm()
print(f'✅ LLM initialized successfully')
"

# Test configuration
python3 -c "
from dotenv import load_dotenv
load_dotenv()
from langgraph_agent.config import get_vfcare_config
cfg = get_vfcare_config()
print(f'✅ VFCare config loaded')
print(f'   Vehicle: {cfg.vehicle_name}')
print(f'   Data dir: {cfg.data_dir}')
"
```

## Bước 5: Chạy Agent

### Chạy LangGraph Agent

```bash
python3 langgraph_agent/agent.py
```

**Output:**
```
============================================================
🚗 VFCare LangGraph Agent - Running Demo
============================================================

[NODE] Loading vehicle...
[NODE] Analyzing vehicle with LLM...
[NODE] Detecting issues...
...
============================================================
📊 EXECUTION RESULTS
============================================================

🚗 Vehicle: VF Lạc Hồng
   Mileage: 45,230 km
   Battery Health: 88%

📈 Analysis:
   Priority: MEDIUM
   Risk Score: 16.8/100
   ...

✅ Demo completed!
```

## Configuration Files Explained

### .env File

```env
# LLM Settings (chọn 1)
LLM_PROVIDER=openai                          # Provider: openai/anthropic/ollama
OPENAI_API_KEY=sk-xxxx...                    # OpenAI API Key (Protected!)
OPENAI_MODEL=gpt-4o-mini                     # Model name

# VFCare Settings  
VEHICLE_ID=VF_LAC_HONG_001                   # Vehicle ID
VEHICLE_NAME=VF Lạc Hồng                     # Display name

# Data Paths
DATA_DIR=./data                              # Data directory
FEEDBACK_DIR=./data                          # Feedback directory

# Thresholds (tunable)
CRITICAL_RISK_THRESHOLD=75                   # Ngưỡng critical
MEDIUM_RISK_THRESHOLD=40                     # Ngưỡng medium
DEFER_DAYS_MEDIUM=5                          # Hoãn medium issues

# Debug
DEBUG=false                                  # Enable debug mode
LOG_LEVEL=INFO                               # Log level
```

### requirements.txt

```
langchain>=0.1.0               # LangChain core
langgraph>=0.0.48              # LangGraph framework  
openai>=1.12.0                 # OpenAI API
anthropic>=0.21.0              # Anthropic API
python-dotenv>=1.0.0           # Environment variables
pydantic>=2.0.0                # Data validation
requests>=2.31.0               # HTTP library
```

## Security Best Practices

### ✅ DO:

1. **Keep .env in .gitignore**
   ```bash
   echo ".env" >> .gitignore
   git rm --cached .env  # If already committed
   ```

2. **Use .env.example as template**
   ```bash
   cat .env.example > .env
   # Then edit with your keys
   ```

3. **Rotate API keys regularly**
   ```bash
   # Update key in .env
   # No restart needed - loads on each run
   ```

4. **Use environment variables only**
   ```python
   api_key = os.getenv("OPENAI_API_KEY")  # ✅ Good
   api_key = "sk-xxxx..."                 # ❌ Bad
   ```

### ❌ DON'T:

1. **Commit .env to git**
2. **Print API keys in logs**
3. **Share .env file**
4. **Use same key for multiple services**
5. **Store keys in source code**

## File Structure

```
VFCare/
├── langgraph_agent/                    # LangGraph version
│   ├── __init__.py                     # Package init
│   ├── agent.py                        # Main entry point (366 lines)
│   ├── config.py                       # Config from .env (131 lines)
│   ├── llm_provider.py                 # LLM abstraction (47 lines)
│   ├── nodes.py                        # Graph nodes (420 lines)
│   ├── state.py                        # State definition (85 lines)
│   └── tools.py                        # Tool functions (230 lines)
│
├── .env                                # Your secrets (git ignored)
├── .env.example                        # Template
├── requirements.txt                    # Dependencies
├── setup_langgraph.py                  # Setup script
├── LANGGRAPH_README.md                 # This guide
│
├── data/                               # Existing data
│   ├── vehicle_status.json
│   ├── maintenance_rules.json
│   ├── workshops.json
│   └── user_feedback.json
│
└── tools/                              # Existing modules
```

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'langchain'"

**Solution:**
```bash
pip install -r requirements.txt
# or
pip install langchain langgraph langchain-openai python-dotenv
```

### Issue: "API key not found" / "Invalid API key"

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check key is set
grep OPENAI_API_KEY .env

# Verify format
# Should be: OPENAI_API_KEY=sk-xxxx (no quotes)
```

### Issue: "Connection refused" on localhost

**Solution (for Ollama):**
```bash
# In another terminal, start Ollama
ollama serve

# In .env, check URL
OLLAMA_BASE_URL=http://localhost:11434

# Load a model
ollama pull llama2
```

### Issue: Rate limit error

**Solution:**
```bash
# Wait a moment and try again
# Or switch to another provider
# Or reduce API usage
```

## Testing Each Component

### Test 1: LLM Provider

```bash
python3 << 'EOF'
from dotenv import load_dotenv
load_dotenv()

from langgraph_agent.llm_provider import get_llm, call_llm

llm = get_llm()
response = call_llm(llm, "What is vehicle maintenance?")
print(f"✅ LLM Response: {response[:100]}...")
EOF
```

### Test 2: Configuration

```bash
python3 << 'EOF'
from dotenv import load_dotenv
load_dotenv()

from langgraph_agent.config import (
    get_llm_config,
    get_vfcare_config,
    get_threshold_config
)

llm_cfg = get_llm_config()
vf_cfg = get_vfcare_config()
thresh = get_threshold_config()

print(f"✅ LLM: {llm_cfg.provider} / {llm_cfg.model}")
print(f"✅ Vehicle: {vf_cfg.vehicle_name}")
print(f"✅ Threshold: {thresh.critical_risk_threshold}")
EOF
```

### Test 3: Full Agent

```bash
python3 langgraph_agent/agent.py
```

## Next Steps

1. ✅ Setup .env with API key
2. ✅ Install dependencies
3. ✅ Run agent: `python3 langgraph_agent/agent.py`
4. 🔄 Extend with custom nodes
5. 🔄 Add tool calling
6. 🔄 Integrate with frontend

## Support

- Check [LANGGRAPH_README.md](LANGGRAPH_README.md) for full docs
- Review [.env.example](.env.example) for all options
- See [langgraph_agent/config.py](langgraph_agent/config.py) for code

---

**Ready to run!** 🚀

```bash
python3 setup_langgraph.py  # Interactive setup
# or
python3 langgraph_agent/agent.py  # Direct run
```
