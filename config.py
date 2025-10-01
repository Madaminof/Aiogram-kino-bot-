import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
UPLOAD_BOT_TOKEN = os.getenv("UPLOAD_BOT_TOKEN")

CHANNEL_ID = os.getenv("CHANNEL_ID")   # @kinotopbot001
SUBSCRIPTION_CHANNEL = int(os.getenv("SUBSCRIPTION_CHANNEL"))  # -100...
SUBSCRIPTION_LINK = os.getenv("SUBSCRIPTION_LINK")

DATABASE_URL = os.getenv("DATABASE_URL")
