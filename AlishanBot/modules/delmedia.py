import asyncio
from telethon import events, Button
from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command
from AlishanBot.utils.database import delmedia
from AlishanBot.modules.helper_funcs.helpers import check_rights, is_admin

DEFAULT_DELAY = 300
MAX_DELAY = 600

@add_command("delmedia", "mediamode")
async def edit_handler(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command works only in group")

    user = await event.get_sender()
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)

    if not await is_admin(user, event):
        return await event.reply("» You must be an admin to manage delmedia")

    keyboard = [
        [
            Button.inline("Enable", data=f"enable_media({event.chat_id})"),
            Button.inline("Disable", data=f"disable_media({event.chat_id})"),
        ]
    ]
    await event.reply("• Choose an option to enable/disable delmedia", buttons=keyboard)


@Alishan.on(events.CallbackQuery(pattern=r"enable_media\((.+)\)"))
async def enable_media(event):
    user = await event.get_sender()
    chat_id = int(event.pattern_match.group(1))

    if not await is_admin(user, event):
        return await event.answer("Only admin can enable delmedia", alert=True)

    delmedia.update_one({"chat_id": chat_id}, {"$set": {"enabled": True}}, upsert=True)
    await event.edit(f"Delmedia enabled by {user.first_name}!")


@Alishan.on(events.CallbackQuery(pattern=r"disable_media\((.+)\)"))
async def disable_media(event):
    user = await event.get_sender()
    chat_id = int(event.pattern_match.group(1))

    if not await is_admin(user, event):
        return await event.answer("Only admin can disable delmedia", alert=True)

    delmedia.update_one({"chat_id": chat_id}, {"$set": {"enabled": False}}, upsert=True)
    await event.edit(f"Delmedia disabled by {user.first_name}...")

def parse_delay(delay_str: str):
    try:
        if delay_str.endswith("m"):
            minutes = int(delay_str[:-1])
            return minutes * 60
        return None
    except Exception:
        return None

@add_command("delay")
async def set_group_delay(event, command, delay_str):
    if not event.is_group:
        return await event.reply("⚠️ This command works only in groups.")

    delay_seconds = parse_delay(delay_str)

    if not delay_seconds:
        return await event.reply("Invalid format! Use `/delay 5m` (max 10m).")

    if delay_seconds > MAX_DELAY:
        return await event.reply(f"Max allowed delay is 10m.")

    delmedia.update_one(
        {"chat_id": event.chat_id},
        {"$set": {"delay": delay_seconds}},
        upsert=True,
    )

    await event.reply(f"Delay set to {delay_str} for this group.")
    
@Alishan.on(events.NewMessage)
async def auto_delete_non_text(event):
    if event.is_private:
        return
    data = delmedia.find_one({"chat_id": event.chat_id, "enabled": True})
    if not data:
        return
    msg = event.message
    if msg.text and not msg.media:
        return

    doc = delmedia.find_one({"chat_id": event.chat_id})
    delay_seconds = doc["delay"] if doc and "delay" in doc else DEFAULT_DELAY

    asyncio.create_task(schedule_delete(event.chat_id, msg.id, delay_seconds))


async def schedule_delete(chat_id, message_id, delay_seconds):
    await asyncio.sleep(delay_seconds)
    try:
        await Alishan.delete_messages(chat_id, message_id)
    except Exception:
        pass