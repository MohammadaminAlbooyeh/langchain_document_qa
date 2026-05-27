from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from backend.llm.openai_llm import OpenAILLM
from backend.llm.claude_llm import ClaudeLLM
from backend.llm.local_llm import LocalLLM
from backend.utils.config import get_settings


class LLMFactory:
    def __init__(self):
        self.settings = get_settings()

    def create_llm(self, provider: str | None = None):
        provider = provider or self.settings.default_llm
        if provider == "openai":
            return OpenAILLM()
        elif provider == "anthropic":
            return ClaudeLLM()
        elif provider == "local":
            return LocalLLM()
        raise ValueError(f"Unknown provider: {provider}")
