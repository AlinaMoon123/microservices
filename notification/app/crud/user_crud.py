from sqlalchemy import select
from sqlalchemy.orm import Session
from app.model.user import Users


def create_user(user: dict, db: Session):
    db_user = Users(id=user["user_id"], name=user["name"], email=user["email"], password=user["password"], role=user["role"])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def find_user(user_id:int, db:Session):
    stmt=select(Users).where(Users.id==user_id)
    res=db.execute(stmt)
    return res.scalars().first()