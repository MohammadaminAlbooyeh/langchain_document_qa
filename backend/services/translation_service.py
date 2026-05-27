from backend.langchain_workflows.translation_chain import translate_document


class TranslationService:
    async def translate(self, text: str, target_language: str) -> dict:
        return await translate_document(text, target_language)
