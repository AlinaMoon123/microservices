import json
from confluent_kafka import Producer

conf = {
    "bootstrap.servers": "kafka:9092",
    "retries": 5,
    "linger.ms": 5,
    "enable.idempotence": True,
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Delivery faild: {err}')
    else:
        print(f'Delivered to {msg.topic()}')

def send_event(topic: str, event: dict, key: str):
    producer.produce(
        topic=topic,
        key=str(key).encode("utf-8"),
        value=json.dumps(event).encode("utf-8"),
        on_delivery=delivery_report,
    )
    producer.poll(0)

producer.flush(10)
