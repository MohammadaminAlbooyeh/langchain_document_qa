from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from backend.langchain_workflows.document_processor import extract_text
from backend.langchain_workflows.summarization_chain import summarize_document, summarize_bullet_points
from backend.langchain_workflows.entity_extraction import extract_entities


class AnalysisState(TypedDict):
    file_path: str
    mode: str
    text: str | None
    summary: str | None
    entities: dict | None
    error: str | None


async def load_text(state: AnalysisState) -> AnalysisState:
    try:
        text = await extract_text(state["file_path"])
        return {**state, "text": text}
    except Exception as e:
        return {**state, "error": str(e)}


async def summarize(state: AnalysisState) -> AnalysisState:
    if state.get("error"):
        return state
    if state["mode"] == "bullet_points":
        summary = await summarize_bullet_points(state["text"])
    else:
        summary = await summarize_document(state["text"])
    return {**state, "summary": summary}


async def extract(state: AnalysisState) -> AnalysisState:
    if state.get("error"):
        return state
    entities = await extract_entities(state["text"])
    return {**state, "entities": entities}


def route_analysis(state: AnalysisState) -> Literal["summarize", "extract", "both"]:
    if state.get("error"):
        return "both"
    if state["mode"] == "summarize":
        return "summarize"
    elif state["mode"] == "extract":
        return "extract"
    return "both"


workflow = StateGraph(AnalysisState)

workflow.add_node("load_text", load_text)
workflow.add_node("summarize", summarize)
workflow.add_node("extract", extract)

workflow.set_entry_point("load_text")
workflow.add_conditional_edges(
    "load_text",
    route_analysis,
    {
        "summarize": "summarize",
        "extract": "extract",
        "both": "summarize",
    },
)
workflow.add_edge("summarize", "extract")
workflow.add_edge("extract", END)

analysis_workflow = workflow.compile()
