from unittest.mock import patch


def test_generate_embeddings():
    with patch('backend.langchain_workflows.embedding_generator.OpenAIEmbeddings') as mock_emb:
        mock_instance = mock_emb.return_value
        mock_instance.embed_query.return_value = [0.1, 0.2, 0.3]
        from backend.langchain_workflows.embedding_generator import generate_embeddings
        embedding = generate_embeddings("Test embedding generation")
        assert isinstance(embedding, list)
        assert len(embedding) > 0
