from AlishanBot.core.bot import Alishan, music
from AlishanBot.core.decorators import add_command, callback_query
import time
from AlishanBot.utils.database import nightmode
from datetime import datetime, time
import pytz
from AlishanBot.__init__ import BOT_ID
import asyncio
from telethon import events, Button
from AlishanBot.modules.helper_funcs.helpers import check_rights, is_admin

IST = pytz.timezone("Asia/Kolkata")


@add_command("nightmode")
async def nightmode_handler(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command works only in group")

    user = await event.get_sender()
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)

    if not await is_admin(user, event):
        return await event.reply("» You must be an admin to manage nightmode")

    keyboard = [
        [
            Button.inline("Enable", data=f"enable_nightmode({event.chat_id})"),
            Button.inline("Disable", data=f"disable_nightmode({event.chat_id})"),
        ]
    ]
    await event.reply("• Choose an option to enable/disable nightmode", buttons=keyboard)


@Alishan.on(events.CallbackQuery(pattern=r"enable_nightmode\((.+)\)"))
async def enable_nightmode(event):
    user = await event.get_sender()
    chat_id = int(event.pattern_match.group(1))

    if not await is_admin(user, event):
        return await event.answer("Only admin can enable nightmode", alert=True)

    nightmode.update_one({"chat_id": chat_id}, {"$set": {"enabled": True}}, upsert=True)
    await event.edit(f"Nightmode enabled by {user.first_name}!")


@Alishan.on(events.CallbackQuery(pattern=r"disable_nightmode\((.+)\)"))
async def disable_nightmode(event):
    user = await event.get_sender()
    chat_id = int(event.pattern_match.group(1))

    if not await is_admin(user, event):
        return await event.answer("Only admin can disable nightmode", alert=True)

    nightmode.update_one({"chat_id": chat_id}, {"$set": {"enabled": False}}, upsert=True)
    await event.edit(f"Nightmode disabled by {user.first_name}...")

async def nightmode_scheduler():
    while True:
        now = datetime.now(IST).time()

        chats = nightmode.find({"enabled": True})
        for chat in chats:
            chat_id = chat["chat_id"]

            has_rights = await check_rights(chat_id, BOT_ID, "change_info")
            
            if not has_rights:
                nightmode.update_one({"chat_id": chat_id}, {"$set": {"enabled": False}})
                try:
                    await Alishan.send_message(chat_id, "Nightmode disabled automatically — Bot has no admin rights.")
                except Exception as e:
                    print(e)
                    pass
                continue
            if now.hour == 0 and now.minute == 0:
                await lock_group(chat_id)

            if now.hour == 8 and now.minute == 0:
                await unlock_group(chat_id)

        await asyncio.sleep(60)


async def lock_group(chat_id):
    try:
        await Alishan.edit_permissions(chat_id, send_messages=False)
        await Alishan.send_message(chat_id, "🌙 Nightmode Actived — Group is Locking Now 🔒\n\nGood Night Sweet Dreams 🌃.")
    except Exception as e:
        print("Lock Error:", e)


async def unlock_group(chat_id):
    try:
        await Alishan.edit_permissions(chat_id, send_messages=True)
        await Alishan.send_message(chat_id, "🕛 Nightmode Deactivated — Group is Unlocking Now 🔐\n\nGood Morning Have a great Day ahead 🌄")
    except Exception as e:
        print("Unlock Error:", e)

asyncio.create_task(nightmode_scheduler())    