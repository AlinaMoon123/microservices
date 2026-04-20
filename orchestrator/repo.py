from sqlalchemy.orm import Session
from model import Saga, SagaStatus


def get_saga(saga_id: str, db: Session):
    return db.get(Saga, saga_id)


def create_saga(saga_id: str, order_id: str, db: Session):
    saga = Saga(
        saga_id=saga_id,
        order_id=order_id,
        status=SagaStatus.START,
    )
    db.add(saga)
    db.commit()
    return saga

#TODO в одну функцию + ошибки
def inventory_reserved_done(saga: Saga, db: Session):
    saga.inventory_reserved = True
    db.commit()


def payment_done(saga: Saga, db: Session):
    saga.payment = True
    db.commit()


def complete_saga(saga: Saga, db: Session):
    saga.status = SagaStatus.COMPLETED
    saga.finished = True
    db.commit()


def cancel_saga(saga: Saga, db: Session):
    saga.status = SagaStatus.CANCELLED
    saga.finished = True
    db.commit()
