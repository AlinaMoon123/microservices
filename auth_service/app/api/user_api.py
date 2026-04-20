from fastapi import APIRouter, Depends, Request, Response
from app.auth.jwt import refresh
from app.core.config import TOKEN_TIME
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.message.producer import send_event
from app.schemas.user import CreateUser, Login, User
from app.services.user_service import login, registration
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

@router.post('/registration')
def register_endpoint(user: CreateUser, db: Session = Depends(get_db)):
    db_user=registration(user, db)
    value={
        "user_id": db_user.id,
        "name": db_user.name,
        "password": db_user.password,
        "email": db_user.email,
        "role": db_user.role
    }
    send_event("notification.command", value, db_user.id)
    return db_user

@router.post('/login')
def login_endpoint(response: Response, login_form: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    refresh_token, access_token=login(login_form.username, login_form.password, db)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/refresh",
        max_age=TOKEN_TIME
    )
    return access_token

@router.post('/refresh')
def refresh_endpoint(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    return refresh(refresh_token)

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}

