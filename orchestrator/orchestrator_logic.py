import uuid

from db import get_db
from sqlalchemy.orm import Session

from producer import send_event
from repo import cancel_saga, complete_saga, create_saga, get_saga, inventory_reserved_done, payment_done

def event_rules(event:dict):
    db=next(get_db())
    saga=get_saga(event["saga_id"], db)
    event_type=event["event_type"]
    if not saga:
        saga=create_saga(event["saga_id"], event["payload"]["order_id"], db)

    if event_type=="order.created":
        event={
            "message_id": str(uuid.uuid4()),
            "command": "reserve_inventory",
            "saga_id": saga.saga_id,
            "retry": 0,
            "payload": event["payload"]
        }
        send_event("inventory.commands", event,saga.order_id)

    elif event_type=="inventory.reserved":
        inventory_reserved_done(saga, db)
        event={
            "message_id": str(uuid.uuid4()),
            "command": "charge_payment",
            "saga_id": saga.saga_id,
            "retry": 0,
            "payload": event["payload"]
        }
        send_event("payment.commands", event, saga.order_id)

    elif event_type=="payment.succeeded":
        payment_done(saga, db)
        complete_saga(saga, db)
        event = {
            "message_id": str(uuid.uuid4()),
            "event_type": "order.completed",
            "saga_id": saga.saga_id,
            "payload": event["payload"]
        }
        send_event("order.events",event,saga.order_id)

    elif event_type=="inventory.reserve-failed" or event_type=="payment.failed":
        cancel_saga(saga, db)

        if saga.inventory_reserved:
            event_inv={
                "message_id": str(uuid.uuid4()),
                "command": "cancel_reservation",
                "saga_id": saga.saga_id,
                "payload": event["payload"]
            }
            send_event(
                "inventory.commands",event_inv,saga.order_id)

        if saga.payment:
            event_pay={ #TODO функция создания событий
                "message_id": str(uuid.uuid4()),
                "command": "refund_payment", #TODO Enum
                "saga_id": saga.saga_id,
                "payload": event["payload"]
            }
            send_event("payment.commands", event_pay, saga.order_id)

        event_cancel={
            "message_id": str(uuid.uuid4()),
            "event_type": "order.cancelled",
            "saga_id": saga.saga_id,
            "payload": event["payload"]
        }
        send_event("order.events",event_cancel, saga.order_id)