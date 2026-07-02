# Production Deployment Guide

**Status**: Ready for production deployment  
**Last Updated**: July 2, 2026  
**Version**: 1.0.0

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Database Configuration](#database-configuration)
4. [Deployment Options](#deployment-options)
5. [Post-Deployment Verification](#post-deployment-verification)
6. [Monitoring & Alerts](#monitoring--alerts)
7. [Scaling & Performance](#scaling--performance)
8. [Disaster Recovery](#disaster-recovery)

---

## Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing: `pytest tests/ -v`
- [ ] Code coverage >80%: `pytest --cov=backend`
- [ ] Type checking passing: `mypy backend`
- [ ] Linting clean: `flake8 backend`
- [ ] Security review completed

### Dependencies
- [ ] Requirements.txt pinned to specific versions
- [ ] All packages security-scanned (`pip audit`)
- [ ] License compliance verified

### Configuration
- [ ] All env vars documented in `.env.example`
- [ ] Secrets stored in secure vault (not git)
- [ ] CORS origins configured for production domains
- [ ] SSL/TLS certificates ready

### Documentation
- [ ] API documentation generated
- [ ] Deployment runbook written
- [ ] Rollback procedure documented
- [ ] Team trained on procedures

---

## Environment Setup

### 1. System Requirements

**Minimum (Production)**
- CPU: 4 cores
- RAM: 8GB
- Storage: 50GB SSD
- OS: Linux (Ubuntu 22.04 LTS recommended)

**Recommended (High Traffic)**
- CPU: 8+ cores
- RAM: 16GB+
- Storage: 100GB+ SSD
- Database: PostgreSQL 14+
- Cache: Redis 7.0+

### 2. Environment Variables

Create `.env` file with:

```bash
# ===== Application =====
APP_NAME=LangChain Document QA
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO

# ===== Database =====
DATABASE_URL=postgresql://user:password@db-host:5432/langchain_qa
DATABASE_POOL_SIZE=20
DATABASE_POOL_RECYCLE=3600
DATABASE_ECHO=false

# ===== API Configuration =====
API_PORT=8000
API_HOST=0.0.0.0
API_KEY_PREFIX=sk_prod_
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]

# ===== LLM Providers =====
DEFAULT_LLM=openai
OPENAI_API_KEY=sk_...
ANTHROPIC_API_KEY=sk-...
COHERE_API_KEY=...

# ===== Embeddings =====
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536

# ===== Vector Store =====
VECTOR_STORE_TYPE=pinecone  # or: chroma, faiss
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=langchain-qa

# ===== Chat Models =====
CHAT_MODEL=gpt-4o-mini
TEMPERATURE=0.0
MAX_TOKENS=4096

# ===== Document Processing =====
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_UPLOAD_SIZE=100  # MB

# ===== Caching =====
CACHE_TYPE=redis  # or: memory
REDIS_URL=redis://redis-host:6379/0
CACHE_TTL=600

# ===== Security =====
SECRET_KEY=your-secret-key-min-32-chars
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_BROWSER_XSS_FILTER=true
SECURE_CONTENT_SECURITY_POLICY=true
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=true

# ===== Rate Limiting =====
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# ===== Monitoring =====
SENTRY_DSN=https://...@sentry.io/...
PROMETHEUS_ENABLED=true
LOG_TO_FILE=/var/log/langchain-qa/app.log

# ===== Email (Optional) =====
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-password
```

### 3. Database Setup (PostgreSQL)

```bash
# Connect to PostgreSQL
psql -h localhost -U postgres

# Create database
CREATE DATABASE langchain_qa;
CREATE USER langchain_user WITH PASSWORD 'secure_password_here';
ALTER ROLE langchain_user SET client_encoding TO 'utf8';
ALTER ROLE langchain_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE langchain_user SET default_transaction_deferrable TO on;
ALTER ROLE langchain_user SET default_time_zone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE langchain_qa TO langchain_user;

# Run migrations
alembic upgrade head
```

### 4. Redis Setup (Caching)

```bash
# Install Redis
apt-get install redis-server

# Configure Redis
sudo nano /etc/redis/redis.conf
# Set: requirepass your_redis_password

# Start Redis
systemctl start redis-server
systemctl enable redis-server

# Test connection
redis-cli ping
```

---

## Database Configuration

### PostgreSQL Production Setup

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: langchain_qa
      POSTGRES_USER: langchain_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U langchain_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://langchain_user:${DB_PASSWORD}@postgres:5432/langchain_qa
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "8000:8000"

volumes:
  postgres_data:
  redis_data:
```

### Backup Strategy

```bash
#!/bin/bash
# backup-db.sh - Run daily via cron

BACKUP_DIR="/backups/langchain_qa"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$DATE.sql.gz"

# Backup database
pg_dump -h localhost -U langchain_user langchain_qa | gzip > $BACKUP_FILE

# Keep only last 30 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

# Upload to S3
aws s3 cp $BACKUP_FILE s3://your-backup-bucket/database/
```

---

## Deployment Options

### Option 1: Docker Compose (Small-Medium Scale)

```bash
# 1. Build images
docker-compose -f docker-compose.prod.yml build

# 2. Start services
docker-compose -f docker-compose.prod.yml up -d

# 3. Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# 4. Verify health
curl http://localhost:8000/health
```

### Option 2: Kubernetes (Large Scale)

```bash
# 1. Create namespace
kubectl create namespace langchain-qa

# 2. Create secrets
kubectl create secret generic langchain-secrets \
  --from-literal=db-password=XXX \
  --from-literal=redis-password=YYY \
  -n langchain-qa

# 3. Deploy
kubectl apply -f kubernetes/ -n langchain-qa

# 4. Check rollout
kubectl rollout status deployment/backend -n langchain-qa

# 5. Verify services
kubectl get pods -n langchain-qa
```

### Option 3: AWS ECS (Fargate)

```bash
# 1. Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker build -t langchain-qa-backend .
docker tag langchain-qa-backend:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/langchain-qa-backend:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/langchain-qa-backend:latest

# 2. Create ECS service via AWS console or CLI
aws ecs create-service \
  --cluster production \
  --service-name langchain-qa-backend \
  --task-definition langchain-qa-backend:1 \
  --desired-count 3

# 3. Configure load balancer
aws elbv2 register-targets \
  --target-group-arn arn:aws:elasticloadbalancing:... \
  --targets Id=i-1234567890abcdef0 Id=i-0987654321fedcba1
```

---

## Post-Deployment Verification

### 1. Health Checks

```bash
# API health
curl -H "Authorization: Bearer sk_prod_..." http://your-domain.com/health

# Database health
curl http://your-domain.com/health/db

# Vector store health
curl http://your-domain.com/health/vector-store
```

### 2. End-to-End Test

```bash
#!/bin/bash
# test-deployment.sh

API_URL="https://yourdomain.com/api/v1"
API_KEY="sk_prod_..."

# Test 1: Create API key
echo "Testing API key generation..."
curl -X POST $API_URL/auth/keys/generate \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "name": "test_key"}'

# Test 2: Upload document
echo "Testing document upload..."
curl -X POST $API_URL/documents/upload \
  -H "Authorization: Bearer $API_KEY" \
  -F "file=@test.pdf"

# Test 3: Ask question
echo "Testing Q&A..."
curl -X POST $API_URL/documents/{doc_id}/qa \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'

# Test 4: Summarize
echo "Testing summarization..."
curl -X POST $API_URL/documents/{doc_id}/summarize \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mode": "paragraphs"}'
```

### 3. Performance Baseline

```bash
# Run load tests
ab -n 1000 -c 10 -H "Authorization: Bearer sk_prod_..." https://yourdomain.com/api/v1/documents

# Expected: >500 req/sec, <100ms avg response time
```

---

## Monitoring & Alerts

### 1. Prometheus Metrics

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'langchain-qa'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### 2. Key Metrics to Monitor

| Metric | Warning | Critical |
|--------|---------|----------|
| Request Latency P95 | >500ms | >2000ms |
| Error Rate | >1% | >5% |
| CPU Usage | >70% | >90% |
| Memory Usage | >75% | >85% |
| DB Connection Pool | >15/20 | >19/20 |
| Cache Hit Rate | <30% | <10% |

### 3. Alerting (PagerDuty/Slack)

```yaml
# alerting-rules.yml
groups:
  - name: langchain_qa
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
          
      - alert: HighLatency
        expr: histogram_quantile(0.95, http_request_duration_seconds) > 2
        for: 10m
        annotations:
          summary: "P95 latency above 2s"
          
      - alert: DatabaseDown
        expr: pg_up == 0
        for: 1m
        annotations:
          summary: "PostgreSQL database is down"
```

---

## Scaling & Performance

### 1. Horizontal Scaling (Multiple Instances)

```bash
# With Kubernetes
kubectl scale deployment backend --replicas=5

# With Docker Compose
docker-compose up -d --scale backend=5

# With ECS
aws ecs update-service --cluster production \
  --service langchain-qa-backend \
  --desired-count 5
```

### 2. Database Optimization

```sql
-- Create indexes
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_conversations_document_id ON conversations(document_id);
CREATE INDEX idx_qa_pairs_conversation_id ON qa_pairs(conversation_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);

-- Analyze query plans
EXPLAIN ANALYZE SELECT * FROM documents WHERE user_id = 'user123';

-- Vacuum and analyze
VACUUM ANALYZE;
```

### 3. Caching Strategy

```python
# From docs/PERFORMANCE.md

@async_cached(ttl_seconds=3600, key_prefix="doc_summary")
async def get_document_summary(doc_id: str) -> str:
    # Cached for 1 hour
    return await qa_service.summarize(doc_id)

@async_cached(ttl_seconds=600, key_prefix="semantic_search")
async def retrieve_context(question: str, doc_id: str) -> list[str]:
    # Cached for 10 minutes
    return await vector_store.similarity_search(question, doc_id)
```

---

## Disaster Recovery

### 1. Backup & Restore

```bash
# Automated daily backup (cron)
0 2 * * * /scripts/backup-db.sh

# Manual restore
gunzip < backup_20260702_020000.sql.gz | psql -U langchain_user langchain_qa

# Test restore procedure monthly
```

### 2. Rollback Plan

```bash
# Keep previous versions tagged in Docker registry
docker tag langchain-qa-backend:latest langchain-qa-backend:v1.0.0-backup

# Quick rollback
docker-compose -f docker-compose.prod.yml down
git checkout v1.0.0
docker-compose -f docker-compose.prod.yml up -d

# Kubernetes rollback
kubectl rollout undo deployment/backend -n langchain-qa
```

### 3. High Availability Setup

```yaml
# kubernetes/ha-setup.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - backend
              topologyKey: kubernetes.io/hostname
```

---

## Troubleshooting

### Common Issues

**Issue**: Database connection refused
```bash
# Check database is running
pg_isready -h localhost -U langchain_user

# Check credentials
psql -h localhost -U langchain_user -d langchain_qa
```

**Issue**: Vector store not responding
```bash
# Verify Pinecone/Chroma connection
curl https://api.pinecone.io/describe_index -H "Api-Key: $PINECONE_API_KEY"
```

**Issue**: High memory usage
```bash
# Check cache hit rate
# Reduce CACHE_TTL if hit rate <30%
# Implement connection pooling limits
```

---

## Rollout Procedure

### Day 1: Staging Validation
1. Deploy to staging environment
2. Run full integration test suite
3. Load test with 1000 req/sec
4. Security audit
5. Performance baseline

### Day 2: Canary Release
1. Deploy to 10% of traffic
2. Monitor metrics for 24 hours
3. If stable, increase to 50%
4. Monitor for 24 hours
5. Full rollout if no issues

### Day 3: Production Release
1. Deploy to 100% of traffic
2. Monitor closely (daily check-ins)
3. Keep rollback ready for 7 days
4. After 7 days, archive old version

---

## Support & Escalation

| Issue | Contact | Response Time |
|-------|---------|----------------|
| Critical (service down) | On-call engineer | 15 min |
| High (degraded) | Team lead | 30 min |
| Medium (errors) | Developer | 2 hours |
| Low (enhancement) | Backlog | 1 week |

---

## Maintenance Windows

```
Weekly: Tuesday 2-3 AM UTC
- Database maintenance
- Security patches
- Dependency updates

Monthly: First Tuesday 2-4 AM UTC
- Major version updates
- Performance tuning
- Compliance checks
```

---

For support or questions, contact the DevOps team.
