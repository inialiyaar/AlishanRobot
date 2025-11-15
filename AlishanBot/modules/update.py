from telethon import events
from telethon.tl.types import MessageService, MessageActionGroupCall, UpdateNewChannelMessage, MessageActionInviteToGroupCall, PeerUser
from AlishanBot.core.bot import Alishan, music, Assistant
from AlishanBot.modules.helper_funcs.queue import queues, current_ind, queue_position
from AlishanBot.utils.database import groups
from AlishanBot.modules.helper_funcs.add_group import add_group
from telethon.tl.functions.channels import LeaveChannelRequest, GetFullChannelRequest
from AlishanBot.__init__ import is_playing, BOT_ID, BOT_MENTION, BOT_USERNAME, ASSISTANT_MENTION, ASSISTANT_ID
import asyncio
from pytgcalls import filters
from pytgcalls.types import ChatUpdate, Update
from datetime import datetime, timedelta
from AlishanBot import config
from telethon import Button
from AlishanBot.modules.helper_funcs.ErrorLog import send_error
import traceback

pending_check = set()

def readable_time(seconds: int) -> str:
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    parts = []
    if days > 0:
        parts.append(f"{days} ᴅᴀʏ{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} ʜᴏᴜʀ{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} ᴍɪɴᴜᴛᴇ{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} sᴇᴄᴏɴᴅ{'s' if seconds != 1 else ''}")
    return " ".join(parts)

@Alishan.on(events.Raw)
async def GroupCallUpdate(event):
    if not isinstance(event, UpdateNewChannelMessage):
        return
    msg = event.message   
    chat = msg.peer_id.channel_id
    chat_id = int(f"-100{abs(chat)}") if not str(chat).startswith("-100") else int(chat)
    if not isinstance(msg,  MessageService):
        return
    action = msg.action
    if isinstance(action, MessageActionGroupCall):
        if action.duration is None:
            return await Alishan.send_message(chat_id, "**♻️ VɪᴅᴇᴏCʜᴀᴛ Sᴛᴀʀᴛᴇᴅ!**")
        duration = readable_time(action.duration)
        if chat_id in queues and len(queues[chat_id]) > 0:
            queues.pop(chat_id, None)
            current_ind.pop(chat_id, None)
            queue_position.pop(chat_id, None)
            is_playing.pop(chat_id, None)
            return await Alishan.send_message(chat_id, f"<b>📴 𝖵ɪᴅᴇᴏ𝖢ʜᴀᴛ 𝖤ɴᴅᴇᴅ! ᴀɴᴅ 𝖰ᴜᴇᴜᴇ 𝖢ʟᴇᴀʀᴇᴅ.</b>\n\n<b>⏰ 𝖣ᴜʀᴀᴛɪᴏɴ:</b> {duration}", parse_mode="html")
        else:
            return await Alishan.send_message(chat_id, f"<b>📴 𝖵ɪᴅᴇᴏ𝖢ʜᴀᴛ 𝖤ɴᴅᴇᴅ!</b>\n\n<b>⏰ 𝖣ᴜʀᴀᴛɪᴏɴ:</b> {duration}", parse_mode="html")
    if isinstance(action, MessageActionInviteToGroupCall):
        inviter_id = msg.from_id.user_id
        invited_users = msg.action.users
        inviter = await Alishan.get_entity(inviter_id)
        invited_entities = [await Alishan.get_entity(u) for u in invited_users]
        inviter_mention = f"<a href='tg://user?id={inviter.id}'>{inviter.first_name}</a>"
        for invited_user in invited_entities:
            invited_mention = f"<a href='tg://user?id={invited_user.id}'>{invited_user.first_name}</a>"
            await Alishan.send_message(
                chat_id, 
                f"{inviter_mention} ɪɴᴠɪᴛᴇᴅ {invited_mention}",
                parse_mode="html"
            )
        
@Assistant.on(events.ChatAction)
async def on_bot_banned(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    user = await event.get_user()
    if event.user_left or event.user_kicked:
        if user.id == BOT_ID:
            try:
                await Assistant(LeaveChannelRequest(chat_id))
                await music.leave_call(chat_id)
                if chat_id in queues and len(queues[chat_id]) > 0:
                    queues.pop(chat_id, None)
                    current_ind.pop(chat_id, None)
                    queue_position.pop(chat_id, None)
                    is_playing.pop(chat_id, None)
            except: 
                pass
    if chat_id in is_playing:
        return
    if chat_id in pending_check:
        return
    if chat_id == config.EVENT_LOGS:
        return
    pending_check.add(chat_id)
    await asyncio.sleep(1800) 
    if chat_id not in queues:
        try:
            await Assistant(LeaveChannelRequest(chat_id))
        except:
            pass
    pending_check.discard(chat_id)
    
@Alishan.on(events.ChatAction)  
async def ChatAction(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    if not groups.find_one({"chat_id": chat_id}):
        await add_group(event)
    user = await event.get_user()
    if event.user_left or event.user_kicked:
        if not user.id == ASSISTANT_ID:
            return
        if chat_id in queues and len(queues[chat_id]) > 0:
            queues.pop(chat_id, None)
            current_ind.pop(chat_id, None)
            queue_position.pop(chat_id, None)
            is_playing.pop(chat_id, None)
            await event.reply(f"<b>{ASSISTANT_MENTION} ᴡᴀs ʙᴀɴɴᴇᴅ! 𝖰ᴜᴇᴜᴇ 𝖢ʟᴇᴀʀᴇᴅ.</b>", parse_mode="html")
    if event.user_added:
        if user.id == BOT_ID:
            added_by = await event.get_added_by()
            chat_title = event.chat.title or "Unknown"
            if added_by:
                mention = f"<a href=\"tg://user?id={added_by.id}\">{added_by.first_name}</a>"
            else:
                mention = "ᴜɴᴋɴᴏᴡɴ"  
            try:   
                await event.reply(
                    file=config.START_IMG,
                    message=f"ʜᴇʏ {mention}\nɪ ᴀᴍ {BOT_MENTION} ᴛʜᴇ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟʟ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ᴀɴᴅ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ bot\n\nᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ {chat_title}, {BOT_MENTION} ᴄᴀɴ ᴘʟᴀʏ sᴏɴɢs ɪɴ ᴛʜɪs ᴄʜᴀᴛ", 
                    buttons = [
                        [
                            Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ", f"https://t.me/{BOT_USERNAME}?startgroup=true"), 
                        ], 
                        [
                            Button.url("sᴜᴘᴘᴏʀᴛ", f"https://t.me/{config.SUPPORT_CHAT}"), 
                            Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}")
                        ]
                    ], 
                    parse_mode="html", 
                )
            except Exception:
                error = traceback.format_exc()
                await send_error(error)
                try:
                    await Alishan.send_file(
                        chat_id, 
                        file=config.START_IMG,
                        message=f"ʜᴇʏ {mention}\nɪ ᴀᴍ {BOT_MENTION} ᴛʜᴇ ᴍᴏsᴛᴘᴏᴡᴇʀғᴜʟʟ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ᴀɴᴅ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ bot\n\nᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ {chat_title}, {BOT_MENTION} ᴄᴀɴ ᴘʟᴀʏ sᴏɴɢs ɪɴ ᴛʜɪs ᴄʜᴀᴛ", 
                        buttons = [
                            [
                                Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ", f"https://t.me/{BOT_USERNAME}?startgroup=true"), 
                            ], 
                            [
                                Button.url("sᴜᴘᴘᴏʀᴛ", f"https://t.me/{config.SUPPORT_CHAT}"), 
                                Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}")
                            ]
                        ], 
                        parse_mode="html", 
                    )
                except:
                    pass   