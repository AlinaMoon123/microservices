import json
import uuid
from confluent_kafka import Consumer

from pay import charge_payment
from producer import send_event
from retry_logic import handle_retry

def consume_orders():
    
    conf = {
        "bootstrap.servers": "kafka:9092",
        "group.id": "order-processing-service",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    }
    consumer = Consumer(conf)
    consumer.subscribe(["payment.commands",
                        "payment.retry.1",
                        "payment.retry.2"])
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

            if event_type == "charge_payment":
                res = charge_payment(event["payload"]["item"])
                if res:
                    out_event = {
                    "message_id": str(uuid.uuid4()),
                    "event_type": "payment.succeeded",
                    "saga_id": saga_id,
                    "payload": event["payload"]
                    }
                    send_event("order.events", out_event,order_id)
                else:
                    handle_retry(event, order_id)

            elif event_type == "refund_payment":
                out_event = {
                    "message_id": str(uuid.uuid4()),
                    "event_type": "payment.refunded",
                    "saga_id": saga_id,
                    "payload": event["payload"]
                }
                send_event("order.events", out_event,order_id)

            consumer.commit(msg)
    finally:
        consumer.close()