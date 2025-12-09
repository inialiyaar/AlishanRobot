from AlishanBot.modules.helper_funcs.queue import queue_position, current_ind, queues
from AlishanBot.core.bot import Alishan, music
from AlishanBot.__init__ import player_stats, BOT_MENTION, update_time
from AlishanBot.core.decorators import add_command, callback_query
from AlishanBot.modules.helper_funcs.play import Play_Stream
from AlishanBot.modules.helper_funcs.helpers import is_admin
from telethon import Button
from AlishanBot.utils.database import stream_mode
from asyncio import sleep

@callback_query("modes")
async def PlayModes_Callback(event):
    buttons = [
        Button.inline("Lofi", data="instent_lofi"), 
        Button.inline("Normal", "instent_normal"), 
        Button.inline("Eco", "instent_eco")
    ]
    try:
        await event.edit(buttons=buttons)
    except:
        await sleep(2)
        try:
            await event.edit(buttons=buttons)
        except:    
            pass   
        
@callback_query("instent_lofi")
async def instent_lofi_handler_callback(event):
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
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "Anonymous"    
    if chat_id in player_stats:
        play_mode = player_stats[chat_id]["play_mode"]
        if play_mode != "lofi":
            play_mode = "lofi"
        else:
            return await event.answer("Lofi mode already activated.", alert=True)
        index = current_ind.get(chat_id, 0)
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        player_stats[chat_id]["is_playing"] = True    
        update_time(chat_id)
        seek = player_stats[chat_id]["current_time"]
        await Play_Stream(chat_id, stream_url, query_format, play_mode, seek)
        player_stats[chat_id]["play_mode"] = "lofi"
        await event.reply(f"{mention} turned on the Lofi mode.", parse_mode="html")
    else:
        await event.answer(f"» {BOT_MENTION} isn't streaming on Voicechat.", parse_mode="html", alert=True)   
        
@callback_query("instent_eco")
async def instent_eco_handler_callback(event):
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
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "Anonymous"    
    if chat_id in player_stats:
        play_mode = player_stats[chat_id]["play_mode"]
        if play_mode != "eco":
            play_mode = "eco"
        else:
            return await event.answer("Eco mode already activated.", alert=True)
        index = current_ind.get(chat_id, 0)
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        player_stats[chat_id]["is_playing"] = True    
        update_time(chat_id)
        seek = player_stats[chat_id]["current_time"]
        await Play_Stream(chat_id, stream_url, query_format, play_mode, seek)
        player_stats[chat_id]["play_mode"] = "eco"
        await event.reply(f"{mention} turned on the Eco mode.", parse_mode="html")
    else:
        await event.answer(f"» {BOT_MENTION} isn't streaming on Voicechat.", parse_mode="html", alert=True)        
        
@callback_query("instent_normal")
async def instent_normal_handler_callback(event):
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
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "Anonymous"    
    if chat_id in player_stats:
        play_mode = player_stats[chat_id]["play_mode"]
        if play_mode != "normal":
            play_mode = "normal"
        else:
            return await event.answer("Normal mode already activated.", alert=True)
        index = current_ind.get(chat_id, 0)
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        player_stats[chat_id]["is_playing"] = True    
        update_time(chat_id)
        seek = player_stats[chat_id]["current_time"]
        await Play_Stream(chat_id, stream_url, query_format, play_mode, seek)
        player_stats[chat_id]["play_mode"] = "normal"
        await event.reply(f"{mention} turned on the Normal mode.", parse_mode="html")
    else:
        await event.answer(f"» {BOT_MENTION} isn't streaming on Voicechat.", parse_mode="html", alert=True)
        