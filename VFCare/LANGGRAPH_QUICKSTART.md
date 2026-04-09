# ⚡ VFCare LangGraph - Quick Start (5 minutes)

## 1️⃣ Install & Configure (2 min)

```bash
cd /Users/huyenchu/Vinuni/day06/VFCare

# Install dependencies
pip install -r requirements.txt

# Interactive setup (picks LLM, gets API key)
python3 setup_langgraph.py
```

**Choose your LLM:**
- `openai` - GPT-4o-mini ($0.15 per 1M tokens, free trial available)
- `anthropic` - Claude ($3 per 1M tokens)
- `ollama` - Local LLM (free, requires local install)

## 2️⃣ Run Agent (2 min)

```bash
python3 langgraph_agent/agent.py
```

**Expected output:**
```
🚗 VFCare LangGraph Agent

[NODE] Loading vehicle... ✓
[NODE] Analyzing with LLM... ✓
[NODE] Detecting issues... ✓
[NODE] Calculating priority... ✓
...
📊 Results:
   Vehicle: VF Lạc Hồng
   Issues: 6 detected
   Priority: MEDIUM
   Risk Score: 16.8/100
```

## 3️⃣ Test Components (1 min)

```bash
# Test LLM connection
python3 -c "
from dotenv import load_dotenv; load_dotenv()
from langgraph_agent.llm_provider import get_llm
llm = get_llm()
print('✅ LLM OK')
"

# Test agent imports
python3 -c "
from langgraph_agent.agent import VFCareGraphAgent
print('✅ Agent OK')
"
```

## What Just Happened?

1. **setup_langgraph.py** configured your LLM provider + API key
2. **.env file** created with your secrets (git-ignored)
3. **agent.py** ran the workflow:
   - Load vehicle data
   - Analyze with LLM
   - Detect issues
   - Calculate priority
   - Generate recommendations (with LLM)
   - Find workshops
   - Save feedback

## ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'langchain'` | `pip install -r requirements.txt` |
| `API key not found` | Run `python3 setup_langgraph.py` again |
| `Connection refused` (Ollama) | Run `ollama serve` in another terminal |
| `Rate limited` | Wait 60s or use different LLM provider |

## 📖 Next: Full Setup Guide

For more details, see [LANGGRAPH_SETUP.md](LANGGRAPH_SETUP.md)

## 🎯 Next Steps

- Extend with custom nodes: Edit `langgraph_agent/nodes.py`
- Add more tools: Edit `langgraph_agent/tools.py`
- Integrate UI: Create `ui/langgraph_cli.py`
- Deploy: Package with `python setup.py bdist_wheel`

---

**That's it!** You now have a LangGraph-powered vehicle maintenance agent. 🚀

For full docs: `cat LANGGRAPH_README.md`
