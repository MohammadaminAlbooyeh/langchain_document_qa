from backend.langchain_workflows.text_splitter import create_overlapping_chunks


def test_create_overlapping_chunks():
    text = "Word " * 5000
    chunks = create_overlapping_chunks(text, chunk_size=1000, chunk_overlap=200)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk.split()) <= 1000
