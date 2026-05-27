from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from backend.utils.config import get_settings

settings = get_settings()

_llm = ChatOpenAI(
    model=settings.chat_model,
    temperature=0.1,
    max_tokens=4096,
    openai_api_key=settings.openai_api_key,
)


async def detect_language(text: str) -> str:
    prompt = "Detect the language of the following text. Return only the language name.\n\n" + text
    response = await _llm.ainvoke([{"role": "user", "content": prompt}])
    return response.content.strip()


async def translate(text: str, target_language: str, source_language: str | None = None) -> str:
    if source_language:
        prompt_text = f"Translate the following text from {source_language} to {target_language}:\n\n{text}"
    else:
        prompt_text = f"Translate the following text to {target_language}:\n\n{text}"
    
    response = await _llm.ainvoke([{"role": "user", "content": prompt_text}])
    return response.content


async def translate_document(text: str, target_language: str) -> dict:
    source_language = await detect_language(text)
    translated = await translate(text, target_language, source_language)
    return {
        "source_language": source_language,
        "target_language": target_language,
        "translated_text": translated,
    }
