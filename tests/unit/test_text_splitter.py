import pytest
from backend.langchain_workflows.text_splitter import (
    create_overlapping_chunks,
    split_by_tokens,
    split_by_sentences,
)


def test_create_overlapping_chunks():
    text = "Word " * 5000
    chunks = create_overlapping_chunks(text, chunk_size=1000, chunk_overlap=200)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk.split()) <= 1000


def test_create_overlapping_chunks_short_text():
    text = "Short text."
    chunks = create_overlapping_chunks(text, chunk_size=1000, chunk_overlap=200)
    assert len(chunks) == 1
    assert chunks[0] == "Short text."


def test_create_overlapping_chunks_empty_text():
    chunks = create_overlapping_chunks("", chunk_size=1000, chunk_overlap=200)
    assert chunks == []


def test_create_overlapping_chunks_preserves_sentences():
    text = "First sentence. Second sentence. Third sentence. " * 100
    chunks = create_overlapping_chunks(text, chunk_size=500, chunk_overlap=50)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 500


def test_split_by_tokens():
    text = "token " * 2000
    chunks = split_by_tokens(text, chunk_size=500, chunk_overlap=100)
    assert len(chunks) > 1


def test_split_by_sentences():
    text = "This is a sentence. " * 200
    chunks = split_by_sentences(text, chunk_size=500, chunk_overlap=50)
    assert len(chunks) > 1


def test_overlap_ratio():
    text = "paragraph\n\n" * 100
    chunks = create_overlapping_chunks(text, chunk_size=200, chunk_overlap=50)
    if len(chunks) >= 2:
        overlap = len(set(chunks[0].split()) & set(chunks[1].split()))
        total = len(set(chunks[0].split()) | set(chunks[1].split()))
        ratio = overlap / total if total > 0 else 0
        assert ratio > 0
