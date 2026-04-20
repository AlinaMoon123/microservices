import time
import random
from app.message.producer import send_event


def reserve_inventory(item:str):
    time.sleep(5)
    return 1 if random.random() < 0.8 else 0
