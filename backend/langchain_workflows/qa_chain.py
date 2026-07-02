from langchain.chains import RetrievalQA
from backend.langchain_workflows.prompt_templates import qa_prompt
from backend.utils.config import get_settings
from backend.utils.singletons import get_llm, get_vector_store
from backend.utils.sanitizer import InputSanitizer
from backend.utils.cache import async_cached

settings = get_settings()


def create_qa_chain() -> RetrievalQA:
    """Create QA chain using shared singleton instances"""
    llm = get_llm()
    vector_store = get_vector_store()
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": qa_prompt},
        return_source_documents=True,
    )


@async_cached(ttl_seconds=600, key_prefix="retrieve_context")
async def retrieve_context(question: str, k: int = 5) -> list[str]:
    """Retrieve context documents from vector store (cached)"""
    # Sanitize input
    question = InputSanitizer.sanitize_llm_prompt(question)

    vector_store = get_vector_store()
    docs = await vector_store.asimilarity_search(question, k=k)
    return [doc.page_content for doc in docs]


async def generate_response(question: str, context: list[str]) -> str:
    """Generate LLM response given context"""
    # Sanitize inputs
    question = InputSanitizer.sanitize_llm_prompt(question)
    context = [InputSanitizer.sanitize_text(c) for c in context]

    combined_context = "\n\n".join(context)
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Answer the question based ONLY on the provided context. Do not make up information.",
        },
        {
            "role": "user",
            "content": f"Context:\n{combined_context}\n\nQuestion: {question}",
        },
    ]
    llm = get_llm()
    response = await llm.ainvoke(messages)
    return response.content


async def answer_question(question: str) -> dict:
    """Answer a question using RAG pipeline"""
    # Sanitize input
    question = InputSanitizer.sanitize_llm_prompt(question)

    chain = create_qa_chain()
    result = await chain.ainvoke({"query": question})
    return {
        "answer": result["result"],
        "sources": [
            doc.metadata.get("source", "unknown") for doc in result["source_documents"]
        ],
    }
