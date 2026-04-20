import json
from confluent_kafka import Consumer

from orchestrator_logic import event_rules
from producer import send_event

def consume_events():
    c_conf = {
            "bootstrap.servers": "kafka:9092",
            "group.id": "order-processing-service",
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
        }
    consumer = Consumer(c_conf)

    consumer.subscribe(['order.events'])
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print(f'Kafka error: {msg.error()}')
                continue

            event = json.loads(msg.value().decode())
            event_rules(event)
            consumer.commit(msg)
            
    finally:
        consumer.close()