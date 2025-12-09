from telethon import events
from telethon.tl.types import MessageService, MessageActionGroupCall, UpdateNewChannelMessage, MessageActionInviteToGroupCall, PeerUser
from AlishanBot.core.bot import Alishan, music, Assistant
from AlishanBot.modules.helper_funcs.queue import queues, current_ind, queue_position
from AlishanBot.utils.database import groups
from AlishanBot.modules.helper_funcs.add_group import add_group
from telethon.tl.functions.channels import LeaveChannelRequest, GetFullChannelRequest
from AlishanBot.__init__ import player_stats, BOT_ID, BOT_MENTION, BOT_USERNAME, ASSISTANT_MENTION, ASSISTANT_ID
import asyncio
from pytgcalls import filters
from pytgcalls.types import GroupCallParticipant, Update
from pytgcalls import filters
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
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
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
            return await Alishan.send_message(chat_id, "**♻️ VideoChat Started!**")
        duration = readable_time(action.duration)
        if chat_id in player_stats:
            queues.pop(chat_id, None)
            current_ind.pop(chat_id, None)
            queue_position.pop(chat_id, None)
            player_stats.pop(chat_id, None)
            return await Alishan.send_message(chat_id, f"<b>📴 VideoChat Ended! and Queue Cleared.</b>\n\n<b>⏰ Duration:</b> {duration}", parse_mode="html")
        else:
            return await Alishan.send_message(chat_id, f"<b>📴 VideoChat Ended!</b>\n\n<b>⏰ Duration:</b> {duration}", parse_mode="html")
    if isinstance(action, MessageActionInviteToGroupCall):
        if not msg.from_id:
            return
        inviter_id = msg.from_id.user_id
        invited_users = msg.action.users
        inviter = await Alishan.get_entity(inviter_id)
        invited_entities = [await Alishan.get_entity(u) for u in invited_users]
        inviter_mention = f"<a href='tg://user?id={inviter.id}'>{inviter.first_name}</a>"
        for invited_user in invited_entities:
            invited_mention = f"<a href='tg://user?id={invited_user.id}'>{invited_user.first_name}</a>"
            await Alishan.send_message(
                chat_id, 
                f"{inviter_mention} invited {invited_mention}",
                parse_mode="html"
            )
        
@Assistant.on(events.ChatAction)
async def on_bot_banned(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    user = await event.get_user()
    if not user:
        return
    if event.user_left or event.user_kicked:
        if user.id == BOT_ID:
            try:
                await Assistant(LeaveChannelRequest(chat_id))
                await music.leave_call(chat_id)
                if chat_id in queues and len(queues[chat_id]) > 0:
                    queues.pop(chat_id, None)
                    current_ind.pop(chat_id, None)
                    queue_position.pop(chat_id, None)
                    player_stats.pop(chat_id, None)
            except Exception: 
                pass
    if chat_id in player_stats:
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
        except Exception:
            pass
    pending_check.discard(chat_id)
    
@Alishan.on(events.ChatAction)  
async def ChatAction(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    if not groups.find_one({"chat_id": chat_id}):
        await add_group(event)
    user = await event.get_user()
    if not user:
        return
    if event.user_left or event.user_kicked:
        if not user.id == ASSISTANT_ID:
            return
        if chat_id in player_stats:
            queues.pop(chat_id, None)
            current_ind.pop(chat_id, None)
            queue_position.pop(chat_id, None)
            player_stats.pop(chat_id, None)
            await event.reply(f"<b>{ASSISTANT_MENTION} was banned! Queue Cleared.</b>", parse_mode="html")
    if event.user_added:
        if user.id == BOT_ID:
            added_by = await event.get_added_by()
            chat_title = event.chat.title or "Unknown"
            if added_by:
                mention = f"<a href=\"tg://user?id={added_by.id}\">{added_by.first_name}</a>"
            else:
                mention = "Unknown"  
            try:   
                await event.reply(
                    file=config.START_IMG,
                    message=f"Hey {mention}\nI am {BOT_MENTION} the most powerful Telegram music and group management bot\n\nThanks for adding me in {chat_title}, {BOT_MENTION} can play songs in this chat", 
                    buttons = [
                        [
                            Button.url("Add Me to Your Chat", f"https://t.me/{BOT_USERNAME}?startgroup=true"), 
                        ], 
                        [
                            Button.url("Support", f"https://t.me/{config.SUPPORT_CHAT}"), 
                            Button.url("Updates", f"https://t.me/{config.SUPPORT_CHANNEL}")
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
                        message=f"Hey {mention}\nI am {BOT_MENTION} the most powerful Telegram music and group management bot\n\nThanks for adding me in {chat_title}, {BOT_MENTION} can play songs in this chat", 
                        buttons = [
                            [
                                Button.url("Add Me to Your Chat", f"https://t.me/{BOT_USERNAME}?startgroup=true"), 
                            ], 
                            [
                                Button.url("Support", f"https://t.me/{config.SUPPORT_CHAT}"), 
                                Button.url("Updates", f"https://t.me/{config.SUPPORT_CHANNEL}")
                            ]
                        ], 
                        parse_mode="html", 
                    )
                except Exception:
                    pass  
                
@music.on_update(filters.call_participant(GroupCallParticipant.Action.LEFT | GroupCallParticipant.Action.JOINED))
async def VoiceChatUpdate(_, update: Update):
    participant = update.participant
    action = participant.action
    chat_id = update.chat_id
    user = await Alishan.get_entity(participant.user_id)
    if action == GroupCallParticipant.Action.JOINED:
        await Assistant.send_message(chat_id, f"{user.first_name} joined the VoiceChat.")
    else:
        await Assistant.send_message(chat_id, f"{user.first_name} left the VoiceChat.")
        