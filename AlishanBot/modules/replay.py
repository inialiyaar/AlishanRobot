from AlishanBot.core.bot import Alishan
from AlishanBot.modules.helper_funcs.play import Play_Stream
from AlishanBot.core.decorators import add_command, callback_query
from AlishanBot.modules.helper_funcs.helpers import is_admin
from AlishanBot.__init__ import player_stats
from AlishanBot.modules.helper_funcs.queue import queues, current_ind, playing_message
from asyncio import create_task
from AlishanBot.utils.database import stream_mode
import time

@add_command("replay")
async def replay_handler(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
    settings = stream_mode.find_one({"chat_id": chat_id})
    admin_cmd = settings.get("admin_cmd", "admins")
    if not await is_admin(user, event) and admin_cmd == "admins":
        await event.answer("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.", alert=True)
        return
    try:
        await event.delete()
    except:
        pass    
    if event.is_group or event.is_channel:
    	await replay(event)
    else:
        await event.reply("𝖸ᴏᴜ ᴄᴀɴ ᴜsᴇ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ!.")
    
@callback_query("replay")
async def replay_callback(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    rights = await Alishan.get_permissions(chat.id, user.id)
    
    settings = stream_mode.find_one({"chat_id": chat_id})
    admin_cmd = settings.get("admin_cmd", "admins")
    if not await is_admin(user, event) and admin_cmd == "admins":
        await event.answer("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.", alert=True)
        return
    if event.is_group or event.is_channel:
    	await replay(event)
    else:
        await event.reply("𝖸ᴏᴜ ᴄᴀɴ ᴜsᴇ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ!.")
        
async def replay(event):
    user = await event.get_sender()
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "ᴀɴᴏɴʏᴍᴏᴜs"
    chat = await event.get_chat()
    
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    if chat_id in player_stats:
        status = await event.reply("**𝖱ᴇᴘʟᴀʏɪɴɢ ᴄᴜʀʀᴇɴᴛ 𝖳ʀᴀᴄᴋ...**")
        index = current_ind.get(chat_id, 0)
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        settings = stream_mode.find_one({"chat_id": chat_id})
        if settings:
            play_mode = settings.get("play_mode", "normal")
        else:
            play_mode = "normal"
        await Play_Stream(chat_id, stream_url, query_format, play_mode)
        create_task(playing_message(title, artist, duration, query_format, thumbnail, chat_id, mention, download)) 
        player_stats[chat_id]["is_playing"] = True
        player_stats[chat_id]["current_time"] = 0
        player_stats[chat_id]["last_update"] = time.time()
        player_stats[chat_id]["play_mode"] = play_mode        
        try:
            await status.edit(f"<b>➭ 𝖳ʀᴀᴄᴋ ʀᴇᴘʟᴀʏ 𝖲ᴛᴀʀᴛᴇᴅ!\n\n𝖱ᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {mention}", parse_mode="html")
        except Exception:
            await event.reply(f"<b>➭ 𝖳ʀᴀᴄᴋ ʀᴇᴘʟᴀʏ 𝖲ᴛᴀʀᴛᴇᴅ! \n\n𝖱ᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {mention}", parse_mode="html")
    else:
        await event.reply(f"» {BOT_MENTION} ɪsɴ'ᴛ 𝖲ᴛʀᴇᴀᴍɪɴɢ ᴏɴ 𝖵ᴏɪᴄᴇᴄʜᴀᴛ.", parse_mode="html")        