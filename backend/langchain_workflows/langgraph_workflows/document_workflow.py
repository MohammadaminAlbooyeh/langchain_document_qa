from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from backend.langchain_workflows.document_processor import extract_text
from backend.langchain_workflows.text_splitter import create_overlapping_chunks
from backend.langchain_workflows.embedding_generator import batch_embed
from backend.langchain_workflows.vector_store_manager import store_embeddings


class DocumentState(TypedDict):
    file_path: str
    raw_text: str | None
    chunks: list[str] | None
    embeddings: list[list[float]] | None
    error: str | None


async def load_document(state: DocumentState) -> DocumentState:
    try:
        text = await extract_text(state["file_path"])
        return {**state, "raw_text": text}
    except Exception as e:
        return {**state, "error": str(e)}


async def split_text(state: DocumentState) -> DocumentState:
    if state.get("error"):
        return state
    chunks = create_overlapping_chunks(state["raw_text"])
    return {**state, "chunks": chunks}


async def generate_embeddings(state: DocumentState) -> DocumentState:
    if state.get("error"):
        return state
    embeddings = await batch_embed(state["chunks"])
    return {**state, "embeddings": embeddings}


async def store_in_vector_db(state: DocumentState) -> DocumentState:
    if state.get("error"):
        return state
    await store_embeddings(state["chunks"])
    return state


def should_continue(state: DocumentState) -> Literal["continue", "end"]:
    if state.get("error"):
        return "end"
    return "continue"


workflow = StateGraph(DocumentState)

workflow.add_node("load_document", load_document)
workflow.add_node("split_text", split_text)
workflow.add_node("generate_embeddings", generate_embeddings)
workflow.add_node("store_in_vector_db", store_in_vector_db)

workflow.set_entry_point("load_document")
workflow.add_conditional_edges(
    "load_document",
    should_continue,
    {"continue": "split_text", "end": END},
)
workflow.add_conditional_edges(
    "split_text",
    should_continue,
    {"continue": "generate_embeddings", "end": END},
)
workflow.add_conditional_edges(
    "generate_embeddings",
    should_continue,
    {"continue": "store_in_vector_db", "end": END},
)
workflow.add_edge("store_in_vector_db", END)

document_workflow = workflow.compile()
