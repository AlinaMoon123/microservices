from sqlalchemy.orm import Session
from app.model.notification import Notification

def create_message(msg:str, user_id:int, db:Session):
    message_db=Notification(message=msg, user_id=user_id)
    db.add(message_db)
    db.commit()
    db.refresh(message_db)