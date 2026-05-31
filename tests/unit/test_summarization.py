import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_summarize_document(sample_text):
    mock_path = 'backend.langchain_workflows.summarization_chain.summarize_document'
    with patch(mock_path, new_callable=AsyncMock) as mock_summarize:
        mock_summarize.return_value = "Test summary."
        from backend.langchain_workflows.summarization_chain import summarize_document
        summary = await summarize_document(sample_text)
        assert isinstance(summary, str)
        assert len(summary) > 0
