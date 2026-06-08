"""Singleton instances for expensive-to-create objects"""

from typing import Optional
from backend.langchain_workflows.qa_chain import _llm as default_llm
from backend.langchain_workflows.qa_chain import _embeddings


class LLMClientSingleton:
    """Singleton for LLM client to avoid recreating on each request"""

    _instance: Optional[object] = None

    @classmethod
    def get_instance(cls):
        """Get or create LLM instance"""
        if cls._instance is None:
            cls._instance = default_llm
        return cls._instance


class EmbeddingsSingleton:
    """Singleton for embeddings client"""

    _instance: Optional[object] = None

    @classmethod
    def get_instance(cls):
        """Get or create embeddings instance"""
        if cls._instance is None:
            cls._instance = _embeddings
        return cls._instance


class VectorStoreSingleton:
    """Singleton for vector store to avoid recreation per request"""

    _instance: Optional[object] = None

    @classmethod
    def get_instance(cls):
        """Get or create vector store instance"""
        if cls._instance is None:
            from langchain_chroma import Chroma
            from backend.utils.singletons import EmbeddingsSingleton

            embeddings = EmbeddingsSingleton.get_instance()
            cls._instance = Chroma(
                embedding_function=embeddings,
                persist_directory="./chroma_db",
            )
        return cls._instance

    @classmethod
    def reset(cls):
        """Reset singleton (useful for testing)"""
        cls._instance = None


def get_llm():
    """Get shared LLM instance"""
    return LLMClientSingleton.get_instance()


def get_embeddings():
    """Get shared embeddings instance"""
    return EmbeddingsSingleton.get_instance()


def get_vector_store():
    """Get shared vector store instance"""
    return VectorStoreSingleton.get_instance()
