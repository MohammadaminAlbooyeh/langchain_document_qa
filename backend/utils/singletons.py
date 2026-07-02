from typing import Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from backend.utils.config import get_settings

settings = get_settings()

_llm = ChatOpenAI(
    model=settings.chat_model,
    temperature=settings.temperature,
    max_tokens=settings.max_tokens,
    openai_api_key=settings.openai_api_key,
)

_embeddings = OpenAIEmbeddings(
    model=settings.embedding_model,
    openai_api_key=settings.openai_api_key,
)


class LLMClientSingleton:
    _instance: Optional[object] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = _llm
        return cls._instance


class EmbeddingsSingleton:
    _instance: Optional[object] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = _embeddings
        return cls._instance


class VectorStoreSingleton:
    _instance: Optional[object] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            from langchain_chroma import Chroma

            embeddings = EmbeddingsSingleton.get_instance()
            chroma_path = getattr(settings, "chroma_db_path", "./chroma_db")
            cls._instance = Chroma(
                embedding_function=embeddings,
                persist_directory=chroma_path,
            )
        return cls._instance

    @classmethod
    def reset(cls):
        cls._instance = None


def get_llm():
    return LLMClientSingleton.get_instance()


def get_embeddings():
    return EmbeddingsSingleton.get_instance()


def get_vector_store():
    return VectorStoreSingleton.get_instance()
