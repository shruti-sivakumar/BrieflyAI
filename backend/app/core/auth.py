# app/core/auth.py
from typing import Optional, Dict, Any
import jwt
from fastapi import Depends, HTTPException, status, Request
from app.core.config import settings

ALGS = ["HS256"]  # Supabase JWTs are signed with HS256 using SUPABASE_JWT_SECRET

def decode_supabase_jwt(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.SUPABASE_JWT_SECRET, algorithms=ALGS, options={"verify_aud": False})
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_bearer_token(request: Request) -> str:
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    return auth.split(" ", 1)[1].strip()

def get_current_user(request: Request) -> Dict[str, Any]:
    token = get_bearer_token(request)
    payload = decode_supabase_jwt(token)
    # Supabase sets 'sub' as the user id
    user_id: Optional[str] = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token (no sub)")
    return {"id": user_id, "email": payload.get("email")}
