"""
Фабрика для создания LLM провайдеров
"""

from typing import Optional
from .provider import (
    LLMProvider,
    OpenAIProvider,
    OpenRouterProvider,
    OllamaProvider,
    LMStudioProvider,
    LocalAIProvider,
    VLLMProvider,
    TextGenProvider,
)


# Маппинг провайдеров
PROVIDER_MAP = {
    "openai": OpenAIProvider,
    "openrouter": OpenRouterProvider,
    "ollama": OllamaProvider,
    "lmstudio": LMStudioProvider,
    "localai": LocalAIProvider,
    "vllm": VLLMProvider,
    "textgen": TextGenProvider,
}


def create_llm_provider(
    provider_name: str,
    api_key: str,
    base_url: str,
    model: str,
    temperature: float = 0.1,
    max_tokens: int = 4096,
    timeout: int = 300,
    **kwargs
) -> LLMProvider:
    """
    Создает экземпляр LLM провайдера на основе имени.
    
    Args:
        provider_name: Имя провайдера (openai, ollama, lmstudio и т.д.)
        api_key: API ключ
        base_url: Базовый URL API
        model: Название модели
        temperature: Температура генерации
        max_tokens: Максимальное количество токенов
        timeout: Таймаут запроса в секундах
        **kwargs: Дополнительные параметры
        
    Returns:
        Экземпляр LLMProvider
        
    Raises:
        ValueError: Если провайдер не поддерживается
    """
    provider_name = provider_name.lower()
    
    if provider_name not in PROVIDER_MAP:
        raise ValueError(
            f"Неподдерживаемый провайдер: {provider_name}. "
            f"Доступные провайдеры: {', '.join(PROVIDER_MAP.keys())}"
        )
    
    provider_class = PROVIDER_MAP[provider_name]
    # dev Bednyakov
    return provider_class(
        api_key=api_key,
        base_url=base_url,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        **kwargs
    )


def create_llm_provider_from_config(config: dict) -> LLMProvider:
    """
    Создает провайдера из словаря конфигурации.
    
    Args:
        config: Словарь с конфигурацией провайдера
        
    Returns:
        Экземпляр LLMProvider
    """
    return create_llm_provider(
        provider_name=config.get("provider", "openai"),
        api_key=config.get("api_key", ""),
        base_url=config.get("base_url", "https://api.openai.com/v1"),
        model=config.get("model", "gpt-4"),
        temperature=config.get("temperature", 0.1),
        max_tokens=config.get("max_tokens", 4096),
        timeout=config.get("timeout", 300),
    )
