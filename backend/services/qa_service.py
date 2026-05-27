from sqlalchemy.ext.asyncio import AsyncSession
from backend.langchain_workflows.qa_chain import answer_question
from backend.models.qa_pair import QAPair
from backend.models.conversation import Conversation
import uuid
from datetime import datetime


class QAService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ask(self, document_id: str, question: str, conversation_id: str | None = None) -> dict:
        result = await answer_question(question)

        if not conversation_id:
            conversation = Conversation(
                id=str(uuid.uuid4()),
                document_id=document_id,
                title=question[:50],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            self.db.add(conversation)
            await self.db.commit()
            conversation_id = conversation.id

        qa = QAPair(
            id=str(uuid.uuid4()),
            document_id=document_id,
            conversation_id=conversation_id,
            question=question,
            answer=result["answer"],
            sources=",".join(result.get("sources", [])),
            created_at=datetime.utcnow(),
        )
        self.db.add(qa)
        await self.db.commit()

        return {
            "answer": result["answer"],
            "sources": result.get("sources", []),
            "conversation_id": conversation_id,
        }

    async def get_history(self, conversation_id: str) -> list[dict]:
        from sqlalchemy import select
        result = await self.db.execute(
            select(QAPair).where(QAPair.conversation_id == conversation_id).order_by(QAPair.created_at)
        )
        pairs = result.scalars().all()
        return [
            {"question": p.question, "answer": p.answer, "created_at": p.created_at.isoformat()}
            for p in pairs
        ]
