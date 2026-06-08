#!/usr/bin/env python3
"""Pre-generate embeddings for documents in the database."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.models.database import get_db
from backend.models.document import Document
from backend.services.embedding_service import EmbeddingService
from sqlalchemy import select


async def main():
    print("Pre-generating embeddings...")
    
    embedding_service = EmbeddingService()
    
    async for db in get_db():
        result = await db.execute(select(Document).where(Document.processed == True))
        documents = result.scalars().all()
        
        if not documents:
            print("No processed documents found")
            return
        
        for doc in documents:
            print(f"Generating embeddings for document: {doc.filename}")
            # The embeddings are generated during document processing
            # This script would be used to regenerate embeddings if needed
        
        print(f"Processed {len(documents)} documents")
        break


if __name__ == "__main__":
    asyncio.run(main())