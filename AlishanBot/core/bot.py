from telethon import TelegramClient
from telethon.sessions import StringSession
from AlishanBot import config
from pytgcalls import PyTgCalls


def start_bot():
    Alishan = TelegramClient("Alishan", config.API_ID, config.API_HASH).start(bot_token=config.BOT_TOKEN)
    Alishan.start()
    return Alishan
    
def start_assistant():
    assistant = TelegramClient(StringSession(config.STRING_SESSION), config.API_ID, config.API_HASH)
    return assistant   
    
Alishan = start_bot()
Assistant = start_assistant()  
music = PyTgCalls(Assistant)