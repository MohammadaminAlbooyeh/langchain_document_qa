#!/usr/bin/env python3
"""Upload sample documents for testing."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.document_service import DocumentService


async def main():
    print("Uploading sample documents...")
    
    service = DocumentService()
    
    sample_docs = [
        {
            "filename": "sample_ai.txt",
            "content": """Artificial Intelligence (AI) is a branch of computer science that aims to create 
software or machines that exhibit human-like intelligence. The field was founded in 1956 at a 
conference at Dartmouth College. Early AI research focused on problem solving and symbolic methods. 
In the 1980s, expert systems were developed to mimic human decision-making. The modern era of AI 
began with the development of machine learning algorithms, particularly deep learning, which uses 
neural networks with many layers. Today, AI is used in many applications including natural language 
processing, computer vision, robotics, and autonomous vehicles. Key figures in AI include Alan Turing, 
John McCarthy, Marvin Minsky, and more recently Geoffrey Hinton, Yann LeCun, and Yoshua Bengio.""",
        },
        {
            "filename": "sample_ml.txt",
            "content": """Machine Learning (ML) is a subset of AI that enables computers to learn without being 
explicitly programmed. There are three main types of machine learning: supervised learning, unsupervised 
learning, and reinforcement learning. Supervised learning uses labeled data to train models for 
classification and regression tasks. Unsupervised learning finds patterns in unlabeled data through 
clustering and dimensionality reduction. Reinforcement learning trains agents to make decisions by 
rewarding desired behaviors. Popular algorithms include linear regression, decision trees, random forests, 
support vector machines, and neural networks. ML is used in recommendation systems, fraud detection, 
image recognition, and natural language processing.""",
        },
    ]
    
    for doc in sample_docs:
        print(f"Uploading: {doc['filename']}")
        await service.upload_document(
            file_content=doc["content"].encode(),
            filename=doc["filename"],
            content_type="text/plain",
        )
    
    print("Sample documents uploaded!")


if __name__ == "__main__":
    asyncio.run(main())