import time
from AlishanBot.modules.helper_funcs.info import get_info
import re
start_time = time.time()
player_stats = {}
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

def update_time(chat_id):
    state = player_stats.get(chat_id)
    if not state:
        return

    if state["is_playing"]:
        now = time.time()
        state["current_time"] += now - state["last_update"]
        state["last_update"] = now

    if state["current_time"] < 0:
        state["current_time"] = 0
    if state["current_time"] > state["duration"]:
        state["current_time"] = state["duration"]