import json
from confluent_kafka import Producer


p_conf = {
    "bootstrap.servers": "kafka:9092",
    "retries": 5,
    "linger.ms": 5,
    "enable.idempotence": True,
}

producer = Producer(p_conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} ")

def send_event(topic: str, event:dict, key: int):
    producer.produce(
        topic=topic,
        key=str(key).encode("utf-8"),
        value=json.dumps(event).encode("utf-8"),
        on_delivery=delivery_report,
    )
    producer.poll(0)
producer.flush()