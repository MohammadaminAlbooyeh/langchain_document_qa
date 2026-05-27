# LangChain Document QA

A comprehensive document question-answering system built with LangChain, FastAPI, and React. Upload documents, ask questions, extract entities, summarize content, and translate documents using AI-powered analysis.

## Features

- **Document Processing**: Load and process PDF, DOCX, TXT files
- **Text Splitting**: Intelligent chunking strategies (token, sentence, overlapping)
- **Vector Embeddings**: Generate embeddings using OpenAI with local caching
- **Vector Stores**: Chroma, FAISS, and Pinecone support
- **Q&A System**: Retrieval-Augmented Generation (RAG) with source attribution
- **Summarization**: Document summarization with multiple modes (paragraphs, bullet points, sections)
- **Entity Extraction**: Extract names, dates, amounts from documents
- **Translation**: Multi-language document translation
- **Conversation Memory**: Persistent chat history with conversation management
- **LangGraph Workflows**: Multi-step agentic workflows
- **REST API**: Full FastAPI backend with OpenAPI docs
- **React Frontend**: Modern UI with Tailwind CSS and real-time updates

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)
- API Keys: OpenAI, Anthropic (optional)

### Local Development

#### 1. Clone Repository
```bash
git clone <repo-url>
cd langchain_document_qa
```

#### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API keys

# Start backend
uvicorn backend.main:app --reload --port 8000
```

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
echo "REACT_APP_API_URL=http://localhost:8000" > .env.local
echo "REACT_APP_API_PREFIX=/api/v1" >> .env.local

# Start frontend
npm start
```

#### 4. Access Application
- Frontend: http://localhost:3000
- API: http://localhost:8000/api/v1
- API Documentation: http://localhost:8000/docs

### Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access
- Frontend: http://localhost:3000
- API: http://localhost:8000/api/v1
```

## Project Structure

```
langchain_document_qa/
├── backend/                          # FastAPI Python backend
│   ├── api/                          # API routes and schemas
│   ├── services/                     # Business logic services
│   ├── models/                       # Database models
│   ├── langchain_workflows/          # LangChain pipelines
│   │   ├── document_processor.py     # PDF/DOCX/TXT extraction
│   │   ├── text_splitter.py          # Text chunking
│   │   ├── embedding_generator.py    # Embedding generation
│   │   ├── qa_chain.py               # Q&A RAG pipeline
│   │   ├── summarization_chain.py    # Summarization
│   │   ├── entity_extraction.py      # Entity extraction
│   │   ├── translation_chain.py      # Translation
│   │   ├── memory_manager.py         # Conversation memory
│   │   └── vector_store_manager.py   # Vector store operations
│   ├── middleware/                   # Middleware (error handling, timing)
│   ├── utils/                        # Config, logging, validators
│   ├── main.py                       # FastAPI application entry
│   └── __init__.py
│
├── frontend/                         # React frontend
│   ├── src/
│   │   ├── components/               # React components
│   │   ├── pages/                    # Page components
│   │   ├── services/                 # API service clients
│   │   ├── hooks/                    # Custom React hooks
│   │   ├── store/                    # Redux store
│   │   ├── styles/                   # CSS/Tailwind styles
│   │   ├── utils/                    # Utility functions
│   │   └── App.js                    # Root component
│   ├── public/                       # Static assets
│   └── package.json
│
├── tests/                            # Test suite
│   ├── unit/                         # Unit tests
│   ├── integration/                  # Integration tests
│   └── conftest.py                   # Pytest configuration
│
├── docs/                             # Documentation
│   ├── ARCHITECTURE.md               # System architecture
│   ├── DEPLOYMENT.md                 # Deployment guide
│   ├── TESTING.md                    # Testing guide
│   ├── API_REFERENCE.md              # API documentation
│   └── LANGCHAIN_GUIDE.md            # LangChain usage
│
├── kubernetes/                       # Kubernetes manifests
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── postgres-deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
│
├── docker-compose.yml                # Docker Compose setup
├── Dockerfile                        # Backend Docker image
├── Dockerfile.frontend               # Frontend Docker image
├── requirements.txt                  # Python dependencies
├── pytest.ini                        # Pytest configuration
└── README.md                         # This file
```

## API Endpoints

### Document Management
- `GET /api/v1/documents` - List documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/{id}` - Get document details
- `DELETE /api/v1/documents/{id}` - Delete document

### Q&A
- `POST /api/v1/documents/{id}/qa` - Ask question about document
- `GET /api/v1/conversations` - List conversations
- `GET /api/v1/conversations/{id}` - Get conversation details
- `POST /api/v1/conversations/{id}/chat` - Continue conversation
- `DELETE /api/v1/conversations/{id}` - Delete conversation

### Analysis
- `POST /api/v1/documents/{id}/summarize` - Summarize document
- `POST /api/v1/documents/{id}/extract-entities` - Extract entities
- `POST /api/v1/documents/{id}/translate` - Translate document

### Health
- `GET /health` - Health check
- `GET /health/db` - Database health
- `GET /health/vector-store` - Vector store health

See [API_REFERENCE.md](docs/API_REFERENCE.md) for detailed documentation.

## Configuration

Create `.env` file with:

```bash
# LLM Configuration
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
COHERE_API_KEY=your_key_here

# Database
DATABASE_URL=sqlite+aiosqlite:///./data/langchain_qa.db

# Vector Store
VECTOR_STORE_TYPE=chroma
PINECONE_API_KEY=optional

# Application
APP_NAME=LangChain Document QA
DEBUG=True
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE=100

# LLM Settings
DEFAULT_LLM=openai
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini
TEMPERATURE=0.0
MAX_TOKENS=4096

# Chunking
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

See [.env.example](.env.example) for complete configuration options.

## Testing

Run tests with:

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit -v

# Integration tests only
pytest tests/integration -v

# With coverage
pytest --cov=backend --cov-report=html
```

See [TESTING.md](docs/TESTING.md) for detailed testing guide.

## Deployment

### Docker Compose
```bash
docker-compose up -d
```

### Kubernetes
```bash
kubectl create namespace langchain-qa
kubectl apply -f kubernetes/ -n langchain-qa
```

### Manual Deployment
See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for complete deployment guide.

## Architecture

The system uses a modular architecture:

```
Frontend (React)
      ↓
API Gateway (FastAPI)
      ↓
    ┌─────────────────────┐
    │  Service Layer      │
    ├─────────────────────┤
    │ DocumentService     │
    │ QAService           │
    │ EmbeddingService    │
    │ VectorDBService     │
    └─────────────────────┘
      ↓
    ┌─────────────────────┐
    │ LangChain Workflows │
    ├─────────────────────┤
    │ Document Processing │
    │ Text Splitting      │
    │ Q&A Chain (RAG)     │
    │ Summarization       │
    │ Entity Extraction   │
    │ Translation         │
    └─────────────────────┘
      ↓
    ┌─────────────────────┐
    │ External Services   │
    ├─────────────────────┤
    │ OpenAI LLMs         │
    │ Vector Store        │
    │ Database (SQLite)   │
    └─────────────────────┘
```

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

## Development

### Code Style
- Python: PEP 8 (enforced with Black)
- JavaScript: ESLint + Prettier
- Use type hints in Python
- Use meaningful variable names

### Commit Conventions
```bash
git commit -m "type: description"
# Types: feat, fix, docs, style, refactor, test, chore
```

### Adding Features
1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and write tests
3. Run tests: `pytest`
4. Commit with conventional message
5. Create pull request

## Troubleshooting

### Backend Issues
```bash
# Check backend health
curl http://localhost:8000/health

# View logs
docker logs -f backend

# Check database connection
pytest tests/unit/test_services.py -v
```

### Frontend Issues
```bash
# Check API connectivity
curl http://localhost:8000/api/v1/documents

# View console logs
# Open browser DevTools (F12)

# Clear cache
rm -rf node_modules/.cache
npm start
```

### Common Errors

**"No module named 'backend'"**
- Ensure you're running from project root
- Check Python path: `export PYTHONPATH=.`

**"Could not connect to database"**
- Check DATABASE_URL in .env
- Ensure SQLite data directory exists: `mkdir -p data`

**"API key not found"**
- Copy .env.example to .env
- Add your API keys to .env

## Performance

### Optimization Tips
1. Use batch embedding generation
2. Enable Redis caching for embeddings
3. Create database indexes
4. Use connection pooling
5. Implement pagination for document lists

### Scaling
- Horizontal: Use load balancer (nginx, HAProxy)
- Vertical: Increase CPU/memory allocation
- Database: Migrate to PostgreSQL for production
- Vector Store: Use Pinecone for managed service

## Security

- ✅ Input validation on all endpoints
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ XSS protection (React escaping)
- ✅ CORS configuration
- ✅ Error handling without exposing internals
- ✅ Environment variables for secrets

Additional recommendations:
- Enable HTTPS/TLS in production
- Implement rate limiting
- Use strong database passwords
- Regular security updates
- Monitor API logs for anomalies

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Write tests
5. Submit pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

MIT License - see [LICENSE](LICENSE) file

## Support

- 📚 [Documentation](docs/)
- 🐛 [Report Issues](https://github.com/your-repo/issues)
- 💬 [Discussions](https://github.com/your-repo/discussions)
- 📧 Email: support@your-domain.com

## Changelog

### Version 1.0.0 (Current)
- ✅ Document upload and processing
- ✅ Q&A with RAG
- ✅ Document summarization
- ✅ Entity extraction
- ✅ Multi-language translation
- ✅ Conversation management
- ✅ Full REST API
- ✅ React frontend with Tailwind CSS
- ✅ Comprehensive testing
- ✅ Docker & Kubernetes support

### Planned Features
- [ ] Real-time collaboration
- [ ] Advanced analytics dashboard
- [ ] Custom model fine-tuning
- [ ] Batch processing
- [ ] WebSocket support for streaming
- [ ] Advanced caching strategies
- [ ] Multi-tenant support

## Citation

If you use this project in your research, please cite:

```bibtex
@software{langchain_document_qa,
  title = {LangChain Document QA},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/your-repo}
}
```

## Acknowledgments

Built with:
- [LangChain](https://langchain.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Chroma](https://www.trychroma.com/)
- [OpenAI](https://openai.com/)
