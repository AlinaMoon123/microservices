
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
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(onupdate=lambda: datetime.now(timezone.utc), nullable=True)
