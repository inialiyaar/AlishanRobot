from AlishanBot.modules.helper_funcs.queue import queue_position, current_ind, queues
from AlishanBot.core.bot import Alishan, music
from AlishanBot.__init__ import player_stats, BOT_MENTION, update_time
from AlishanBot.core.decorators import add_command, callback_query
from AlishanBot.modules.helper_funcs.play import Play_Stream
from AlishanBot.modules.helper_funcs.helpers import is_admin
from telethon import Button
from AlishanBot.utils.database import stream_mode

@callback_query("modes")
async def PlayModes_Callback(event):
    buttons = [
        Button.inline("ʟᴏғɪ", data="instent_lofi"), 
        Button.inline("ɴᴏʀᴍᴀʟ", "instent_normal"), 
        Button.inline("ᴇᴄᴏ", "instent_eco")
    ]
    await event.edit(buttons=buttons)

@callback_query("instent_lofi")
async def instent_lofi_handler_callback(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    settings = stream_mode.find_one({"chat_id": chat_id})
    admin_cmd = settings.get("admin_cmd", "admins")
    if not await is_admin(user, event) and admin_cmd == "admins":
        await event.answer("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.", alert=True)
        return
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "ᴀɴᴏɴʏᴍᴏᴜs"    
    if chat_id in player_stats:
        play_mode = player_stats[chat_id]["play_mode"]
        if play_mode != "lofi":
            play_mode = "lofi"
        else:
            return await event.answer("ʟᴏғɪ ᴍᴏᴅᴇ ᴀʟʀᴇᴀᴅʏ ᴀᴄᴛɪᴠᴀᴛᴇᴅ. ", alert=True)
        index = current_ind.get(chat_id, 0)
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        player_stats[chat_id]["is_playing"] = True    
        update_time(chat_id)
        seek = player_stats[chat_id]["current_time"]
        await Play_Stream(chat_id, stream_url, query_format, play_mode, seek)
        player_stats[chat_id]["play_mode"] = "lofi"
        await event.reply(f"{mention} ᴛᴜʀɴᴇᴅ ᴏɴ ᴛʜᴇ ʟᴏғɪ ᴍᴏᴅᴇ. ", parse_mode="html")
    else:
        await event.answer(f"» {BOT_FULLNAME} ɪsɴ'ᴛ 𝖲ᴛʀᴇᴀᴍɪɴɢ ᴏɴ 𝖵ᴏɪᴄᴇᴄʜᴀᴛ.", parse_mode="html", alert=true)   
        
@callback_query("instent_eco")
async def instent_eco_handler_callback(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    settings = stream_mode.find_one({"chat_id": chat_id})
    admin_cmd = settings.get("admin_cmd", "admins")
    if not await is_admin(user, event) and admin_cmd == "admins":
        await event.answer("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.", alert=True)
        return
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "ᴀɴᴏɴʏᴍᴏᴜs"    
    if chat_id in player_stats:
        play_mode = player_stats[chat_id]["play_mode"]
        if play_mode != "eco":
            play_mode = "eco"
        else:
            return await event.answer("ᴇᴄᴏ ᴍᴏᴅᴇ ᴀʟʀᴇᴀᴅʏ ᴀᴄᴛɪᴠᴀᴛᴇᴅ. ", alert=True)
        index = current_ind.get(chat_id, 0)
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        player_stats[chat_id]["is_playing"] = True    
        update_time(chat_id)
        seek = player_stats[chat_id]["current_time"]
        await Play_Stream(chat_id, stream_url, query_format, play_mode, seek)
        player_stats[chat_id]["play_mode"] = "eco"
        await event.reply(f"{mention} ᴛᴜʀɴᴇᴅ ᴏɴ ᴛʜᴇ ᴇᴄᴏ ᴍᴏᴅᴇ. ", parse_mode="html")
    else:
        await event.answer(f"» {BOT_FULLNAME} ɪsɴ'ᴛ 𝖲ᴛʀᴇᴀᴍɪɴɢ ᴏɴ 𝖵ᴏɪᴄᴇᴄʜᴀᴛ.", parse_mode="html", alert=true)        
        
@callback_query("instent_normal")
async def instent_normal_handler_callback(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    settings = stream_mode.find_one({"chat_id": chat_id})
    admin_cmd = settings.get("admin_cmd", "admins")
    if not await is_admin(user, event) and admin_cmd == "admins":
        await event.answer("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.", alert=True)
        return
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "ᴀɴᴏɴʏᴍᴏᴜs"    
    if chat_id in player_stats:
        play_mode = player_stats[chat_id]["play_mode"]
        if play_mode != "normal":
            play_mode = "normal"
        else:
            return await event.answer("ɴᴏʀᴍᴀʟ ᴍᴏᴅᴇ ᴀʟʀᴇᴀᴅʏ ᴀᴄᴛɪᴠᴀᴛᴇᴅ. ", alert=True)
        index = current_ind.get(chat_id, 0)
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        player_stats[chat_id]["is_playing"] = True    
        update_time(chat_id)
        seek = player_stats[chat_id]["current_time"]
        await Play_Stream(chat_id, stream_url, query_format, play_mode, seek)
        player_stats[chat_id]["play_mode"] = "normal"
        await event.reply(f"{mention} ᴛᴜʀɴᴇᴅ ᴏɴ ᴛʜᴇ ɴᴏʀᴍᴀʟ ᴍᴏᴅᴇ. ", parse_mode="html")
    else:
        await event.answer(f"» {BOT_FULLNAME} ɪsɴ'ᴛ 𝖲ᴛʀᴇᴀᴍɪɴɢ ᴏɴ 𝖵ᴏɪᴄᴇᴄʜᴀᴛ.", parse_mode="html", alert=true)                   