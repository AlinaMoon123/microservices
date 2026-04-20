from app.message.consumer import consume_orders


def start_comsumer():
    consume_orders()

if __name__=="__main__":
    start_comsumer()