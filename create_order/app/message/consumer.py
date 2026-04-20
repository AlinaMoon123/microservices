import json
from confluent_kafka import Consumer

from app.crud.order_crud import change_status, status_cancelled, status_completed
from app.db.database import SessionLocal
from app.models.order import OrderStatus

def consume_orders():
    
    conf = {
        "bootstrap.servers": "kafka:9092",
        "group.id": "create-order-service",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    }
    consumer = Consumer(conf)
    consumer.subscribe(["order.events"])
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print(f"Kafka error: {msg.error()}")
                continue

            event = json.loads(msg.value().decode("utf-8"))
            order_id=event['payload']['order_id']
            print(f"Received order_id={order_id} ")
            event_type = event['event_type']

            if event_type == "order.completed":
                with SessionLocal() as db:
                    change_status(order_id, OrderStatus.COMPLETED, db)
                print(f'Order completed: {order_id}')

            elif event_type == "order.cancelled":
                with SessionLocal() as db:
                    change_status(order_id, OrderStatus.CANCELLED, db)
                print(f'Order cancelled: {order_id}')

            consumer.commit(msg)

    finally:
        consumer.close()