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
PROTECT_COST_PER_DAY = 200
TZ = ZoneInfo("Asia/Kolkata")

if datetime.now(TZ).hour == 0:
    economy.update_many({}, {"$set": {"daily": False}})

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
        return await event.reply("These commands you can use only in groups.")
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)    
    if event.is_group:
        chat_settings = economy_settings.find_one({"chat_id": chat_id})
        if chat_settings:
            if not chat_settings["enabled"] and command_used not in ["close", "open"]:
                return await event.reply("Economy game is disabled in this group\n\nUse /open to enable.")
            
    sender = await event.get_sender()
    if command_used not in ["toprich", "topkill"] and not sender:
        return await event.reply("You are anonymous, can't use these commands.")
    if sender.bot:
        return await event.reply("Bot can't use economy!")
    user_id = sender.id 
    if command_used in ["open", "close"] and not await is_admin(sender, event):
        return await event.reply("Only admin can use these commands.")
    if command_used == "open":
        chat_settings = economy_settings.find_one({"chat_id": chat_id})
        if chat_settings:
            if chat_settings["enabled"] is False:
                economy_settings.update_one(
                    {"chat_id": chat_id}, 
                    {"$set": {"enabled": True}}, 
                    upsert=True
                )
                return await event.reply("Now economy game is enabled in this group.")
            else: 
                return await event.reply("Economy game is already enabled in this group.")
        else:
            # If entry doesn't exist, assume it's currently disabled and enable it.
            # Or insert the new setting and assume it was enabled by default, but based on your "else" block below, 
            # I'll stick to logic similar to the original, but simplified.
            economy_settings.insert_one(
                {"chat_id": chat_id, 
                "enabled": True}, 
            )
            return await event.reply("Now economy game is enabled in this group.") # Assuming enabling is the intent if it's not found
    
    if command_used == "close":
        chat_settings = economy_settings.find_one({"chat_id": chat_id})
        if chat_settings:
            if chat_settings["enabled"] is True:
                economy_settings.update_one(
                    {"chat_id": chat_id}, 
                    {"$set": {"enabled": False}}, 
                    upsert=True
                )
                return await event.reply("Now economy game is disabled in this group.")
            else:
                return await event.reply("Economy game is already disabled in this group.")      
        else:
            economy_settings.insert_one(
                    {"chat_id": chat_id, 
                    "enabled": False}, 
                )
            return await event.reply("Now economy game is disabled in this group.")   
            
    if command_used in ["rob", "kill", "give"] and not event.is_reply:
        await event.reply(f"Please reply to a user to {command_used} them.")
        return # Added return to stop execution if no reply

    if command_used in ["bal", "revive", "protect"]:
        target_user_id = user_id
        if event.is_reply:
            replied = await event.get_reply_message()
            target_sender = await Alishan.get_entity(replied.sender_id)
            if not target_sender:
                return await event.reply("You can't use these commands on anonymous users.")
            if target_sender.bot:
                return await event.reply("You can't use these commands on bots.")
            target_user_id = target_sender.id
        else:
            target_sender = sender

        user_data = economy.find_one({"user_id": target_user_id})
        if not user_data:
            user_data = {
                "user_id": target_user_id, 
                "balance": 100,
                "kills": 0,
                "dead": False, 
                "daily": False,
            }
            economy.insert_one(user_data)
        
        if command_used == "bal":
            if user_data.get("dead", False):
                 status = "☠️ <b>Status :</b> Dead"
            else:
                status = "♥ <b>Status :</b> Alive"
            rank = get_rank(target_user_id)
            return await event.reply(
                f"👤 <b>Name :</b> <a href='tg://user?id={target_user_id}'>{target_sender.first_name}</a>\n"
                f"💰 <b>Total Balance :</b> ${user_data['balance']}\n"
                f"🏆 <b>Global Rank :</b> {rank}\n"
                f"{status}\n"
                f"⚔️ <b>Kills :</b> {user_data['kills']}", 
                parse_mode="html"
            )

    if command_used in ["give", "rob", "kill", "transfer", "daily", "crime", "bet"]:
        user_data = economy.find_one({"user_id": user_id})
        if not user_data:
            user_data = {
                "user_id": user_id, 
                "balance": 100,
                "kills": 0,
                "dead": False, 
                "daily": False,
            }
            economy.insert_one(user_data)        

    if command_used == "daily":
        if not user_data.get("daily", False):
            amount = random.randint(DAILY_MIN, DAILY_MAX)
            # balance is already handled by $inc, no need to recalculate locally unless needed for the message
            economy.update_one(
                {"user_id": user_id},
                {
                    "$inc": {"balance": amount},
                    "$set": {"daily": True}
                }
            )
            return await event.reply(f"You earned ${amount} from your daily gift 🎁!")
        else:
            return await event.reply("Hey, wait! You already claimed your daily gift. Try next day!")

    # From here onwards, we assume event.is_reply is True for ['rob', 'kill', 'give']
    if event.is_reply:
        replied = await event.get_reply_message() 
        user_entity = await Alishan.get_entity(replied.sender_id)
    else:
        # Should not happen based on checks above, but needed for subsequent logic if not returned
        return 

    if command_used in ["rob", "kill", "give"] and user_entity.id == BOT_ID:
        return await event.reply(f"Hehe, you can't {command_used} myself.") 
    if command_used in ["rob", "kill", "give"] and user_entity.id == sender.id:
        return await event.reply(f"You can't {command_used} yourself.")       
    if user_entity.bot and command_used in ["rob", "kill", "give"]:
        return await event.reply("You can't use these commands on a bot.")

    if command_used == "kill":
        pass
        