from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from backend.utils.config import get_settings

settings = get_settings()

_llm = ChatOpenAI(model=settings.chat_model, temperature=0.0, openai_api_key=settings.openai_api_key)


class AgentState(TypedDict):
    input: str
    intent: str | None
    result: str | None
    error: str | None


async def classify_intent(state: AgentState) -> AgentState:
    prompt = f"""Classify the user request into one of: QA, SUMMARIZE, EXTRACT_ENTITIES, TRANSLATE, or UNKNOWN.
Request: {state['input']}
Intent:"""
    response = await _llm.ainvoke([{"role": "user", "content": prompt}])
    intent = response.content.strip()
    return {**state, "intent": intent}


async def handle_qa(state: AgentState) -> AgentState:
    from backend.langchain_workflows.qa_chain import answer_question
    result = await answer_question(state["input"])
    return {**state, "result": result["answer"]}


async def handle_summarize(state: AgentState) -> AgentState:
    from backend.langchain_workflows.summarization_chain import summarize_document
    result = await summarize_document(state["input"])
    return {**state, "result": result}


async def handle_extract(state: AgentState) -> AgentState:
    from backend.langchain_workflows.entity_extraction import extract_entities
    result = await extract_entities(state["input"])
    return {**state, "result": str(result)}


async def handle_translate(state: AgentState) -> AgentState:
    from backend.langchain_workflows.translation_chain import translate
    result = await translate(state["input"], target_language="english")
    return {**state, "result": result}


async def handle_unknown(state: AgentState) -> AgentState:
    return {**state, "result": "Unable to determine the request type. Please try again."}


def route_intent(state: AgentState) -> Literal["qa", "summarize", "extract", "translate", "unknown"]:
    intent_map = {
        "QA": "qa",
        "SUMMARIZE": "summarize",
        "EXTRACT_ENTITIES": "extract",
        "TRANSLATE": "translate",
    }
    return intent_map.get(state["intent"], "unknown")


workflow = StateGraph(AgentState)

workflow.add_node("classify_intent", classify_intent)
workflow.add_node("handle_qa", handle_qa)
workflow.add_node("handle_summarize", handle_summarize)
workflow.add_node("handle_extract", handle_extract)
workflow.add_node("handle_translate", handle_translate)
workflow.add_node("handle_unknown", handle_unknown)

workflow.set_entry_point("classify_intent")
workflow.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "qa": "handle_qa",
        "summarize": "handle_summarize",
        "extract": "handle_extract",
        "translate": "handle_translate",
        "unknown": "handle_unknown",
    },
)
workflow.add_edge("handle_qa", END)
workflow.add_edge("handle_summarize", END)
workflow.add_edge("handle_extract", END)
workflow.add_edge("handle_translate", END)
workflow.add_edge("handle_unknown", END)

agent_workflow = workflow.compile()
