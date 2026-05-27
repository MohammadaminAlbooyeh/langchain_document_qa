from datetime import datetime
from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    file_size: int
    status: str
    created_at: datetime
    updated_at: datetime


class DocumentUploadResponse(BaseModel):
    id: str
    filename: str
    message: str


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4096)
    conversation_id: str | None = None


class QAResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float
    conversation_id: str


class SummarizeRequest(BaseModel):
    mode: str = Field(default="paragraphs", pattern="^(paragraphs|bullet_points|sections)$")


class SummarizeResponse(BaseModel):
    summary: str
    mode: str


class EntityExtractionResponse(BaseModel):
    entities: dict[str, list[str]]


class TranslationRequest(BaseModel):
    target_language: str = Field(..., min_length=2, max_length=50)


class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4096)


class ChatResponse(BaseModel):
    response: str
    conversation_id: str


class ErrorResponse(BaseModel):
    detail: str
    error_code: str | None = None
