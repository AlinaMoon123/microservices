from pydantic import BaseModel

class CreateOrder(BaseModel):
    item: str
    quantity: int

class OutputOrder(CreateOrder):
    order_id: int
    status:str

class OrderEvent(BaseModel):
    order_id: int
    user_id: int
    item: str
    quantity: int