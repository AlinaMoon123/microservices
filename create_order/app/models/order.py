import enum
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum

from app.db.database import Base

class OrderStatus(str, enum.Enum):
    NEW = "new"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    saga_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False,index=True)
    item: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[OrderStatus] = mapped_column(nullable=False,default=OrderStatus.NEW,index=True)
    quantity: Mapped[int] = mapped_column(nullable=False)