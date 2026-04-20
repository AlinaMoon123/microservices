import random
import time

from producer import send_event


def charge_payment(item:str):
    time.sleep(5)
    # return 1 if random.random() < 0.7 else 0
    return 0