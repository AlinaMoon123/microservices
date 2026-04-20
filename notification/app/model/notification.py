from sqlalchemy import ForeignKey
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Notification(Base):
    __tablename__="notification"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
