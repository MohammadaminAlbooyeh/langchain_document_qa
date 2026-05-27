# Deployment Guide

This guide provides instructions for deploying the LangChain Document QA system to production.

## Prerequisites

- Docker & Docker Compose
- Kubernetes cluster (optional, for K8s deployment)
- API Keys (OpenAI, Anthropic, etc.)
- PostgreSQL database (optional, for production)

## Local Development

### Using Docker Compose

1. Clone the repository:
```bash
git clone <repo-url>
cd langchain_document_qa
```

2. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Build and run:
```bash
docker-compose up -d
```

4. Access the application:
- Frontend: http://localhost:3000
- API: http://localhost:8000/api/v1
- API Docs: http://localhost:8000/docs

### Local Setup (Without Docker)

#### Backend Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize database:
```bash
python -m backend.models.database
```

4. Run backend:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create `.env.local`:
```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_PREFIX=/api/v1
```

3. Run development server:
```bash
npm start
```

## Production Deployment

### Using Docker Compose

1. Create production `.env`:
```bash
# Database
DATABASE_URL=postgresql://user:password@db:5432/langchain_qa

# API Keys
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Application
DEBUG=False
LOG_LEVEL=INFO
```

2. Deploy:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment

1. Create namespace:
```bash
kubectl create namespace langchain-qa
```

2. Create secrets:
```bash
kubectl create secret generic langchain-qa-secrets \
  --from-literal=openai-api-key=your_key \
  --from-literal=database-url=postgresql://... \
  -n langchain-qa
```

3. Deploy applications:
```bash
kubectl apply -f kubernetes/ -n langchain-qa
```

4. Check status:
```bash
kubectl get all -n langchain-qa
kubectl logs deployment/backend -n langchain-qa
```

## Performance Optimization

### Caching Strategy

Enable Redis caching for embeddings and query results.

### Database Optimization

Create indexes for frequently queried columns:
```sql
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_qa_pairs_document_id ON qa_pairs(document_id);
```

## Monitoring & Logging

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Database connection
curl http://localhost:8000/health/db

# Vector store
curl http://localhost:8000/health/vector-store
```

### Log Files

Logs are stored in `/var/log/langchain_qa/`:
- `application.log` - General application logs
- `error.log` - Error logs
- `access.log` - API access logs

## Scaling

### Horizontal Scaling

Use Kubernetes HPA (Horizontal Pod Autoscaler) or Docker Swarm for load balancing.

### Vertical Scaling

Increase resource allocations for memory and CPU as needed.

## Backup & Recovery

### Database Backups

Daily backup:
```bash
pg_dump langchain_qa > backup_$(date +%Y%m%d).sql
```

Restore:
```bash
psql langchain_qa < backup_20240527.sql
```

### Vector Store Backups

Chroma automatically persists data to disk. For production, configure persistent storage.

## Security

- Use environment variables for secrets
- Enable HTTPS/TLS in production
- Configure firewall rules
- Implement rate limiting
- Regular security updates

## Troubleshooting

### Database Connection Issues
```bash
python -c "from backend.models.database import init_db; import asyncio; asyncio.run(init_db())"
```

### Vector Store Issues
```bash
python scripts/check_vector_store.py
```

### API Errors
Check logs:
```bash
docker logs -f backend
```

## Rollback

Rollback to previous version:
```bash
docker-compose down
docker-compose up -d  # with previous image tag
```

For Kubernetes:
```bash
kubectl rollout undo deployment/backend -n langchain-qa
```

## Further Reading

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Docs](https://kubernetes.io/docs/)
- [PostgreSQL Best Practices](https://www.postgresql.org/docs/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

