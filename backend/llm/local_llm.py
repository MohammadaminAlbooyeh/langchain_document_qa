from langchain_community.chat_models import ChatOllama


class LocalLLM:
    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.0,
        )

    async def invoke(self, prompt: str) -> str:
        response = await self.llm.ainvoke(prompt)
        return response.content

    async def stream(self, prompt: str):
        async for chunk in self.llm.astream(prompt):
            yield chunk.content
