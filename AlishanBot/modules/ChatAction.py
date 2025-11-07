import re
import asyncio
from datetime import timedelta, datetime
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.types import (
    ChatBannedRights,
    ChannelParticipantCreator,
    ChannelParticipantAdmin
)
from AlishanBot.core.bot import Alishan
from AlishanBot import config

sudo_list = config.sudo_list


ban_rights = ChatBannedRights(until_date=None, view_messages=True)
unban_rights = ChatBannedRights(until_date=None, view_messages=False)

async def has_ban_permission(chat, user_id):
    try:
        participant = await Alishan(GetParticipantRequest(chat.id, user_id))
        participant = participant.participant
        if isinstance(participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            return participant.admin_rights and participant.admin_rights.ban_users
    except Exception as e:
        print(f"[has_ban_permission error] {e}")
    return False

async def get_target_user(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        return reply_msg.sender_id 
    else:
        args = event.raw_text.split()
        if len(args) >= 2:
            try:
                user = await Alishan.get_entity(args[1])
                return user.id
            except:
                return None
    return None

@Alishan.on(events.NewMessage(pattern=r"(?i)\/ban(?:\s|$)"))
async def ban_handler(event):
    if not event.is_group:
        return await event.reply("This command only works in groups.")

    chat = await event.get_chat()
    sender = await event.get_sender()
    bot = await Alishan.get_me()
    user_id = await get_target_user(event)

    if not user_id:
        return await event.reply("Reply to a user or provide a valid username/ID.")

    args = event.raw_text.split(maxsplit=2)
    reason = args[2] if len(args) >= 3 else "No reason provided."

    if not (sender.id in sudo_list or await has_ban_permission(chat, sender.id)):
        return await event.reply("You need **ban rights** to do that!")

    if not await has_ban_permission(chat, bot.id):
        return await event.reply("I don't have **Ban Users** rights.")

    try:
        await Alishan(EditBannedRequest(chat.id, user_id, ban_rights))
        return await event.reply(
            f"`{user_id}` **Banned successfully.**\n\n**Banned by:** {sender.first_name}\n**Reason:** {reason}"
        )
    except Exception as e:
        return await event.reply(f"Failed to ban user.\n**Reason:** `{e}`")

@Alishan.on(events.NewMessage(pattern=r"(?i)\/unban(?:\s|$)"))
async def unban_handler(event):
    if not event.is_group:
        return await event.reply("This command only works in groups.")

    chat = await event.get_chat()
    sender = await event.get_sender()
    bot = await Alishan.get_me()
    user_id = await get_target_user(event)

    if not user_id:
        return await event.reply("Reply to a user or provide a valid username/ID.")

    if not (sender.id in sudo_list or await has_ban_permission(chat, sender.id)):
        return await event.reply("You need **ban rights** to do that!")

    if not await has_ban_permission(chat, bot.id):
        return await event.reply("I don't have **Ban Users** rights.")

    try:
        await Alishan(EditBannedRequest(chat.id, user_id, unban_rights))
        return await event.reply(f"User ID: `{user_id}` has been **unbanned**.")
    except Exception as e:
        return await event.reply(f"Failed to unban user.\n**Reason:** `{e}`")

@Alishan.on(events.NewMessage(pattern=r"(?i)\/mute(?:\s|$)"))
async def mute_handler(event):
    if not event.is_group:
        return await event.reply("This command only works in groups.")

    chat = await event.get_chat()
    sender = await event.get_sender()
    bot = await Alishan.get_me()
    user_id = await get_target_user(event)

    args = event.raw_text.split(maxsplit=3)
    if len(args) < 3:
        return await event.reply("Usage: `/mute username p|1h20m reason`")

    time_or_perm = args[2]
    reason = args[3] if len(args) >= 4 else "No reason provided."

    if not user_id:
        return await event.reply("Provide a valid user to mute.")

    if not (sender.id in sudo_list or await has_ban_permission(chat, sender.id)):
        return await event.reply("You need **ban rights** to mute users.")

    if not await has_ban_permission(chat, bot.id):
        return await event.reply("I don't have **Ban Users** rights.")

    until = None
    if time_or_perm.lower() != "p":
        time_matches = re.findall(r"(\d+)([smhd])", time_or_perm)
        if not time_matches:
            return await event.reply("Invalid time format. Use like: `1h20m`")
        seconds = 0
        for value, unit in time_matches:
            value = int(value)
            if unit == 's': seconds += value
            elif unit == 'm': seconds += value * 60
            elif unit == 'h': seconds += value * 3600
            elif unit == 'd': seconds += value * 86400
        until = datetime.utcnow() + timedelta(seconds=seconds)

    mute_rights = ChatBannedRights(
        until_date=until,
        send_messages=True
    )

    try:
        await Alishan(EditBannedRequest(chat.id, user_id, mute_rights))
        await event.reply(
            f"`{user_id}` **Muted succeessfully.**\n\n**Muted by:** {sender.first_name}\n**Reason:** {reason}\n**Duration:** {'Permanent' if not until else time_or_perm}"
        )
        if until:
            await asyncio.sleep(seconds)
            await Alishan(EditBannedRequest(chat.id, user_id, unban_rights))
    except Exception as e:
        pass

@Alishan.on(events.NewMessage(pattern=r"(?i)\/unmute(?:\s|$)"))
async def unmute_handler(event):
    if not event.is_group:
        return await event.reply("This command only works in groups.")

    chat = await event.get_chat()
    sender = await event.get_sender()
    bot = await Alishan.get_me()
    user_id = await get_target_user(event)

    if not user_id:
        return await event.reply("Provide a valid user to unmute.")

    if not (sender.id in sudo_list or await has_ban_permission(chat, sender.id)):
        return await event.reply("You need **ban rights** to do that!")

    if not await has_ban_permission(chat, bot.id):
        return await event.reply("I don't have **Ban Users** rights.")

    try:
        await Alishan(EditBannedRequest(chat.id, user_id, unban_rights))
        await event.reply(f"User ID: `{user_id}` has been **unmuted**.")
    except Exception as e:
        await event.reply(f"Failed to unmute user.\n**Reason:** `{e}`")
        