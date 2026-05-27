from backend.langchain_workflows.vector_store_manager import search_similar, store_embeddings


class VectorDBService:
    async def search(self, query: str, k: int = 5) -> list[tuple[str, float]]:
        return await search_similar(query, k)

    async def store(self, chunks: list[str], metadatas: list[dict] | None = None) -> list[str]:
        return await store_embeddings(chunks, metadatas)
