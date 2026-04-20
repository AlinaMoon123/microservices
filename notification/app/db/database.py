from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(url=DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

@contextmanager
def get_db():
    with SessionLocal() as db:
        try:
            yield db
        finally:
            db.close()
