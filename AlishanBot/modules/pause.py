from AlishanBot.core.bot import Alishan, music
from AlishanBot.modules.helper_funcs.queue import queues
from AlishanBot.__init__ import player_stats, BOT_MENTION, update_time
from AlishanBot.core.decorators import add_command, callback_query
from AlishanBot.modules.helper_funcs.helpers import is_admin
import time
from AlishanBot.utils.database import stream_mode


@add_command("pause", "resume")
async def command_handler(event, command_used, args):
    if event.is_group or event.is_channel:
        user = await event.get_sender()
        chat = await event.get_chat()
        chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
        settings = stream_mode.find_one({"chat_id": chat_id})
        if settings:
            admin_cmd = settings.get("admin_cmd", "admins")
        else:
            admin_cmd = "admins"  
        if not await is_admin(user, event) and admin_cmd == "admins":
            await event.reply("You must be an admin to use this.")
            return
        try:
            await event.delete()
            if command_used == "pause":
                await pause(event)
            else:
                await resume(event) 
        except Exception:
            pass
    else:
        await event.reply("You can use in groups only!.")
    

@callback_query("pause")
async def pause_callback(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    settings = stream_mode.find_one({"chat_id": chat_id})
    if settings:
        admin_cmd = settings.get("admin_cmd", "admins")
    else:
        admin_cmd = "admins"  
    if not await is_admin(user, event) and admin_cmd == "admins":
        await event.answer("You must be an admin to use this.", alert=True)
        return
    await pause(event)
    

async def pause(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    user = await event.get_sender()
    if chat_id in queues and len(queues[chat_id]) > 0:
        try:
            mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
        except Exception:
            mention = "Anonymous"

        if player_stats[chat_id]["is_playing"]:
            await music.pause(chat_id)
            update_time(chat_id)
            player_stats[chat_id]["is_playing"] = False
            await event.reply(f"<b>➭ Stream paused. \nPaused by:</b> {mention}", parse_mode="html")
        else:
            await event.reply(f"<b>➭ Stream already paused.</b> {mention}", parse_mode="html")
    else:
        await event.reply(f"» {BOT_MENTION} isn't streaming on Voicechat.", parse_mode="html")

    

@callback_query("resume")
async def resume_callback(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    settings = stream_mode.find_one({"chat_id": chat_id})
    if settings:
        admin_cmd = settings.get("admin_cmd", "admins")
    else:
        admin_cmd = "admins"  
    if not await is_admin(user, event) and admin_cmd == "admins":
        await event.answer("You must be an admin to use this.", alert=True)
        return
    await resume(event)
    

async def resume(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    user = await event.get_sender()
    if chat_id in queues and len(queues[chat_id]) > 0:
        try:
            mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
        except Exception:
            mention = "Anonymous"
        if not player_stats[chat_id]["is_playing"]:
            await music.resume(chat_id)
            player_stats[chat_id]["is_playing"] = True
            player_stats[chat_id]["last_update"] = time.time()
            await event.reply(f"<b>➭ Stream resumed. \nResumed by:</b> {mention}", parse_mode="html")
        else:
            await event.reply(f"<b>➭ Stream already resumed.</b> {mention}", parse_mode="html")
    else:
        await event.reply(f"» {BOT_MENTION} isn't streaming on Voicechat.", parse_mode="html")
        