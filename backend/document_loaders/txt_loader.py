from pathlib import Path
from langchain_community.document_loaders import TextLoader


async def load_txt(file_path: str | Path) -> list[dict]:
    loader = TextLoader(str(file_path))
    documents = await loader.aload()
    return [
        {"content": doc.page_content, "metadata": doc.metadata}
        for doc in documents
    ]
