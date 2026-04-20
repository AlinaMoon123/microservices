from sqlalchemy import select, update
from app.models.order import Order, OrderStatus
from app.schemas.orders_schemas import CreateOrder
from sqlalchemy.orm import Session


def create(order:CreateOrder, user:dict,saga_id,db:Session):
    db_order = Order(
        saga_id=saga_id,
        user_id=user["user_id"],
        item=order.item,
        quantity=order.quantity,
        status=OrderStatus.NEW,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_all(db:Session):
    stmt=select(Order)
    res=db.execute(stmt)
    return res.scalars().all()

def get_orders(user_id:int,db:Session):
    stmt=select(Order).where(Order.user_id==user_id)
    res=db.execute(stmt)
    return res.scalars().all()

def change_status(order_id:int, status: str, db:Session):
    stmt=update(Order).where(Order.id==order_id).values(status=status)
    db.execute(stmt)
    db.commit()
