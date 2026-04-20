from uuid import uuid4
from app.crud.order_crud import create, get_all, get_orders
from app.schemas.orders_schemas import CreateOrder
from sqlalchemy.orm import Session

def create_order(order: CreateOrder, user: dict, db:Session):
    saga_id = uuid4()
    return create(order, user, saga_id,db)

def get_all_orders(db:Session):
    return get_all(db)

def get_user_orders(user_id:int, db:Session):
    return get_orders(user_id, db)
