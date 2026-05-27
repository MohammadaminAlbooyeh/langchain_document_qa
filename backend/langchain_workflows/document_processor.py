from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader


async def load_pdf(file_path: str | Path) -> str:
    loader = PyPDFLoader(str(file_path))
    pages = await loader.aload()
    return "\n".join(page.page_content for page in pages)


async def load_docx(file_path: str | Path) -> str:
    loader = Docx2txtLoader(str(file_path))
    documents = await loader.aload()
    return "\n".join(doc.page_content for doc in documents)


async def load_txt(file_path: str | Path) -> str:
    loader = TextLoader(str(file_path))
    documents = await loader.aload()
    return "\n".join(doc.page_content for doc in documents)


async def extract_text(file_path: str | Path) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return await load_pdf(path)
    elif suffix == ".docx":
        return await load_docx(path)
    elif suffix == ".txt":
        return await load_txt(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")
