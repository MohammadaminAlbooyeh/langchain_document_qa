from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from backend.utils.config import get_settings

settings = get_settings()

embeddings = OpenAIEmbeddings(
    model=settings.embedding_model,
    openai_api_key=settings.openai_api_key,
)


class FAISSStore:
    def __init__(self):
        self.store: FAISS | None = None

    async def add_texts(self, texts: list[str], metadatas: list[dict] | None = None):
        if self.store is None:
            self.store = await FAISS.afrom_texts(texts, embeddings, metadatas=metadatas)
        else:
            await self.store.aadd_texts(texts, metadatas=metadatas)

    async def similarity_search(self, query: str, k: int = 5) -> list[tuple[str, float]]:
        if self.store is None:
            return []
        results = await self.store.asimilarity_search_with_relevance_scores(query, k=k)
        return [(doc.page_content, score) for doc, score in results]

    def save_local(self, path: str = "./faiss_index"):
        if self.store:
            self.store.save_local(path)

    def load_local(self, path: str = "./faiss_index"):
        self.store = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
