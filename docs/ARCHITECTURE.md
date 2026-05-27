# Architecture

## System Overview

```
Frontend (React) -> API (FastAPI) -> LangChain Workflows -> LLM / Vector Store
```

## Components

1. **Frontend**: React SPA with Tailwind CSS
2. **Backend API**: FastAPI with async support
3. **LangChain Workflows**: Document processing, Q&A, summarization
4. **Vector Store**: Chroma/FAISS/Pinecone for embeddings
5. **LLM**: OpenAI/Anthropic/Local models
6. **Database**: SQLite/PostgreSQL via SQLAlchemy
