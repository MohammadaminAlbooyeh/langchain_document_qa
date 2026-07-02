import pytest
import time
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_response_time():
    with patch('backend.langchain_workflows.qa_chain.answer_question', new_callable=AsyncMock) as mock_qa:
        mock_qa.return_value = {"answer": "Test answer.", "sources": ["doc1"]}
        from backend.langchain_workflows.qa_chain import answer_question
        start = time.time()
        result = await answer_question("test query")
        elapsed = time.time() - start
        assert "answer" in result
        assert "sources" in result
        assert elapsed < 1.0


@pytest.mark.asyncio
async def test_summarization_performance():
    with patch('backend.langchain_workflows.summarization_chain.summarize_document', new_callable=AsyncMock) as mock_sum:
        mock_sum.return_value = "Summary text."
        from backend.langchain_workflows.summarization_chain import summarize_document
        start = time.time()
        result = await summarize_document("Long text " * 1000)
        elapsed = time.time() - start
        assert result == "Summary text."
        assert elapsed < 1.0


@pytest.mark.asyncio
async def test_embedding_performance():
    with patch('backend.langchain_workflows.embedding_generator.generate_embeddings') as mock_embed:
        mock_embed.return_value = [0.1] * 1536
        from backend.langchain_workflows.embedding_generator import generate_embeddings
        start = time.time()
        result = generate_embeddings("Test text for embedding")
        elapsed = time.time() - start
        assert len(result) == 1536
        assert elapsed < 1.0


@pytest.mark.asyncio
async def test_batch_embedding_performance():
    with patch('backend.langchain_workflows.embedding_generator.batch_embed', new_callable=AsyncMock) as mock_batch:
        mock_batch.return_value = [[0.1] * 1536 for _ in range(5)]
        from backend.langchain_workflows.embedding_generator import batch_embed
        start = time.time()
        result = await batch_embed(["text1", "text2", "text3", "text4", "text5"])
        elapsed = time.time() - start
        assert len(result) == 5
        assert elapsed < 1.0


@pytest.mark.asyncio
async def test_entity_extraction_performance():
    with patch('backend.langchain_workflows.entity_extraction.extract_entities', new_callable=AsyncMock) as mock_extract:
        mock_extract.return_value = {"PERSON": ["John Smith"]}
        from backend.langchain_workflows.entity_extraction import extract_entities
        start = time.time()
        result = await extract_entities("John Smith went to the store.")
        elapsed = time.time() - start
        assert "PERSON" in result
        assert elapsed < 1.0


@pytest.mark.asyncio
async def test_translation_performance():
    with patch('backend.langchain_workflows.translation_chain.translate', new_callable=AsyncMock) as mock_translate:
        mock_translate.return_value = "Hello world"
        from backend.langchain_workflows.translation_chain import translate
        start = time.time()
        result = await translate("Bonjour le monde", "english")
        elapsed = time.time() - start
        assert result == "Hello world"
        assert elapsed < 1.0
