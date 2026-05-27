from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from backend.utils.config import get_settings

settings = get_settings()


class LLMService:
    def __init__(self):
        self._instances: dict[str, ChatOpenAI | ChatAnthropic] = {}

    def get_llm(self, provider: str | None = None) -> ChatOpenAI | ChatAnthropic:
        provider = provider or settings.default_llm
        if provider not in self._instances:
            if provider == "openai":
                self._instances[provider] = ChatOpenAI(
                    model=settings.chat_model,
                    temperature=settings.temperature,
                    max_tokens=settings.max_tokens,
                    openai_api_key=settings.openai_api_key,
                )
            elif provider == "anthropic":
                self._instances[provider] = ChatAnthropic(
                    model="claude-3-opus-20240229",
                    temperature=settings.temperature,
                    max_tokens=settings.max_tokens,
                    anthropic_api_key=settings.anthropic_api_key,
                )
            else:
                raise ValueError(f"Unsupported LLM provider: {provider}")
        return self._instances[provider]
