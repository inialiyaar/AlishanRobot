from AlishanBot.core.bot import Alishan
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from datetime import timedelta, datetime
from AlishanBot import config
from AlishanBot.core.decorators import add_command
from AlishanBot.__init__ import BOT_ID
from AlishanBot.modules.helper_funcs.helpers import check_rights, get_target_user, is_admin
from AlishanBot.modules.helper_funcs.ErrorLog import send_error
import traceback

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)


@add_command("mute")
async def mute_user(event, command_used, args):
    if not event.is_group:
        return await event.reply("This command can only be used in groups.")
    
    if not args and not event.is_reply:
        return await event.reply("I doubt that's a user.")
        
    chat = await event.get_chat()
    sender = await event.get_sender()
    user = await get_target_user(event)

    if not user:
        return await event.reply("This user not found in this group")

    if user.id == BOT_ID:
        return await event.reply("Oh yeah, mute myself, noob!")
    if user.id == config.OWNER_ID:
        return await event.reply("Trying to mute a god level disaster huh?")

    if not await check_rights(event, BOT_ID, "ban_users"):
        return await event.reply("Ohh shit!! I don't have mute rights!")

    if not await check_rights(event, sender.id, "ban_users"):
        return await event.reply("Can't mute! You don't have mute permission")

    if await is_admin(user, event):
        return await event.reply("» Lol, you trying to mute an admin?")

    args = event.raw_text.split(maxsplit=2)
    reason = args[2] if len(args) >= 3 else "No reason."

    try:
        await Alishan(EditBannedRequest(chat.id, user.id, MUTE_RIGHTS))
    except Exception as e:
        error = traceback.format_exc()
        await send_error(error)
        return

    text = (
        f"<code>❕</code><b>Mute Event</b>\n"
        f"<code> </code><b>•  Muted By:</b> <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
        f"<code> </code><b>•  User:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>"
    )
    if reason:
        text += f"\n<code> </code><b>•  Reason:</b> \n{reason}"

    await event.reply(text, parse_mode="html")


@add_command("tmute")
async def temp_mute_user(event, command_used, args):
    if not event.is_group:
        return await event.reply("This command can only be used in groups.")
    
    sender = await event.get_sender()
    chat = await event.get_chat()

    if not await check_rights(event, BOT_ID, "ban_users"):
        return await event.reply("Ohh shit!! I don't have mute rights!")

    if not await check_rights(event, sender.id, "ban_users"):
        return await event.reply("Can't mute! You don't have mute permission")

    if not args and not event.is_reply:
        return await event.reply("Ohh shit!! What are you doing?")
    if event.is_reply and not args:
        return await event.reply("You haven't specified a time to mute this user!")

    user = await get_target_user(event)
    if not user:
        return await event.reply("This user not found in this group")

    if user.id in [BOT_ID, config.OWNER_ID]:
        return await event.reply("Trying to mute a legend?")

    if await is_admin(user, event):
        return await event.reply("» Lol, mute an admin? Yeah noop.")

    parts = args.split()

    try:
        value_unite = parts[1]
        value = int("".join(filter(str.isdigit, value_unite)))
        unit = "".join(filter(str.isalpha, value_unite))
        reason = parts[2] if len(parts) > 2 else None
    except Exception:
        return await event.reply("Invalid format. Example: `/tmute 10m Reason`")

    try:
        if unit == "m":
            until_date = datetime.now() + timedelta(minutes=value)
            time_val = f"{value} minutes"
        elif unit == "h":
            until_date = datetime.now() + timedelta(hours=value)
            time_val = f"{value} hours"
        elif unit == "d":
            until_date = datetime.now() + timedelta(days=value)
            time_val = f"{value} days"
        else:
            return await event.reply("Invalid time format. Use m/h/d.")
    except:
        return await event.reply("Invalid format. Example: `/tmute 10m Reason`")

    rights = ChatBannedRights(until_date=until_date, send_messages=True)
    await Alishan(EditBannedRequest(chat.id, user.id, rights))

    text = (
        f"<b>{chat.title}:</b>\n"
        "Temp Mute\n"
        f"<b>Muted By:</b> <a href='tg://user?id={sender.id}'>{sender.first_name}</a>\n"
        f"<b>User:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
        f"<b>Time:</b> {time_val}"
    )
    if reason:
        text += f"\n<b>Reason:</b> {reason}"

    await event.reply(text, parse_mode="html")


@add_command("unmute")
async def unmute_user(event, command_used, args):
    if not event.is_group:
        return await event.reply("This command can only be used in groups.")
    
    sender = await event.get_sender()
    chat = await event.get_chat()

    if not await check_rights(event, BOT_ID, "ban_users"):
        return await event.reply("I don't have mute rights!")

    if not await check_rights(event, sender.id, "ban_users"):
        return await event.reply("Can't unmute! You don't have permission")

    if not args and not event.is_reply:
        return await event.reply("Ohh shit!! What are you doing?")

    user = await get_target_user(event)
    if not user:
        return await event.reply("This user not found in this group")

    try:
        await Alishan(EditBannedRequest(chat.id, user.id, UNMUTE_RIGHTS))
    except:
        error = traceback.format_exc()
        await send_error(error)
        return

    await event.reply(
        f"Yep, this user can chat now!\n\nUnmuted <a href='tg://user?id={user.id}'>{user.first_name}</a>",
        parse_mode="html"
    )