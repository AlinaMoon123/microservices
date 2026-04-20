from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

def get_db():
    with SessionLocal() as db:
        try:
            yield db
        finally:
            db.close()