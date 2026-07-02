# Deployment Runbook

**Quick Reference for Deploying LangChain Document QA to Production**

---

## Pre-Deployment (1 hour before)

```bash
# 1. Verify all tests pass
pytest tests/ -v --tb=short

# 2. Build Docker images
docker build -t langchain-qa-backend:latest -f Dockerfile .
docker build -t langchain-qa-frontend:latest -f frontend/Dockerfile ./frontend

# 3. Verify environment configuration
python -c "from backend.utils.config import settings; print('✅ Config valid')"

# 4. Check git status
git status
git log --oneline -5

# 5. Notify team
echo "Deployment starting in 1 hour"
```

---

## Staging Deployment (30 min test)

### Using Docker Compose

```bash
# 1. Pull latest code
git pull origin main

# 2. Start staging environment
docker-compose -f docker-compose.staging.yml up -d

# 3. Run migrations
docker-compose -f docker-compose.staging.yml exec backend alembic upgrade head

# 4. Run health checks
curl -f http://localhost:8000/health
curl -f http://localhost:8000/health/db
curl -f http://localhost:8000/health/vector-store

# 5. Run smoke tests
pytest tests/smoke -v

# 6. Test one complete workflow
# - Upload a test document
# - Ask a question
# - Get summary
```

### Using Kubernetes

```bash
# 1. Update image in staging
kubectl set image deployment/backend \
  backend=langchain-qa-backend:latest \
  -n langchain-qa-staging

# 2. Wait for rollout
kubectl rollout status deployment/backend -n langchain-qa-staging --timeout=5m

# 3. Verify deployment
kubectl get pods -n langchain-qa-staging
kubectl logs -f deployment/backend -n langchain-qa-staging
```

---

## Production Deployment

### Option A: Rolling Update (Recommended)

```bash
# 1. Create deployment manifest with new image
kubectl set image deployment/backend \
  backend=langchain-qa-backend:v1.0.0 \
  -n langchain-qa \
  --record

# 2. Monitor rollout (watch pods restart)
kubectl rollout status deployment/backend -n langchain-qa

# 3. Verify all pods running
kubectl get pods -n langchain-qa | grep backend

# 4. Run health checks
for i in {1..10}; do
  curl -f https://yourdomain.com/health && echo "✅ Attempt $i passed" || echo "❌ Attempt $i failed"
  sleep 5
done

# 5. Verify metrics
curl https://yourdomain.com/metrics | head -20

# 6. Check logs for errors
kubectl logs -l app=backend -n langchain-qa --tail=50
```

### Option B: Blue-Green Deployment (Zero Downtime)

```bash
# 1. Create new deployment (green)
kubectl create deployment backend-green \
  --image=langchain-qa-backend:v1.0.0 \
  -n langchain-qa

# 2. Wait for green to be ready
kubectl wait --for=condition=available \
  --timeout=300s \
  deployment/backend-green \
  -n langchain-qa

# 3. Run health checks on green
kubectl port-forward svc/backend-green 8000:8000 -n langchain-qa &
sleep 2
curl -f http://localhost:8000/health

# 4. Switch traffic to green
kubectl patch service backend \
  -p '{"spec":{"selector":{"version":"green"}}}' \
  -n langchain-qa

# 5. Monitor for 5 minutes
# Check error rates, latency, etc.

# 6. Delete old blue deployment
kubectl delete deployment backend-blue -n langchain-qa
kubectl rename backend-green backend -n langchain-qa
```

### Option C: Canary Deployment (Progressive)

```bash
# 1. Deploy canary version to 10% of traffic
kubectl patch virtualservice backend -n langchain-qa --type merge -p '
{
  "spec": {
    "hosts": ["yourdomain.com"],
    "http": [{
      "match": [{"uri": {"prefix": "/"}}],
      "route": [
        {"destination": {"host": "backend-stable"}, "weight": 90},
        {"destination": {"host": "backend-canary"}, "weight": 10}
      ]
    }]
  }
}'

# 2. Monitor canary metrics for 1 hour
watch -n 5 'kubectl top pods -n langchain-qa'

# 3. If stable, increase to 50% traffic
kubectl patch virtualservice backend -n langchain-qa --type merge -p '{"spec":{"http":[{"route":[{"weight": 50},{"weight": 50}]}]}}'

# 4. Monitor for 1 more hour

# 5. Promote canary to stable
kubectl patch virtualservice backend -n langchain-qa --type merge -p '{"spec":{"http":[{"route":[{"weight": 0},{"weight": 100}]}]}}'

# 6. Remove old version
kubectl delete deployment backend-stable -n langchain-qa
```

---

## Post-Deployment Verification (30 min)

```bash
# 1. Health checks
curl -v https://yourdomain.com/health
curl -v https://yourdomain.com/health/db
curl -v https://yourdomain.com/health/vector-store

# 2. Check metrics
curl https://yourdomain.com/metrics | grep http_requests_total | head -5

# 3. Verify logs (no errors)
kubectl logs deployment/backend -n langchain-qa --tail=100 | grep ERROR || echo "✅ No errors found"

# 4. Test critical APIs
# Document upload
curl -X POST https://yourdomain.com/api/v1/documents/upload \
  -H "Authorization: Bearer $API_KEY" \
  -F "file=@test.pdf"

# Get documents
curl -H "Authorization: Bearer $API_KEY" \
  https://yourdomain.com/api/v1/documents

# 5. Check database connections
kubectl exec deployment/backend -n langchain-qa -- \
  python -c "from backend.models.database import engine; engine.execute('SELECT 1')" && echo "✅ DB connected"

# 6. Monitor resource usage
kubectl top nodes
kubectl top pods -n langchain-qa

# 7. Check cache performance
curl https://yourdomain.com/metrics | grep cache_hits

# 8. Review error logs
kubectl logs deployment/backend -n langchain-qa --tail=200 | grep -i "error\|exception" | head -20 || echo "✅ No errors"
```

---

## Rollback Procedures

### Immediate Rollback (If Critical Issue)

```bash
# 1. Undo the deployment
kubectl rollout undo deployment/backend -n langchain-qa

# 2. Wait for rollback to complete
kubectl rollout status deployment/backend -n langchain-qa --timeout=5m

# 3. Verify old version running
kubectl describe deployment backend -n langchain-qa | grep Image

# 4. Verify health checks pass
for i in {1..10}; do
  curl -f https://yourdomain.com/health && break || sleep 5
done

# 5. Notify team
echo "❌ Rollback completed. Investigating issue..."

# 6. Pull logs for debugging
kubectl logs deployment/backend -n langchain-qa --tail=500 > rollback-logs.txt

# 7. Create incident ticket
# Document what went wrong for post-mortem
```

### Keep Previous Versions

```bash
# Keep version history
kubectl rollout history deployment/backend -n langchain-qa

# Show revision details
kubectl rollout history deployment/backend -n langchain-qa --revision=5

# Rollback to specific revision
kubectl rollout undo deployment/backend -n langchain-qa --to-revision=3
```

---

## Monitoring During Deployment

### Real-time Monitoring

```bash
# Watch pod status
watch -n 2 'kubectl get pods -n langchain-qa | grep backend'

# Watch events
kubectl get events -n langchain-qa --sort-by='.lastTimestamp' -w

# Watch resource usage
watch -n 5 'kubectl top pods -n langchain-qa'

# Tail logs from all replicas
kubectl logs -l app=backend -n langchain-qa -f
```

### Metrics to Watch

```bash
# Request rate
curl -s https://yourdomain.com/metrics | grep 'http_requests_total'

# Error rate
curl -s https://yourdomain.com/metrics | grep 'http_requests_total{status="500"}'

# Latency (P95)
curl -s https://yourdomain.com/metrics | grep 'http_request_duration_seconds_bucket'

# Database connections
curl -s https://yourdomain.com/metrics | grep 'db_connection_pool'
```

---

## Troubleshooting

### Pod won't start

```bash
# Check pod description
kubectl describe pod backend-xxx -n langchain-qa

# Check logs
kubectl logs backend-xxx -n langchain-qa

# Check events
kubectl get events -n langchain-qa | grep backend
```

### High memory usage

```bash
# Check memory limits
kubectl describe deployment backend -n langchain-qa | grep Memory

# Increase if needed
kubectl set resources deployment backend \
  --limits=memory=4Gi \
  -n langchain-qa
```

### Database connection errors

```bash
# Verify database is accessible
kubectl run postgres-test --image=postgres:15 -it --rm -- \
  psql -h $DB_HOST -U $DB_USER -c "SELECT 1"

# Check DATABASE_URL environment variable
kubectl describe pod backend-xxx -n langchain-qa | grep DATABASE_URL
```

### Slow requests

```bash
# Check vector store performance
kubectl exec deployment/backend -n langchain-qa -- \
  python -c "import time; from backend.utils.singletons import get_vector_store; s=time.time(); get_vector_store(); print(f'Load time: {time.time()-s:.2f}s')"

# Check cache hit rate
curl https://yourdomain.com/metrics | grep cache_hit_rate

# Restart if needed
kubectl rollout restart deployment/backend -n langchain-qa
```

---

## Communication Template

### Before Deployment
```
🚀 Deployment scheduled for [TIME]
Version: v1.0.0
Expected downtime: None (rolling update)
Contact: [ON-CALL ENGINEER]
```

### During Deployment
```
📝 Deployment in progress
Current status: Rolling out 1/3 replicas
ETA: 10 minutes
```

### After Successful Deployment
```
✅ Deployment successful!
Version: v1.0.0
Status: All health checks passing
No issues detected

Metrics:
- Error rate: 0.02%
- P95 latency: 120ms
- Cache hit rate: 45%
```

### After Failed Deployment (Rollback)
```
❌ Deployment rolled back
Previous version restored: v0.9.9
Investigation: See #incident-123
Post-mortem: Tomorrow 2 PM
```

---

## Checklist Template

```markdown
## Deployment Checklist - [DATE]

- [ ] All tests passing locally
- [ ] Docker images built and pushed
- [ ] Staging deployment successful
- [ ] Staging load tests passed
- [ ] Staging health checks passed
- [ ] Security audit passed
- [ ] Team approval obtained
- [ ] Runbook reviewed
- [ ] On-call engineer notified
- [ ] Monitoring alerts configured
- [ ] Communication plan ready
- [ ] Rollback procedure tested

### Production Deployment
- [ ] Pre-flight checks all green
- [ ] Canary deployment started (10%)
- [ ] Canary metrics stable for 1 hour
- [ ] Gradual rollout to 100%
- [ ] Full health checks passing
- [ ] No errors in logs
- [ ] Database performance normal
- [ ] Cache operating normally
- [ ] 24-hour monitoring period

### Post-Deployment
- [ ] Logs reviewed for errors
- [ ] Metrics within normal range
- [ ] User feedback gathered
- [ ] Documentation updated
- [ ] Deployment marked complete
```

---

## Emergency Contacts

| Role | Name | Phone | Slack |
|------|------|-------|-------|
| On-Call | TBD | TBD | @oncall |
| DevOps Lead | TBD | TBD | @devops-lead |
| Product Lead | TBD | TBD | @product-lead |

---

**Last Updated**: July 2, 2026  
**Next Review**: 7 days post-deployment

For detailed information, see PRODUCTION_DEPLOYMENT.md
