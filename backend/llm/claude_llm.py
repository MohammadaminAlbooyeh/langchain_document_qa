from langchain_anthropic import ChatAnthropic
from backend.utils.config import get_settings

settings = get_settings()


class ClaudeLLM:
    def __init__(self, model: str = "claude-3-opus-20240229"):
        self.llm = ChatAnthropic(
            model=model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            anthropic_api_key=settings.anthropic_api_key,
        )

    async def invoke(self, prompt: str) -> str:
        response = await self.llm.ainvoke(prompt)
        return response.content

    async def stream(self, prompt: str):
        async for chunk in self.llm.astream(prompt):
            yield chunk.content
