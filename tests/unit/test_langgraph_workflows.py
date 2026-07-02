import pytest
from unittest.mock import patch, AsyncMock, MagicMock


class TestQAWorkflow:
    @pytest.mark.asyncio
    async def test_qa_workflow_retrieve_and_answer(self):
        with patch('backend.langchain_workflows.langgraph_workflows.qa_workflow.retrieve_context', new_callable=AsyncMock) as mock_retrieve:
            mock_retrieve.return_value = ["Context doc"]
            with patch('backend.langchain_workflows.langgraph_workflows.qa_workflow.generate_response', new_callable=AsyncMock) as mock_generate:
                mock_generate.return_value = "Answer text"

                from backend.langchain_workflows.langgraph_workflows.qa_workflow import qa_workflow

                result = await qa_workflow.ainvoke({"question": "What is this?"})
                assert result["answer"] == "Answer text"
                assert result["context"] == ["Context doc"]

    @pytest.mark.asyncio
    async def test_qa_workflow_no_context(self):
        from backend.langchain_workflows.langgraph_workflows.qa_workflow import qa_workflow

        result = await qa_workflow.ainvoke({"question": "What is this?"})
        assert result.get("answer") is None or result.get("error")


class TestDocumentWorkflow:
    @pytest.mark.asyncio
    async def test_document_workflow_full_pipeline(self):
        with patch('backend.langchain_workflows.langgraph_workflows.document_workflow.extract_text', new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = "Full document text"
            with patch('backend.langchain_workflows.langgraph_workflows.document_workflow.create_overlapping_chunks') as mock_chunk:
                mock_chunk.return_value = ["chunk1", "chunk2"]
                with patch('backend.langchain_workflows.langgraph_workflows.document_workflow.batch_embed', new_callable=AsyncMock) as mock_embed:
                    mock_embed.return_value = [[0.1, 0.2], [0.3, 0.4]]
                    with patch('backend.langchain_workflows.langgraph_workflows.document_workflow.store_embeddings', new_callable=AsyncMock) as mock_store:
                        mock_store.return_value = None

                        from backend.langchain_workflows.langgraph_workflows.document_workflow import document_workflow

                        result = await document_workflow.ainvoke({"file_path": "/tmp/test.pdf"})
                        assert result["raw_text"] == "Full document text"
                        assert result["chunks"] == ["chunk1", "chunk2"]
                        assert result["error"] is None

    @pytest.mark.asyncio
    async def test_document_workflow_extract_fails(self):
        with patch('backend.langchain_workflows.langgraph_workflows.document_workflow.extract_text', new_callable=AsyncMock) as mock_extract:
            mock_extract.side_effect = Exception("File not found")

            from backend.langchain_workflows.langgraph_workflows.document_workflow import document_workflow

            result = await document_workflow.ainvoke({"file_path": "/nonexistent.pdf"})
            assert result["error"] is not None


class TestAnalysisWorkflow:
    @pytest.mark.asyncio
    async def test_analysis_workflow_summarize(self):
        with patch('backend.langchain_workflows.langgraph_workflows.analysis_workflow.extract_text', new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = "Document text"
            with patch('backend.langchain_workflows.langgraph_workflows.analysis_workflow.summarize_document', new_callable=AsyncMock) as mock_sum:
                mock_sum.return_value = "Summary text"

                from backend.langchain_workflows.langgraph_workflows.analysis_workflow import analysis_workflow

                result = await analysis_workflow.ainvoke({"file_path": "/tmp/doc.pdf", "mode": "summarize"})
                assert result["summary"] == "Summary text"
                assert result["text"] == "Document text"

    @pytest.mark.asyncio
    async def test_analysis_workflow_extract_entities(self):
        with patch('backend.langchain_workflows.langgraph_workflows.analysis_workflow.extract_text', new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = "John Smith works at Acme."
            with patch('backend.langchain_workflows.langgraph_workflows.analysis_workflow.extract_entities', new_callable=AsyncMock) as mock_entity:
                mock_entity.return_value = {"PERSON": ["John Smith"], "ORGANIZATION": ["Acme"]}

                from backend.langchain_workflows.langgraph_workflows.analysis_workflow import analysis_workflow

                result = await analysis_workflow.ainvoke({"file_path": "/tmp/doc.pdf", "mode": "extract"})
                assert "PERSON" in result["entities"]
                assert "John Smith" in result["entities"]["PERSON"]


class TestAgentWorkflow:
    @pytest.mark.asyncio
    async def test_agent_classifies_qa_intent(self):
        with patch('backend.langchain_workflows.langgraph_workflows.agent_workflow._llm') as mock_llm:
            mock_response = MagicMock()
            mock_response.content = "QA"
            mock_llm.ainvoke.return_value = mock_response

            with patch('backend.langchain_workflows.langgraph_workflows.agent_workflow.answer_question', new_callable=AsyncMock) as mock_qa:
                mock_qa.return_value = {"answer": "Test answer"}

                from backend.langchain_workflows.langgraph_workflows.agent_workflow import agent_workflow

                result = await agent_workflow.ainvoke({"input": "What is this document about?"})
                assert result["intent"] == "QA"

    @pytest.mark.asyncio
    async def test_agent_classifies_translate_intent(self):
        with patch('backend.langchain_workflows.langgraph_workflows.agent_workflow._llm') as mock_llm:
            mock_response = MagicMock()
            mock_response.content = "TRANSLATE"
            mock_llm.ainvoke.return_value = mock_response

            with patch('backend.langchain_workflows.langgraph_workflows.agent_workflow.translate', new_callable=AsyncMock) as mock_translate:
                mock_translate.return_value = "Translated text"

                from backend.langchain_workflows.langgraph_workflows.agent_workflow import agent_workflow

                result = await agent_workflow.ainvoke({"input": "Translate this to French"})
                assert result["intent"] == "TRANSLATE"

    def test_route_intent(self):
        from backend.langchain_workflows.langgraph_workflows.agent_workflow import route_intent

        state = MagicMock()
        state.__getitem__.side_effect = lambda key: {"intent": "QA"}["intent"]
        assert route_intent({"intent": "QA"}) == "qa"
        assert route_intent({"intent": "SUMMARIZE"}) == "summarize"
        assert route_intent({"intent": "TRANSLATE"}) == "translate"
        assert route_intent({"intent": "UNKNOWN"}) == "unknown"
