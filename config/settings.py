# config/settings.py

from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")

LOCATION = os.getenv("LOCATION")

MODEL_NAME = os.getenv("MODEL_NAME")

BUCKET_NAME = os.getenv("BUCKET_NAME")

DATABASE_URL = os.getenv("DATABASE_URL")
