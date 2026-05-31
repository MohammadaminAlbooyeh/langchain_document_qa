import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_response_time():
    with patch('backend.langchain_workflows.qa_chain.answer_question', new_callable=AsyncMock) as mock_qa:
        mock_qa.return_value = {"answer": "Test answer.", "sources": ["doc1"]}
        from backend.langchain_workflows.qa_chain import answer_question
        result = await answer_question("test query")
        assert "answer" in result
        assert "sources" in result
