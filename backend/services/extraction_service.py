from backend.langchain_workflows.entity_extraction import extract_entities


class ExtractionService:
    async def extract(self, text: str) -> dict[str, list[str]]:
        return await extract_entities(text)
