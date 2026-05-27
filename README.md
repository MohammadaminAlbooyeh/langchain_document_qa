# LangChain Document QA

A comprehensive document question-answering system built with LangChain, FastAPI, and React.

## Features

- **Document Processing**: Load and process PDF, DOCX, TXT, CSV files and web content
- **Text Splitting**: Intelligent chunking strategies (token, sentence, overlapping)
- **Vector Embeddings**: Generate and cache embeddings using multiple providers
- **Vector Stores**: Chroma, FAISS, and Pinecone support
- **Q&A System**: Retrieval-Augmented Generation (RAG) pipeline
- **Summarization**: Document summarization with multiple modes
- **Entity Extraction**: Extract names, dates, amounts from documents
- **Translation**: Multi-language document translation
- **Conversation Memory**: Persistent chat history
- **LangGraph Workflows**: Multi-step agentic workflows
- **REST API**: Full FastAPI backend with OpenAPI docs
- **React Frontend**: Modern UI with Tailwind CSS

## Setup

```bash
# Clone the repository
git clone <repo-url>
cd langchain-document-qa

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run the application
docker-compose up
```

## Project Structure

```
backend/         # FastAPI Python backend
frontend/        # React frontend
notebooks/       # Jupyter notebooks for experimentation
data/            # Raw and processed data
models/          # Serialized models
tests/           # Unit, integration, and load tests
scripts/         # Utility scripts
docs/            # Documentation
config/          # Configuration files
```

## License

MIT
