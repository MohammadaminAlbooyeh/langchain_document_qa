# CI/CD Pipeline Setup Guide

**Status**: Ready for implementation  
**Target**: GitHub Actions, GitLab CI, or Jenkins  
**Version**: 1.0.0

---

## Overview

This guide provides complete CI/CD pipeline configurations for automated testing, building, and deploying the LangChain Document QA application.

---

## GitHub Actions Pipeline

### 1. Test & Code Quality Workflow

```yaml
# .github/workflows/test.yml
name: Test & Code Quality

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Lint with flake8
      run: |
        flake8 backend --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 backend --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Type check with mypy
      run: mypy backend --ignore-missing-imports
    
    - name: Format check with black
      run: black --check backend
    
    - name: Import sort check with isort
      run: isort --check-only backend
    
    - name: Run unit tests
      run: |
        pytest tests/unit -v --cov=backend --cov-report=xml --cov-report=html
    
    - name: Run integration tests
      run: pytest tests/integration -v
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Bandit security scan
      run: |
        pip install bandit
        bandit -r backend -f json -o bandit-report.json || true
    
    - name: Run pip audit
      run: |
        pip install pip-audit
        pip-audit --desc
    
    - name: Upload security reports
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: security-reports
        path: |
          bandit-report.json
```

### 2. Build & Push Docker Images

```yaml
# .github/workflows/build.yml
name: Build & Push Docker Images

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Log in to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: |
          docker.io/${{ secrets.DOCKER_USERNAME }}/langchain-qa-backend
        tags: |
          type=ref,event=branch
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha
    
    - name: Build and push Backend image
      uses: docker/build-push-action@v4
      with:
        context: .
        file: ./Dockerfile
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=registry,ref=docker.io/${{ secrets.DOCKER_USERNAME }}/langchain-qa-backend:buildcache
        cache-to: type=registry,ref=docker.io/${{ secrets.DOCKER_USERNAME }}/langchain-qa-backend:buildcache,mode=max
    
    - name: Build and push Frontend image
      uses: docker/build-push-action@v4
      with:
        context: ./frontend
        file: ./frontend/Dockerfile
        push: true
        tags: ${{ steps.meta.outputs.tags }}-frontend
        labels: ${{ steps.meta.outputs.labels }}
```

### 3. Deploy to Staging

```yaml
# .github/workflows/deploy-staging.yml
name: Deploy to Staging

on:
  push:
    branches: [ develop ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to staging
      uses: actions/github-script@v6
      with:
        script: |
          const deploymentUrl = process.env.STAGING_DEPLOY_URL;
          const response = await github.rest.repos.createDeployment({
            owner: context.repo.owner,
            repo: context.repo.repo,
            ref: context.ref,
            environment: 'staging',
            required_contexts: [],
            auto_merge: false,
          });
          console.log(`Deployment created: ${response.data.id}`);
      env:
        STAGING_DEPLOY_URL: ${{ secrets.STAGING_DEPLOY_URL }}
    
    - name: Run smoke tests
      run: |
        sleep 30  # Wait for deployment
        curl -f http://staging.yourdomain.com/health || exit 1
        curl -f http://staging.yourdomain.com/health/db || exit 1
        curl -f http://staging.yourdomain.com/health/vector-store || exit 1
    
    - name: Notify Slack
      if: always()
      uses: slackapi/slack-github-action@v1
      with:
        webhook-url: ${{ secrets.SLACK_WEBHOOK }}
        payload: |
          {
            "text": "Staging deployment ${{ job.status }}",
            "blocks": [
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "Staging Deployment *${{ job.status }}*\nCommit: ${{ github.sha }}\nAuthor: ${{ github.actor }}"
                }
              }
            ]
          }
```

### 4. Deploy to Production

```yaml
# .github/workflows/deploy-production.yml
name: Deploy to Production

on:
  release:
    types: [ published ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
    - uses: actions/checkout@v4
      with:
        ref: ${{ github.event.release.tag_name }}
    
    - name: Deploy to production
      env:
        PROD_DEPLOY_TOKEN: ${{ secrets.PROD_DEPLOY_TOKEN }}
      run: |
        curl -X POST https://your-deployment-service.com/deploy \
          -H "Authorization: Bearer $PROD_DEPLOY_TOKEN" \
          -H "Content-Type: application/json" \
          -d '{
            "version": "${{ github.event.release.tag_name }}",
            "environment": "production",
            "rollback_on_failure": true
          }'
    
    - name: Wait for deployment
      run: sleep 60
    
    - name: Verify production health
      run: |
        for i in {1..30}; do
          if curl -f https://yourdomain.com/health && \
             curl -f https://yourdomain.com/health/db; then
            echo "✅ Production health check passed"
            exit 0
          fi
          echo "Attempt $i: Health check failed, retrying..."
          sleep 10
        done
        exit 1
    
    - name: Run production smoke tests
      run: |
        pytest tests/smoke -v --tb=short
    
    - name: Notify success
      if: success()
      uses: slackapi/slack-github-action@v1
      with:
        webhook-url: ${{ secrets.SLACK_WEBHOOK }}
        payload: |
          {
            "text": "🚀 Production deployment successful",
            "blocks": [
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "✅ Production Deployment Successful\nVersion: ${{ github.event.release.tag_name }}\nCommit: ${{ github.sha }}"
                }
              }
            ]
          }
    
    - name: Notify failure
      if: failure()
      uses: slackapi/slack-github-action@v1
      with:
        webhook-url: ${{ secrets.SLACK_WEBHOOK }}
        payload: |
          {
            "text": "❌ Production deployment failed",
            "blocks": [
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "❌ Production Deployment Failed\nVersion: ${{ github.event.release.tag_name }}\nCommit: ${{ github.sha }}\nPlease check logs and rollback if necessary"
                }
              }
            ]
          }
```

---

## GitLab CI Pipeline

### .gitlab-ci.yml

```yaml
stages:
  - test
  - build
  - deploy_staging
  - deploy_production

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  DOCKER_IMAGE_LATEST: $CI_REGISTRY_IMAGE:latest

before_script:
  - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

test:
  stage: test
  image: python:3.12
  script:
    - pip install -r requirements.txt
    - pytest tests/ -v --cov=backend --cov-report=xml
    - flake8 backend
    - mypy backend --ignore-missing-imports
    - black --check backend
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

security_scan:
  stage: test
  image: python:3.12
  script:
    - pip install bandit pip-audit
    - bandit -r backend -f json -o bandit-report.json || true
    - pip-audit --desc
  artifacts:
    reports:
      sast: bandit-report.json

build_backend:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $DOCKER_IMAGE -f Dockerfile .
    - docker tag $DOCKER_IMAGE $DOCKER_IMAGE_LATEST
    - docker push $DOCKER_IMAGE
    - docker push $DOCKER_IMAGE_LATEST
  only:
    - main

build_frontend:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $DOCKER_IMAGE-frontend -f frontend/Dockerfile ./frontend
    - docker tag $DOCKER_IMAGE-frontend $DOCKER_IMAGE_LATEST-frontend
    - docker push $DOCKER_IMAGE-frontend
    - docker push $DOCKER_IMAGE_LATEST-frontend
  only:
    - main

deploy_staging:
  stage: deploy_staging
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context staging
    - kubectl set image deployment/backend backend=$DOCKER_IMAGE -n langchain-qa
    - kubectl rollout status deployment/backend -n langchain-qa
    - curl -f https://staging.yourdomain.com/health || exit 1
  environment:
    name: staging
    kubernetes:
      namespace: langchain-qa
  only:
    - develop

deploy_production:
  stage: deploy_production
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context production
    - kubectl set image deployment/backend backend=$DOCKER_IMAGE -n langchain-qa
    - kubectl rollout status deployment/backend -n langchain-qa
    - sleep 30
    - curl -f https://yourdomain.com/health || exit 1
    - curl -f https://yourdomain.com/health/db || exit 1
  environment:
    name: production
    kubernetes:
      namespace: langchain-qa
  when: manual
  only:
    - tags
```

---

## Jenkins Pipeline

### Jenkinsfile

```groovy
pipeline {
    agent any
    
    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['none', 'staging', 'production'], defaultValue: 'none')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                sh '''
                    python -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest tests/ -v --cov=backend --cov-report=xml --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')]
                }
            }
        }
        
        stage('Code Quality') {
            parallel {
                stage('Lint') {
                    steps {
                        sh '''
                            source venv/bin/activate
                            flake8 backend --format=json --output-file=flake8-report.json || true
                        '''
                    }
                }
                stage('Type Check') {
                    steps {
                        sh '''
                            source venv/bin/activate
                            mypy backend --ignore-missing-imports > mypy-report.txt || true
                        '''
                    }
                }
                stage('Security Scan') {
                    steps {
                        sh '''
                            source venv/bin/activate
                            pip install bandit
                            bandit -r backend -f json -o bandit-report.json || true
                        '''
                    }
                }
            }
        }
        
        stage('Build') {
            steps {
                sh '''
                    docker build -t langchain-qa-backend:${BUILD_NUMBER} -f Dockerfile .
                    docker build -t langchain-qa-frontend:${BUILD_NUMBER} -f frontend/Dockerfile ./frontend
                '''
            }
        }
        
        stage('Deploy Staging') {
            when {
                expression { params.DEPLOY_ENV == 'staging' }
            }
            steps {
                sh '''
                    docker-compose -f docker-compose.staging.yml down
                    docker-compose -f docker-compose.staging.yml up -d
                    sleep 10
                    curl -f http://staging:8000/health || exit 1
                '''
            }
        }
        
        stage('Deploy Production') {
            when {
                expression { params.DEPLOY_ENV == 'production' }
                branch 'main'
            }
            input {
                message "Deploy to production?"
                ok "Deploy"
            }
            steps {
                sh '''
                    kubectl set image deployment/backend \
                        backend=langchain-qa-backend:${BUILD_NUMBER} \
                        -n langchain-qa
                    kubectl rollout status deployment/backend -n langchain-qa
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        failure {
            sh '''
                curl -X POST ${SLACK_WEBHOOK} \
                    -H 'Content-Type: application/json' \
                    -d '{"text": "Build failed: ${JOB_NAME} #${BUILD_NUMBER}"}'
            '''
        }
        success {
            sh '''
                curl -X POST ${SLACK_WEBHOOK} \
                    -H 'Content-Type: application/json' \
                    -d '{"text": "Build successful: ${JOB_NAME} #${BUILD_NUMBER}"}'
            '''
        }
    }
}
```

---

## Key Features

### Automated Testing
- Unit and integration tests on every push
- Code coverage reporting
- Flake8 linting
- MyPy type checking
- Black formatting
- Isort import sorting

### Security
- Bandit security scanning
- pip-audit for dependency vulnerabilities
- No secrets in logs
- Production deployments require approval

### Docker Build Optimization
- Multi-stage builds for smaller images
- Layer caching for faster builds
- Separate frontend/backend images
- Image tagging with commit SHA and version

### Deployment Strategies
- Staging: Automatic on develop branch
- Production: Manual approval, tagged releases
- Health checks after deployment
- Automated rollback on failure

### Notifications
- Slack notifications for build status
- Email alerts on production deployment
- Failed pipeline notifications
- Deployment summaries

---

## Environment Secrets

Add these to your CI/CD platform:

```
DOCKER_USERNAME
DOCKER_PASSWORD
SLACK_WEBHOOK
PROD_DEPLOY_TOKEN
DATABASE_URL (staging)
DATABASE_URL (production)
OPENAI_API_KEY
ANTHROPIC_API_KEY
VECTOR_STORE_API_KEY
```

---

## Testing Strategy

### Unit Tests (Fast)
- Run on every push
- <5 minutes total
- ~70 test cases
- Code coverage >80%

### Integration Tests (Medium)
- Run on every push
- ~5-10 minutes
- End-to-end workflows
- Database included

### Smoke Tests (Quick)
- Run after deployment
- ~1 minute
- Health checks
- API basic functionality

### Load Tests (Slow)
- Run before production
- ~10-30 minutes
- 1000+ req/sec
- Performance baseline

### Security Tests
- Run before deployment
- Bandit scanning
- Dependency audits
- SAST/DAST tools

---

## Deployment Checklist

Before deploying to production:

```bash
☑ All tests passing
☑ Code coverage >80%
☑ No security vulnerabilities
☑ Docker images built and pushed
☑ Staging deployment successful
☑ Staging health checks passed
☑ Load tests completed
☑ Performance baseline met
☑ Security audit passed
☑ Team approval received
☑ Rollback plan ready
☑ On-call engineer notified
☑ Monitoring alerts configured
```

---

## Rollback Procedure

```bash
# Quick rollback in Kubernetes
kubectl rollout undo deployment/backend -n langchain-qa

# Verify rollback
kubectl rollout status deployment/backend -n langchain-qa
curl https://yourdomain.com/health

# Or revert to previous tag
git tag -l | sort -V | tail -2  # Get last 2 versions
git checkout v1.0.0
docker build -t langchain-qa-backend:v1.0.0 .
kubectl set image deployment/backend backend=langchain-qa-backend:v1.0.0 -n langchain-qa
```

---

For support or questions, contact the DevOps team.
