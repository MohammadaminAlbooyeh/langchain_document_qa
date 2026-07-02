import re
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from backend.langchain_workflows.prompt_templates import entity_extraction_prompt
from backend.utils.config import get_settings

settings = get_settings()

_llm = ChatOpenAI(
    model=settings.chat_model,
    temperature=0.0,
    max_tokens=2048,
    openai_api_key=settings.openai_api_key,
)


async def extract_entities(text: str) -> dict[str, list[str]]:
    # Use LCEL chain syntax: prompt | llm | output_parser
    chain = entity_extraction_prompt | _llm | StrOutputParser()
    result = await chain.ainvoke({"text": text})

    entities: dict[str, list[str]] = {}
    for line in result.split("\n"):
        if ":" in line:
            category, values = line.split(":", 1)
            entities[category.strip()] = [v.strip() for v in values.split(",") if v.strip()]
    return entities


def extract_names(text: str) -> list[str]:
    pattern = r"\b[A-Z][a-z]+ [A-Z][a-z]+\b"
    return list(set(re.findall(pattern, text)))


def extract_dates(text: str) -> list[str]:
    patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b\d{2}/\d{2}/\d{4}\b",
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},?\s*\d{4}\b",
    ]
    dates = []
    for pattern in patterns:
        dates.extend(re.findall(pattern, text))
    return list(set(dates))


def extract_amounts(text: str) -> list[str]:
    patterns = [
        r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?",
        r"\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|EUR|GBP)",
    ]
    amounts = []
    for pattern in patterns:
        amounts.extend(re.findall(pattern, text))
    return list(set(amounts))
