from datetime import datetime, timezone

from sqlalchemy import DateTime

from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Event(Base):
    __tablename__="events"

    id: Mapped[int]=mapped_column(primary_key=True)
    message_id: Mapped[str]=mapped_column(unique=True, nullable=False)
    event_type: Mapped[str]
    order_id: Mapped[int]
    processed_at: Mapped[DateTime]=mapped_column(default=datetime.now(timezone.utc))
