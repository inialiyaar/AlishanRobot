from AlishanBot.core.bot import Alishan
from AlishanBot import config

async def send_error(error):
    try:
        await Alishan.send_message(config.EVENT_LOGS, f"#ERRORLOG\nᴇʀʀᴏʀ Sᴘᴏᴛᴛᴇᴅ!\n```shell\n\n{error}\n```")
    except:
        pass