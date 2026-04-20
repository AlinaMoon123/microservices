from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]=mapped_column(nullable=False)
    password: Mapped[str]
    role: Mapped[str]
