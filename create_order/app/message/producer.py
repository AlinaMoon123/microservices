from uuid import uuid4
import uuid
from confluent_kafka import Producer
import json

conf = {
    "bootstrap.servers": "kafka:9092",
    "retries": 5,
    "linger.ms": 5,
    "enable.idempotence": True,
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} ")

def send_event(topic: str, event_type:str, saga_id: str, value: dict, key: int):
    event = {
        "message_id": str(uuid.uuid4()),
        "event_type": event_type,
        "saga_id": saga_id,
        "payload": value
    }
    producer.produce(
        topic=topic,
        key=str(key).encode("utf-8"),
        value=json.dumps(event).encode("utf-8"),
        on_delivery=delivery_report,
    )
    producer.poll(0)

producer.flush(10)
 