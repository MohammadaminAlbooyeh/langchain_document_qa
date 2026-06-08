from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
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
    prompt = summarization_prompt.format(text=text)
    response = await _llm.ainvoke([{"role": "user", "content": prompt}])
    return response.content


async def summarize_bullet_points(text: str) -> str:
    prompt_text = "Summarize the following text as bullet points:\n\n{text}\n\nBullet points:"
    prompt = PromptTemplate(
        template=prompt_text,
        input_variables=["text"],
    )
    formatted = prompt.format(text=text)
    response = await _llm.ainvoke([{"role": "user", "content": formatted}])
    return response.content


async def summarize_by_sections(text: str) -> str:
    prompt_text = "Split the following text into logical sections and summarize each:\n\n{text}\n\nSection summaries:"
    prompt = PromptTemplate(
        template=prompt_text,
        input_variables=["text"],
    )
    formatted = prompt.format(text=text)
    response = await _llm.ainvoke([{"role": "user", "content": formatted}])
    return response.content
