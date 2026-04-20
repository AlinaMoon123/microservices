from dotenv import load_dotenv
import os

load_dotenv()

RETRY_QUANTITY = os.getenv("RETRY_QUANTITY")
RETRY_DELTA = os.getenv("RETRY_DELTA")