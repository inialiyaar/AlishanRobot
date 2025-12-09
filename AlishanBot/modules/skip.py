from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command, callback_query
from telethon import events
from AlishanBot.modules.helper_funcs.queue import play_next
from asyncio import create_task
from AlishanBot.__init__ import player_stats, BOT_MENTION
from telethon import Button
from AlishanBot.modules.helper_funcs.helpers import is_admin
from AlishanBot.utils.database import stream_mode

votes = {}

@add_command("skip")
async def skip_handler(event, command_used, args):
    if event.is_group or event.is_channel:
        user = await event.get_sender()
        chat = await event.get_chat()
        chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
        settings = stream_mode.find_one({"chat_id": chat_id})
        if settings:
            admin_cmd = settings.get("admin_cmd", "admins")
        else:
            admin_cmd = "admins"  
        if not await is_admin(user, event) and admin_cmd == "admins":
            votes_target = 5
            msg = await event.reply(
                f"**Admin rights needed**\n\n⧽ {votes_target} votes needed for performing this action.",
                buttons = [
                    [Button.inline("Vote", data=b"skip_vote")]
                ]
                )
            votes[chat_id, msg.id] = {
                "users": [], 
                "count": 0,
                "target": 5
            }    
            return
        try:
            mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
        except Exception:
            mention = "Anonymous"
        chat = await event.get_chat()
        chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
        if chat_id in player_stats:
            try:
                await play_next(chat_id)
                await event.delete()
            except Exception:
                pass
            await event.reply(f"<b>➭ Track skipped successfully.</b>\nSkipped by: {mention}", parse_mode="html")
        else:
            await event.reply(f"» {BOT_MENTION} isn't streaming on Voicechat.", parse_mode="html")
                
    else:
        await event.reply("You can use in groups only!.")
    
@callback_query("skip")
async def callback_skip(event):
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
    mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    if chat_id in player_stats:
        try:
            await play_next(chat_id)
        except Exception:
            pass
        await event.reply(f"<b>➭ Track skipped successfully.</b>\nSkipped by: {mention}", parse_mode="html")
    else:
        await event.reply(f"» {BOT_MENTION} isn't streaming on Voicechat.", parse_mode="html")
        
@callback_query("skip_vote")
async def skip_vote_callback(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    msg_id = event.message_id
    user_id = event.sender_id
    key = (chat_id, msg_id)
    if key not in votes:
        return
    vote_data = votes[key]  
    if user_id in vote_data["users"]:
        return await event.answer("You already voted!", alert=True)
    vote_data["users"].append(user_id)
    vote_data["count"] +=1
    if vote_data["count"] >= vote_data["target"]:
        if chat_id in player_stats:
            try:
                await play_next(chat_id)
            except Exception:
                pass
            try:
                await status.edit(f"<b>➭ Track skipped successfully.</b>\nSkipped by: Voting", buttons=None, parse_mode="html")
            except Exception:
                await event.reply(f"<b>➭ Track skipped successfully.</b>\nSkipped by: Voting", buttons=None, parse_mode="html")
            del votes[key]  
        else:
            await event.reply(f"» {BOT_MENTION} isn't streaming on Voicechat.", parse_mode="html")
    else:
        remaining = vote_data["target"] - vote_data["count"]
        target = vote_data["target"]
        count = vote_data["count"]
        await event.answer("Added 1 up vote")
        await event.edit(
            f"**Admin rights needed**\n\n⧽ {target} votes needed for performing this action.", 
            buttons= [
                    [Button.inline(f"{count} 👍", data=b"skip_vote")]
                ]
            )
            