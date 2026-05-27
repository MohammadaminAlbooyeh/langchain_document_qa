# Testing Guide

This document describes how to run tests for the LangChain Document QA project.

## Prerequisites

Install test dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

### All Tests
```bash
pytest
```

### Unit Tests Only
```bash
pytest tests/unit -v
```

### Integration Tests Only
```bash
pytest tests/integration -v
```

### Specific Test File
```bash
pytest tests/unit/test_services.py -v
```

### With Coverage Report
```bash
pytest --cov=backend --cov-report=html
```

## Test Structure

```
tests/
├── unit/
│   ├── test_services.py         # Service layer tests
│   ├── test_text_splitter.py    # Text processing tests
│   ├── test_entity_extraction.py # Entity extraction tests
│   ├── test_embedding.py        # Embedding tests
│   └── test_qa_chain.py         # Q&A chain tests
├── integration/
│   ├── test_api_endpoints.py    # API endpoint tests
│   ├── test_summarization_flow.py # Complete workflows
│   ├── test_qa_flow.py
│   └── test_document_upload.py
└── conftest.py                   # Shared fixtures
```

## Test Coverage

Current test coverage includes:

### Unit Tests
- Document service (create, list, get, delete, process)
- QA service (ask questions, get history)
- Text splitting (token, sentence, overlapping chunks)
- Entity extraction (names, dates, amounts)
- Embedding generation

### Integration Tests
- Document upload flow
- Q&A workflow
- Summarization workflow
- Entity extraction workflow
- Translation workflow
- Conversation management

### API Endpoint Tests
- Document endpoints (GET, POST, DELETE)
- Q&A endpoints
- Summarization endpoints
- Entity extraction endpoints
- Translation endpoints
- Conversation endpoints

## Mocking Strategy

Tests use mocks for:
- Database operations (AsyncMock)
- LLM calls (openai, anthropic)
- File system operations
- Vector store operations

This allows tests to run quickly without requiring API keys or external services.

## Environment Variables for Testing

Tests automatically set these environment variables:
- `OPENAI_API_KEY=test-key`
- `ANTHROPIC_API_KEY=test-key`
- `DATABASE_URL=sqlite+aiosqlite:///:memory:`
- `DEBUG=True`
- `VECTOR_STORE_TYPE=chroma`
- `MAX_UPLOAD_SIZE=100`

## Continuous Integration

To run tests in CI/CD:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest --cov=backend --cov-report=xml

# Check code quality
black --check backend/
flake8 backend/
mypy backend/ --ignore-missing-imports
```

## Debugging Tests

Run tests with verbose output:
```bash
pytest -vv
```

Run specific test with full output:
```bash
pytest tests/unit/test_services.py::test_document_service_create -vv -s
```

Print statements in tests:
```bash
pytest -s  # Shows print() statements
```

## Performance Testing

For performance/load testing:
```bash
# Run specific performance test
pytest tests/performance/ -v
```

## Known Limitations

- Tests use mocked LLM responses
- Database tests use in-memory SQLite
- File uploads use temporary directories
- Vector store operations are mocked

To test with real services, set:
```bash
export OPENAI_API_KEY=your_key_here
export USE_REAL_SERVICES=true
```

## Adding New Tests

1. Create test file in appropriate directory (unit/ or integration/)
2. Use naming convention: `test_*.py`
3. Use fixtures from `conftest.py`
4. Mock external services
5. Follow existing test patterns

Example:
```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_feature(mock_db):
    # Arrange
    with patch('module.function', new_callable=AsyncMock) as mock_func:
        mock_func.return_value = expected_value
        
        # Act
        result = await function_under_test()
        
        # Assert
        assert result == expected_value
        assert mock_func.called
```

## Troubleshooting

### Import errors
Ensure you're running pytest from the project root:
```bash
cd /path/to/langchain_document_qa
pytest
```

### Async/await issues
Tests using `async def` should have the `@pytest.mark.asyncio` decorator.

### Database issues
Tests use in-memory SQLite by default. If you need a real database:
```bash
export DATABASE_URL=sqlite:///./test.db
pytest
```

### Mocking issues
Make sure to patch at the location where the object is used, not where it's defined:
```python
# Correct
with patch('backend.services.document_service.DocumentService.get_document'):
    pass

# Incorrect
with patch('backend.models.document.Document'):
    pass
```
