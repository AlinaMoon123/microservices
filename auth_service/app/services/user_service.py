from fastapi import HTTPException
from app.auth.hash_passw import check_password
from app.auth.jwt import create_access_token, create_refresh_token
from app.schemas.user import CreateUser
from sqlalchemy.orm import Session
from app.crud.user_crud import create_user, find_email

def registration(user: CreateUser, db: Session):
    if find_email(user.email, db):
        raise HTTPException(status_code=409, detail="User with this email is exist")
    if user.password==user.accept_password:
        db_user=create_user(user, db)
        return db_user
    raise HTTPException(status_code=400, detail="Passwords dont match")

    

def login(email: str, password: str, db:Session):
    db_user = find_email(email, db)
    if db_user==None or check_password(password, db_user.password)==False:
        raise HTTPException(status_code=401, detail="Wrong login or password")
    access_token=create_access_token(db_user.id, db_user.role)
    refresh_token=create_refresh_token(db_user.id, db_user.role)
    return refresh_token, {"access_token": access_token, "token_type": "bearer"}



