from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from backend.utils.config import get_settings

settings = get_settings()


def create_memory(memory_type: str = "buffer") -> ConversationBufferMemory | ConversationSummaryMemory:
    if memory_type == "summary":
        llm = ChatOpenAI(model=settings.chat_model, openai_api_key=settings.openai_api_key)
        return ConversationSummaryMemory(llm=llm, return_messages=True)
    return ConversationBufferMemory(return_messages=True)


async def save_conversation(memory: ConversationBufferMemory, user_input: str, ai_output: str):
    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(ai_output)


async def load_conversation(memory: ConversationBufferMemory) -> list[dict]:
    messages = memory.chat_memory.messages
    return [
        {"role": msg.type, "content": msg.content}
        for msg in messages
    ]


async def clear_memory(memory: ConversationBufferMemory):
    memory.clear()
