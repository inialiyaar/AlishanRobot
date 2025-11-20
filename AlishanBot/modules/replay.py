from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command, callback_query
from AlishanBot.modules.helper_funcs.queue import replay
from AlishanBot.modules.helper_funcs.helpers import is_admin
from AlishanBot.__init__ is_playing, playing_lofi
from AlishanBot.modules.helper_funcs.queue import queues, current_ind

@add_command("replay")
async def replay_handler(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    if not await is_admin(user, event):
        await event.reply("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.")
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
    if not await is_admin(user, event):
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
    if chat_id in queues and queues[chat_id]:
        if chat_id in playing_lofi:
            playing_lofi.pop(chat_id, None)
        try:
            await music.mute(chat_id)
        except:
            pass     
        status = await event.reply("**𝖱ᴇᴘʟᴀʏɪɴɢ ᴄᴜʀʀᴇɴᴛ 𝖳ʀᴀᴄᴋ...**")
        index = current_ind.get(chat_id, 0)
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        try:
            if query_format == "video":
                await Play_Video(chat_id, stream_url)
            else:
                await Play_Audio(chat_id, stream_url)
            if chat_id in active_bars:
                active_bars[chat_id]["active"] = False    
            create_task(playing_message(title, artist, duration, query_format, thumbnail, chat_id, mention, download)) 
            is_playing[chat_id] = True
            try:
                await status.edit(f"<b>➭ 𝖳ʀᴀᴄᴋ ʀᴇᴘʟᴀʏ 𝖲ᴛᴀʀᴛᴇᴅ!\n\n𝖱ᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {mention}", parse_mode="html")
            except Exception:
                await event.reply(f"<b>➭ 𝖳ʀᴀᴄᴋ ʀᴇᴘʟᴀʏ 𝖲ᴛᴀʀᴛᴇᴅ! \n\n𝖱ᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {mention}", parse_mode="html")
        except Exception as e:
            await status.edit(f"Replay failed: {str(e)}")
    else:
        await event.reply(f"» {BOT_MENTION} ɪsɴ'ᴛ 𝖲ᴛʀᴇᴀᴍɪɴɢ ᴏɴ 𝖵ᴏɪᴄᴇᴄʜᴀᴛ.", parse_mode="html")        