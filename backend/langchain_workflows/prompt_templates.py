from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

# Chat-based prompts for LLM integration with LCEL
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers questions based on the given context.\nIf you don't know the answer, say you don't know. Don't make up information."),
    ("user", "Context:\n{context}\n\nQuestion: {question}"),
])

summarization_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful summarization assistant."),
    ("user", "Summarize the following text in a clear and concise way.\nCapture all important points and maintain the original meaning.\n\nText:\n{text}"),
])

entity_extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a named entity extraction assistant."),
    ("user", """Extract named entities from the following text.
Categorize them as: PERSON, ORGANIZATION, LOCATION, DATE, AMOUNT, and OTHER.

Return the result as:
PERSON: name1, name2
ORGANIZATION: org1, org2
LOCATION: loc1, loc2
DATE: date1, date2
AMOUNT: amount1, amount2
OTHER: other1, other2

Text:
{text}"""),
])

translation_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a translation assistant."),
    ("user", "Translate the following text to {target_language}.\nPreserve the original formatting and tone as much as possible.\n\nText:\n{text}"),
])

# Legacy PromptTemplate versions for backward compatibility (used in non-LCEL contexts)
qa_prompt_legacy = PromptTemplate(
    template="""You are a helpful assistant that answers questions based on the given context.
If you don't know the answer, say you don't know. Don't make up information.

Context:
{context}

Question: {question}

Answer:""",
    input_variables=["context", "question"],
)

summarization_prompt_legacy = PromptTemplate(
    template="""Summarize the following text in a clear and concise way.
Capture all important points and maintain the original meaning.

Text:
{text}

Summary:""",
    input_variables=["text"],
)

entity_extraction_prompt_legacy = PromptTemplate(
    template="""Extract named entities from the following text.
Categorize them as: PERSON, ORGANIZATION, LOCATION, DATE, AMOUNT, and OTHER.

Return the result as:
PERSON: name1, name2
ORGANIZATION: org1, org2
LOCATION: loc1, loc2
DATE: date1, date2
AMOUNT: amount1, amount2
OTHER: other1, other2

Text:
{text}

Entities:""",
    input_variables=["text"],
)

translation_prompt_legacy = PromptTemplate(
    template="""Translate the following text to {target_language}.
Preserve the original formatting and tone as much as possible.

Text:
{text}

Translation:""",
    input_variables=["text", "target_language"],
)

custom_prompts: dict[str, ChatPromptTemplate] = {
    "qa": qa_prompt,
    "summarization": summarization_prompt,
    "entity_extraction": entity_extraction_prompt,
    "translation": translation_prompt,
}
