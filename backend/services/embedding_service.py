from backend.langchain_workflows.embedding_generator import generate_embeddings, batch_embed


class EmbeddingService:
    async def generate(self, text: str) -> list[float]:
        return generate_embeddings(text)

    async def batch_generate(self, texts: list[str]) -> list[list[float]]:
        return await batch_embed(texts)
