"""Cognito JWT validation for FastAPI."""
import os
import time
import threading
import httpx
from typing import Optional
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

COGNITO_USER_POOL_ID = os.environ.get('COGNITO_USER_POOL_ID', '__COGNITO_POOL_ID__')
COGNITO_CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID', '__COGNITO_CLIENT_ID__')
COGNITO_REGION = os.environ.get('AWS_REGION', 'us-east-1')

JWKS_URL = f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json'
ISSUER = f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}'

_jwks_cache: dict = {}
_jwks_fetched_at: float = 0
_jwks_lock = threading.Lock()

security = HTTPBearer(auto_error=False)


def _fetch_jwks() -> dict:
    global _jwks_cache, _jwks_fetched_at
    now = time.time()
    if _jwks_cache and (now - _jwks_fetched_at) < 3600:
        return _jwks_cache
    with _jwks_lock:
        if _jwks_cache and (now - _jwks_fetched_at) < 3600:
            return _jwks_cache
        resp = httpx.get(JWKS_URL, timeout=5.0)
        resp.raise_for_status()
        _jwks_cache = resp.json()
        _jwks_fetched_at = time.time()
        return _jwks_cache


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> str:
    if not credentials:
        raise HTTPException(401, 'Missing authorization token')
    try:
        headers = jwt.get_unverified_headers(credentials.credentials)
        jwks = _fetch_jwks()
        key = next((k for k in jwks.get('keys', []) if k['kid'] == headers.get('kid')), None)
        if not key:
            raise JWTError('Key not found')
        claims = jwt.decode(credentials.credentials, key, algorithms=['RS256'],
                          audience=COGNITO_CLIENT_ID, issuer=ISSUER, options={'verify_at_hash': False})
        email = claims.get('email', '')
        if email and '@' in email:
            return email.split('@')[0].lower()
        return claims.get('sub', 'unknown')
    except Exception as e:
        raise HTTPException(401, f'Invalid token: {e}')
