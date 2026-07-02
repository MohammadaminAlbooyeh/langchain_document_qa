# Environment Variables Complete Guide

This guide documents all environment variables used by the LangChain Document QA application.

---

## Overview

Environment variables are organized by category:
- **Application Settings**
- **Database Configuration**
- **API & Security**
- **LLM Providers**
- **Vector Stores**
- **Caching**
- **Monitoring & Logging**
- **Optional/Advanced**

---

## Application Settings

### `APP_ENV`
**Type**: String  
**Options**: `development`, `staging`, `production`  
**Default**: `development`  
**Example**: `APP_ENV=production`

Controls behavior based on environment. Sets logging levels, enables/disables debugging features, etc.

### `APP_NAME`
**Type**: String  
**Default**: `LangChain Document QA`  
**Example**: `APP_NAME="My Custom QA System"`

Application name displayed in UI and logs.

### `DEBUG`
**Type**: Boolean  
**Options**: `true`, `false`  
**Default**: `true` (development), `false` (production)  
**Example**: `DEBUG=false`

**⚠️ IMPORTANT**: Always set to `false` in production. Exposes stack traces and sensitive information.

### `LOG_LEVEL`
**Type**: String  
**Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`  
**Default**: `INFO`  
**Example**: `LOG_LEVEL=INFO`

Controls verbosity of logs. Use `DEBUG` for troubleshooting, `INFO` for normal operation.

### `API_PORT`
**Type**: Integer  
**Default**: `8000`  
**Example**: `API_PORT=8000`

Port the FastAPI application listens on.

### `API_HOST`
**Type**: String  
**Default**: `0.0.0.0` (accessible from any IP)  
**Example**: `API_HOST=0.0.0.0`

IP address the API binds to. Use `127.0.0.1` for localhost-only access.

### `API_KEY_PREFIX`
**Type**: String  
**Default**: `sk_`  
**Example**: `API_KEY_PREFIX=sk_prod_`

Prefix for generated API keys. Useful for distinguishing production vs. staging keys.

---

## Database Configuration

### `DATABASE_URL`
**Type**: String (Connection String)  
**Required**: Yes  
**Format**: 
- SQLite: `sqlite:///./data/langchain_qa.db`
- PostgreSQL: `postgresql://user:password@localhost:5432/langchain_qa`
- PostgreSQL Async: `postgresql+asyncpg://user:password@localhost:5432/langchain_qa`

**Example**: 
```
DATABASE_URL=postgresql+asyncpg://langchain_user:secure_password@db.example.com:5432/langchain_qa
```

Connection string for the database. Use PostgreSQL for production.

### `DATABASE_POOL_SIZE`
**Type**: Integer  
**Default**: `5`  
**Example**: `DATABASE_POOL_SIZE=20`

Maximum number of database connections in the pool. Increase for high-traffic applications.

### `DATABASE_POOL_RECYCLE`
**Type**: Integer (seconds)  
**Default**: `3600` (1 hour)  
**Example**: `DATABASE_POOL_RECYCLE=3600`

Recycle database connections after this time to prevent stale connections.

### `DATABASE_ECHO`
**Type**: Boolean  
**Default**: `false`  
**Example**: `DATABASE_ECHO=false`

**⚠️ Only for development**: Set to `true` to log all SQL queries. **Never use in production** (performance impact).

---

## API & Security

### `SECRET_KEY`
**Type**: String  
**Required**: Yes  
**Minimum Length**: 32 characters  
**Example**: 
```
SECRET_KEY=your_super_secret_key_with_at_least_32_characters_long
```

**Generate secure key**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Used for signing JWT tokens and other cryptographic operations.

### `CORS_ORIGINS`
**Type**: JSON array or comma-separated string  
**Default**: `["http://localhost:3000"]`  
**Example**: 
```
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]
```

List of allowed origins for CORS requests. Add all frontend domains here.

### `ALLOWED_HOSTS`
**Type**: Comma-separated string  
**Default**: `localhost,127.0.0.1`  
**Example**: 
```
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com
```

Allowed hosts for the API. Prevents Host header attacks.

### `MAX_UPLOAD_SIZE`
**Type**: Integer (MB)  
**Default**: `100`  
**Example**: `MAX_UPLOAD_SIZE=500`

Maximum file upload size in megabytes.

---

## LLM Providers

### `DEFAULT_LLM`
**Type**: String  
**Options**: `openai`, `anthropic`, `cohere`  
**Default**: `openai`  
**Example**: `DEFAULT_LLM=openai`

Default LLM provider to use.

### `OPENAI_API_KEY`
**Type**: String  
**Required**: If using OpenAI  
**Format**: `sk-...`  
**Example**: `OPENAI_API_KEY=sk-proj-...`

API key for OpenAI. Get from https://platform.openai.com/api-keys

### `OPENAI_ORG_ID`
**Type**: String  
**Optional**: Only if you have organization access  
**Example**: `OPENAI_ORG_ID=org-...`

Organization ID for OpenAI (optional).

### `ANTHROPIC_API_KEY`
**Type**: String  
**Required**: If using Anthropic  
**Format**: `sk-ant-...`  
**Example**: `ANTHROPIC_API_KEY=sk-ant-...`

API key for Anthropic Claude. Get from https://console.anthropic.com/

### `COHERE_API_KEY`
**Type**: String  
**Required**: If using Cohere  
**Example**: `COHERE_API_KEY=...`

API key for Cohere. Get from https://dashboard.cohere.ai/

### `CHAT_MODEL`
**Type**: String  
**Default**: `gpt-4o-mini`  
**Examples**: 
- OpenAI: `gpt-4o-mini`, `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`
- Anthropic: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`
- Cohere: `command-r-plus`, `command-r`

**Example**: `CHAT_MODEL=gpt-4o-mini`

Model to use for chat/question answering.

### `TEMPERATURE`
**Type**: Float (0.0 - 2.0)  
**Default**: `0.0`  
**Example**: `TEMPERATURE=0.7`

Controls randomness. 0 = deterministic, 1 = balanced, 2 = creative.

### `MAX_TOKENS`
**Type**: Integer  
**Default**: `4096`  
**Example**: `MAX_TOKENS=8192`

Maximum number of tokens in LLM response.

### `EMBEDDING_MODEL`
**Type**: String  
**Default**: `text-embedding-3-small`  
**Examples**:
- OpenAI: `text-embedding-3-small`, `text-embedding-3-large`, `text-embedding-ada-002`

**Example**: `EMBEDDING_MODEL=text-embedding-3-small`

Model to use for generating embeddings.

### `EMBEDDING_DIMENSION`
**Type**: Integer  
**Default**: `1536` (for text-embedding-3-small)  
**Example**: `EMBEDDING_DIMENSION=1536`

Dimension of embedding vectors. Must match selected embedding model.

---

## Vector Stores

### `VECTOR_STORE_TYPE`
**Type**: String  
**Options**: `chroma`, `faiss`, `pinecone`  
**Default**: `chroma`  
**Example**: `VECTOR_STORE_TYPE=pinecone`

Which vector store backend to use.

### `CHROMA_DB_PATH`
**Type**: String  
**Default**: `./chroma_db`  
**Example**: `CHROMA_DB_PATH=/data/chroma_db`

Local path for Chroma database (used if `VECTOR_STORE_TYPE=chroma`).

### `PINECONE_API_KEY`
**Type**: String  
**Required**: If using Pinecone  
**Example**: `PINECONE_API_KEY=...`

API key for Pinecone. Get from https://www.pinecone.io/

### `PINECONE_ENVIRONMENT`
**Type**: String  
**Required**: If using Pinecone  
**Example**: `PINECONE_ENVIRONMENT=us-east-1-aws`

Pinecone environment/region.

### `PINECONE_INDEX_NAME`
**Type**: String  
**Required**: If using Pinecone  
**Default**: `langchain-qa`  
**Example**: `PINECONE_INDEX_NAME=langchain-qa-prod`

Name of the Pinecone index.

### `VECTOR_STORE_RECREATE_ON_START`
**Type**: Boolean  
**Default**: `false`  
**Example**: `VECTOR_STORE_RECREATE_ON_START=false`

Whether to recreate vector store on application startup (development only).

---

## Text Processing

### `CHUNK_SIZE`
**Type**: Integer (tokens)  
**Default**: `1000`  
**Example**: `CHUNK_SIZE=1500`

Number of tokens per document chunk.

### `CHUNK_OVERLAP`
**Type**: Integer (tokens)  
**Default**: `200`  
**Example**: `CHUNK_OVERLAP=300`

Overlap between chunks (for context continuity).

### `CHUNK_STRATEGY`
**Type**: String  
**Options**: `token`, `sentence`, `character`  
**Default**: `token`  
**Example**: `CHUNK_STRATEGY=token`

Strategy for splitting documents into chunks.

---

## Caching

### `CACHE_TYPE`
**Type**: String  
**Options**: `memory`, `redis`  
**Default**: `memory`  
**Example**: `CACHE_TYPE=redis`

Cache backend to use.

### `REDIS_URL`
**Type**: String  
**Required**: If `CACHE_TYPE=redis`  
**Format**: `redis://[:password]@host:port/db`  
**Example**: `REDIS_URL=redis://:mypassword@localhost:6379/0`

Connection string for Redis server.

### `CACHE_TTL`
**Type**: Integer (seconds)  
**Default**: `600` (10 minutes)  
**Example**: `CACHE_TTL=3600`

Time-to-live for cached responses.

### `CACHE_ENABLE_COMPRESSION`
**Type**: Boolean  
**Default**: `false`  
**Example**: `CACHE_ENABLE_COMPRESSION=true`

Whether to compress cached values (saves memory, uses more CPU).

---

## Rate Limiting

### `RATE_LIMIT_ENABLED`
**Type**: Boolean  
**Default**: `true`  
**Example**: `RATE_LIMIT_ENABLED=true`

Whether to enable rate limiting.

### `RATE_LIMIT_REQUESTS`
**Type**: Integer  
**Default**: `100`  
**Example**: `RATE_LIMIT_REQUESTS=1000`

Maximum requests allowed per period.

### `RATE_LIMIT_PERIOD`
**Type**: Integer (seconds)  
**Default**: `60`  
**Example**: `RATE_LIMIT_PERIOD=60`

Time period for rate limit (usually 60 = per minute).

---

## Monitoring & Logging

### `LOG_TO_FILE`
**Type**: String (filepath)  
**Optional**: Leave empty to disable file logging  
**Example**: `LOG_TO_FILE=/var/log/langchain-qa/app.log`

File path for application logs. Creates log files in this directory.

### `LOG_FILE_SIZE`
**Type**: Integer (bytes)  
**Default**: `10485760` (10 MB)  
**Example**: `LOG_FILE_SIZE=52428800` (50 MB)

Maximum size of each log file before rotation.

### `LOG_FILES_TO_KEEP`
**Type**: Integer  
**Default**: `10`  
**Example**: `LOG_FILES_TO_KEEP=30`

Number of old log files to keep.

### `PROMETHEUS_ENABLED`
**Type**: Boolean  
**Default**: `true`  
**Example**: `PROMETHEUS_ENABLED=true`

Whether to expose Prometheus metrics at `/metrics`.

### `SENTRY_DSN`
**Type**: String (URL)  
**Optional**: For error tracking  
**Example**: `SENTRY_DSN=https://your-key@sentry.io/your-project-id`

Sentry DSN for error tracking. Get from https://sentry.io/

### `SENTRY_TRACES_SAMPLE_RATE`
**Type**: Float (0.0 - 1.0)  
**Default**: `0.1`  
**Example**: `SENTRY_TRACES_SAMPLE_RATE=0.1`

Sample rate for performance tracing (0.1 = 10% of requests).

---

## Email Configuration (Optional)

### `SMTP_HOST`
**Type**: String  
**Example**: `SMTP_HOST=smtp.gmail.com`

SMTP server hostname.

### `SMTP_PORT`
**Type**: Integer  
**Example**: `SMTP_PORT=587`

SMTP server port (usually 587 for TLS, 465 for SSL).

### `SMTP_USERNAME`
**Type**: String  
**Example**: `SMTP_USERNAME=your-email@gmail.com`

SMTP username/email.

### `SMTP_PASSWORD`
**Type**: String  
**Example**: `SMTP_PASSWORD=your-app-password`

SMTP password (use app-specific passwords for Gmail).

### `SMTP_FROM_EMAIL`
**Type**: String  
**Example**: `SMTP_FROM_EMAIL=noreply@yourdomain.com`

Email address to send from.

---

## Security Headers

### `SECURE_BROWSER_XSS_FILTER`
**Type**: Boolean  
**Default**: `true`  
**Example**: `SECURE_BROWSER_XSS_FILTER=true`

Enable X-XSS-Protection header.

### `SECURE_CONTENT_SECURITY_POLICY`
**Type**: Boolean  
**Default**: `true`  
**Example**: `SECURE_CONTENT_SECURITY_POLICY=true`

Enable Content-Security-Policy header.

### `SECURE_HSTS_SECONDS`
**Type**: Integer  
**Default**: `31536000` (1 year)  
**Example**: `SECURE_HSTS_SECONDS=31536000`

HSTS max-age in seconds.

### `SECURE_HSTS_INCLUDE_SUBDOMAINS`
**Type**: Boolean  
**Default**: `true`  
**Example**: `SECURE_HSTS_INCLUDE_SUBDOMAINS=true`

Include subdomains in HSTS.

---

## Development Variables

### `MOCK_LLM`
**Type**: Boolean  
**Default**: `false`  
**Example**: `MOCK_LLM=true`

Use mock LLM responses instead of real API calls (testing only).

### `MOCK_EMBEDDINGS`
**Type**: Boolean  
**Default**: `false`  
**Example**: `MOCK_EMBEDDINGS=true`

Use mock embeddings instead of real API calls (testing only).

### `SKIP_DB_INIT`
**Type**: Boolean  
**Default**: `false`  
**Example**: `SKIP_DB_INIT=true`

Skip database initialization on startup.

---

## Example Configurations

### Development (.env.local)
```bash
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///./data/langchain_qa.db
OPENAI_API_KEY=sk-proj-...
VECTOR_STORE_TYPE=chroma
CACHE_TYPE=memory
CORS_ORIGINS=["http://localhost:3000"]
```

### Staging (.env.staging)
```bash
APP_ENV=staging
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql+asyncpg://user:pass@db-staging:5432/langchain_qa
OPENAI_API_KEY=sk-proj-...
VECTOR_STORE_TYPE=pinecone
PINECONE_INDEX_NAME=langchain-qa-staging
CACHE_TYPE=redis
REDIS_URL=redis://cache-staging:6379/0
CORS_ORIGINS=["https://staging.yourdomain.com"]
SENTRY_DSN=https://key@sentry.io/staging-project-id
```

### Production (.env.production)
```bash
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql+asyncpg://user:securepass@db-prod.example.com:5432/langchain_qa
DATABASE_POOL_SIZE=30
OPENAI_API_KEY=sk-proj-...
VECTOR_STORE_TYPE=pinecone
PINECONE_INDEX_NAME=langchain-qa-prod
CACHE_TYPE=redis
REDIS_URL=redis://:password@cache-prod.example.com:6379/0
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]
SENTRY_DSN=https://key@sentry.io/production-project-id
LOG_TO_FILE=/var/log/langchain-qa/app.log
PROMETHEUS_ENABLED=true
MAX_UPLOAD_SIZE=500
RATE_LIMIT_REQUESTS=1000
SECURE_HSTS_SECONDS=31536000
```

---

## Loading Environment Variables

### Using .env file

1. Create `.env` file in project root:
```bash
cp .env.example .env
# Edit .env with your values
```

2. Load automatically (python-dotenv handles this):
```python
from backend.utils.config import settings
# Settings automatically loaded from .env
```

### Using environment variables directly

```bash
export OPENAI_API_KEY=sk-proj-...
export DATABASE_URL=postgresql://...
python -m uvicorn backend.main:app
```

### Using Docker

```bash
docker run --env-file .env langchain-qa-backend
```

### Using Kubernetes

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: langchain-qa-config
data:
  APP_ENV: production
  VECTOR_STORE_TYPE: pinecone
  CACHE_TYPE: redis
---
apiVersion: v1
kind: Secret
metadata:
  name: langchain-qa-secrets
type: Opaque
stringData:
  DATABASE_URL: postgresql://...
  OPENAI_API_KEY: sk-proj-...
  SECRET_KEY: ...
```

---

## Validation

The application validates all environment variables on startup. Invalid configurations will cause the application to fail with a clear error message.

To test your configuration:

```bash
python -c "from backend.utils.config import settings; print('✅ Configuration valid')"
```

---

For more information, see:
- SETUP.md - Local development setup
- PRODUCTION_DEPLOYMENT.md - Production configuration
- SECURITY.md - Security considerations
