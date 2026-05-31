import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport


@pytest.fixture
async def async_client():
    from backend.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_qa_flow(async_client):
    with patch('backend.services.document_service.DocumentService.get_document', new_callable=AsyncMock) as mock_get:
        mock_doc = MagicMock()
        mock_doc.id = 'test-doc-id'
        mock_doc.text_content = "Sample document text."
        mock_doc.filename = "test.pdf"
        mock_get.return_value = mock_doc

        with patch('backend.services.qa_service.QAService.ask', new_callable=AsyncMock) as mock_ask:
            mock_ask.return_value = {
                'answer': 'Test answer.',
                'sources': ['page 1'],
                'confidence': 0.95,
                'conversation_id': 'conv-123'
            }

            response = await async_client.post(
                "/api/v1/documents/test-doc-id/qa",
                json={"question": "What is this about?"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert "sources" in data
            assert "conversation_id" in data
