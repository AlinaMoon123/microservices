from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum
from db import Base

class SagaStatus(enum.Enum):
    START = "START"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Saga(Base):
    __tablename__ = "sagas"

    saga_id: Mapped[str] = mapped_column(primary_key=True)
    order_id: Mapped[str] = mapped_column(index=True)
    inventory_reserved: Mapped[bool] = mapped_column(default=False)
    payment: Mapped[bool] = mapped_column(default=False)
    status: Mapped[SagaStatus] = mapped_column(Enum(SagaStatus), default=SagaStatus.START)
    finished: Mapped[bool] = mapped_column(default=False)