import time
from AlishanBot.modules.helper_funcs.info import get_info
start_time = time.time()
is_playing = {}
download_data = {}
info = get_info()
BOT_MENTION = info["BOT_MENTION"]
BOT_USERNAME = info["BOT_USERNAME"]
BOT_ID = info["BOT_ID"]
BOT_FULL_NAME = info["BOT_FULL_NAME"]
ASSISTANT_ID = info["ASSISTANT_ID"]
ASSISTANT_MENTION = info["ASSISTANT_MENTION"]
ASSISTANT_USERNAME = info["ASSISTANT_USERNAME"]
ASSISTANT_FULL_NAME = info["ASSISTANT_FULL_NAME"]