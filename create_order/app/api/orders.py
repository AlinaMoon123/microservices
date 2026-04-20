from fastapi import APIRouter, Depends
from app.db.database import get_db
from app.message.producer import send_event
from app.schemas.orders_schemas import CreateOrder, OrderEvent
from app.services.order_service import create_order, get_all_orders, get_user_orders
from sqlalchemy.orm import Session
from app.services.user_service import get_current_user



router = APIRouter(prefix = "/orders")

@router.post("/")
def endpoint(order: CreateOrder, db:Session=Depends(get_db), user=Depends(get_current_user)):
    new_order = create_order(order, user, db)
    value = OrderEvent(
        order_id= new_order.id,
        user_id= new_order.user_id,
        item= new_order.item,
        quantity= new_order.quantity
    )
    send_event("order.events", "order.created", str(new_order.saga_id), value.model_dump(), new_order.id)

@router.get("/")
def endpoint(user=Depends(get_current_user), db: Session=Depends(get_db)):
    user_id = user["user_id"]
    user_role=user["role"]
    if user_role=="admin":
        return get_all_orders(db)
    else:
        return get_user_orders(user_id, db)

