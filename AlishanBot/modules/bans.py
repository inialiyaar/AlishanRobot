from AlishanBot.core.bot import Alishan
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantCreator, ChannelParticipantAdmin
from datetime import timedelta, datetime
from AlishanBot import config
from AlishanBot.core.decorators import add_command
from AlishanBot.__init__ import BOT_ID
from AlishanBot.modules.helper_funcs.helpers import check_rights, get_target_user, is_admin
from AlishanBot.modules.helper_funcs.ErrorLog import send_error
import traceback

BAN_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)
UNBAN_RIGHTS = ChatBannedRights(until_date=None, view_messages=False)

@add_command("ban")
async def ban_user(event, command_used, args):
    if not event.is_group:
        return await event.reply("This command can only be used in groups.")
    
    if not args and not event.is_reply:
        return await event.reply("I doubt that's a user.")
        
    chat = await event.get_chat()
    sender = await event.get_sender()
    reply = await event.get_reply_message()
    user = await get_target_user(event)    
    if not user:
        return await event.reply("This user not found in this group")
    if user.id == BOT_ID:
        return await event.reply("Oh yeah, ban myself, noob!")
    if user.id == config.OWNER_ID:
        return await event.reply("Trying to put me against a god level disaster huh? ")
    if not await check_rights(event, BOT_ID, "ban_users"):
        return await event.reply("Ohh shit!! I don't have ban users rights")    
    if not await check_rights(event, sender.id, "ban_users"):
        return await event.reply("Can't ban! You don't have ban permission")
    if await is_admin(user, event):
        return await event.reply("» Lol, you trying to ban admin?")    
    args = event.raw_text.split(maxsplit=2)
    reason = args[2] if len(args) >= 3 else "No reason."
    try:
        await Alishan(EditBannedRequest(chat.id, user.id, BAN_RIGHTS))
    except Exception:
        if "tried to ban an admin" in str(e):
            return await event.reply(f"Lol, you trying to ban admin? ")
        error = traceback.format_exc()
        await send_error(error)

    text = (
        f"<code>❕</code><b>Ban Event</b>\n"
        f"<code> </code><b>•  Banned by:</b> <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
        f"<code> </code><b>•  User:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>"
    )
    if reason:
        text += f"\n<code> </code><b>•  Reason:</b> \n{reason}"

    await event.reply(text, parse_mode="html")

@add_command("tban")
async def temp_ban_user(event, command_used, args):
    if not event.is_group:
        return await event.reply("This command can only be used in groups.")
    chat = await event.get_chat()
    sender = await event.get_sender()
    if not await check_rights(event, BOT_ID, "ban_users"):
        return await event.reply("Ohh shit!! I don't have ban users rights")
    if not await check_rights(event, sender.id, "ban_users"):
        return await event.reply("Can't ban! You don't have ban permission")   
    if not args and not event.is_reply:
        return await event.reply("Ohh shit!! What are you doing?")
    if event.is_reply and not args:
        return await event.reply("You haven't specified a time to ban this user for!")
    user = await get_target_user(event)
    if not user:
        return await event.reply("This user not found in this group")
    if user.id == BOT_ID:
        return await event.reply("Oh yeah, ban myself, noob!")
    if user.id == config.OWNER_ID:
        return await event.reply("Trying to put me against a god level disaster huh? ")    
    if user.id == BOT_ID:
        return await event.reply("Oh yeah, ban myself, noob!")
    if await is_admin(user, event):
        return await event.reply("» Lol, you trying to ban admin?")    
    chat = await event.get_chat()
    parts = args.split()
    try:
        value_unite = parts[1]
        value = int("".join(filter(str.isdigit, value_unite)))
        unit = "".join(filter(str.isalpha, value_unite)) 
        reason = parts[2] if len(parts) >2 else None
    except Exception:
        error = traceback.format_exc()
        await send_error(error)
        return await event.reply("Invalid time format. Example: `/tban 10m Reason`")

    try:
        if unit == "m":
            until_date = datetime.now() + timedelta(minutes=value)
            time_val = f"{value} minute{'s' if value != 1 else ''}"
        elif unit == "h":
            until_date = datetime.now() + timedelta(hours=value)
            time_val = f"{value} hour{'s' if value != 1 else ''}"
        elif unit == "d":
            until_date = datetime.now() + timedelta(days=value)
            time_val = f"{value} day{'s' if value != 1 else ''}"
        else:
            return await event.reply("Invalid time format. Use m/h/d (e.g., 10m, 2h, 1d).")
    except Exception:
        error = traceback.format_exc()
        await send_error(error)
        return await event.reply("Invalid time format. Example: `/tban 10m Reason`")
    rights = ChatBannedRights(until_date=until_date, view_messages=True)
    await Alishan(EditBannedRequest(chat.id, user.id, rights))

    text = (
        f"<b>{chat.title}:</b>\n"
        "Temp Ban\n"
        f"<b>Banned By:</b> <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
        f"<b>User:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
        f"<b>Time:</b> {time_val}"
    )
    if reason:
        text += f"\n<b>Reason:</b> {reason}"

    await event.reply(text, parse_mode="html")


@add_command("unban")
async def unban_user(event, command_used, args):
    if not event.is_group:
        return await event.reply("This command can only be used in groups.")
    chat = await event.get_chat()
    sender = await event.get_sender()
    if not await check_rights(event, BOT_ID, "ban_users"):
        return await event.reply("Ohh shit!! I don't have ban users rights")
    if not await check_rights(event, sender.id, "ban_users"):
        return await event.reply("Can't unban! You don't have ban permission")   
    if not args and not event.is_reply:
        return await event.reply("Ohh shit!! What are you doing?")
    user = await get_target_user(event)
    if not user:
        return await event.reply("This user not found in this group")
    if await is_admin(user, event):
        return await event.reply("» Lol, you trying to ban admin?")
    try:
        await Alishan(EditBannedRequest(chat.id, user.id, UNBAN_RIGHTS))
    except Exception:
        error = traceback.format_exc()
        await send_error(error)
        return
    await event.reply(f"Yep, this user can join!\n\nUnbanned <a href='tg://user?id={user.id}'>{user.first_name}</a>", parse_mode="html")


@add_command("kick")
async def kick_user(event, command_used, args):
    if not event.is_group:
        return await event.reply("This command can only be used in groups.")
    chat = await event.get_chat()
    sender = await event.get_sender()
    if not await check_rights(event, BOT_ID, "ban_users"):
        return await event.reply("Ohh shit!! I don't have ban users rights")
    if not await check_rights(event, sender.id, "ban_users"):
        return await event.reply("Can't ban! You don't have ban permission")
    user = await get_target_user(event)
    if not user:
        return await event.reply("This user not found in this group")
    if user.id == BOT_ID:
        return await event.reply("Oh yeah, kick myself, noob!")
    if user.id == config.OWNER_ID:
        return await event.reply("Trying to put me against a god level disaster huh? ")
    if await is_admin(user, event):
        return await event.reply("» Lol, you trying to kick admin?")    
    chat = await event.get_chat()
    try:
        await Alishan(EditBannedRequest(chat.id, user.id, BAN_RIGHTS))
        await Alishan(EditBannedRequest(chat.id, user.id, UNBAN_RIGHTS))
    except Exception:
        error = traceback.format_exc()
        await send_error(error)
        return
    text = (
        f"<b>{chat.title}:</b>\n"
        f"Kicked\n"
        f"<b>Kicked By:</b> <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
        f"<b>User:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>"
    )
    await event.reply(text, parse_mode="html")


@add_command("kickme")
async def kick_me(event, command_used, args):
    if not event.is_group:
        return await event.reply("This command can only be used in groups.")
    if not await check_rights(event, BOT_ID, "ban_users"):
        return await event.reply("Ohh shit!! I don't have ban users rights")   

    user = await event.get_sender()
    chat = await event.get_chat()
    try:
        await Alishan(EditBannedRequest(chat.id, user.id, BAN_RIGHTS))
        await Alishan(EditBannedRequest(chat.id, user.id, UNBAN_RIGHTS))
    except Exception:
        error = traceback.format_exc()
        await send_error(error)
        return   
    await event.reply("**Kicks you out of the group**")
    