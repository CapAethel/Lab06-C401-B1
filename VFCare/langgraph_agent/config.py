"""Configuration module for VFCare LangGraph Agent"""
import os
from typing import Literal
from pydantic import BaseModel
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class LLMConfig(BaseModel):
    """LLM Configuration"""
    provider: Literal["openai", "anthropic", "ollama"] = "openai"
    model: str = "gpt-4o-mini"
    api_key: str | None = None
    base_url: str | None = None
    temperature: float = 0.7
    max_tokens: int = 2048


class VFCareConfig(BaseModel):
    """VFCare Configuration"""
    vehicle_id: str = "VF_LAC_HONG_001"
    vehicle_name: str = "VF Lạc Hồng"
    data_dir: str = "./data"
    feedback_dir: str = "./data"
    debug: bool = False
    log_level: str = "INFO"
    max_iterations: int = 10
    timeout: int = 30


class ThresholdConfig(BaseModel):
    """Risk and Priority Thresholds"""
    critical_risk_threshold: float = 75.0
    medium_risk_threshold: float = 40.0
    critical_task_hours: float = 1.5
    medium_task_hours: float = 3.0
    defer_days_medium: int = 5
    defer_days_low: int = 30


def load_llm_config() -> LLMConfig:
    """Load LLM configuration from environment"""
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider == "openai":
        return LLMConfig(
            provider="openai",
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    elif provider == "anthropic":
        return LLMConfig(
            provider="anthropic",
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    elif provider == "ollama":
        return LLMConfig(
            provider="ollama",
            model=os.getenv("OLLAMA_MODEL", "llama2"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


def load_vfcare_config() -> VFCareConfig:
    """Load VFCare configuration from environment"""
    return VFCareConfig(
        vehicle_id=os.getenv("VEHICLE_ID", "VF_LAC_HONG_001"),
        vehicle_name=os.getenv("VEHICLE_NAME", "VF Lạc Hồng"),
        data_dir=os.getenv("DATA_DIR", "./data"),
        feedback_dir=os.getenv("FEEDBACK_DIR", "./data"),
        debug=os.getenv("DEBUG", "false").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        max_iterations=int(os.getenv("MAX_ITERATIONS", "10")),
        timeout=int(os.getenv("TIMEOUT", "30")),
    )


def load_threshold_config() -> ThresholdConfig:
    """Load threshold configuration from environment"""
    return ThresholdConfig(
        critical_risk_threshold=float(os.getenv("CRITICAL_RISK_THRESHOLD", "75")),
        medium_risk_threshold=float(os.getenv("MEDIUM_RISK_THRESHOLD", "40")),
        critical_task_hours=float(os.getenv("CRITICAL_TASK_HOURS", "1.5")),
        medium_task_hours=float(os.getenv("MEDIUM_TASK_HOURS", "3")),
        defer_days_medium=int(os.getenv("DEFER_DAYS_MEDIUM", "5")),
        defer_days_low=int(os.getenv("DEFER_DAYS_LOW", "30")),
    )


def get_data_file_path(filename: str) -> str:
    """Get full path to data file"""
    data_dir = os.getenv("DATA_DIR", "./data")
    return os.path.join(data_dir, filename)


# Singleton instances
_llm_config: LLMConfig | None = None
_vfcare_config: VFCareConfig | None = None
_threshold_config: ThresholdConfig | None = None


def get_llm_config() -> LLMConfig:
    """Get LLM config (cached)"""
    global _llm_config
    if _llm_config is None:
        _llm_config = load_llm_config()
    return _llm_config


def get_vfcare_config() -> VFCareConfig:
    """Get VFCare config (cached)"""
    global _vfcare_config
    if _vfcare_config is None:
        _vfcare_config = load_vfcare_config()
    return _vfcare_config


def get_threshold_config() -> ThresholdConfig:
    """Get threshold config (cached)"""
    global _threshold_config
    if _threshold_config is None:
        _threshold_config = load_threshold_config()
    return _threshold_config
