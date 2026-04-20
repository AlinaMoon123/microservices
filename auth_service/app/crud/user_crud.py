from sqlalchemy import select
from app.auth.hash_passw import hash_password
from app.models.user import Users
from app.schemas.user import CreateUser
from sqlalchemy.orm import Session

def create_user(user: CreateUser, db: Session):
    file = open("admin_emails.txt")
    if str(user.email) in [admin_email for admin_email in file]:
        user_role = "admin"
    else:
        user_role="user"
    db_user = Users(name=user.name, email=user.email, password=hash_password(user.password), role=user_role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def find_email(email:str, db:Session):
    stmt = select(Users).where(Users.email==email)
    res = db.execute(stmt)
    return res.scalars().first()

def find_user(user_id:int, db:Session):
    stmt=select(Users).where(Users.id==user_id)
    res = db.execute(stmt)
    return res.scalars().first()