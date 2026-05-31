import os
import pytest
from unittest.mock import AsyncMock
import asyncio

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)

# Set test environment variables BEFORE importing app modules
os.environ.setdefault('OPENAI_API_KEY', 'test-key')
os.environ.setdefault('ANTHROPIC_API_KEY', 'test-key')
os.environ.setdefault('DATABASE_URL', 'sqlite+aiosqlite:///:memory:')
os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('VECTOR_STORE_TYPE', 'chroma')
os.environ.setdefault('MAX_UPLOAD_SIZE', '100')


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


@pytest.fixture
def async_mock():
    """Provide AsyncMock fixture"""
    return AsyncMock


@pytest.fixture(scope="session")
def event_loop_policy():
    """Set event loop policy for test session."""
    policy = asyncio.get_event_loop_policy()
    return policy


def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "asyncio: mark test as an asyncio test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
