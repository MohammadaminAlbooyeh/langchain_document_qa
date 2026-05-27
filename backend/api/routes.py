from fastapi import APIRouter

router = APIRouter()


@router.get("/documents")
async def list_documents():
    pass


@router.post("/documents/upload")
async def upload_document():
    pass


@router.get("/documents/{document_id}")
async def get_document(document_id: str):
    pass


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    pass


@router.post("/documents/{document_id}/qa")
async def ask_question(document_id: str):
    pass


@router.post("/documents/{document_id}/summarize")
async def summarize_document(document_id: str):
    pass


@router.post("/documents/{document_id}/extract-entities")
async def extract_entities(document_id: str):
    pass


@router.post("/documents/{document_id}/translate")
async def translate_document(document_id: str):
    pass


@router.get("/conversations")
async def list_conversations():
    pass


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    pass


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    pass


@router.post("/conversations/{conversation_id}/chat")
async def chat(conversation_id: str):
    pass
