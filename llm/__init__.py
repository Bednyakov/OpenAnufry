"""
LLM Provider Module

Модуль для работы с различными LLM провайдерами через единый интерфейс.
Поддерживает OpenAI API, локальные LLM (Ollama, LM Studio, LocalAI, vLLM) и другие.
"""

from .provider import LLMProvider
from .factory import create_llm_provider

__all__ = ["LLMProvider", "create_llm_provider"]
