import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
UPLOAD_BOT_TOKEN = os.getenv("UPLOAD_BOT_TOKEN")

CHANNEL_ID = os.getenv("CHANNEL_ID")
SUBSCRIPTION_CHANNEL = os.getenv("SUBSCRIPTION_CHANNEL")
DATABASE_URL = os.getenv("DATABASE_URL")
