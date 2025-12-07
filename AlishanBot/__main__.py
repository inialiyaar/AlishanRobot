from AlishanBot.core.bot import Alishan, Assistant, music
import asyncio
import importlib
import os
from AlishanBot import config
from AlishanBot.modules.helper_funcs.info import load_info
from asyncio import create_task

async def main():
    print("Starting client")
    await music.start()
    print("Client started")
    await load_info()
    print("Loading Modules... ")
    import_modules()
    print("All Modules loaded")
    print("Starting Bot... ")
    bot = await Alishan.get_me()
    bot_name = f"{bot.first_name or ''} {bot.last_name or ''}"
    await Alishan.send_file(
        config.EVENT_LOGS,
        file=config.START_IMG, 
        caption=f"<a href=\"tg://user?id={bot.id}\">{bot_name}</a> ʙᴏᴛ sᴛᴀʀᴛᴇᴅ:\n\n<b>ᴄᴏʀᴇ sʏsᴛᴇᴍ ᴀɴᴅ ᴍᴏᴅᴜᴏᴇs ᴀʀᴇ ʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ</b>\n\n<b>ɪᴅ:</b> {bot.id}\n<b>ɴᴀᴍᴇ:</b> {bot_name}\n<b>ᴜsᴇʀɴᴀᴍᴇ:</b> @{bot.username}\n", 
        parse_mode="html"
        )
    await Assistant.send_message(config.EVENT_LOGS, "**ɪ ᴀᴍ ʀᴇᴀᴅʏ ғᴏʀ ᴘʟᴀʏ ᴛʀᴀᴄᴋs ʙᴀʙʏ!**")  
    print("BOT RUNNING.. ")
    from AlishanBot.modules.helper_funcs.queue import update_bar
    create_task(update_bar())
    await Alishan.run_until_disconnected()
    
def import_modules():
    path = "AlishanBot/modules"
    for file in os.listdir(path):
        if file.endswith(".py") and not file.startswith("__"):
            importlib.import_module(f"AlishanBot.modules.{file[:-3]}")
            
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
