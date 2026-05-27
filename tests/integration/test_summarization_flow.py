import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from backend.models.document import Document, DocumentStatus
from datetime import datetime


@pytest.fixture
def client():
    """Create test client"""
    from backend.main import app
    return TestClient(app)


@pytest.fixture
def sample_document():
    """Create a sample document"""
    return {
        'id': 'test-doc-id',
        'filename': 'test.pdf',
        'file_type': 'pdf',
        'file_size': 10240,
        'status': DocumentStatus.PROCESSED,
        'text_content': 'This is a test document with sample content.',
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
    }


@pytest.mark.asyncio
async def test_summarization_flow(client, sample_document):
    """Test complete summarization workflow"""
    # Mock document retrieval
    with patch('backend.services.document_service.DocumentService.get_document', new_callable=AsyncMock) as mock_get:
        mock_doc = MagicMock()
        mock_doc.id = sample_document['id']
        mock_doc.text_content = sample_document['text_content']
        mock_doc.filename = sample_document['filename']
        mock_get.return_value = mock_doc
        
        # Mock summarization
        with patch('backend.langchain_workflows.summarization_chain.summarize_text', new_callable=AsyncMock) as mock_summarize:
            mock_summarize.return_value = "Test summary of the document."
            
            response = client.post(
                f"/api/v1/documents/{sample_document['id']}/summarize",
                json={"mode": "paragraphs"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "summary" in data
            assert data["summary"] == "Test summary of the document."
            assert data["mode"] == "paragraphs"


@pytest.mark.asyncio
async def test_entity_extraction_flow(client, sample_document):
    """Test complete entity extraction workflow"""
    with patch('backend.services.document_service.DocumentService.get_document', new_callable=AsyncMock) as mock_get:
        mock_doc = MagicMock()
        mock_doc.id = sample_document['id']
        mock_doc.text_content = "John Smith and Jane Doe met in New York on 2024-05-27."
        mock_doc.filename = sample_document['filename']
        mock_get.return_value = mock_doc
        
        with patch('backend.langchain_workflows.entity_extraction.extract_entities', new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = {
                'PERSON': ['John Smith', 'Jane Doe'],
                'LOCATION': ['New York'],
                'DATE': ['2024-05-27']
            }
            
            response = client.post(
                f"/api/v1/documents/{sample_document['id']}/extract-entities"
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "entities" in data
            assert 'PERSON' in data['entities']
            assert 'LOCATION' in data['entities']
            assert 'DATE' in data['entities']


@pytest.mark.asyncio
async def test_qa_flow(client, sample_document):
    """Test complete Q&A workflow"""
    with patch('backend.services.document_service.DocumentService.get_document', new_callable=AsyncMock) as mock_get:
        mock_doc = MagicMock()
        mock_doc.id = sample_document['id']
        mock_doc.text_content = sample_document['text_content']
        mock_get.return_value = mock_doc
        
        with patch('backend.langchain_workflows.qa_chain.answer_question', new_callable=AsyncMock) as mock_qa:
            mock_qa.return_value = {
                'answer': 'This is a test answer.',
                'sources': ['page 1', 'page 2']
            }
            
            with patch('backend.services.qa_service.QAService.ask', new_callable=AsyncMock) as mock_ask:
                mock_ask.return_value = {
                    'answer': 'This is a test answer.',
                    'sources': ['page 1', 'page 2'],
                    'confidence': 0.95,
                    'conversation_id': 'conv-123'
                }
                
                response = client.post(
                    f"/api/v1/documents/{sample_document['id']}/qa",
                    json={"question": "What is this document about?"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert "answer" in data
                assert "sources" in data
                assert "conversation_id" in data


@pytest.mark.asyncio
async def test_document_processing_flow(client):
    """Test document processing workflow"""
    with patch('pathlib.Path.mkdir'):
        with patch('builtins.open', create=True):
            with patch('backend.services.document_service.DocumentService.create_document', new_callable=AsyncMock) as mock_create:
                mock_doc = MagicMock()
                mock_doc.id = 'new-doc-id'
                mock_doc.filename = 'test.pdf'
                mock_create.return_value = mock_doc
                
                # Upload document
                from io import BytesIO
                test_file = ("test.pdf", BytesIO(b"test"), "application/pdf")
                
                response = client.post(
                    "/api/v1/documents/upload",
                    files={"file": test_file}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data['id'] == 'new-doc-id'
                assert data['filename'] == 'test.pdf'


@pytest.mark.asyncio
async def test_conversation_flow(client):
    """Test complete conversation workflow"""
    with patch('sqlalchemy.ext.asyncio.AsyncSession.execute', new_callable=AsyncMock) as mock_execute:
        # Mock list conversations
        mock_result = AsyncMock()
        mock_result.scalars().all.return_value = []
        mock_execute.return_value = mock_result
        
        response = client.get("/api/v1/conversations")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_translation_flow(client, sample_document):
    """Test document translation workflow"""
    with patch('backend.services.document_service.DocumentService.get_document', new_callable=AsyncMock) as mock_get:
        mock_doc = MagicMock()
        mock_doc.id = sample_document['id']
        mock_doc.text_content = "Hello world"
        mock_get.return_value = mock_doc
        
        with patch('backend.langchain_workflows.translation_chain.translate', new_callable=AsyncMock) as mock_translate:
            mock_translate.return_value = "Hola mundo"
            
            response = client.post(
                f"/api/v1/documents/{sample_document['id']}/translate",
                json={"target_language": "es"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "translated_text" in data
            assert data["target_language"] == "es"

