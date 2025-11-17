from AlishanBot.core.bot import Alishan, Assistant
from AlishanBot.modules.helper_funcs.queue import add_to_queue
from AlishanBot.core.decorators import add_command
from AlishanBot.modules.helper_funcs.helpers import check_rights, is_admin
from AlishanBot.__init__ import BOT_MENTION, BOT_ID, ASSISTANT_MENTION,ASSISTANT_ID, is_playing
from AlishanBot.modules.helper_funcs.ErrorLog import send_error
from telethon.tl.functions.messages import ExportChatInviteRequest, ImportChatInviteRequest
from telethon.tl.functions.channels import GetParticipantRequest, EditBannedRequest, GetFullChannelRequest
from telethon.errors import UserNotParticipantError, ChatAdminRequiredError
from telethon.tl.types import ChannelParticipantBanned, ChatBannedRights
import traceback
from asyncio import create_task
from re import search

UNBAN_RIGHTS = ChatBannedRights(until_date=None, view_messages=False)

@add_command("vplay", "play", "playforce", "vplayforce")
async def Play_Handler(event, command_used, song_name):
    force_play = False
    if command_used in ["vplay", "vplayforce"]:
        query_format = "video"
    else:
        query_format = "audio"  
    download = False
    if command_used in ["playforce", "vplayforce"]:
        force_play = True
    try:
        await event.delete()
    except:
        pass
    if event.is_private:
        return await event.reply("𝖸ᴏᴜ ᴄᴀɴ ᴜsᴇ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ!.")
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)    
    full_channel = await Alishan(GetFullChannelRequest(chat_id))
    call = full_channel.full_chat.call
    if not call:
        return await event.reply("**𝖵ᴏɪᴄᴇ ᴄʜᴀᴛ ɪs ɴᴏᴛ ᴀᴄᴛɪᴠᴇ,** ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ᴛʜᴇ ᴠᴄ ғɪʀsᴛ!")    
    if force_play:
        await Play(event, song_name, query_format, chat_id, download, force_play) 
    elif not chat_id in is_playing:
        await Play(event, song_name, query_format, chat_id, download, force_play) 
    else:
        create_task(Play(event, song_name, query_format, chat_id, download)) 
    
    
async def Play(event, song_name, query_format, chat_id, download, force_play=False):
    user = await event.get_sender()
    chat = await event.get_chat()
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "ᴀɴᴏɴʏᴍᴏᴜs"
    if force_play: 
        if not await is_admin(user, event):
            return await event.reply(f"{mention} ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ, ᴏɴʟʏ ᴀᴅᴍɪɴ ᴄᴀɴ ғᴏʀᴄᴇ ᴘʟᴀʏ. ", parse_mode="html")        
    if event.is_reply and not song_name:
        download = True
        reply = await event.get_reply_message()
        promsg = await event.respond("**𝖯ʀᴏᴄᴇssɪɴɢ...💫**")
        if reply.video and query_format == "video":
            song_name = await reply.download_media(file="downloads/local_download.mp4")
            
        elif reply.video and query_format == "audio":
            return await promsg.edit("𝖯ʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ **𝖠ᴜᴅɪᴏ** ᴏʀ ɢɪᴠᴇ ᴍᴇ **𝖲ᴏɴɢ 𝖭ᴀᴍᴇ ᴀɴᴅ 𝖸ᴏᴜᴛᴜʙᴇ 𝖴ʀʟ**. ᴀғᴛᴇʀ /play")
            
        elif reply.audio and query_format == "audio":
            song_name = await reply.download_media(file="downloads/local_download.mp3")
        elif reply.audio and query_format == "video":
            return await promsg.edit("𝖯ʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ **𝖵ɪᴅᴇᴏ** ᴏʀ ɢɪᴠᴇ ᴍᴇ **𝖲ᴏɴɢ 𝖭ᴀᴍᴇ ᴀɴᴅ 𝖸ᴏᴜᴛᴜʙᴇ 𝖴ʀʟ**. ᴀғᴛᴇʀ /vplay")
        else:
            if query_format == "video":
                return await promsg.edit("𝖯ʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ **𝖠ᴜᴅɪᴏ ᴀɴᴅ 𝖵ɪᴅᴇᴏ** ᴏʀ ɢɪᴠᴇ ᴍᴇ **𝖲ᴏɴɢ 𝖭ᴀᴍᴇ ᴀɴᴅ 𝖸ᴏᴜᴛᴜʙᴇ 𝖴ʀʟ**. ᴀғᴛᴇʀ /vplay")
            else:
                return await promsg.edit("𝖯ʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ **𝖠ᴜᴅɪᴏ** ᴏʀ ɢɪᴠᴇ ᴍᴇ **𝖲ᴏɴɢ 𝖭ᴀᴍᴇ ᴀɴᴅ 𝖸ᴏᴜᴛᴜʙᴇ 𝖴ʀʟ**. ᴀғᴛᴇʀ /play")
        await promsg.delete()            
    elif not song_name:
        return await event.reply("𝖯ʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ **𝖲ᴏɴɢ 𝖭ᴀᴍᴇ** ᴏʀ **𝖸ᴏᴜᴛᴜʙᴇ 𝖴ʀʟ** ᴀғᴛᴇʀ /play")
    bot = await Alishan.get_me()
    assistant = await Assistant.get_me()    
    if not await is_admin(bot, event):
        return await event.reply(f"{BOT_MENTION} ɪs ɴᴏᴛ ᴀᴅᴍɪɴ, 𝖯ʟᴇᴀsᴇ ɢɪʙᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ <b>(ᴄʀᴇᴀᴛᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ)</b> ᴀᴅᴍɪɴ ʀɪɢʜᴛs.", parse_mode="html")
    if chat_id in is_playing:
        await add_to_queue(song_name, chat_id, query_format, mention, download, force_play)
    try:
        await Assistant(GetParticipantRequest(chat.id, assistant.id))
        await add_to_queue(song_name, chat_id, query_format, mention, download, force_play)
        return
    except:
        pass  
    try:
        try:
            result = await Alishan(GetParticipantRequest(chat_id, assistant.id))
        except UserNotParticipantError:
            if chat_id in is_playing:
                is_playing.pop(chat_id, None)
            if not await check_rights(event, BOT_ID, "invite_users"):      
                return await event.reply(f"{BOT_MENTION} ʜᴀs ɴᴏ ᴀᴄᴄᴇss ᴛᴏ ɪɴᴠɪᴛᴇ {ASSISTANT_MENTION}, 𝖯ʟᴇᴀsᴇ ɢɪʙᴇ ᴍᴇ <b>(ᴄʀᴇᴀᴛᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ)</b> ᴀᴅᴍɪɴ ʀɪɢʜᴛs", parse_mode="html")
            await Alishan(EditBannedRequest(chat_id, assistant.id, UNBAN_RIGHTS))   
            export_link = await Alishan(ExportChatInviteRequest(chat_id))
            chat_link = export_link.link
            invite_code = search(r"(?:joinchat/|\+)([a-zA-Z0-9_-]+)", chat_link).group(1)
            await Assistant(ImportChatInviteRequest(invite_code))
            await Assistant.send_message(chat_id, f"<b>{ASSISTANT_MENTION} 𝖴ɴʙᴀɴɴᴇᴅ! , 𝖱ᴇᴀᴅʏ?</b> 𝖨 ᴀᴍ ᴄᴏᴍᴍɪɴɢ ᴛᴏ 𝖵ᴏɪᴄᴇ 𝖢ʜᴀᴛ. .", parse_mode="html")
            return await add_to_queue(song_name, chat_id, query_format, mention, download, force_play)    
        assistant_status = result.participant
        
        if isinstance(assistant_status, ChannelParticipantBanned):
            if not await check_rights(event, BOT_ID, "ban_users"):
                return await event.reply(f"{BOT_MENTION} ʜᴀs ɴᴏ ᴀᴄᴄᴇss ᴛᴏ ɪɴᴠɪᴛᴇ {ASSISTANT_MENTION}, 𝖯ʟᴇᴀsᴇ ɢɪʙᴇ ᴍᴇ <b>(ᴄʀᴇᴀᴛᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ)</b> ᴀᴅᴍɪɴ ʀɪɢʜᴛs", parse_mode="html")
            if not await check_rights(event, BOT_ID, "invite_users"):      
                return await event.reply(f"{BOT_MENTION} ʜᴀs ɴᴏ ᴀᴄᴄᴇss ᴛᴏ ɪɴᴠɪᴛᴇ {ASSISTANT_MENTION}, 𝖯ʟᴇᴀsᴇ ɢɪʙᴇ ᴍᴇ <b>(ᴄʀᴇᴀᴛᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ)</b> ᴀᴅᴍɪɴ ʀɪɢʜᴛs", parse_mode="html")
            await Alishan(EditBannedRequest(chat_id, assistant.id, UNBAN_RIGHTS))   
            export_link = await Alishan(ExportChatInviteRequest(chat_id))
            chat_link = export_link.link
            invite_code = search(r"(?:joinchat/|\+)([a-zA-Z0-9_-]+)", chat_link).group(1)
            await Assistant(ImportChatInviteRequest(invite_code))
            await Assistant.send_message(chat_id, f"<b>{ASSISTANT_MENTION} 𝖴ɴʙᴀɴɴᴇᴅ! , 𝖱ᴇᴀᴅʏ?</b> 𝖨 ᴀᴍ ᴄᴏᴍᴍɪɴɢ ᴛᴏ 𝖵ᴏɪᴄᴇ 𝖢ʜᴀᴛ. .", parse_mode="html")
            await add_to_queue(song_name, chat_id, query_format, mention, download, force_play)
            return
        else:
            try:
                await Assistant(GetParticipantRequest(chat_id, assistant.id))
                await add_to_queue(song_name, chat_id, query_format, mention, download, force_play)
                return
            except UserNotParticipantError:
                pass
            except Exception:
                error = traceback.format_exc()
                return await send_error(error)
                
            export_link = await Alishan(ExportChatInviteRequest(chat_id))
            chat_link = export_link.link
            invite_code = search(r"(?:joinchat/|\+)([a-zA-Z0-9_-]+)", chat_link).group(1)
            await Assistant(ImportChatInviteRequest(invite_code))
            await Assistant.send_message(chat_id, f"{ASSISTANT_MENTION} 𝖩ᴏɪɴᴇᴅ ᴛʜᴇ ɢʀᴏᴜᴘ! 𝖨 ᴀᴍ ᴄᴏᴍᴍɪɴɢ ɪɴ <b>𝖵ᴏɪᴄᴇ 𝖢ʜᴀᴛ</b>", parse_mode="html")
            await add_to_queue(song_name, chat_id, query_format, mention, download, force_play)
            return
    except UserNotParticipantError:
        export_link = await Alishan(ExportChatInviteRequest(chat_id))
        chat_link = export_link.link
        invite_code = search(r"(?:joinchat/|\+)([a-zA-Z0-9_-]+)", chat_link).group(1)
        await Assistant(ImportChatInviteRequest(invite_code))
        await Assistant.send_message(chat_id, f"{ASSISTANT_MENTION} 𝖩ᴏɪɴᴇᴅ ᴛʜᴇ ɢʀᴏᴜᴘ! 𝖨 ᴀᴍ ᴄᴏᴍᴍɪɴɢ ɪɴ <b>𝖵ᴏɪᴄᴇ 𝖢ʜᴀᴛ</b>", parse_mode="html")
        await add_to_queue(song_name, chat_id, query_format, mention, download, force_play)
        return
    except ChatAdminRequiredError:
        return await event.reply(f"{BOT_MENTION} ʜᴀs ɴᴏᴛ ᴀᴄᴄᴇss ᴛᴏ ᴄʜᴇᴄᴋ {ASSISTANT_MENTION} ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀ ɴᴏᴛ, 𝖯ʟᴇᴀsᴇ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ <pre> (ᴄʀᴇᴀᴛᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ) ʀɪɢʜᴛs </pre>", parse_mode="html")
    except Exception:
        error = traceback.format_exc()
        await send_error(error)
        return await event.reply(f"{BOT_MENTION} ʜᴀs ɴᴏᴛ ᴀᴄᴄᴇss ᴛᴏ ᴄʜᴇᴄᴋ {ASSISTANT_MENTION} ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀ ɴᴏᴛ, 𝖯ʟᴇᴀsᴇ ᴍᴀᴋᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ʜɪsᴛᴏʀʏ ᴠɪsᴀʙʟᴇ <pre> ᴄᴏɴᴠᴇʀᴛ ᴛᴏ (sᴜᴘᴇʀ ɢʀᴏᴜᴘ)</pre>", parse_mode="html")