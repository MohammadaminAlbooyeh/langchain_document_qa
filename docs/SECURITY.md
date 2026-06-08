# Security Guide

## Overview

This document outlines the security measures implemented in the LangChain Document QA application and best practices for deployment.

## Security Features

### 1. Authentication & Authorization

#### API Key Management
- **Database-Backed Keys**: All API keys are persisted in the database (not in-memory)
- **Key Expiration**: Keys expire after 90 days by default
- **Key Revocation**: Users can revoke keys at any time
- **Key Rotation**: Generate new keys regularly for security
- **Last Used Tracking**: Monitors when each key was last used

```python
# Login to get API key
POST /api/v1/auth/login
{
    "email": "user@example.com",
    "password": "secure_password"
}

# Response includes expiration
{
    "token": "lq-...",
    "user_id": "abc123",
    "expires_at": "2025-09-06T10:30:00Z"
}
```

#### Request Authentication
- All API endpoints (except `/health` and auth) require valid API key
- Keys are verified against database on each request
- Expired or inactive keys are rejected
- Missing keys return 401 Unauthorized

### 2. Input Validation & Sanitization

#### Text Sanitization
- **Null Byte Removal**: Prevents null injection attacks
- **Whitespace Normalization**: Removes excessive whitespace
- **Length Limits**: Enforces max input length (10,000 chars default)
- **Character Validation**: Removes special characters where appropriate

#### Filename Sanitization
- **Path Traversal Prevention**: Removes `../` and absolute paths
- **Special Character Removal**: Strips `<`, `>`, `;`, etc.
- **Hidden File Prevention**: Removes leading dots
- **Alphanumeric Enforcement**: Keeps only safe characters

#### LLM Prompt Sanitization
- **Injection Prevention**: Removes prompt injection keywords
  - "ignore", "bypass", "override", "system", "instruction"
- **Context Preservation**: Maintains meaning while removing threats
- **Injection Detection**: System prompts instructed to reject injections

#### Email Validation
- **Format Validation**: RFC 5322 basic compliance
- **Length Limits**: Max 254 characters
- **Case Normalization**: Stored as lowercase

### 3. Audit Logging

All user actions are logged for compliance and security monitoring:

```python
AuditLog(
    user_id: str,          # User performing action
    action: str,           # Action type (upload, delete, etc)
    resource_type: str,    # What was affected (document, etc)
    resource_id: str,      # ID of affected resource
    details: str,          # Additional context
    ip_address: str,       # Source IP
    user_agent: str,       # Browser/client info
    timestamp: datetime,   # When it happened
)
```

#### Actions Logged
- Document upload
- Document deletion
- Q&A queries
- Summarization requests
- Entity extraction
- API key generation
- API key revocation
- Failed authentication attempts

#### Accessing Audit Logs
```python
GET /api/v1/audit/logs
Headers: X-API-Key: lq-...

# Response
{
    "logs": [
        {
            "id": "123",
            "action": "document_upload",
            "resource_type": "document",
            "resource_id": "doc-456",
            "timestamp": "2025-06-08T10:30:00Z",
            "ip_address": "192.168.1.1"
        }
    ]
}
```

### 4. Rate Limiting

Prevents abuse and DoS attacks:

- **Limit**: 100 requests per 60 seconds per client
- **Granularity**: Per IP address
- **Response**: 429 Too Many Requests

```python
# Example rate limiting
if requests_in_window > 100:
    return 429, "Rate limit exceeded"
```

### 5. Database Security

#### SQLAlchemy ORM
- **SQL Injection Prevention**: Uses parameterized queries
- **No String Concatenation**: All inputs bound as parameters
- **Type Safety**: Column types enforced

#### Async Operations
- **Connection Pooling**: Reuses connections efficiently
- **Transaction Isolation**: Prevents dirty reads

### 6. Error Handling

#### Information Disclosure Prevention
- **Generic Messages**: Users see "Internal server error"
- **Detailed Logs**: Full errors logged server-side only
- **No Stack Traces**: Stack traces never sent to client
- **Error Codes**: Machine-readable error types without details

```python
# User sees this
{
    "detail": "Internal server error",
    "error_code": "INTERNAL_ERROR"
}

# Server logs this
ERROR: Full exception stack trace with context
```

### 7. CORS Configuration

- **Origin Whitelist**: Only trusted domains allowed
- **Credentials**: Cookies/auth only sent to trusted origins
- **Methods**: Only necessary HTTP methods allowed
- **Headers**: Only necessary headers allowed

```python
# Development
CORS origins: ["http://localhost:3000", "http://localhost:5173"]

# Production
CORS origins: ["https://yourdomain.com", "https://app.yourdomain.com"]
```

### 8. File Upload Security

#### Validation
- **Type Whitelist**: Only PDF, DOCX, TXT allowed
- **Size Limits**: Default 100MB, configurable
- **Content Verification**: Magic number validation recommended
- **Isolation**: Files stored outside web root

#### Handling
- **Sandboxed Processing**: Documents processed in isolation
- **No Direct Execution**: Files never executed
- **Cleanup**: Temporary files deleted after processing
- **Path Sanitization**: Filenames sanitized before storage

### 9. LLM Security

#### Prompt Injection Prevention
- **System Prompt**: Instructions to reject injections
- **Input Sanitization**: Removes injection patterns
- **Output Validation**: Responses validated before returning
- **Context Limiting**: Only relevant context included

#### API Key Protection
- **Never in Prompts**: LLM never sees API keys
- **Environment Variables**: Keys stored in .env (never committed)
- **Rotation**: Rotate keys regularly
- **Monitoring**: Track API usage patterns

## Deployment Security Checklist

### Pre-Deployment
- [ ] Change default passwords/secrets
- [ ] Review CORS origins for production URLs
- [ ] Enable HTTPS/TLS
- [ ] Configure CSRF protection
- [ ] Set up WAF (Web Application Firewall)
- [ ] Enable security headers

### Runtime
- [ ] Monitor audit logs regularly
- [ ] Set up alerting for failed auth attempts
- [ ] Track API usage for anomalies
- [ ] Rotate API keys periodically
- [ ] Keep dependencies updated

### Infrastructure
- [ ] Use environment variables for secrets
- [ ] Enable database encryption at rest
- [ ] Use private networks for services
- [ ] Enable VPC security groups
- [ ] Set up backup/recovery procedures

## Security Headers

Recommended headers to add:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Referrer-Policy: no-referrer
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

## Environment Variables

Never commit secrets. Use `.env` file:

```bash
# .env (do not commit)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=claude-...
DATABASE_URL=postgresql://user:password@localhost/db
JWT_SECRET=your-secret-key-here
```

## Vulnerability Reporting

If you discover a security vulnerability, please email security@yourdomain.com instead of using the public issue tracker.

## Security Best Practices

### For Users
1. **Use Strong Passwords**: Min 12 characters, mixed case, numbers, symbols
2. **Rotate Keys**: Generate new keys every 3-6 months
3. **Don't Share Keys**: Treat API keys like passwords
4. **Monitor Usage**: Check audit logs regularly
5. **Report Suspicious Activity**: Report immediately if key compromised

### For Developers
1. **Never Log Secrets**: Filter API keys from logs
2. **Review Permissions**: Principle of least privilege
3. **Input Validation**: Always validate user input
4. **Dependency Updates**: Keep libraries updated
5. **Security Testing**: Include security in test suite

### For Operations
1. **Network Isolation**: Use VPCs and security groups
2. **Access Control**: Limit who can deploy
3. **Monitoring**: Set up security monitoring
4. **Backup Strategy**: Regular backups, test recovery
5. **Incident Response**: Have playbook for security incidents

## Compliance

### Data Protection
- **GDPR**: Implement data deletion, privacy controls
- **HIPAA**: If handling health data, implement additional controls
- **SOC 2**: Audit logging and access controls

### Audit Trail
- Maintain 90-day audit log retention
- Hash sensitive data before logging
- Implement access controls on logs

## Known Limitations

1. **In-Memory Cache**: Cache is not persisted, cleared on restart
2. **Single Database**: No read replicas configured by default
3. **No 2FA**: Currently username/password only (add 2FA for production)
4. **No IP Whitelisting**: Rate limit based on IP only

## Future Security Enhancements

- [ ] Implement 2FA/MFA
- [ ] Add IP whitelisting
- [ ] Enable OAuth/OIDC integration
- [ ] Implement encryption at field level
- [ ] Add secrets rotation automation
- [ ] Implement request signing
- [ ] Add machine learning anomaly detection

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [SQLAlchemy ORM Security](https://docs.sqlalchemy.org/en/20/faq/security.html)
- [LangChain Security Best Practices](https://python.langchain.com/docs/guides/safety/)

---

For questions or concerns, contact: security@yourdomain.com
