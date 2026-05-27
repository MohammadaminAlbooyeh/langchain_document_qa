from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from backend.utils.config import get_settings

settings = get_settings()

embeddings = OpenAIEmbeddings(
    model=settings.embedding_model,
    openai_api_key=settings.openai_api_key,
)


class ChromaStore:
    def __init__(self, collection_name: str = "documents"):
        self.store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory="./chroma_db",
        )

    async def add_texts(self, texts: list[str], metadatas: list[dict] | None = None) -> list[str]:
        return await self.store.aadd_texts(texts, metadatas=metadatas)

    async def similarity_search(self, query: str, k: int = 5) -> list[tuple[str, float]]:
        results = await self.store.asimilarity_search_with_relevance_scores(query, k=k)
        return [(doc.page_content, score) for doc, score in results]

    async def delete(self, ids: list[str]):
        await self.store.adelete(ids)
