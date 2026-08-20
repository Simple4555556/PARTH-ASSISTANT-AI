"""
PARTH ASSISTANT AI — LLM Model Configuration
Configures LLM Providers (Local Hybrid Engine, Gemini, OpenAI) and generation hyper-parameters.
"""

import os
from typing import Dict, Any


class ModelConfig:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "local_hybrid")  # local_hybrid | gemini | openai
        self.model_name = os.getenv("LLM_MODEL", "parth-hybrid-v2")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "512"))
        self.api_key = os.getenv("AI_API_KEY", "")
        self.timeout_seconds = int(os.getenv("LLM_TIMEOUT", "10"))

    def get_config(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout_seconds": self.timeout_seconds
        }


model_config = ModelConfig()
