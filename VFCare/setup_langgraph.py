#!/usr/bin/env python3
"""Setup for LangGraph Version - Creates .env file"""
import os
import sys
from pathlib import Path


def setup_env():
    """Create and configure .env file"""
    project_root = Path(__file__).parent
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    print("🔧 VFCare LangGraph Setup")
    print("="*60)
    
    # Check if .env exists
    if env_file.exists():
        print(f"✅ .env file already exists at {env_file}")
        response = input("Do you want to overwrite it? (y/n): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    # Load example
    if env_example.exists():
        with open(env_example, 'r') as f:
            example_content = f.read()
    else:
        print("❌ .env.example not found. Please create .env manually.")
        return
    
    # Ask for configuration
    print("\n📝 Configuration:")
    print("\n1. LLM Provider (default: openai)")
    print("   Options: openai, anthropic, ollama")
    llm_provider = input("   LLM Provider [openai]: ").strip().lower() or "openai"
    
    if llm_provider == "openai":
        api_key = input("   OpenAI API Key: ").strip()
        model = input("   Model [gpt-4o-mini]: ").strip() or "gpt-4o-mini"
    elif llm_provider == "anthropic":
        api_key = input("   Anthropic API Key: ").strip()
        model = input("   Model [claude-3-5-sonnet-20241022]: ").strip() or "claude-3-5-sonnet-20241022"
    elif llm_provider == "ollama":
        api_key = ""
        base_url = input("   Ollama Base URL [http://localhost:11434]: ").strip() or "http://localhost:11434"
        model = input("   Model [llama2]: ").strip() or "llama2"
    else:
        print(f"❌ Unknown provider: {llm_provider}")
        return
    
    # Create .env content
    env_content = example_content
    env_content = env_content.replace("LLM_PROVIDER=openai", f"LLM_PROVIDER={llm_provider}")
    
    if llm_provider == "openai":
        env_content = env_content.replace("OPENAI_API_KEY=sk-your-api-key-here", f"OPENAI_API_KEY={api_key}")
        env_content = env_content.replace("OPENAI_MODEL=gpt-4o-mini", f"OPENAI_MODEL={model}")
    elif llm_provider == "anthropic":
        env_content = env_content.replace("ANTHROPIC_API_KEY=sk-ant-your-key-here", f"ANTHROPIC_API_KEY={api_key}")
        env_content = env_content.replace("ANTHROPIC_MODEL=claude-3-5-sonnet-20241022", f"ANTHROPIC_MODEL={model}")
    elif llm_provider == "ollama":
        env_content = env_content.replace("OLLAMA_BASE_URL=http://localhost:11434", f"OLLAMA_BASE_URL={base_url}")
        env_content = env_content.replace("OLLAMA_MODEL=llama2", f"OLLAMA_MODEL={model}")
    
    # Save .env
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ .env file created at {env_file}")
    print(f"\n📋 Summary:")
    print(f"   LLM Provider: {llm_provider}")
    print(f"   Model: {model}")
    print(f"   API Key: {'***' + api_key[-10:] if api_key else 'N/A'}")
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    try:
        import langgraph
        print("   ✅ langgraph")
    except ImportError:
        print("   ❌ langgraph - Run: pip install langgraph")
    
    try:
        import langchain_core
        print("   ✅ langchain-core")
    except ImportError:
        print("   ❌ langchain-core - Run: pip install langchain-core")
    
    try:
        if llm_provider == "openai":
            import langchain_openai
            print("   ✅ langchain-openai")
        elif llm_provider == "anthropic":
            import langchain_anthropic
            print("   ✅ langchain-anthropic")
    except ImportError:
        print(f"   ❌ langchain-{llm_provider} - Run: pip install langchain-{llm_provider}")
    
    print("\n" + "="*60)
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Run the agent: python3 langgraph_agent/agent.py")
    print("="*60)


if __name__ == "__main__":
    setup_env()
