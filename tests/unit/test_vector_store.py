from backend.langchain_workflows.vector_store_manager import search_similar


def test_vector_store_search():
    results = search_similar("test query", k=1)
    assert isinstance(results, list)
