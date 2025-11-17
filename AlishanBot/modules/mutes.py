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
        return await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs.")
    
    if not args and not event.is_reply:
        return await event.reply("ɪ ᴅᴏᴜʙᴛ ᴛʜᴀᴛ's ᴀ ᴜsᴇʀ.")
        
    chat = await event.get_chat()
    sender = await event.get_sender()
    user = await get_target_user(event)

    if not user:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")

    if user.id == BOT_ID:
        return await event.reply("ᴏʜ ʏᴇᴀʜ, ᴍᴜᴛᴇ ᴍʏsᴇʟғ, ɴᴏᴏʙ!")
    if user.id == config.OWNER_ID:
        return await event.reply("ᴛʀʏɪɴɢ ᴛᴏ ᴍᴜᴛᴇ ᴀ ɢᴏᴅ ʟᴇᴠᴇʟ ᴅɪsᴀsᴛᴇʀ ʜᴜʜ?")

    if not await check_rights(event, BOT_ID, "ban_users"):
        return await event.reply("Ohh shit!! I don't have mute rights!")

    if (sender.id not in config.sudo_list) and not await check_rights(event, sender.id, "ban_users"):
        return await event.reply("ᴄᴀɴ'ᴛ ᴍᴜᴛᴇ! ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴍᴜᴛᴇ ᴘᴇʀᴍɪssɪᴏɴ")

    if await is_admin(user, event):
        return await event.reply("» ʟᴏʟ, ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ᴍᴜᴛᴇ ᴀɴ ᴀᴅᴍɪɴ?")

    args = event.raw_text.split(maxsplit=2)
    reason = args[2] if len(args) >= 3 else "ɴᴏ ʀᴇᴀsᴏɴ."

    try:
        await Alishan(EditBannedRequest(chat.id, user.id, MUTE_RIGHTS))
    except Exception as e:
        error = traceback.format_exc()
        await send_error(error)
        return

    text = (
        f"<code>❕</code><b>ᴍᴜᴛᴇ ᴇᴠᴇɴᴛ</b>\n"
        f"<code> </code><b>•  ᴍᴜᴛᴇᴅ ʙʏ:</b> <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
        f"<code> </code><b>•  ᴜsᴇʀ:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>"
    )
    if reason:
        text += f"\n<code> </code><b>•  ʀᴇᴀsᴏɴ:</b> \n{reason}"

    await event.reply(text, parse_mode="html")


@add_command("tmute")
async def temp_mute_user(event, command_used, args):
    if not event.is_group:
        return await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs.")
    
    sender = await event.get_sender()
    chat = await event.get_chat()

    if not await check_rights(event, BOT_ID, "ban_users"):
        return await event.reply("Ohh shit!! I don't have mute rights!")

    if (sender.id not in config.sudo_list) and not await check_rights(event, sender.id, "ban_users"):
        return await event.reply("ᴄᴀɴ'ᴛ ᴍᴜᴛᴇ! ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴍᴜᴛᴇ ᴘᴇʀᴍɪssɪᴏɴ")

    if not args and not event.is_reply:
        return await event.reply("ᴏʜʜ sʜɪᴛ!! ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴅᴏɪɴɢ?")
    if event.is_reply and not args:
        return await event.reply("You haven't specified a time to mute this user!")

    user = await get_target_user(event)
    if not user:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")

    if user.id in [BOT_ID, config.OWNER_ID]:
        return await event.reply("ᴛʀʏɪɴɢ ᴛᴏ ᴍᴜᴛᴇ ᴀ ʟᴇɢᴇɴᴅ?")

    if await is_admin(user, event):
        return await event.reply("» ʟᴏʟ, ᴍᴜᴛᴇ ᴀɴ ᴀᴅᴍɪɴ? ʏᴇᴀʜ ɴᴏᴏᴘ.")

    parts = args.split()

    try:
        value_unite = parts[1]
        value = int("".join(filter(str.isdigit, value_unite)))
        unit = "".join(filter(str.isalpha, value_unite))
        reason = parts[2] if len(parts) > 2 else None
    except Exception:
        return await event.reply("ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ. ᴇxᴀᴍᴘʟᴇ: `/tmute 10m Reason`")

    try:
        if unit == "m":
            until_date = datetime.now() + timedelta(minutes=value)
            time_val = f"{value} ᴍɪɴᴜᴛᴇs"
        elif unit == "h":
            until_date = datetime.now() + timedelta(hours=value)
            time_val = f"{value} ʜᴏᴜʀs"
        elif unit == "d":
            until_date = datetime.now() + timedelta(days=value)
            time_val = f"{value} ᴅᴀʏs"
        else:
            return await event.reply("ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ ғᴏʀᴍᴀᴛ. ᴜsᴇ m/h/d.")
    except:
        return await event.reply("ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ. ᴇxᴀᴍᴘʟᴇ: `/tmute 10m Reason`")

    rights = ChatBannedRights(until_date=until_date, send_messages=True)
    await Alishan(EditBannedRequest(chat.id, user.id, rights))

    text = (
        f"<b>{chat.title}:</b>\n"
        "ᴛᴇᴍᴩ ᴍᴜᴛᴇ\n"
        f"<b>ᴍᴜᴛᴇᴅ ʙʏ:</b> <a href='tg://user?id={sender.id}'>{sender.first_name}</a>\n"
        f"<b>ᴜsᴇʀ:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
        f"<b>ᴛɪᴍᴇ:</b> {time_val}"
    )
    if reason:
        text += f"\n<b>ʀᴇᴀsᴏɴ:</b> {reason}"

    await event.reply(text, parse_mode="html")


@add_command("unmute")
async def unmute_user(event, command_used, args):
    if not event.is_group:
        return await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs.")
    
    sender = await event.get_sender()
    chat = await event.get_chat()

    if not await check_rights(event, BOT_ID, "ban_users"):
        return await event.reply("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴍᴜᴛᴇ ʀɪɢʜᴛs!")

    if (sender.id not in config.sudo_list) and not await check_rights(event, sender.id, "ban_users"):
        return await event.reply("ᴄᴀɴ'ᴛ ᴜɴᴍᴜᴛᴇ! ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ")

    if not args and not event.is_reply:
        return await event.reply("ᴏʜʜ sʜɪᴛ!! ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴅᴏɪɴɢ?")

    user = await get_target_user(event)
    if not user:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")

    try:
        await Alishan(EditBannedRequest(chat.id, user.id, UNMUTE_RIGHTS))
    except:
        error = traceback.format_exc()
        await send_error(error)
        return

    await event.reply(
        f"ʏᴇᴘ, ᴛʜɪs ᴜsᴇʀ ᴄᴀɴ ᴄʜᴀᴛ ɴᴏᴡ!\n\nᴜɴᴍᴜᴛᴇᴅ <a href='tg://user?id={user.id}'>{user.first_name}</a>",
        parse_mode="html"
    )