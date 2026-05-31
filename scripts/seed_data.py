#!/usr/bin/env python3
import asyncio
from backend.models.database import get_session
from backend.models.document import Document
from datetime import datetime
import uuid


async def main():
    print("Seeding sample data...")
    from backend.models.database import async_session
    from sqlalchemy import select

    async with async_session() as session:
        result = await session.execute(select(Document))
        existing = result.scalars().all()
        if existing:
            print(f"Found {len(existing)} existing documents. Skipping seed.")
            return

        sample_docs = [
            Document(
                id=str(uuid.uuid4()),
                filename="sample_report.pdf",
                file_type="pdf",
                file_size=20480,
                file_path="data/samples/sample_report.pdf",
                status=DocumentStatus.PROCESSED,
                text_content="This is a sample report about quarterly earnings. The company reported strong growth in Q3 with revenue increasing by 25% year-over-year. Operating income reached $1.2 billion. The board approved a $500 million share buyback program.",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
            Document(
                id=str(uuid.uuid4()),
                filename="sample_contract.docx",
                file_type="docx",
                file_size=15360,
                file_path="data/samples/sample_contract.docx",
                status=DocumentStatus.PROCESSED,
                text_content="This agreement is entered into between Acme Corp and Beta Inc. The effective date is January 1, 2025. The contract value is $2.5 million. Both parties agree to the terms and conditions outlined herein.",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
            Document(
                id=str(uuid.uuid4()),
                filename="sample_manual.txt",
                file_type="txt",
                file_size=8192,
                file_path="data/samples/sample_manual.txt",
                status=DocumentStatus.PROCESSED,
                text_content="Welcome to the product manual. This document covers installation, configuration, and troubleshooting steps. For support, contact support@example.com or call 1-800-555-0199.",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
        ]

        for doc in sample_docs:
            session.add(doc)

        await session.commit()
        print(f"Seeded {len(sample_docs)} sample documents.")


if __name__ == "__main__":
    asyncio.run(main())
