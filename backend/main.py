"""
__APP_NAME__ — FastAPI Backend

Provisioned by BioForge. Runs on ECS Fargate behind ALB.
"""
import os
import time
from fastapi import FastAPI
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

@app.get('/health')
async def health():
    return {'status': 'healthy', 'service': APP_NAME, 'timestamp': int(time.time())}

app.include_router(api.router, prefix='/api')
