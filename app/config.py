import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

CASHFREE_APP_ID = os.getenv("CASHFREE_APP_ID")
CASHFREE_SECRET_KEY = os.getenv("CASHFREE_SECRET_KEY")
CASHFREE_WEBHOOK_SECRET = os.getenv("CASHFREE_WEBHOOK_SECRET")

BASE_URL = os.getenv("BASE_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

GROUP_1_LOG = int(os.getenv("GROUP_1_LOG"))
GROUP_2_LOG = int(os.getenv("GROUP_2_LOG"))
