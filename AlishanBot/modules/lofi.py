from AlishanBot.modules.helper_funcs.queue import queue_position, current_ind, queues
from AlishanBot.core.bot import Alishan, music
from AlishanBot.__init__ import is_playing, BOT_MENTION, playing_lofi
from AlishanBot.core.decorators import add_command, callback_query
from AlishanBot.modules.helper_funcs.play import Play_Audio, Play_Video
from AlishanBot.modules.helper_funcs.helpers import is_admin


@callback_query("instent_lofi")
async def instent_lofi_handler_callback(event):
    user = await event.get_sender()
    if not await is_admin(user, event):
        await event.answer("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.", alert=True)
        return
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id) 
    if chat_id in playing_lofi:
        seek = True
        eco=False
        playing_lofi.pop(chat_id, None)
    else:
        seek=False
        eco=True 
        playing_lofi[chat_id] = True
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "ᴀɴᴏɴʏᴍᴏᴜs"    
    if chat_id in is_playing:
        is_playing[chat_id] = True
        index = current_ind.get(chat_id, 0)
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        if query_format == "video":
            await Play_Video(chat_id, stream_url, eco, seek)
        else:
            await Play_Audio(chat_id, stream_url, eco, seek)
        if eco:
            await event.reply(f"{mention} ᴛᴜʀɴᴇᴅ ᴏɴ ᴛʜᴇ ʟᴏғʏ ᴍᴏᴅᴇ. ", parse_mode="html")
        else:
            await event.reply(f"{mention} ᴛᴜʀɴᴇᴅ ᴏғ ᴛʜᴇ ʟᴏғɪ ᴍᴏᴅᴇ.", parse_mode="html")
    else:
        await event.reply(f"» {BOT_MENTION} ɪsɴ'ᴛ 𝖲ᴛʀᴇᴀᴍɪɴɢ ᴏɴ 𝖵ᴏɪᴄᴇᴄʜᴀᴛ.", parse_mode="html")   