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
async def test_end_to_end(async_client):
    with patch('backend.services.document_service.DocumentService.get_document', new_callable=AsyncMock) as mock_get:
        mock_doc = MagicMock()
        mock_doc.id = 'test-doc-id'
        mock_doc.text_content = "Sample document with useful information for analysis."
        mock_doc.filename = "test.pdf"
        mock_get.return_value = mock_doc

        mock_path = 'backend.langchain_workflows.summarization_chain.summarize_text'
        with patch(mock_path, new_callable=AsyncMock) as mock_summarize:
            mock_summarize.return_value = "Summary of the document."

            response = await async_client.post(
                "/api/v1/documents/test-doc-id/summarize",
                json={"mode": "paragraphs"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "summary" in data
            assert data["mode"] == "paragraphs"
