# Usage Examples

## Upload a Document
```python
POST /api/v1/documents/upload
Content-Type: multipart/form-data
File: report.pdf
```

## Ask a Question
```python
POST /api/v1/documents/{id}/qa
{"question": "What is the main topic?"}
```

## Summarize
```python
POST /api/v1/documents/{id}/summarize
{"mode": "paragraphs"}
```
