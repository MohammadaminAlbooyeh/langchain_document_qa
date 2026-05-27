import uuid
from pathlib import Path
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models.document import Document, DocumentStatus
from backend.langchain_workflows.document_processor import extract_text
from backend.langchain_workflows.text_splitter import create_overlapping_chunks
from backend.langchain_workflows.vector_store_manager import store_embeddings


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_document(self, filename: str, file_type: str, file_size: int, file_path: str) -> Document:
        doc = Document(
            id=str(uuid.uuid4()),
            filename=filename,
            file_type=file_type,
            file_size=file_size,
            file_path=file_path,
            status=DocumentStatus.UPLOADED,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.add(doc)
        await self.db.commit()
        await self.db.refresh(doc)
        return doc

    async def process_document(self, document_id: str) -> Document:
        result = await self.db.execute(select(Document).where(Document.id == document_id))
        doc = result.scalar_one_or_none()
        if not doc:
            raise ValueError(f"Document {document_id} not found")

        doc.status = DocumentStatus.PROCESSING
        await self.db.commit()

        try:
            text = await extract_text(doc.file_path)
            doc.text_content = text
            chunks = create_overlapping_chunks(text)
            await store_embeddings(chunks, metadatas=[{"document_id": document_id}] * len(chunks))
            doc.status = DocumentStatus.PROCESSED
        except Exception:
            doc.status = DocumentStatus.FAILED

        doc.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(doc)
        return doc

    async def get_document(self, document_id: str) -> Document | None:
        result = await self.db.execute(select(Document).where(Document.id == document_id))
        return result.scalar_one_or_none()

    async def list_documents(self) -> list[Document]:
        result = await self.db.execute(select(Document).order_by(Document.created_at.desc()))
        return list(result.scalars().all())

    async def delete_document(self, document_id: str):
        result = await self.db.execute(select(Document).where(Document.id == document_id))
        doc = result.scalar_one_or_none()
        if doc:
            path = Path(doc.file_path)
            if path.exists():
                path.unlink()
            await self.db.delete(doc)
            await self.db.commit()
