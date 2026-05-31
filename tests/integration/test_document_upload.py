import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from io import BytesIO


@pytest.fixture
async def async_client():
    from backend.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
def mock_background_tasks():
    with patch('fastapi.BackgroundTasks.add_task'):
        yield


@pytest.mark.asyncio
async def test_document_upload_flow(async_client):
    with patch('pathlib.Path.mkdir'):
        with patch('builtins.open', create=True):
            mock_path = 'backend.services.document_service.DocumentService.create_document'
            with patch(mock_path, new_callable=AsyncMock) as mock_create:
                mock_doc = MagicMock()
                mock_doc.id = 'new-doc-id'
                mock_doc.filename = 'test.pdf'
                mock_create.return_value = mock_doc

                response = await async_client.post(
                    "/api/v1/documents/upload",
                    files={"file": ("test.pdf", BytesIO(b"test"), "application/pdf")}
                )

                assert response.status_code == 200
                data = response.json()
                assert data['id'] == 'new-doc-id'
                assert data['filename'] == 'test.pdf'


@pytest.mark.asyncio
async def test_document_processing_flow(async_client):
    with patch('pathlib.Path.mkdir'):
        with patch('builtins.open', create=True):
            mock_path = 'backend.services.document_service.DocumentService.create_document'
            with patch(mock_path, new_callable=AsyncMock) as mock_create:
                mock_doc = MagicMock()
                mock_doc.id = 'new-doc-456'
                mock_doc.filename = 'report.docx'
                mock_create.return_value = mock_doc

                response = await async_client.post(
                    "/api/v1/documents/upload",
                    files={"file": ("report.docx", BytesIO(b"report content"), "application/octet-stream")}
                )

                assert response.status_code == 200
                data = response.json()
                assert data['filename'] == 'report.docx'
