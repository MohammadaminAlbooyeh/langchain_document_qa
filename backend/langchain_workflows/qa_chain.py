from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from backend.langchain_workflows.prompt_templates import qa_prompt
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


def create_qa_chain() -> RetrievalQA:
    vector_store = Chroma(
        embedding_function=_embeddings,
        persist_directory="./chroma_db",
    )
    return RetrievalQA.from_chain_type(
        llm=_llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": qa_prompt},
        return_source_documents=True,
    )


async def retrieve_context(question: str, k: int = 5) -> list[str]:
    vector_store = Chroma(
        embedding_function=_embeddings,
        persist_directory="./chroma_db",
    )
    docs = await vector_store.asimilarity_search(question, k=k)
    return [doc.page_content for doc in docs]


async def generate_response(question: str, context: list[str]) -> str:
    combined_context = "\n\n".join(context)
    messages = [
        {"role": "system", "content": "Answer the question based on the provided context."},
        {"role": "user", "content": f"Context:\n{combined_context}\n\nQuestion: {question}"},
    ]
    response = await _llm.ainvoke(messages)
    return response.content


async def answer_question(question: str) -> dict:
    chain = create_qa_chain()
    result = await chain.ainvoke({"query": question})
    return {
        "answer": result["result"],
        "sources": [doc.metadata.get("source", "unknown") for doc in result["source_documents"]],
    }
