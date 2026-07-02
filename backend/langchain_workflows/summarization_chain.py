from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.langchain_workflows.prompt_templates import summarization_prompt
from backend.utils.config import get_settings

settings = get_settings()

_llm = ChatOpenAI(
    model=settings.chat_model,
    temperature=0.3,
    max_tokens=1024,
    openai_api_key=settings.openai_api_key,
)


async def summarize_text(text: str, mode: str = "paragraphs") -> str:
    if mode == "bullet_points":
        return await summarize_bullet_points(text)
    elif mode == "sections":
        return await summarize_by_sections(text)
    else:
        return await summarize_document(text)


async def summarize_document(text: str) -> str:
    # Use LCEL chain syntax: prompt | llm | output_parser
    chain = summarization_prompt | _llm | StrOutputParser()
    result = await chain.ainvoke({"text": text})
    return result


async def summarize_bullet_points(text: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a summarization assistant that creates bullet points."),
        ("user", "Summarize the following text as bullet points:\n\n{text}\n\nBullet points:"),
    ])
    chain = prompt | _llm | StrOutputParser()
    result = await chain.ainvoke({"text": text})
    return result


async def summarize_by_sections(text: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a document analysis assistant."),
        ("user", "Split the following text into logical sections and summarize each:\n\n{text}\n\nSection summaries:"),
    ])
    chain = prompt | _llm | StrOutputParser()
    result = await chain.ainvoke({"text": text})
    return result
