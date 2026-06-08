from langchain_text_splitters import (
    TokenTextSplitter,
    SentenceTransformersTokenTextSplitter,
    RecursiveCharacterTextSplitter,
)


def split_by_tokens(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)


def split_by_sentences(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    splitter = SentenceTransformersTokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)


def create_overlapping_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_text(text)
