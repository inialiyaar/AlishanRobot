from AlishanBot.core.bot import Alishan, Assistant
from AlishanBot.utils.database import users
from AlishanBot.modules.helper_funcs.safedict import SafeDict
from AlishanBot.__init__ import BOT_MENTION
from AlishanBot import config

async def add_user(event):
    user = await event.get_sender()
    user_id = user.id
    username = user.username or "None"
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    full_name = (first_name + " " + last_name).strip()
    
    users.insert_one({"user_id": user_id})
    caption = f"#USERLOG\nɴᴇᴡ ᴜsᴇʀ ʜᴀs sᴛᴀʀᴛᴇᴅ ᴛʜᴇ {BOT_MENTION}.\n\nᴜsᴇʀ: <a href=\"tg://user?id={user_id}\">{full_name}</a>\nᴜsᴇʀɴᴀᴍᴇ: {username}\nɪᴅ: {user_id}"
        
    await Alishan.send_message(
        config.EVENT_LOGS,
        caption,
        parse_mode="html", 
            )