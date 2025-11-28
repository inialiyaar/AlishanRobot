from pymongo import MongoClient
from AlishanBot import config

client = MongoClient(config.MONGO_DB_URL)
db = client["Alishan"]
users = db["users"]
groups = db["chats"]
chat_bot_groups = db["chat_bot_groups"]
economy = db["economy"]
economy_settings = db["economy_settings"]
greetings = db["greetings"]
sudo_users = db["sudo_users"]
stream_mode = db["stream_mode"]