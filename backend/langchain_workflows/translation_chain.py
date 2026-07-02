from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.utils.config import get_settings
from backend.langchain_workflows.prompt_templates import translation_prompt

settings = get_settings()

_llm = ChatOpenAI(
    model=settings.chat_model,
    temperature=0.1,
    max_tokens=4096,
    openai_api_key=settings.openai_api_key,
)

_detection_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a language detection assistant. Return only the language name."),
    ("user", "Detect the language of the following text. Return only the language name.\n\n{text}"),
])


async def detect_language(text: str) -> str:
    # Use LCEL chain syntax: prompt | llm | output_parser
    chain = _detection_prompt | _llm | StrOutputParser()
    result = await chain.ainvoke({"text": text})
    return result.strip()


async def translate(text: str, target_language: str, source_language: str | None = None) -> str:
    # Use LCEL chain syntax: prompt | llm | output_parser
    chain = translation_prompt | _llm | StrOutputParser()
    result = await chain.ainvoke({"text": text, "target_language": target_language})
    return result


async def translate_document(text: str, target_language: str) -> dict:
    source_language = await detect_language(text)
    translated = await translate(text, target_language, source_language)
    return {
        "source_language": source_language,
        "target_language": target_language,
        "translated_text": translated,
    }
