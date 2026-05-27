# API Reference

## Endpoints

### Health
- `GET /health` - Health check

### Documents
- `GET /api/v1/documents` - List documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/{id}` - Get document
- `DELETE /api/v1/documents/{id}` - Delete document

### Q&A
- `POST /api/v1/documents/{id}/qa` - Ask question
- `POST /api/v1/documents/{id}/summarize` - Summarize document
- `POST /api/v1/documents/{id}/extract-entities` - Extract entities
- `POST /api/v1/documents/{id}/translate` - Translate document

### Conversations
- `GET /api/v1/conversations` - List conversations
- `GET /api/v1/conversations/{id}` - Get conversation
- `DELETE /api/v1/conversations/{id}` - Delete conversation
