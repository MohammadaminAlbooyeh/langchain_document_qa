from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from backend.langchain_workflows.qa_chain import retrieve_context, generate_response


class QAState(TypedDict):
    question: str
    context: list[str] | None
    answer: str | None
    error: str | None


async def retrieve(state: QAState) -> QAState:
    try:
        context = await retrieve_context(state["question"])
        return {**state, "context": context}
    except Exception as e:
        return {**state, "error": str(e)}


async def answer(state: QAState) -> QAState:
    if state.get("error"):
        return state
    answer = await generate_response(state["question"], state["context"])
    return {**state, "answer": answer}


def check_context(state: QAState) -> Literal["has_context", "no_context"]:
    if state.get("error"):
        return "no_context"
    if state.get("context"):
        return "has_context"
    return "no_context"


workflow = StateGraph(QAState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("answer", answer)

workflow.set_entry_point("retrieve")
workflow.add_conditional_edges(
    "retrieve",
    check_context,
    {"has_context": "answer", "no_context": END},
)
workflow.add_edge("answer", END)

qa_workflow = workflow.compile()
