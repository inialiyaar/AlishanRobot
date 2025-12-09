from AlishanBot.modules.helper_funcs.queue import queue_position, current_ind, queues
from AlishanBot.core.bot import Alishan, music
from AlishanBot.__init__ import player_stats, BOT_MENTION, update_time
from AlishanBot.core.decorators import add_command, callback_query
from AlishanBot.modules.helper_funcs.play import Play_Stream
from AlishanBot.modules.helper_funcs.helpers import is_admin
from AlishanBot.utils.database import stream_mode


@callback_query("seek_forward")
async def forward_handler(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id) 
    user = await event.get_sender()
    settings = stream_mode.find_one({"chat_id": chat_id})
    if settings:
        admin_cmd = settings.get("admin_cmd", "admins")
    else:
        admin_cmd = "admins"  
    if not await is_admin(user, event) and admin_cmd == "admins":
        await event.answer("You must be an admin to use this.", alert=True)
        return
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id) 
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "Anonymous" 
    if chat_id in player_stats:
        player_stats[chat_id]["is_playing"] = True
        update_time(chat_id)
        index = current_ind.get(chat_id, 0)
        player_stats[chat_id]["current_time"] += 20
        if player_stats[chat_id]["current_time"] > player_stats[chat_id]["duration"]:
            player_stats[chat_id]["current_time"] = player_stats[chat_id]["duration"]
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        seek = player_stats[chat_id]["current_time"]
        play_mode = player_stats[chat_id]["play_mode"]
        await Play_Stream(chat_id, stream_url, query_format, play_mode, seek)
        await event.reply(f"{mention} seek the track 20s forward.", parse_mode="html")
    else:
        await event.reply(f"» {BOT_MENTION} isn't streaming on Voicechat.", parse_mode="html")       

@callback_query("seek_backward")
async def backward_handler(event):
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
        player_stats[chat_id]["is_playing"] = True
        update_time(chat_id)
        index = current_ind.get(chat_id, 0)
        player_stats[chat_id]["current_time"] -= 20
        if player_stats[chat_id]["current_time"] < 0:
            player_stats[chat_id]["current_time"] = 0
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        seek = player_stats[chat_id]["current_time"]
        play_mode = player_stats[chat_id]["play_mode"]
        await Play_Stream(chat_id, stream_url, query_format, play_mode, seek)
        await event.reply(f"{mention} seek the track 20s backward.", parse_mode="html")
    else:
        await event.reply(f"» {BOT_MENTION} isn't streaming on Voicechat.", parse_mode="html")       
@add_command("seek")
async def seek_handler(event, command, args):
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
    if not args:
        return await event.reply("Please give a time like 1m, -20s, 120")
    try:
        seconds = int(args)
    except:
        return await event.reply("Invalid time! Use 60 / 100 / -20 / -200")
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "Anonymous" 
    if chat_id not in player_stats:
        return await event.reply(f"» {BOT_MENTION} isn't streaming on Voicechat.", parse_mode="html")

    update_time(chat_id)
    player_stats[chat_id]["current_time"]
    if seconds < 0:
        player_stats[chat_id]["current_time"] -= abs(seconds)
        direction = "backward"
    else:
        player_stats[chat_id]["current_time"] += seconds
        direction = "forward"
    seek = player_stats[chat_id]["current_time"]
    index = current_ind.get(chat_id, 0)
    stream_url, title, artist, duration, thumbnail, mention, q_format, dl = queues[chat_id][index]    
    if seek < 0: 
        return await event.reply(f"You can't seek beyond 0:00\nTrack length {duration}s")
    if seek > duration:
        return await event.reply(f"You can't seek beyond the track\nTrack length {duration}s")
    play_mode = player_stats[chat_id]["play_mode"]
    await Play_Stream(chat_id, stream_url, q_format, play_mode, seek)

    return await event.reply(
        f"Seeked {int(seconds)} {direction}.\n"
        f"Seeked by: {mention}",
        parse_mode="html"
    )
    