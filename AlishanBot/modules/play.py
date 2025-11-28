from AlishanBot.core.bot import Alishan, Assistant
from AlishanBot.modules.helper_funcs.queue import add_to_queue
from AlishanBot.core.decorators import add_command
from AlishanBot.modules.helper_funcs.helpers import check_rights, is_admin
from AlishanBot.__init__ import BOT_MENTION, BOT_ID, ASSISTANT_MENTION, ASSISTANT_ID, player_stats
from AlishanBot.modules.helper_funcs.ErrorLog import send_error
from AlishanBot import config
from telethon.tl.functions.messages import ExportChatInviteRequest, ImportChatInviteRequest
from telethon.tl.functions.channels import GetParticipantRequest, EditBannedRequest, GetFullChannelRequest
from telethon.errors import UserNotParticipantError, ChatAdminRequiredError
from telethon.tl.types import ChannelParticipantBanned, ChatBannedRights
from AlishanBot.utils.database import stream_mode

from asyncio import create_task
from re import search
import traceback

UNBAN_RIGHTS = ChatBannedRights(until_date=None, view_messages=False)
EVENT_LOGS = config.EVENT_LOGS

@add_command("vplay", "play", "playforce", "vplayforce")
async def Play_Handler(event, command_used, song_name):

    force_play = command_used in ["playforce", "vplayforce"]
    query_format = "video" if command_used in ["vplay", "vplayforce"] else "audio"

    try: await event.delete()
    except: pass

    if event.is_private:
        return await event.reply("𝖸ᴏᴜ ᴄᴀɴ ᴜsᴇ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ!.")

    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)

    full_channel = await Alishan(GetFullChannelRequest(chat_id))
    if not full_channel.full_chat.call:
        return await event.reply("**𝖵ᴏɪᴄᴇ ᴄʜᴀᴛ ɪs ɴᴏᴛ ᴀᴄᴛɪᴠᴇ,** ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ᴛʜᴇ ᴠᴄ ғɪʀsᴛ!")
    if not force_play and chat_id in player_stats:
        create_task(Play(event, song_name, query_format, chat_id, False))
        return

    await Play(event, song_name, query_format, chat_id, False, force_play=force_play)



async def Play(event, song_name, query_format, chat_id, download, force_play=False):

    user = await event.get_sender()
    
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except:
        mention = "ᴀɴᴏɴʏᴍᴏᴜs"
    settings = stream_mode.find_one({"chat_id": chat_id})
    if settings:
        vote_mode = settings.get("vote_mode", 5)
        play_mode = settings.get("play_mode", "normal")
        admin_cmd = settings.get("admin_cmd", "admins")
        can_play = settings.get("can_play", "everyone")
    else:
        vote_mode = 5
        play_mode = "normal"
        admin_cmd = "admins"
        can_play = "everyone"
    if force_play and not await is_admin(user, event) and admin_cmd == "admins":
        return await event.reply(
            f"{mention} ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ, ᴏɴʟʏ ᴀᴅᴍɪɴ ᴄᴀɴ ғᴏʀᴄᴇ ᴘʟᴀʏ. ",
            parse_mode="html"
        )

    if event.is_reply and not song_name:
        reply = await event.get_reply_message()
        if reply.audio or reply.video:
            processing = await event.respond("**𝖯ʀᴏᴄᴇssɪɴɢ...💫**")
            download = True
        else:
            download = False    

        if reply.audio and query_format == "audio":
            song_name = await reply.download_media(file="downloads/local_download.mp3")

        elif reply.video and query_format == "video":
            song_name = await reply.download_media(file="downloads/local_download.mp4")

        elif reply.text:
            song_name = reply.raw_text

        else:
            await processing.delete()
            return await event.reply(
                "𝖯ʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ **𝖠ᴜᴅɪᴏ/𝖵ɪᴅᴇᴏ** ᴏʀ ɢɪᴠᴇ 𝖲ᴏɴɢ 𝖭ᴀᴍᴇ ᴀɴᴅ 𝖸ᴏᴜᴛᴜʙᴇ 𝖴ʀʟ."
            )
        if reply.audio or reply.video:
            await processing.delete()

    elif not song_name:
        return await event.reply(
            "𝖯ʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ **𝖲ᴏɴɢ 𝖭ᴀᴍᴇ** ᴏʀ **𝖸ᴏᴜᴛᴜʙᴇ 𝖴ʀʟ** ᴀғᴛᴇʀ /play"
        )

    bot = await Alishan.get_me()
    assistant = await Assistant.get_me()

    if not await is_admin(bot, event):
        return await event.reply(
            f"{BOT_MENTION} ɪs ɴᴏᴛ ᴀᴅᴍɪɴ, 𝖯ʟᴇᴀsᴇ ɢɪʙᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ <b>(ᴄʀᴇᴀᴛᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ)</b>.",
            parse_mode="html"
        )

    if chat_id in player_stats:
        await add_to_queue(song_name, chat_id, query_format, mention, download, force_play)
        create_task(Play_Log(song_name, chat_id, query_format, mention, download, force_play))
        return

    try:
        part = await Alishan(GetParticipantRequest(chat_id, assistant.id))
        if isinstance(part.participant, ChannelParticipantBanned):
            if not await check_rights(event, BOT_ID, "ban_users"):
                return await event.reply(
                    f"{BOT_MENTION} ʜᴀs ɴᴏ ᴀᴄᴄᴇss ᴛᴏ ᴜɴʙᴀɴ {ASSISTANT_MENTION}.",
                    parse_mode="html"
                )
            await Alishan(EditBannedRequest(chat_id, assistant.id, UNBAN_RIGHTS))
            await _invite_assistant(chat_id)
            await add_to_queue(song_name, chat_id, query_format, mention, download, force_play)
            create_task(Play_Log(song_name, chat_id, query_format, mention, download, force_play))
            return

        await add_to_queue(song_name, chat_id, query_format, mention, download, force_play)
        create_task(Play_Log(song_name, chat_id, query_format, mention, download, force_play))
        return

    except UserNotParticipantError:
        await _invite_assistant(chat_id)
        await add_to_queue(song_name, chat_id, query_format, mention, download, force_play)
        create_task(Play_Log(song_name, chat_id, query_format, mention, download, force_play))
        return
        

    except ChatAdminRequiredError:
        return await event.reply(
            f"{BOT_MENTION} ʜᴀs ɴᴏ ᴀᴄᴄᴇss ᴛᴏ ᴄʜᴇᴄᴋ {ASSISTANT_MENTION}. ᴘʟᴇᴀsᴇ ɢɪʙᴇ (ᴄʀᴇᴀᴛᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ)",
            parse_mode="html"
        )

    except Exception:
        error = traceback.format_exc()
        await send_error(error)
        return await event.reply(
            f"{BOT_MENTION} ᴄᴀɴɴᴏᴛ ᴄʜᴇᴄᴋ ᴀssɪsᴛᴀɴᴛ. ᴘʟᴇᴀsᴇ ᴍᴀᴋᴇ ɢʀᴏᴜᴘ ʜɪsᴛᴏʀʏ ᴠɪsɪʙʟᴇ.",
            parse_mode="html"
        )


async def _invite_assistant(chat_id):
    export = await Alishan(ExportChatInviteRequest(chat_id))
    code = search(r"(?:joinchat/|\+)([a-zA-Z0-9_-]+)", export.link).group(1)
    await Assistant(ImportChatInviteRequest(code))
    await Assistant.send_message(chat_id, f"{ASSISTANT_MENTION} 𝖩ᴏɪɴᴇᴅ ᴛʜᴇ ɢʀᴏᴜᴘ! 𝖨 ᴀᴍ ᴄᴏᴍᴍɪɴɢ ɪɴ <b>𝖵ᴏɪᴄᴇ 𝖢ʜᴀᴛ</b>", parse_mode="html")


async def Play_Log(song_name, chat_id, query_format, mention, download, force_play):
    if force_play:
        playforce = "ᴛʀᴜᴇ"
    else:
        playforce = "ғᴀʟsᴇ"   
    if download:
        download = "ᴛʀᴜᴇ" 
    else:
        download = "ғᴀʟsᴇ"   
    text = f"#PLAYLOG\nɴᴇᴡ ǫᴜᴇʀʏ ʜᴀs ᴀʀʀɪᴠᴇᴅ!\n\nǫᴜᴇʀʏ : {song_name}\nғᴏʀᴍᴀᴛ : {query_format}\nғᴏʀᴄᴇ ᴘʟᴀʏ : {playforce}\nᴅᴏᴡɴʟᴏᴀᴅ : {download}\nǫᴜᴇʀʏ ʙʏ : {mention}"
    
    await Alishan.send_message(EVENT_LOGS, text, parse_mode="html")