from langchain_community.document_loaders import WebBaseLoader


async def load_from_url(url: str) -> list[dict]:
    loader = WebBaseLoader(url)
    documents = await loader.aload()
    return [
        {"content": doc.page_content, "metadata": doc.metadata}
        for doc in documents
    ]
