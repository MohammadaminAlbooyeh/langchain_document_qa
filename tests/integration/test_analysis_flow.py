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
async def test_full_analysis_flow(async_client):
    with patch('backend.services.document_service.DocumentService.get_document', new_callable=AsyncMock) as mock_get:
        mock_doc = MagicMock()
        mock_doc.id = 'test-doc-id'
        mock_doc.text_content = "John Smith and Jane Doe met in New York on 2024-05-27."
        mock_doc.filename = "test.pdf"
        mock_get.return_value = mock_doc

        mock_path = 'backend.langchain_workflows.entity_extraction.extract_entities'
        with patch(mock_path, new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = {
                'PERSON': ['John Smith', 'Jane Doe'],
                'LOCATION': ['New York'],
                'DATE': ['2024-05-27']
            }

            response = await async_client.post(
                "/api/v1/documents/test-doc-id/extract-entities"
            )

            assert response.status_code == 200
            data = response.json()
            assert "entities" in data
            assert 'PERSON' in data['entities']
            assert 'LOCATION' in data['entities']
