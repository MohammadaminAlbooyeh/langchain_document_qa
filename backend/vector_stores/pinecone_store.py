from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from backend.utils.config import get_settings

settings = get_settings()

embeddings = OpenAIEmbeddings(
    model=settings.embedding_model,
    openai_api_key=settings.openai_api_key,
)


class PineconeStore:
    def __init__(self, index_name: str | None = None):
        self.index_name = index_name or settings.pinecone_index_name
        self.store = PineconeVectorStore(
            index_name=self.index_name,
            embedding=embeddings,
        )

    async def add_texts(self, texts: list[str], metadatas: list[dict] | None = None) -> list[str]:
        return await self.store.aadd_texts(texts, metadatas=metadatas)

    async def similarity_search(self, query: str, k: int = 5) -> list[tuple[str, float]]:
        results = await self.store.asimilarity_search_with_relevance_scores(query, k=k)
        return [(doc.page_content, score) for doc, score in results]

    async def delete(self, ids: list[str]):
        await self.store.adelete(ids)
