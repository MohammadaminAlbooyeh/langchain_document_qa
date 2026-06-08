#!/usr/bin/env python3
"""Setup vector database for the application."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.vector_stores.chroma_store import ChromaStore
from backend.utils.config import get_settings


async def main():
    print("Setting up vector database...")
    settings = get_settings()
    
    if settings.vector_store_type != "chroma":
        print(f"Vector store type is {settings.vector_store_type}, skipping Chroma setup")
        return
    
    store = ChromaStore()
    await store.initialize()
    print("Vector database setup complete!")


if __name__ == "__main__":
    asyncio.run(main())