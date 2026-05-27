from functools import lru_cache
from langchain_openai import OpenAIEmbeddings
from backend.utils.config import get_settings

settings = get_settings()


def generate_embeddings(text: str) -> list[float]:
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )
    return embeddings.embed_query(text)


async def batch_embed(texts: list[str]) -> list[list[float]]:
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )
    return await embeddings.aembed_documents(texts)


@lru_cache(maxsize=1024)
def cache_embeddings(text: str) -> list[float]:
    return generate_embeddings(text)
