import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__name__).resolve().parent
ENV_FILE = BASE_DIR / '.env'


if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)

BOT_TOKEN = os.getenv('BOT_TOKEN')
DOMAIN = os.getenv('DOMAIN')
API_URL = os.getenv('API_URL')
ADMIN_IDS = os.getenv("ADMIN_IDS").split(" ")
CHANNEL_ID= int(os.getenv('CHANNEL_ID'))
CHANNEL_URL=os.getenv("CHANNEL_URL")