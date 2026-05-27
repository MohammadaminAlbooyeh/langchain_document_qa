import pytest


@pytest.fixture
def sample_text():
    return "This is a sample document text for testing purposes."


@pytest.fixture
def sample_question():
    return "What is this document about?"


@pytest.fixture
def mock_document():
    return {
        "id": "test-doc-123",
        "filename": "test_document.pdf",
        "file_type": "pdf",
        "file_size": 1024,
        "status": "processed",
    }
