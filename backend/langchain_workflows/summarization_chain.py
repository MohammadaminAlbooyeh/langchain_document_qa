from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from backend.langchain_workflows.prompt_templates import summarization_prompt
from backend.utils.config import get_settings

settings = get_settings()

_llm = ChatOpenAI(
    model=settings.chat_model,
    temperature=0.3,
    max_tokens=1024,
    openai_api_key=settings.openai_api_key,
)


async def summarize_document(text: str) -> str:
    chain = LLMChain(llm=_llm, prompt=summarization_prompt)
    return await chain.arun(text=text)


async def summarize_bullet_points(text: str) -> str:
    prompt = PromptTemplate(
        template="Summarize the following text as bullet points:\n\n{text}\n\nBullet points:",
        input_variables=["text"],
    )
    chain = LLMChain(llm=_llm, prompt=prompt)
    return await chain.arun(text=text)


async def summarize_by_sections(text: str) -> str:
    prompt = PromptTemplate(
        template="Split the following text into logical sections and summarize each:\n\n{text}\n\nSection summaries:",
        input_variables=["text"],
    )
    chain = LLMChain(llm=_llm, prompt=prompt)
    return await chain.arun(text=text)
