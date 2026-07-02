from backend.llm.llm_factory import LLMFactory
from backend.utils.config import get_settings

settings = get_settings()


class LLMService:
    def __init__(self):
        self._factory = LLMFactory()
        self._instances: dict[str, object] = {}

    def get_llm(self, provider: str | None = None):
        provider = provider or settings.default_llm
        if provider not in self._instances:
            self._instances[provider] = self._factory.create_llm(provider)
        return self._instances[provider]
