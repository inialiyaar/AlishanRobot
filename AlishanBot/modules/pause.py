from AlishanBot.core.bot import Alishan, music
from AlishanBot.modules.helper_funcs.queue import queues
from AlishanBot.__init__ import is_playing, BOT_MENTION
from AlishanBot.core.decorators import add_command, callback_query


@add_command("pause", "resume")
async def command_handler(event, command_used, args):
    if event.is_group or event.is_channel:
        user = await event.get_sender()
        chat = await event.get_chat()
        chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
        rights = await Alishan.get_permissions(chat.id, user.id)
        if not rights.is_admin:
            await event.reply("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.")
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
        await event.reply("𝖸ᴏᴜ ᴄᴀɴ ᴜsᴇ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ!.")
    

@callback_query("pause")
async def pause_callback(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
    rights = await Alishan.get_permissions(chat.id, user.id)
    if not rights.is_admin:
        await event.answer("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.", alert=True)
        return
    await pause(event)
    

async def pause(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
    user = await event.get_sender()
    if chat_id in queues and len(queues[chat_id]) > 0:
        try:
            mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
        except Exception:
            mention = "ᴀɴᴏɴʏᴍᴏᴜs"

        if is_playing.get(chat_id, True):
            await music.pause(chat_id)
            is_playing[chat_id] = False
            await event.reply(f"<b>➭ sᴛʀᴇᴀᴍ ᴘᴀᴜsᴇᴅ. \nᴘᴀᴜsᴇᴅ ʙʏ :</b> {mention}", parse_mode="html")
        else:
            await event.reply(f"<b>➭ sᴛʀᴇᴀᴍ ᴀʟʀᴇᴀᴅʏ ᴘᴀᴜsᴇᴅ.</b> {mention}", parse_mode="html")
    else:
        await event.reply(f"» {BOT_MENTION} ɪsɴ'ᴛ 𝖲ᴛʀᴇᴀᴍɪɴɢ ᴏɴ 𝖵ᴏɪᴄᴇᴄʜᴀᴛ.")

    

@callback_query("resume")
async def resume_callback(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
    rights = await Alishan.get_permissions(chat.id, user.id)
    if not rights.is_admin:
        await event.answer("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.", alert=True)
        return
    await resume(event)
    

async def resume(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
    user = await event.get_sender()
    if chat_id in queues and len(queues[chat_id]) > 0:
        try:
            mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
        except Exception:
            mention = "ᴀɴᴏɴʏᴍᴏᴜs"
        if not is_playing.get(chat_id, True):
            await music.resume(chat_id)
            is_playing[chat_id] = True
            await event.reply(f"<b>➭ sᴛʀᴇᴀᴍ ʀᴇsᴜᴍᴇᴅ. \nʀᴇsᴜᴍᴇᴅ ʙʏ :</b> {mention}", parse_mode="html")
        else:
            await event.reply(f"<b>➭ sᴛʀᴇᴀᴍ ᴀʟʀᴇᴀᴅʏ ʀᴇsᴜᴍᴇᴅ.</b> {mention}", parse_mode="html")
    else:
        await event.reply(f"» {BOT_MENTION} ɪsɴ'ᴛ 𝖲ᴛʀᴇᴀᴍɪɴɢ ᴏɴ 𝖵ᴏɪᴄᴇᴄʜᴀᴛ.")