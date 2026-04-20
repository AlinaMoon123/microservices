from sqlalchemy.orm import Session
from app.crud.message import create_message
from app.crud.user_crud import create_user, find_user


def write_message(msg:str,user_id:int,db:Session):
    create_message(msg, user_id, db)

def add_user(user:dict, db:Session):
    db_user=find_user(user["user_id"], db)
    if db_user==None:
        create_user(user,db)