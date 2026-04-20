from consumer import consume_events
from db import Base, engine
from model import Saga


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    consume_events()