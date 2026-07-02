from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from backend.utils.config import get_settings

settings = get_settings()


class ConversationBufferMemory(BaseChatMessageHistory):
    """Simple in-memory buffer for conversation history"""

    def __init__(self):
        self.messages: list[BaseMessage] = []

    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the buffer"""
        self.messages.append(message)

    def add_user_message(self, message: str) -> None:
        """Add a user message"""
        self.add_message(HumanMessage(content=message))

    def add_ai_message(self, message: str) -> None:
        """Add an AI message"""
        self.add_message(AIMessage(content=message))

    def clear(self) -> None:
        """Clear all messages"""
        self.messages = []


class ConversationSummaryMemory(BaseChatMessageHistory):
    """Memory that keeps only recent messages and a summary"""

    def __init__(self, max_messages: int = 10):
        self.messages: list[BaseMessage] = []
        self.max_messages = max_messages
        self.summary = ""

    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the buffer"""
        self.messages.append(message)
        # Keep only recent messages, older ones are summarized
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def add_user_message(self, message: str) -> None:
        """Add a user message"""
        self.add_message(HumanMessage(content=message))

    def add_ai_message(self, message: str) -> None:
        """Add an AI message"""
        self.add_message(AIMessage(content=message))

    def clear(self) -> None:
        """Clear all messages and summary"""
        self.messages = []
        self.summary = ""


def create_memory(memory_type: str = "buffer") -> BaseChatMessageHistory:
    """Create a conversation memory instance"""
    if memory_type == "summary":
        return ConversationSummaryMemory(max_messages=10)
    return ConversationBufferMemory()


async def save_conversation(memory: BaseChatMessageHistory, user_input: str, ai_output: str):
    """Save a conversation turn to memory"""
    if hasattr(memory, 'add_user_message'):
        memory.add_user_message(user_input)
        memory.add_ai_message(ai_output)


async def load_conversation(memory: BaseChatMessageHistory) -> list[dict]:
    """Load conversation history from memory"""
    messages = memory.messages if hasattr(memory, 'messages') else []
    return [
        {"role": "human" if isinstance(msg, HumanMessage) else "ai", "content": msg.content}
        for msg in messages
    ]


async def clear_memory(memory: BaseChatMessageHistory):
    """Clear all messages from memory"""
    if hasattr(memory, 'clear'):
        memory.clear()
