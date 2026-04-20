import json
import uuid
from confluent_kafka import Consumer, KafkaException

from app.config import RETRY_DELTA, RETRY_QUANTITY
from app.message.producer import send_event
from app.order_processing import reserve_inventory
from app.retry_logic import handle_retry



def consume_orders():
    
    conf = {
        "bootstrap.servers": "kafka:9092",
        "group.id": "order-processing-service",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    }
    consumer = Consumer(conf)
    consumer.subscribe(["inventory.commands"])
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print(f"Kafka error: {msg.error()}")
                continue

            event = json.loads(msg.value().decode("utf-8"))
            event_type=event["command"]
            order_id = event["payload"]["order_id"]
            saga_id = event["saga_id"]

            if event_type == "reserve_inventory":
                res = reserve_inventory(event["payload"]["item"])
                if res:
                    out_event = {
                    "message_id": str(uuid.uuid4()),
                    "event_type": "inventory.reserved",
                    "saga_id": saga_id,
                    "payload": event["payload"]
                    }

                    send_event("order.events", out_event, order_id)
                else:
                    handle_retry(event, order_id, RETRY_QUANTITY, RETRY_DELTA)

            elif event_type == "cancel_reservation":
                out_event = {
                    "message_id": str(uuid.uuid4()),
                    "event_type": "inventory.reservation-cancelled",
                    "saga_id": saga_id,
                    "payload": event["payload"]
                }
                send_event("order.events", out_event, order_id)

            consumer.commit(msg)
    finally:
        consumer.close()