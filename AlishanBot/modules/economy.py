import time
import random
from datetime import datetime
from zoneinfo import ZoneInfo

from telethon import Button
from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command
from AlishanBot.utils.database import economy, economy_settings
from AlishanBot.modules.helper_funcs.helpers import is_admin
from AlishanBot.__init__ import BOT_ID

DAILY_MIN = 200
DAILY_MAX = 500
REVIVE_COST = 500
TZ = ZoneInfo("Asia/Kolkata")

ECON_CMDS = ["open", "close", "bal", "give", "rob", "kill","revive", "protect", "transfer", "toprich", "topkill","daily", "crime", "bet"]

def get_rank(user_id):
    cursor = economy.find().sort("balance", -1)

    rank = 1
    for u in cursor:
        if u["user_id"] == int(user_id):
            return rank
        rank += 1

    return rank
    
@add_command(*ECON_CMDS)
async def economy_system(event, command_used, args):
    if command_used not in ["toprich", "topkill", "bal", "daily", "bet", "crime", "protect", "revive"] and event.is_private:
        return await event.reply("ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘs. ")
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)    
    if event.is_group:
        chat = economy_settings.find_one({"chat_id": chat_id})
        if chat:
            if not chat["enabled"] and command_used not in ["close", "open"]:
                return await event.reply("ᴇᴄᴏɴᴏᴍʏ ɢᴀᴍᴇ ɪs ᴅɪsᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ\n\nᴜsᴇ /open ᴛᴏ ᴇɴᴀʙʟᴇ.")
            
    sender = await event.get_sender()
    if command_used not in ["toprich", "topkill"] and not sender:
        return await event.reply("ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅ.")
    if command_used not in ["open", "close"] and not await is_admin(sender, event):
        return await event.reply("ᴏɴʟʏ ᴀᴅᴍɪɴ ᴄᴀɴ ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅ.")
    if command_used == "open":
        chat = economy_settings.find_one({"chat_id": chat_id})
        if chat:
            if chat["enabled"] is False:
                economy_settings.update_one(
                    {"chat_id": chat_id}, 
                    {"$set": {"enabled": True}}, 
                    upsert=True
                )
                return await event.reply("ɴᴏᴡ ᴇᴄᴏɴᴏᴍʏ ɢᴀᴍᴇ ɪs ᴇɴᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ. ")
            else: 
                return await event.reply("ᴇᴄᴏɴᴏᴍʏ ɢᴀᴍᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.")
        else:
            return await event.reply("ᴇᴄᴏɴᴏᴍʏ ɢᴀᴍᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.")
    if command_used == "close":
        chat = economy_settings.find_one({"chat_id": chat_id})
        if chat:
            if chat["enabled"] is True:
                economy_settings.update_one(
                    {"chat_id": chat_id}, 
                    {"$set": {"enabled": False}}, 
                    upsert=True
                )
                return await event.reply("ɴᴏᴡ ᴇᴄᴏɴᴏᴍʏ ɢᴀᴍᴇ ɪs ᴅɪsᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ. ")
            else:
                return await event.reply("ᴇᴄᴏɴᴏᴍʏ ɢᴀᴍᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.")      
        else:
            economy_settings.insert_one(
                    {"chat_id": chat_id, 
                    "enabled": False}, 
                )
            return await event.reply("ɴᴏᴡ ᴇᴄᴏɴᴏᴍʏ ɢᴀᴍᴇ ɪs ᴅɪsᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.")   
    if command_used in ["rob", "kill", "give"] and not event.is_reply:
        await event.reply(f"ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ ᴛᴏ {command_used} ᴛʜᴇᴍ.")
    if command_used in ["bal", "revive", "protect"]:
        if event.is_reply:
            replied = await event.get_reply_message()
            user_entity = await Alishan.get_entity(replied.sender_id)
            if not user_entity:
                return await event.reply("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅ ᴏɴ ᴀɴᴏɴʏᴍᴏᴜs.")
            if user_entity.bot:
                return await event.reply("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅ ᴏɴ ʙᴏᴛ.")
        else:
            user_entity = await event.get_sender()
        if command_used == "bal":
            user_id = int(user_entity.id)
            user = economy.find_one({"user_id": user_id})
            if not user:
                user = {
                    "user_id": user_id, 
                    "balance": 100,
                    "kills": 0,
                    "dead": False
                }
                economy.insert_one(user)
            if user["dead"]:
                 status = "☠️ <b>sᴛᴀᴛᴜs :</b> ᴅᴇᴀᴅ"
            else:
                status = "♥ <b>sᴛᴀᴛᴜs :</b> ᴀʟɪᴠᴇ"
            rank = get_rank(user_id)
            return await event.reply(f"👤 <b>ɴᴀᴍᴇ :</b> <a href='{user_entity.id}'>{user_entity.first_name}</a>\n💰 <b>ᴛᴏᴛᴀʟ ʙᴀʟᴀɴᴄᴇ :</b> ${user['balance']}\n🏆 <b>ɢʟᴏʙᴀʟ_ʀᴀɴᴋ :</b> {rank}\n{status}\n⚔️ <b>ᴋɪʟʟs :</b> {user['kills']}", parse_mode="html")
    replied = await event.get_reply_message() 
    user_entity = await Alishan.get_entity(replied.sender_id)
    if command_used in ["rob", "kill", "give"] and user_entity.id == BOT_ID:
        return await event.reply(f"ʜᴇʜᴇ, ʏᴏᴜ ᴄᴀɴ'ᴛ {command_used} ᴍʏ sᴇʟғ.") 
    if command_used in ["rob", "kill", "give"] and user_entity.id == sender.id:
        return await event.reply(f"ʏᴏᴜ ᴄᴀɴ'ᴛ {command_used} ʏᴏᴜʀ sᴇʟғ.")       
    if user_entity.bot and command_used in ["rob", "kill", "give"]:
        return await event.reply("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅ ᴏɴ ʙᴏᴛ. ")