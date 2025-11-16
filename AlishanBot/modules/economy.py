import time
from telethon import events, Button
from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command
from AlishanBot.utils.database import economy, economy_settings


# ────────────────────────────────────────────────────────────────
# DATABASE HELPERS
# ────────────────────────────────────────────────────────────────

async def get_user(user_id):
    user = economy.find_one({"user_id": user_id})
    if not user:
        user = {
            "user_id": user_id,
            "balance": 0,
            "kills": 0,
            "protection_until": 0,
            "is_dead": False
        }
        economy.insert_one(user)
    return user


async def save_user(user):
    economy.update_one({"user_id": user["user_id"]}, {"$set": user}, upsert=True)


async def is_group_open(chat_id):
    res = economy_settings.find_one({"chat_id": chat_id})
    if not res:
        economy_settings.insert_one({"chat_id": chat_id, "enabled": True})
        return True
    return res.get("enabled", True)


async def set_group_status(chat_id, status):
    economy_settings.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )


ECON_CMDS = [
    "open", "close", "bal", "give", "rob", "kill",
    "revive", "protect", "transfer", "toprich", "topkill"
]


async def get_global_rank(user_id, by="balance"):
    if by == "balance":
        sorted_users = list(economy.find().sort("balance", -1))
    else:
        sorted_users = list(economy.find().sort("kills", -1))
    for idx, u in enumerate(sorted_users, start=1):
        if u["user_id"] == user_id:
            return idx
    return len(sorted_users)



@add_command(*ECON_CMDS)
async def economy_system(event, command_used, args):
    chat_id = event.chat_id
    sender = event.sender_id

    if command_used not in ["toprich", "topkill"]:
        if event.is_private and command_used not in ["bal"]:
            return await event.reply("❌ **ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ.**")

        if not await is_group_open(chat_id) and command_used not in ["open", "close"]:
            return await event.reply("❌ **ᴇᴄᴏɴᴏᴍʏ sʏsᴛᴇᴍ ɪs ᴄʟᴏsᴇᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ!**")

    if command_used == "open":
        await set_group_status(chat_id, True)
        return await event.reply("✅ **ᴇᴄᴏɴᴏᴍʏ sʏsᴛᴇᴍ ɪs ɴᴏᴡ ᴏᴘᴇɴ!**")

    if command_used == "close":
        await set_group_status(chat_id, False)
        return await event.reply("❌ **ᴇᴄᴏɴᴏᴍʏ sʏsᴛᴇᴍ ɪs ɴᴏᴡ ᴄʟᴏsᴇᴅ!**")

    user = await get_user(sender)

    if command_used == "bal":
        reply = await event.get_reply_message()
        target_id = reply.sender_id if reply else sender
        target = await get_user(target_id)

        status = "ᴀʟɪᴠᴇ" if not target["is_dead"] else "ᴅᴇᴀᴅ"
        try:
            user_entity = await Alishan.get_entity(target_id)
            name = user_entity.first_name or str(target_id)
        except:
            name = str(target_id)
        rank = await get_global_rank(target_id, by="balance")

        msg = f"👤 **ɴᴀᴍᴇ:** {name}\n💰 **ʙᴀʟᴀɴᴄᴇ:** {target['balance']}\n🔪 **ᴋɪʟʟs:** {target['kills']}\n❤️ **sᴛᴀᴛᴜs:** {status}\n🏆 **ɢʟᴏʙᴀʟ ʀᴀɴᴋ:** {rank}"
        return await event.reply(msg)

    if command_used == "give":
        reply = await event.get_reply_message()
        if not reply:
            return await event.reply("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's:\n`/give ᴀᴍᴏᴜɴᴛ`")

        if not args or not args[0].isdigit():
            return await event.reply("❌ ɢɪᴠᴇ ᴍᴇ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ!")

        amount = int(args[0])
        if amount <= 0:
            return await event.reply("❌ ᴀᴍᴏᴜɴᴛ ᴍᴜsᴛ ʙᴇ ᴘᴏsɪᴛɪᴠᴇ!")

        receiver = await get_user(reply.sender_id)

        fee = amount // 10
        total = amount + fee

        if user["balance"] < total:
            return await event.reply("❌ **𝗜𝗻𝘀𝘂𝗳𝗳𝗶𝗰𝗶𝗲𝗻𝘁 𝗯𝗮𝗹𝗮𝗻𝗰𝗲!**")

        user["balance"] -= total
        receiver["balance"] += amount

        await save_user(user)
        await save_user(receiver)

        return await event.reply(
            f"🎁 **ɢɪғᴛᴇᴅ:** {amount}  🔥 **ғᴇᴇ:** {fee}"
        )

    if command_used == "rob":
        reply = await event.get_reply_message()
        if not reply:
            return await event.reply("ʀᴇᴘʟʏ ᴛᴏ sᴏᴍᴇᴏɴᴇ ғɪʀsᴛ!")

        if not args or not args[0].isdigit():
            return await event.reply("ɢɪʙᴇ ᴍᴇ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ!")

        amt = int(args[0])
        victim = await get_user(reply.sender_id)

        if victim["protection_until"] > time.time():
            return await event.reply("🛡️ **ᴜsᴇʀ ɪs ᴜɴᴅᴇʀ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ!**")

        if victim["balance"] < amt:
            return await event.reply("❌ ᴛʜᴇ ᴠɪᴄᴛɪᴍ ʜᴀs ɴᴏ ᴍᴏɴᴇʏ!")

        victim["balance"] -= amt
        user["balance"] += amt

        await save_user(user)
        await save_user(victim)

        return await event.reply(f"🔪 **ʏᴏᴜ ʀᴏʙʙᴇᴅ:** {amt}")

    if command_used == "kill":
        reply = await event.get_reply_message()
        if not reply:
            return await event.reply("ʀᴇᴘʟʏ ᴛᴏ sᴏᴍᴇᴏɴᴇ!")

        target = await get_user(reply.sender_id)

        if target["is_dead"]:
            return await event.reply("❌ ᴀʟʀᴇᴀᴅʏ ᴅᴇᴀᴅ!")

        target["is_dead"] = True
        user["kills"] += 1

        await save_user(target)
        await save_user(user)

        return await event.reply("💀 **ᴜsᴇʀ ᴋɪʟʟᴇᴅ!**")

    if command_used == "revive":
        reply = await event.get_reply_message()
        target_id = reply.sender_id if reply else sender
        target = await get_user(target_id)

        target["is_dead"] = False
        await save_user(target)

        return await event.reply("❤️ **ᴜsᴇʀ ʀᴇᴠɪᴠᴇᴅ!**")

    if command_used == "protect":
        if not args:
            return await event.reply("ᴜsᴇ: `/protect 1d | 2d`")

        days = args[0].replace("d", "")
        if not days.isdigit():
            return await event.reply("❌ ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ!")

        secs = int(days) * 24 * 3600

        user["protection_until"] = time.time() + secs
        await save_user(user)

        return await event.reply(f"🛡️ **ᴘʀᴏᴛᴇᴄᴛᴇᴅ ғᴏʀ {days} ᴅᴀʏ(ꜱ)!**")

    if command_used == "transfer":
        owner = (await Alishan.get_permissions(chat_id, sender)).is_creator
        if not owner:
            return await event.reply("❌ **ᴏɴʟʏ group ᴏᴡɴᴇʀ!**")

        if not args or not args[0].isdigit():
            return await event.reply("ᴀᴍᴏᴜɴᴛ + ʀᴇᴘʟᴛ ᴛᴏ ᴜsᴇʀ!")

        amount = int(args[0])
        reply = await event.get_reply_message()
        if not reply:
            return await event.reply("ʀᴇᴘʟʏ ᴛᴏ sᴏᴍᴇᴏɴᴇ!")

        target = await get_user(reply.sender_id)
        target["balance"] += amount
        await save_user(target)

        return await event.reply(f"💰 **ᴛʀᴀɴsғᴇʀʀᴇᴅ:** {amount}")

    if command_used == "toprich":
        data = economy.find().sort("balance", -1).limit(10)
        msg = "🏆 **ᴛᴏᴘ 10 ʀɪᴄʜᴇsᴛ**:\n\n"
        i = 1
        for u in data:
            try:
                user_entity = await Alishan.get_entity(u["user_id"])
                name = user_entity.first_name or str(u["user_id"])
            except:
                name = str(u["user_id"])
            msg += f"{i}. {name}: {u['balance']}\n"
            i += 1
        return await event.reply(msg)

    if command_used == "topkill":
        data = economy.find().sort("kills", -1).limit(10)
        msg = "🔪 **ᴛᴏᴘ 10 ᴋɪʟʟᴇʀs**:\n\n"
        i = 1
        for u in data:
            try:
                user_entity = await Alishan.get_entity(u["user_id"])
                name = user_entity.first_name or str(u["user_id"])
            except:
                name = str(u["user_id"])
            msg += f"{i}. {name}: {u['kills']}\n"
            i += 1
        return await event.reply(msg)