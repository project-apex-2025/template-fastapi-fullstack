"""Starter API routes. Add your application routes here."""
from fastapi import APIRouter, Depends
from auth import get_current_user

router = APIRouter(tags=['api'])


@router.get('/hello')
async def hello(username: str = Depends(get_current_user)):
    return {'message': f'Hello, {username}!', 'app': '__APP_NAME__'}
