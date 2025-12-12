import asyncio
from telethon import events, Button
from telethon.tl.types import Message, MessageEmpty
from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command
from AlishanBot.utils.database import deledit
from AlishanBot import config
from AlishanBot.modules.helper_funcs.helpers import check_rights, is_admin
from AlishanBot.__init__ import player_stats, BOT_USERNAME

message_cache = {}

@add_command("deledit", "editmode")
async def edit_handler(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command works only in group")

    user = await event.get_sender()
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)

    if not await is_admin(user, event):
        return await event.reply("» You must be an admin to manage deledit")

    keyboard = [
        [
            Button.inline("Enable", data=f"enable_edit({event.chat_id})"),
            Button.inline("Disable", data=f"disable_edit({event.chat_id})"),
        ]
    ]
    await event.reply("• Choose an option to enable/disable deledit", buttons=keyboard)


@Alishan.on(events.CallbackQuery(pattern=r"enable_edit\((.+)\)"))
async def enable_edit(event):
    user = await event.get_sender()
    chat_id = int(event.pattern_match.group(1))

    if not await is_admin(user, event):
        return await event.answer("Only admin can enable deledit", alert=True)

    deledit.update_one({"chat_id": chat_id}, {"$set": {"enabled": True}}, upsert=True)
    await event.edit(f"Deledit enabled by {user.first_name}!")


@Alishan.on(events.CallbackQuery(pattern=r"disable_edit\((.+)\)"))
async def disable_edit(event):
    user = await event.get_sender()
    chat_id = int(event.pattern_match.group(1))

    if not await is_admin(user, event):
        return await event.answer("Only admin can disable deledit", alert=True)

    deledit.update_one({"chat_id": chat_id}, {"$set": {"enabled": False}}, upsert=True)
    await event.edit(f"Deledit disabled by {user.first_name}...")


@Alishan.on(events.NewMessage)
async def cache_message(event):
    if not event.is_private:
        msg = event.message
        if not msg:
            return
        message_cache[msg.id] = (msg.text, bool(msg.media), None)


@Alishan.on(events.MessageEdited)
async def handle_edit(event):
    try:
        if event.is_private:
            return
        chat_id = event.chat_id
        data = deledit.find_one({"chat_id": chat_id, "enabled": True})
        if not data:
            return
        msg = event.message or await event.get_message()
        if not msg or isinstance(msg, MessageEmpty):
            return

        old_text, had_media, last_edit = message_cache.get(msg.id, (None, False, None))

        if (old_text == msg.text) and (had_media == bool(msg.media)):
            return

        if last_edit and msg.edit_date and msg.edit_date == last_edit:
            return

        message_cache[msg.id] = (msg.text, bool(msg.media), msg.edit_date)

        user = await msg.get_sender()
        first_name = getattr(user, "first_name", "") or ""
        last_name = getattr(user, "last_name", "") or ""
        full_name = (first_name + " " + last_name).strip()
        warn_text = f"⚠️ Hey <a href=\"tg://user?id={user.id}\">{first_name}</a>\nyour edited message will be deleted in ⏳ {config.DELETE_EDIT_DELAY}s\nfor security reasons 🔐"
        buttons = [[Button.url("Add Me to Your Group", f"https://t.me/{BOT_USERNAME}?startgroup=true")]]
        warn_msg = await msg.reply(warn_text,buttons=buttons, parse_mode="html")
        asyncio.create_task(schedule_delete(msg.chat_id, [msg.id, warn_msg.id]))

    except Exception as e:
        print("Edit handler error:", e)


async def schedule_delete(chat_id, msg_ids):
    await asyncio.sleep(config.DELETE_EDIT_DELAY)
    try:
        await Alishan.delete_messages(chat_id, msg_ids)
    except Exception:
        pass