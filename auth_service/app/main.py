from fastapi import FastAPI
from app.api.user_api import router
from app.db.database import Base, engine
from app.models.user import Users

app = FastAPI()
app.include_router(router)
# Base.metadata.create_all(bind=engine)