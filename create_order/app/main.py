from app.db.database import Base, engine
from fastapi import FastAPI
from app.api.orders import router
from app.message.consumer import consume_orders
from app.models.order import Order

app = FastAPI()
app.include_router(router)
# Base.metadata.create_all(bind=engine)

