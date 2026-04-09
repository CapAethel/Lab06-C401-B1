"""LLM provider abstraction for VFCare Agent"""
from typing import Any
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage


def get_llm() -> Any:
    """Get LLM instance based on provider configuration"""
    from .config import get_llm_config
    
    config = get_llm_config()
    
    if config.provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=config.model,
            api_key=config.api_key,
            temperature=config.temperature,
        )
    
    elif config.provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=config.model,
            api_key=config.api_key,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )
    
    elif config.provider == "ollama":
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(
            model=config.model,
            base_url=config.base_url,
            temperature=config.temperature,
        )
    
    else:
        raise ValueError(f"Unknown LLM provider: {config.provider}")


def call_llm(llm: Any, messages: list[BaseMessage] | str) -> str:
    """Call LLM and return response text
    
    Args:
        llm: LLM instance
        messages: Either a list of BaseMessage objects or a string
        
    Returns:
        Response text from the LLM
    """
    if isinstance(messages, str):
        messages = [HumanMessage(content=messages)]
    elif isinstance(messages, list) and all(isinstance(m, dict) for m in messages):
        # Convert dict messages to proper BaseMessage objects
        converted = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role == "system":
                converted.append(SystemMessage(content=content))
            elif role == "assistant":
                from langchain_core.messages import AIMessage
                converted.append(AIMessage(content=content))
            else:
                converted.append(HumanMessage(content=content))
        messages = converted
    
    response = llm.invoke(messages)
    
    if hasattr(response, 'content'):
        return response.content
    return str(response)
