import json
from confluent_kafka import Consumer, KafkaException
from app.crud.user_crud import create_user
from app.db.database import get_db
from app.services.notification_service import add_user, write_message



def consume_notification():
    conf = {
    "bootstrap.servers": "kafka:9092",
    "group.id": "notification-service",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
}
    consumer=Consumer(conf)
    consumer.subscribe(["order.events", "notification.command"])
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print(f"Kafka error: {msg.error()}")
                continue
            
            event = json.loads(msg.value().decode("utf-8"))
            event_type=event["event_type"]
            if event_type=="update-user-table":
                user=event["payload"]
                with get_db() as db:
                    add_user(user, db)
            else:
                with get_db() as db:
                    write_message(event_type, event["payload"]["user_id"], db)
                print(event["payload"]["order_id"], event_type)

    finally:
        consumer.close()