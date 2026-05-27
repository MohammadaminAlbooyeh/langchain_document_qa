from backend.langchain_workflows.summarization_chain import (
    summarize_document,
    summarize_bullet_points,
    summarize_by_sections,
)


class SummarizationService:
    async def summarize(self, text: str, mode: str = "paragraphs") -> str:
        if mode == "bullet_points":
            return await summarize_bullet_points(text)
        elif mode == "sections":
            return await summarize_by_sections(text)
        return await summarize_document(text)
