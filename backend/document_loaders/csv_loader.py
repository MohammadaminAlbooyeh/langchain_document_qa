from pathlib import Path
from langchain_community.document_loaders import CSVLoader


async def load_csv(file_path: str | Path) -> list[dict]:
    loader = CSVLoader(str(file_path))
    documents = await loader.aload()
    return [
        {"content": doc.page_content, "metadata": doc.metadata}
        for doc in documents
    ]
