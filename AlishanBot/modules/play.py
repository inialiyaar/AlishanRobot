from AlishanBot.core.bot import Alishan, Assistant
from AlishanBot.modules.helper_funcs.queue import add_to_queue
from AlishanBot.core.decorators import add_command
from AlishanBot.__init__ import BOT_MENTION, ASSISTANT_MENTION
from telethon.tl.functions.channels import GetParticipantRequest, EditBannedRequest, GetFullChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest, ImportChatInviteRequest
from telethon.errors import UserNotParticipantError, ChatAdminRequiredError, UserAlreadyParticipantError
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantBanned, ChatBannedRights
from telethon import events
from re import search
import os

@add_command("play", "vplay")
async def play_handler(event, command_used, song_name):
    if command_used == "vplay":
        query_format = "video"
    else:
        query_format = "audio"  
    download = False
    if event.is_private:
        return await event.reply("𝖸ᴏᴜ ᴄᴀɴ ᴜsᴇ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ!.")
    try:
        await event.delete()
    except:
        pass
    user = await event.get_sender()
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "ᴀɴᴏɴʏᴍᴏᴜs"
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    full_channel = await Alishan(GetFullChannelRequest(chat_id))
    call = full_channel.full_chat.call
    if not call:
        return await event.reply("**𝖵ᴏɪᴄᴇ ᴄʜᴀᴛ ɪs ɴᴏᴛ ᴀᴄᴛɪᴠᴇ,** ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ᴛʜᴇ ᴠᴄ ғɪʀsᴛ!")
    me = await Alishan.get_me()
    assistant_entity = await Assistant.get_me()
    if event.is_reply and not song_name:
        download = True
        reply = await event.get_reply_message()
        promsg = await event.respond("**𝖯ʀᴏᴄᴇssɪɴɢ...💫**")
        if reply.video and command_used == "vplay":
            song_name = await reply.download_media(file="downloads/local_download.mp4")
            
        elif reply.video and command_used == "play":
            return await promsg.edit("𝖯ʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ **𝖠ᴜᴅɪᴏ** ᴏʀ ɢɪᴠᴇ ᴍᴇ **𝖲ᴏɴɢ 𝖭ᴀᴍᴇ ᴀɴᴅ 𝖸ᴏᴜᴛᴜʙᴇ 𝖴ʀʟ**. ᴀғᴛᴇʀ /play")
            
        elif reply.audio and command_used == "play":
            song_name = await reply.download_media(file="downloads/local_download.mp3")
        elif reply.audio and command_used == "vplay":
            return await promsg.edit("𝖯ʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ **𝖵ɪᴅᴇᴏ** ᴏʀ ɢɪᴠᴇ ᴍᴇ **𝖲ᴏɴɢ 𝖭ᴀᴍᴇ ᴀɴᴅ 𝖸ᴏᴜᴛᴜʙᴇ 𝖴ʀʟ**. ᴀғᴛᴇʀ /vplay")
        else:
            if command_used == " vplay":
                return await promsg.edit("𝖯ʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ **𝖠ᴜᴅɪᴏ ᴀɴᴅ 𝖵ɪᴅᴇᴏ** ᴏʀ ɢɪᴠᴇ ᴍᴇ **𝖲ᴏɴɢ 𝖭ᴀᴍᴇ ᴀɴᴅ 𝖸ᴏᴜᴛᴜʙᴇ 𝖴ʀʟ**. ᴀғᴛᴇʀ /vplay")
            else:
                return await promsg.edit("𝖯ʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ **𝖠ᴜᴅɪᴏ** ᴏʀ ɢɪᴠᴇ ᴍᴇ **𝖲ᴏɴɢ 𝖭ᴀᴍᴇ ᴀɴᴅ 𝖸ᴏᴜᴛᴜʙᴇ 𝖴ʀʟ**. ᴀғᴛᴇʀ /play")
        await promsg.delete()            
    elif not song_name:
        return await event.reply("𝖯ʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ **𝖲ᴏɴɢ 𝖭ᴀᴍᴇ** ᴏʀ **𝖸ᴏᴜᴛᴜʙᴇ 𝖴ʀʟ** ᴀғᴛᴇʀ /play")
    try:
        await Assistant(GetParticipantRequest(chat_id, assistant_entity.id))
        await add_to_queue(song_name, chat_id, query_format, mention, download)
        return
    except Exception:
        pass
    try:
        result = await Alishan(GetParticipantRequest(chat_id, assistant_entity.id))
        assistant_status = result.participant
        if isinstance(assistant_status, ChannelParticipantBanned):
            admin_status = await Alishan(GetParticipantRequest(chat_id, me.id))
            if isinstance(admin_status.participant, ChannelParticipantAdmin):
                admin_rights = admin_status.participant.admin_rights
                if admin_rights.ban_users:
                    rights = ChatBannedRights(
                        until_date=0,
                        view_messages=False,
                        send_messages=False,
                        send_media=False,
                        send_stickers=False,
                        send_gifs=False,
                        send_games=False,
                        send_inline=False,
                        embed_links=False,
                    )
                    await Alishan(EditBannedRequest(chat_id, assistant_entity.id, rights))
                    if admin_rights.invite_users:
                        export_link = await Alishan(ExportChatInviteRequest(chat_id))
                        chat_link = export_link.link
                        invite_code = search(r"(?:joinchat/|\+)([a-zA-Z0-9_-]+)", chat_link).group(1)
                        await Assistant(ImportChatInviteRequest(invite_code))
                        await Assistant.send_message(chat_id, f"<b>{ASSISTANT_MENTION} 𝖴ɴʙᴀɴɴᴇᴅ! , 𝖱ᴇᴀᴅʏ?</b> 𝖨 ᴀᴍ ᴄᴏᴍᴍɪɴɢ ᴛᴏ 𝖵ᴏɪᴄᴇ 𝖢ʜᴀᴛ. .", parse_mode="html")
                        await add_to_queue(song_name, chat_id, query_format, mention, download)
                    else:
                        return await event.reply(f"{BOT_MENTION} ʜᴀs ɴᴏ ᴀᴄᴄᴇss ᴛᴏ ɪɴᴠɪᴛᴇ {ASSISTANT_MENTION}, 𝖯ʟᴇᴀsᴇ ɢɪʙᴇ ᴍᴇ <b>(ᴄʀᴇᴀᴛᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ)</b> ᴀᴅᴍɪɴ ʀɪɢʜᴛs", parse_mode="html")
                else:
                    return await event.reply(f"{BOT_MENTION} ʜᴀs ɴᴏ ᴀᴄᴄᴇss ᴛᴏ ᴜɴʙᴀɴ {ASSISTANT_MENTION}, 𝖯ʟᴇᴀsᴇ ɢɪʙᴇ ᴍᴇ <b>(ʙᴀɴ ʀɪɢʜᴛs)</b>", parse_mode="html")
            else:
                return await event.reply(f"{BOT_MENTION} ɪs ɴᴏᴛ ᴀᴅᴍɪɴ, 𝖯ʟᴇᴀsᴇ ɢɪʙᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ <b>(ᴄʀᴇᴀᴛᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ)</b> ᴀᴅᴍɪɴ ʀɪɢʜᴛs.", parse_mode="html")
        else:
            try:
                export_link = await Alishan(ExportChatInviteRequest(chat_id))
            except ChatAdminRequiredError:
                return await event.reply(f"{BOT_MENTION} ɪs ɴᴏᴛ ᴀᴅᴍɪɴ, 𝖯ʟᴇᴀsᴇ ɢɪʙᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ <b>(ᴄʀᴇᴀᴛᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ)</b> ᴀᴅᴍɪɴ ʀɪɢʜᴛs.", parse_mode="html")
            chat_link = export_link.link
            invite_code = search(r"(?:joinchat/|\+)([a-zA-Z0-9_-]+)", chat_link).group(1)
            await Assistant(ImportChatInviteRequest(invite_code))
            await Assistant.send_message(chat_id, f"{ASSISTANT_MENTION} 𝖩ᴏɪɴᴇᴅ ᴛʜᴇ ɢʀᴏᴜᴘ! 𝖨 ᴀᴍ ᴄᴏᴍᴍɪɴɢ ɪɴ <b>𝖵ᴏɪᴄᴇ 𝖢ʜᴀᴛ</b>", parse_mode="html")
            await add_to_queue(song_name, chat_id, query_format, mention, download)
    except UserNotParticipantError:
        try:
            export_link = await Alishan(ExportChatInviteRequest(chat_id))
        except ChatAdminRequiredError:
            return await event.reply(f"{BOT_MENTION} ɪs ɴᴏᴛ ᴀᴅᴍɪɴ, 𝖯ʟᴇᴀsᴇ ɢɪʙᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ <b>(ᴄʀᴇᴀᴛᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ)</b> ᴀᴅᴍɪɴ ʀɪɢʜᴛs.", parse_mode="html")
        chat_link = export_link.link
        invite_code = search(r"(?:joinchat/|\+)([a-zA-Z0-9_-]+)", chat_link).group(1)
        await Assistant(ImportChatInviteRequest(invite_code))
        await Assistant.send_message(chat_id, f"{ASSISTANT_MENTION} 𝖩ᴏɪɴᴇᴅ ᴛʜᴇ ɢʀᴏᴜᴘ! 𝖨 ᴀᴍ ᴄᴏᴍᴍɪɴɢ ɪɴ <b>𝖵ᴏɪᴄᴇ 𝖢ʜᴀᴛ</b>", parse_mode="html")
        await add_to_queue(song_name, chat_id, query_format, mention, download)
    except UserAlreadyParticipantError:
        await add_to_queue(song_name, chat_id, query_format, mention, download)
    except Exception as e:
        print(f"Error {str(e)}")
        return await event.reply(f"{BOT_MENTION} ʜᴀs ɴᴏᴛ ᴀᴄᴄᴇss ᴛᴏ ᴄʜᴇᴄᴋ {ASSISTANT_MENTION} ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀ ɴᴏᴛ, 𝖯ʟᴇᴀsᴇ ᴍᴀᴋᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ʜɪsᴛᴏʀʏ ᴠɪsᴀʙʟᴇ <pre> ᴄᴏɴᴠᴇʀᴛ ᴛᴏ (sᴜᴘᴇʀ ɢʀᴏᴜᴘ)</pre>", parse_mode="html")
        