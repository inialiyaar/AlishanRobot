import time
from AlishanBot.__init__ import start_time

def get_uptime():
    current_time = time.time()
    seconds = int(current_time - start_time)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    parts = []
    if days > 0:
        parts.append(f"{days} ᴅᴀʏ{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} ʜᴏᴜʀ{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} ᴍɪɴᴜᴛᴇ{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} sᴇᴄᴏɴᴅ{'s' if seconds != 1 else ''}")
    return " ".join(parts)