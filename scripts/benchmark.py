#!/usr/bin/env python3
"""Run performance benchmarks for the application."""

import asyncio
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.langchain_workflows.qa_chain import answer_question
from backend.langchain_workflows.summarization_chain import summarize_text
from backend.langchain_workflows.entity_extraction import extract_entities


async def benchmark_qa():
    """Benchmark QA chain."""
    test_question = "What is the main topic of the document?"
    test_context = "This is a test document about machine learning and artificial intelligence. " * 50
    
    start = time.perf_counter()
    for _ in range(10):
        await answer_question(test_question, test_context)
    elapsed = time.perf_counter() - start
    print(f"QA Chain (10 runs): {elapsed:.2f}s ({10/elapsed:.1f} ops/sec)")


async def benchmark_summarization():
    """Benchmark summarization chain."""
    test_text = "This is a test document about machine learning and artificial intelligence. " * 100
    
    start = time.perf_counter()
    for _ in range(5):
        await summarize_text(test_text, "paragraph")
    elapsed = time.perf_counter() - start
    print(f"Summarization (5 runs): {elapsed:.2f}s ({5/elapsed:.1f} ops/sec)")


async def benchmark_entity_extraction():
    """Benchmark entity extraction."""
    test_text = "John Smith works at Google in New York. He met with Jane Doe from Microsoft on January 15, 2024. The deal was worth $1.5 million."
    
    start = time.perf_counter()
    for _ in range(10):
        await extract_entities(test_text)
    elapsed = time.perf_counter() - start
    print(f"Entity Extraction (10 runs): {elapsed:.2f}s ({10/elapsed:.1f} ops/sec)")


async def main():
    print("Running benchmarks...\n")
    
    await benchmark_qa()
    await benchmark_summarization()
    await benchmark_entity_extraction()
    
    print("\nBenchmark complete!")


if __name__ == "__main__":
    asyncio.run(main())