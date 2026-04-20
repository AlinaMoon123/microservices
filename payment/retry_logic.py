import time
import uuid

from producer import send_event

def retry_topic(retry_num:int):
    return f'payment.retry.{retry_num}'


def handle_retry(event:dict, order_id:int):
    retry = event.get("retry", 0)

    if retry < 2:
        delay=10*(retry+1)
        print(f"Retry {retry+1}, sleeping {delay}s...")
        time.sleep(delay)
        event["retry"] = retry + 1
        num=retry+1
        topic=retry_topic(num)
        send_event(topic, event, order_id)
    else:
        print("Sending to DLQ")
        send_event('payment.dlq', event, order_id)

        fail_event = {
            "message_id": str(uuid.uuid4()),
            "event_type": "payment.failed",
            "saga_id": event["saga_id"],
            "payload": event["payload"]
        }
        send_event("order.events", fail_event, order_id)