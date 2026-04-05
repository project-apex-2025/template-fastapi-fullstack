"""
__APP_NAME__ — FastAPI Backend

Provisioned by BioForge. Runs on ECS Fargate behind ALB.
All /api/* routes require Cognito JWT authentication (enforced at router level).
"""
import os
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from auth import get_current_user
from routers import api

APP_NAME = os.environ.get('APP_NAME', '__APP_NAME__')
APP_HOSTNAME = os.environ.get('APP_HOSTNAME', '__APP_HOSTNAME__')

app = FastAPI(title=APP_NAME, version='0.1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f'https://{APP_HOSTNAME}',
        'http://localhost:5173',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# Health check — unauthenticated (ALB health check)
@app.get('/health')
async def health():
    return {'status': 'healthy', 'service': APP_NAME, 'timestamp': int(time.time())}


# All API routes require auth — enforced by router-level dependency
app.include_router(api.router, prefix='/api', dependencies=[__import__('fastapi').Depends(get_current_user)])
