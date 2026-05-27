from langchain_openai import ChatOpenAI
from backend.utils.config import get_settings

settings = get_settings()


class OpenAILLM:
    def __init__(self, model: str | None = None):
        self.model = model or settings.chat_model
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            openai_api_key=settings.openai_api_key,
        )

    async def invoke(self, prompt: str) -> str:
        response = await self.llm.ainvoke(prompt)
        return response.content

    async def stream(self, prompt: str):
        async for chunk in self.llm.astream(prompt):
            yield chunk.content
