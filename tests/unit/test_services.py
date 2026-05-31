import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from backend.services.document_service import DocumentService
from backend.services.qa_service import QAService


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    mock_result = MagicMock()
    mock_result.scalars = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_result.scalar_one_or_none.return_value = None
    db.execute.return_value = mock_result

    return db


@pytest.mark.asyncio
async def test_document_service_create(mock_db):
    mock_db.execute.reset_mock()
    mock_db.execute.return_value = MagicMock()
    mock_db.execute.return_value.scalar_one_or_none.return_value = None

    service = DocumentService(mock_db)

    await service.create_document(
        filename="test.pdf",
        file_type="pdf",
        file_size=1024,
        file_path="/tmp/test.pdf"
    )

    assert mock_db.add.called
    assert mock_db.commit.called
    assert mock_db.refresh.called


@pytest.mark.asyncio
async def test_document_service_list(mock_db):
    service = DocumentService(mock_db)

    docs = await service.list_documents()

    assert isinstance(docs, list)
    assert mock_db.execute.called


@pytest.mark.asyncio
async def test_document_service_get(mock_db):
    service = DocumentService(mock_db)

    doc = await service.get_document("non-existent-id")

    assert doc is None
    assert mock_db.execute.called


@pytest.mark.asyncio
async def test_document_service_delete(mock_db):
    service = DocumentService(mock_db)

    with patch('pathlib.Path.exists', return_value=False):
        with patch('pathlib.Path.unlink'):
            await service.delete_document("test-id")
            assert mock_db.execute.called


def test_text_splitter():
    from backend.langchain_workflows.text_splitter import create_overlapping_chunks

    text = "This is a test. " * 200
    chunks = create_overlapping_chunks(text, chunk_size=500, chunk_overlap=100)

    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)


def test_extract_names():
    from backend.langchain_workflows.entity_extraction import extract_names

    text = "John Smith and Mary Johnson attended the meeting."
    names = extract_names(text)

    assert "John Smith" in names
    assert "Mary Johnson" in names


def test_extract_dates():
    from backend.langchain_workflows.entity_extraction import extract_dates

    text = "The event is on 2024-05-27 and also on 05/27/2024."
    dates = extract_dates(text)

    assert len(dates) > 0


def test_extract_amounts():
    from backend.langchain_workflows.entity_extraction import extract_amounts

    text = "The price is $100.50 or 100.50 USD."
    amounts = extract_amounts(text)

    assert len(amounts) > 0


@pytest.mark.asyncio
async def test_qa_service_ask(mock_db):
    service = QAService(mock_db)

    with patch('backend.langchain_workflows.qa_chain.answer_question') as mock_answer:
        mock_answer.return_value = {
            "answer": "Test answer",
            "sources": ["source1.pdf"]
        }

        result = await service.ask(
            document_id="test-id",
            question="Test question?"
        )

        assert "answer" in result
        assert "conversation_id" in result
        assert mock_db.add.called
        assert mock_db.commit.called
