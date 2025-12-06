from dotenv import load_dotenv
from os import getenv
load_dotenv()

START_IMG = getenv("START_IMG", "https://i.ibb.co/hRtNhLC8/x.jpg")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "inialiyaar")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "inialiyaar_timeline")
OWNER_ID = int(getenv("OWNER_ID", 8370504630))

API_ID = getenv("API_ID", 12345)
API_HASH = getenv("API_HASH", "abcd1245")
BOT_TOKEN = getenv("BOT_TOKEN", "TOKEN")
STRING_SESSION = getenv("STRING_SESSION", "session")
MONGO_DB_URL = getenv("MONGO_DB_URL", "MONGO_DB_URL")
EVENT_LOGS = int(getenv("EVENT_LOGS", -1003196237043))
ROUTER_API = getenv("API_KEY", None)
DURATION_LIMIT = 7200
DATABASE_CHANNEL_ID = int(getenv("DATABASE_ID", None)) 