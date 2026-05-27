from backend.langchain_workflows.summarization_chain import summarize_document


@pytest.mark.asyncio
async def test_summarize_document(sample_text):
    summary = await summarize_document(sample_text)
    assert isinstance(summary, str)
    assert len(summary) > 0
