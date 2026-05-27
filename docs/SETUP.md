# Setup Guide

## Prerequisites
- Python 3.12+
- Node.js 20+
- Docker (optional)

## Installation

### Backend
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn backend.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Docker
```bash
docker-compose up
```
