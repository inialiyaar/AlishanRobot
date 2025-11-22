from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("ENTER YOUR API ID: "))
api_hash = input("ENTER YOUR API HASH: ")

with TelegramClient(StringSession(), int(api_id), api_hash) as client:
    client.send_message("me", client.session.save())
