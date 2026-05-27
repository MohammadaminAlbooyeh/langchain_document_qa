from pathlib import Path
from langchain_community.document_loaders import Docx2txtLoader


async def load_docx(file_path: str | Path) -> list[dict]:
    loader = Docx2txtLoader(str(file_path))
    documents = await loader.aload()
    return [
        {"content": doc.page_content, "metadata": doc.metadata}
        for doc in documents
    ]
