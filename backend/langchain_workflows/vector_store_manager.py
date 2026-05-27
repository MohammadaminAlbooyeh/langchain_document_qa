from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from backend.utils.config import get_settings

settings = get_settings()

embeddings = OpenAIEmbeddings(
    model=settings.embedding_model,
    openai_api_key=settings.openai_api_key,
)

_vector_store: Chroma | None = None


def _get_store() -> Chroma:
    global _vector_store
    if _vector_store is None:
        _vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory="./chroma_db",
        )
    return _vector_store


async def store_embeddings(chunks: list[str], metadatas: list[dict] | None = None) -> list[str]:
    store = _get_store()
    return await store.aadd_texts(chunks, metadatas=metadatas)


async def search_similar(query: str, k: int = 5) -> list[tuple[str, float]]:
    store = _get_store()
    results = await store.asimilarity_search_with_relevance_scores(query, k=k)
    return [(doc.page_content, score) for doc, score in results]


async def delete_old_vectors(ids: list[str]):
    store = _get_store()
    await store.adelete(ids)
