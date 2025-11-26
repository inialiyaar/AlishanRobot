import asyncio
from telethon import functions, errors
from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command
from AlishanBot.utils.database import users, groups, sudo_users 
from AlishanBot import config



@add_command("broadcast")
async def broadcast_handler(event, command_used, text):
    sender = await event.get_sender()
    if not sudo_users.find_one({"user_id": sender.id}) and sender.id != config.OWNER_ID:
        return

    reply = await event.get_reply_message()

    pin_broadcast = False
    if text and text.strip().endswith("-pin"):
        text = text.replace("-pin", "").strip()
        pin_broadcast = True
    elif reply and event.raw_text.strip().endswith("-pin"):
        pin_broadcast = True

    if not text and not reply:
        return await event.reply("⚠️ **𝖴sᴇ:** `/broadcast <message>` ᴏʀ 𝖱ᴇᴘʟᴀʏ ᴛᴏ ᴀ 𝖬ᴇssᴀɢᴇ.\n𝖠ᴅᴅ `-pin` ᴛᴏ 𝖯ɪɴ 𝖦ʀᴏᴜᴘs.")

    status = await event.reply("🕐 **𝖡ʀᴏᴀᴅᴄᴀsᴛ 𝖲ᴛᴀʀᴛᴇᴅ ɪɴ 𝖡ᴀᴄᴋɢʀᴏᴜɴᴅ...**")

    asyncio.create_task(do_broadcast(event, text, reply, status, pin_broadcast))


async def do_broadcast(event, text, reply, status, pin_broadcast):
    success_users = 0
    success_groups = 0
    pinned_groups = 0
    normal_groups = 0
    for user in users.find():
        try:
            user_id = int(user["user_id"])
            if text:
                await Alishan.send_message(user_id, text)
            elif reply:
                await reply.forward_to(user_id)
            success_users += 1
            await asyncio.sleep(0.05)
        except errors.FloodWaitError as e:
            await asyncio.sleep(e.seconds + 5)
        except Exception:
            continue

    await status.edit("**𝖲ᴇɴᴛ ᴛᴏ 𝖠ʟʟ ᴜsᴇʀs 𝖣ᴏɴᴇ! ɴᴏᴡ 𝖲ᴇɴᴅɪɴɢ ᴛᴏ 𝖦𝗋𝗈𝗎𝗉s...**")

    counter = 0
    for group in groups.find():
        try:
            chat_id = int(group["chat_id"])
            try:
                entity = await Alishan.get_input_entity(chat_id)
            except Exception:
                continue

            sent_msg = None
            if text:
                sent_msg = await Alishan.send_message(entity, text)
            elif reply:
                sent_msg = await reply.forward_to(entity)

            success_groups += 1

            if pin_broadcast and sent_msg:
                try:
                    await Alishan(functions.messages.UpdatePinnedMessageRequest(
                        peer=entity,
                        id=sent_msg.id,
                        silent=False
                    ))
                    pinned_groups += 1
                except errors.ChatAdminRequiredError:
                    normal_groups += 1
                except Exception:
                    normal_groups += 1

            counter += 1
            if counter % 25 == 0:
                await asyncio.sleep(5)
            else:
                await asyncio.sleep(0.1)

        except errors.FloodWaitError as e:
            await asyncio.sleep(e.seconds + 5)
        except Exception as e:
            continue

    result = (
        f"**𝖡ʀᴏᴀᴅᴄᴀsᴛ 𝖢ᴏᴍᴘʟᴇᴛᴇ!**\n\n"
        f"**👤 𝖲ᴇɴᴛ ᴛᴏ 𝖴sᴇʀs :** `{success_users}`\n"
        f"**👥 𝖲ᴇɴᴛ ᴛᴏ 𝖦ʀᴏᴜᴘs :** `{success_groups}`\n"
    )

    if pin_broadcast:
        result += f"**📌 𝖯ɪɴɴᴇᴅ ɪɴ 𝖦ʀᴏᴜᴘs :** `{pinned_groups}`\n**💬 𝖭ᴏʀᴍᴀʟ 𝖲ᴇɴᴛ (𝖭ᴏ 𝖯ɪɴ) :** `{normal_groups}`"

    await status.edit(result)