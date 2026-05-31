from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, BackgroundTasks, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.api.dependencies import get_db_session
from backend.api.schemas import (
    DocumentResponse, DocumentUploadResponse, QuestionRequest, QAResponse,
    SummarizeRequest, SummarizeResponse, EntityExtractionResponse,
    TranslationRequest, TranslationResponse
)
from backend.services.document_service import DocumentService
from backend.services.qa_service import QAService
from backend.models.conversation import Conversation
from backend.utils.exceptions import DocumentNotFoundError, UnsupportedFileTypeError, FileSizeExceededError
from backend.utils.config import get_settings
from pathlib import Path

router = APIRouter()
settings = get_settings()

UPLOAD_DIR = Path("data/uploads")
ALLOWED_TYPES = {"pdf", "docx", "txt"}


@router.get("/documents")
async def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db_session),
):
    try:
        service = DocumentService(db)
        documents = await service.list_documents(skip=skip, limit=limit)
        return [
            DocumentResponse(
                id=doc.id,
                filename=doc.filename,
                file_type=doc.file_type,
                file_size=doc.file_size,
                status=doc.status.value,
                created_at=doc.created_at,
                updated_at=doc.updated_at,
            )
            for doc in documents
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(get_db_session),
):
    try:
        file_type = file.filename.split(".")[-1].lower()

        if file_type not in ALLOWED_TYPES:
            raise UnsupportedFileTypeError(file_type)

        file_content = await file.read()
        file_size_mb = len(file_content) / (1024 * 1024)

        if file_size_mb > settings.max_upload_size:
            raise FileSizeExceededError(settings.max_upload_size)

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        service = DocumentService(db)
        file_path = str(UPLOAD_DIR / file.filename)

        with open(file_path, "wb") as f:
            f.write(file_content)

        doc = await service.create_document(
            filename=file.filename,
            file_type=file_type,
            file_size=len(file_content),
            file_path=file_path,
        )

        background_tasks.add_task(service.process_document, doc.id)

        return DocumentUploadResponse(
            id=doc.id,
            filename=doc.filename,
            message="Document uploaded. Processing started.",
        )
    except (UnsupportedFileTypeError, FileSizeExceededError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str, db: AsyncSession = Depends(get_db_session)):
    try:
        service = DocumentService(db)
        doc = await service.get_document(document_id)

        if not doc:
            raise DocumentNotFoundError(document_id)

        return DocumentResponse(
            id=doc.id,
            filename=doc.filename,
            file_type=doc.file_type,
            file_size=doc.file_size,
            status=doc.status.value,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
        )
    except DocumentNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str, db: AsyncSession = Depends(get_db_session)):
    try:
        service = DocumentService(db)
        doc = await service.get_document(document_id)

        if not doc:
            raise DocumentNotFoundError(document_id)

        await service.delete_document(document_id)
        return {"message": "Document deleted successfully"}
    except DocumentNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/documents/{document_id}/qa", response_model=QAResponse)
async def ask_question(
    document_id: str,
    request: QuestionRequest,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        service = DocumentService(db)
        doc = await service.get_document(document_id)

        if not doc:
            raise DocumentNotFoundError(document_id)

        qa_service = QAService(db)
        result = await qa_service.ask(document_id, request.question, request.conversation_id)

        return QAResponse(
            answer=result["answer"],
            sources=result.get("sources", []),
            confidence=result.get("confidence", 0.5),
            conversation_id=result["conversation_id"],
        )
    except DocumentNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/documents/{document_id}/summarize", response_model=SummarizeResponse)
async def summarize_document(
    document_id: str,
    request: SummarizeRequest,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        service = DocumentService(db)
        doc = await service.get_document(document_id)

        if not doc:
            raise DocumentNotFoundError(document_id)

        if not doc.text_content:
            raise HTTPException(status_code=400, detail="Document has not been processed yet")

        from backend.langchain_workflows.summarization_chain import summarize_text
        summary = await summarize_text(doc.text_content, mode=request.mode)

        return SummarizeResponse(summary=summary, mode=request.mode)
    except DocumentNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/documents/{document_id}/extract-entities", response_model=EntityExtractionResponse)
async def extract_entities_endpoint(
    document_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        service = DocumentService(db)
        doc = await service.get_document(document_id)

        if not doc:
            raise DocumentNotFoundError(document_id)

        if not doc.text_content:
            raise HTTPException(status_code=400, detail="Document has not been processed yet")

        from backend.langchain_workflows.entity_extraction import extract_entities
        entities = await extract_entities(doc.text_content)

        return EntityExtractionResponse(entities=entities)
    except DocumentNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/documents/{document_id}/translate", response_model=TranslationResponse)
async def translate_document(
    document_id: str,
    request: TranslationRequest,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        service = DocumentService(db)
        doc = await service.get_document(document_id)

        if not doc:
            raise DocumentNotFoundError(document_id)

        if not doc.text_content:
            raise HTTPException(status_code=400, detail="Document has not been processed yet")

        from backend.langchain_workflows.translation_chain import translate
        translated_text = await translate(doc.text_content, request.target_language)

        return TranslationResponse(
            translated_text=translated_text,
            source_language="en",
            target_language=request.target_language,
        )
    except DocumentNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations")
async def list_conversations(db: AsyncSession = Depends(get_db_session)):
    try:
        result = await db.execute(select(Conversation).order_by(Conversation.created_at.desc()))
        conversations = result.scalars().all()

        return [
            {
                "id": c.id,
                "document_id": c.document_id,
                "title": c.title,
                "created_at": c.created_at,
                "updated_at": c.updated_at,
            }
            for c in conversations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, db: AsyncSession = Depends(get_db_session)):
    try:
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        qa_service = QAService(db)
        history = await qa_service.get_history(conversation_id)

        return {
            "id": conversation.id,
            "document_id": conversation.document_id,
            "title": conversation.title,
            "history": history,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, db: AsyncSession = Depends(get_db_session)):
    try:
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        await db.delete(conversation)
        await db.commit()
        return {"message": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversations/{conversation_id}/chat")
async def chat(
    conversation_id: str,
    request: QuestionRequest,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        if not conversation.document_id:
            raise HTTPException(status_code=400, detail="Conversation has no associated document")

        qa_service = QAService(db)
        result = await qa_service.ask(conversation.document_id, request.question, conversation_id)

        return {
            "answer": result["answer"],
            "sources": result.get("sources", []),
            "conversation_id": result["conversation_id"],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
