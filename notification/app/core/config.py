from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
LOCAL_DATABASE_URL=os.getenv("LOCAL_DATABASE_URL")