from backend.langchain_workflows.langgraph_workflows.document_workflow import document_workflow
from backend.langchain_workflows.langgraph_workflows.qa_workflow import qa_workflow
from backend.langchain_workflows.langgraph_workflows.analysis_workflow import analysis_workflow
from backend.langchain_workflows.langgraph_workflows.agent_workflow import agent_workflow


class WorkflowOrchestrator:
    async def process_document(self, file_path: str) -> dict:
        result = await document_workflow.ainvoke({"file_path": file_path})
        return result

    async def answer_question(self, question: str) -> dict:
        result = await qa_workflow.ainvoke({"question": question})
        return result

    async def analyze_document(self, file_path: str, mode: str = "both") -> dict:
        result = await analysis_workflow.ainvoke({"file_path": file_path, "mode": mode})
        return result

    async def run_agent(self, user_input: str) -> dict:
        result = await agent_workflow.ainvoke({"input": user_input})
        return result
