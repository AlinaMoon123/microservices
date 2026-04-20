from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.crud.user_crud import find_user
from app.db.database import get_db
from app.core.config import ALGORITHM, SECRET_KEY
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_token(user_id: int, role: str, exp_time: int, jwt_type: str):
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=exp_time),
        "type": jwt_type
        }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(user_id: int, role: str):
    return create_token(user_id, role, 15, "access")
    

def create_refresh_token(user_id: int, role: str):
    days = 24*60*30
    return create_token(user_id, role, days, "refresh")

def refresh(refresh_token: dict):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["type"] != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload["sub"]
        role = payload["role"]
        new_access = create_access_token(user_id, role)
        return {"access_token": new_access, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    