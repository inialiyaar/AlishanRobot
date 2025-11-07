from pymongo import MongoClient
from AlishanBot import config

client = MongoClient(config.MONGO_DB_URL)
db = client["Alishan"]
users = db["users"]
groups = db["chats"]