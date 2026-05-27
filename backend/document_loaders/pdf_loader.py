from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


async def load_pdf(file_path: str | Path) -> list[dict]:
    loader = PyPDFLoader(str(file_path))
    pages = await loader.aload()
    return [
        {"page": i + 1, "content": page.page_content, "metadata": page.metadata}
        for i, page in enumerate(pages)
    ]
