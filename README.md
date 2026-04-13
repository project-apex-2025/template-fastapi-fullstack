# __APP_NAME__

> Provisioned by [Halo](https://halo.apex.hcls.aws.dev) — Knowledge & Product Platform

## Quick Start

```bash
# Frontend
cd frontend && npm install && npm run dev

# Backend
cd backend && pip install -r requirements.txt && uvicorn main:app --reload

# Infrastructure
cd infrastructure && terraform init && terraform plan
```

## Architecture

React + FastAPI on ECS Fargate behind ALB, with Cognito auth and CloudFront.

## Deployment

Push to `main` → GitHub Actions builds and deploys automatically.

**URL:** https://__APP_HOSTNAME__
