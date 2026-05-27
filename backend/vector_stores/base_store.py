from abc import ABC, abstractmethod


class BaseVectorStore(ABC):
    @abstractmethod
    async def add_texts(self, texts: list[str], metadatas: list[dict] | None = None) -> list[str]:
        ...

    @abstractmethod
    async def similarity_search(self, query: str, k: int = 5) -> list[tuple[str, float]]:
        ...

    @abstractmethod
    async def delete(self, ids: list[str]):
        ...
