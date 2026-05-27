from backend.langchain_workflows.embedding_generator import generate_embeddings


def test_generate_embeddings():
    text = "Test embedding generation"
    embedding = generate_embeddings(text)
    assert isinstance(embedding, list)
    assert len(embedding) > 0
