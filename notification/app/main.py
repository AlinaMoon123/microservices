from app.db.database import Base, engine
from app.message.consumer import consume_notification
from app.model.notification import Notification
from app.model.user import Users


if __name__ == "__main__":
    # Base.metadata.create_all(bind=engine)
    consume_notification()