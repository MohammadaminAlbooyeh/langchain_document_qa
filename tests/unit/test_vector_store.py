import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_vector_store_search():
    with patch('backend.langchain_workflows.vector_store_manager._get_store') as mock_get_store:
        mock_store = AsyncMock()
        mock_store.asimilarity_search_with_relevance_scores.return_value = []
        mock_get_store.return_value = mock_store
        from backend.langchain_workflows.vector_store_manager import search_similar
        results = await search_similar("test query", k=1)
        assert isinstance(results, list)
