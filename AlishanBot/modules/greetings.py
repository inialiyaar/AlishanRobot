from telethon import events
from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command
from AlishanBot import config
from telethon import Button
from AlishanBot.modules.helper_funcs.ErrorLog import send_error
from AlishanBot.utils.database import greetings
from AlishanBot.modules.helper_funcs.safedict import SafeDict
from AlishanBot.__init__ import BOT_ID, BOT_USERNAME, BOT_MENTION
import traceback
import re
from AlishanBot.modules.helper_funcs.helpers import is_admin
import time

DATABASE = config.DATABASE_CHANNEL_ID
last_greetings = {}

@add_command("welcome", "wel")
async def Welcome_Handler(event, command_used, args):
    if event.is_private:
        return await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴍᴀᴅᴇ ᴛᴏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs! ")
    user = await event.get_sender()
    if not user:
        return await event.reply("ᴀɴᴏɴʏᴍᴏᴜs ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅ.")
    if not await is_admin(user, event):
        return await event.reply("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴᴅ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪs.")
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)    
    group_greetings = greetings.find_one({"chat_id": chat_id})     
    if not group_greetings:
        welcoming = True
        wel_clean_up = False
        msg_id = 3
    else:
        welcoming = group_greetings.get("welcoming", True)
        wel_clean_up = group_greetings.get("wel_clean_up", False)
        msg_id = group_greetings.get("wel_msg_id", 3)
    if not args:
        stats = await event.reply(f"ɪ ᴀᴍ ᴄᴜʀʀᴇɴᴛʟʏ ᴡᴇʟᴄᴏᴍɪɴɢ ᴜsᴇʀs: {welcoming}\nɪ ᴀᴍ ᴄᴜʀʀᴇɴᴛʟʏ ᴅᴇʟᴇᴛɪɴɢ ᴏʟᴅ ᴡᴇʟᴄᴏᴍᴇs: {wel_clean_up}\n\nᴍᴇᴍʙᴇʀs ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ ᴡᴇʟᴄᴏᴍᴇ ᴡɪᴛʜ:")
        msg = await Alishan.get_messages(DATABASE, ids=msg_id)
        await stats.reply(
            message=msg.text if msg.text else None,
            file=msg.media if msg.media else None, 
            buttons=msg.buttons if msg.buttons else None,
        )
    else:
        if args.lower() in ["on", "yes"]:
            greetings.update_one(
                {"chat_id": chat_id}, 
                {
                    "$set": {
                        "welcoming": True, 
                        "wel_clean_up": wel_clean_up,
                        "wel_msg_id": msg_id, 
                    }, 
                }, 
                upsert=True, 
            )
            return await event.reply("ᴏᴋᴇʏ! ! ɪ'ʟʟ ɢʀᴇᴇᴛ ᴍᴇᴍʙᴇʀs ᴡʜᴇɴ ᴛʜᴇʏ ᴊᴏɪɴ. ")
        if args.lower() in ["off", "no"]:
            greetings.update_one(
                {"chat_id": chat_id}, 
                {
                    "$set": {
                        "welcoming": False, 
                        "wel_clean_up": wel_clean_up,
                        "wel_msg_id": msg_id, 
                    }, 
                }, 
                upsert=True, 
            )
            return await event.reply("ɪ'ʟʟ ɢᴏ ʟᴏᴀғ ᴀʀᴏᴜɴᴅ ᴀɴᴅ ɴᴏᴛ ᴡᴇʟᴄᴏᴍᴇ ᴀɴʏᴏɴᴇ ᴛʜᴇɴ.")
        else:
            return await event.reply("ɪ ᴜɴᴅᴇʀsᴛᴀɴᴅ ᴏɴʟʏ 'on/yes' ᴏʀ 'off/no'")
            
@add_command("goodbye", "gb")
async def Welcome_Handler(event, command_used, args):
    if event.is_private:
        return await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴍᴀᴅᴇ ᴛᴏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs! ")
    user = await event.get_sender()
    if not user:
        return await event.reply("ᴀɴᴏɴʏᴍᴏᴜs ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅ.")
    if not await is_admin(user, event):
        return await event.reply("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴᴅ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪs.")    
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)    
    group_greetings = greetings.find_one({"chat_id": chat_id})     
    if not group_greetings:
        goodbye = True
        gb_clean_up = False
        msg_id = 10
    else:
        goodbye = group_greetings.get("goodbye", True)
        gb_clean_up = group_greetings.get("wel_clean_up", False)
        msg_id = group_greetings.get("gb_msg_id", 10)
    if not args:
        stats = await event.reply(f"ɪ ᴀᴍ ᴄᴜʀʀᴇɴᴛʟʏ ɢᴏᴏᴅʙʏᴇ ᴛᴏ ᴜsᴇʀs: {goodbye}\nɪ ᴀᴍ ᴄᴜʀʀᴇɴᴛʟʏ ᴅᴇʟᴇᴛɪɴɢ ᴏʟᴅ ɢᴏᴏᴅʙʏᴇs: {gb_clean_up}\n\nᴍᴇᴍʙᴇʀs ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ ɢᴏᴏᴅʙʏᴇ ᴡɪᴛʜ:")
        msg = await Alishan.get_messages(DATABASE, ids=msg_id)
        await stats.reply(
            message=msg.text if msg.text else None,
            file=msg.media if msg.media else None, 
            buttons=msg.buttons if msg.buttons else None,
        )
    else:
        if args.lower() in ["on", "yes"]:
            greetings.update_one(
                {"chat_id": chat_id}, 
                {
                    "$set": {
                        "goodbye": True, 
                        "gb_clean_up": gb_clean_up,
                        "gb_msg_id": msg_id, 
                    }, 
                }, 
                upsert=True, 
            )
            return await event.reply("ᴏᴋᴇʏ! ! ɪ'ʟʟ ɢʀᴇᴇᴛ ᴍᴇᴍʙᴇʀs ᴡʜᴇɴ ᴛʜᴇʏ ᴊᴏɪɴ. ")
        if args.lower() in ["off", "no"]:
            greetings.update_one(
                {"chat_id": chat_id}, 
                {
                    "$set": {
                        "goodbye": False, 
                        "gb_clean_up": gb_clean_up,
                        "gb_msg_id": msg_id, 
                    }, 
                }, 
                upsert=True, 
            )
            return await event.reply("ɪ'ʟʟ ɢᴏ ʟᴏᴀғ ᴀʀᴏᴜɴᴅ ᴀɴᴅ ɴᴏᴛ ᴡᴇʟᴄᴏᴍᴇ ᴀɴʏᴏɴᴇ ᴛʜᴇɴ.")
        else:
            return await event.reply("ɪ ᴜɴᴅᴇʀsᴛᴀɴᴅ ᴏɴʟʏ 'on/yes' ᴏʀ 'off/no'")            
            
@add_command("setwelcome", "setwel")   
async def set_new_welcome(event, command_used, args):
    if event.is_private:
        return await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴍᴀᴅᴇ ᴛᴏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs!")
    user = await event.get_sender()
    if not user:
        return await event.reply("ᴀɴᴏɴʏᴍᴏᴜs ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅ.")
    if not await is_admin(user, event):
        return await event.reply("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴᴅ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪs.")    
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)       
    sender = await event.get_sender()
    if not sender:
        return await event.reply("ᴀɴᴏɴʏᴍᴏᴜs ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅ. ")
    if sender.bot:
        return
    if not args and not event.is_reply:
        return await event.reply("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ɢɪᴠᴇ ᴛʜᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ sᴏᴍᴇ ᴄᴏɴᴛᴇɴᴛ.")
    if event.is_reply:
        replied = await event.get_reply_message()
        text = replied.message or ""
        media = replied.media or None
        buttons = replied.buttons or None
    else:
        media = event.media or None
        text = args
        buttons = None
    group_greetings = greetings.find_one({"chat_id": chat_id})     
    if not group_greetings:
        if not media: 
            msg = await Alishan.send_message(
                DATABASE, 
                text, 
                buttons=buttons,
            ) 
        else:
             msg = await Alishan.send_file(
                DATABASE, 
                caption=text, 
                file=media, 
                buttons=buttons,
            )   
        msg_id = msg.id
    else:
        msg_id = group_greetings.get("wel_msg_id", 3) 
        if msg_id == 3:
            if not media: 
                msg = await Alishan.send_message(
                    DATABASE, 
                    text, 
                    buttons=buttons,
                    ) 
            else:
                msg = await Alishan.send_file(
                    DATABASE, 
                    caption=text, 
                    file=media, 
                    buttons=buttons,
                    )   
        else:
            msg = await Alishan.get_messages(DATABASE, ids=msg_id)
            if msg.media:
                await msg.delete()  
                if not media: 
                    msg = await Alishan.send_message(
                        DATABASE, 
                        text, 
                        buttons=buttons,
                        ) 
                else:
                    msg = await Alishan.send_file(
                        DATABASE, 
                        caption=text, 
                        file=media, 
                        buttons=buttons,
                        )   
            else:
                await Alishan.edit_message(
                    DATABASE, 
                    msg_id, 
                    text=text, 
                    file=media, 
                    buttons=buttons,
                    ) 
    msg_id = msg.id
    greetings.update_one(
            {"chat_id": chat_id}, 
            {
                "$set": {
                    "wel_msg_id": msg_id, 
                }, 
            }, 
            upsert=True, 
        )
    return await event.reply("ʏᴇss!! ᴛʜɪs ɴᴇᴡ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ ʜᴀs ʙᴇᴇɴ sᴀᴠᴇᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ. ") 
    
@add_command("setgoodbye", "setgb")   
async def set_new_welcome(event, command_used, args):
    if event.is_private:
        return await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴍᴀᴅᴇ ᴛᴏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs!")
    user = await event.get_sender()
    if not user:
        return await event.reply("ᴀɴᴏɴʏᴍᴏᴜs ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅ.")
    if not await is_admin(user, event):
        return await event.reply("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴᴅ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪs.")    
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)       
    sender = await event.get_sender()
    if not sender:
        return await event.reply("ᴀɴᴏɴʏᴍᴏᴜs ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅ. ")
    if sender.bot:
        return
    if not args and not event.is_reply:
        return await event.reply("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ɢɪᴠᴇ ᴛʜᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ sᴏᴍᴇ ᴄᴏɴᴛᴇɴᴛ.")
    if event.is_reply:
        replied = await event.get_reply_message()
        text = replied.message or ""
        media = replied.media or None
        buttons = replied.buttons or None
    else:
        media = event.media or None
        text = args
        buttons = None
    group_greetings = greetings.find_one({"chat_id": chat_id})     
    if not group_greetings:
        if not media: 
            msg = await Alishan.send_message(
                DATABASE, 
                text, 
                buttons=buttons,
            ) 
        else:
             msg = await Alishan.send_file(
                DATABASE, 
                caption=text, 
                file=media, 
                buttons=buttons,
            )   
        msg_id = msg.id
    else:
        msg_id = group_greetings.get("gb_msg_id", 10) 
        if msg_id == 10:
            if not media: 
                msg = await Alishan.send_message(
                    DATABASE, 
                    text, 
                    buttons=buttons,
                    ) 
            else:
                msg = await Alishan.send_file(
                    DATABASE, 
                    caption=text, 
                    file=media, 
                    buttons=buttons,
                    )   
        else:
            msg = await Alishan.get_messages(DATABASE, ids=msg_id)
            if msg.media:
                await msg.delete()  
                if not media: 
                    msg = await Alishan.send_message(
                        DATABASE, 
                        text, 
                        buttons=buttons,
                        ) 
                else:
                    msg = await Alishan.send_file(
                        DATABASE, 
                        caption=text, 
                        file=media, 
                        buttons=buttons,
                        )   
            else:
                await Alishan.edit_message(
                    DATABASE, 
                    msg_id, 
                    text=text, 
                    file=media, 
                    buttons=buttons,
                    ) 
    msg_id = msg.id
    greetings.update_one(
            {"chat_id": chat_id}, 
            {
                "$set": {
                    "gb_msg_id": msg_id, 
                }, 
            }, 
            upsert=True, 
        )
    return await event.reply("ʏᴇss!! ᴛʜɪs ɴᴇᴡ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ ʜᴀs ʙᴇᴇɴ sᴀᴠᴇᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ. ")     
    
@Alishan.on(events.ChatAction)  
async def Greetings_Handler(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    user = await event.get_user()
    if not user:
        return
    if not (
        event.user_left or 
        event.user_kicked or 
        event.user_joined or 
        event.user_added
        ):
        return
    now = time.time()
    if chat_id not in last_greetings:
        last_greetings[chat_id] = {}
    if user.id in last_greetings[chat_id] and now - last_greetings[chat_id][user.id] <5:
        return
    last_greetings[chat_id][user.id] = now    
    first = user.first_name or ""
    last = user.last_name or ""
    fullname = (first + " " + last).strip()
    username = f"@{user.username}" if user.username else ""
    id = user.id
    mention = f"<a href='tg://user?Id={id}'>{first}</a>"
    chatname = chat.title or ""
    safe_data = SafeDict(
            chatname=chatname, 
            mention=mention, 
            fullname=fullname, 
            last=last, 
            first=first, 
            username=username, 
            id=id,
            chatid=chat_id, 
        )    
    group_greetings = greetings.find_one({"chat_id": chat_id})    
    if event.user_left or event.user_kicked:
        if user.id == BOT_ID:
            return
        if not group_greetings:
            msg = await Alishan.get_messages(DATABASE, ids=10)
        else:
            goodbye = group_greetings.get("goodbye", True)
            if not goodbye:
                return
        if group_greetings:
            if not goodbye:
                return
            msg_id = group_greetings.get("gb_msg_id", 10) 
            msg = await Alishan.get_messages(DATABASE, ids=msg_id)
        text = msg.text if msg.text else None
        if text:
            text = text.format_map(safe_data)
        media = msg.media if msg.media else None
        buttons_list = msg.buttons if msg.buttons else None
        await event.reply(
            message=text, 
            file=media, 
            buttons=buttons_list, 
            parse_mode="html"
        )
    if event.user_added or event.user_joined:
        if user.id == BOT_ID:
            return
        if not group_greetings:
            msg = await Alishan.get_messages(DATABASE, ids=3)
        else:
            welcoming = group_greetings.get("welcoming", True)
            if not welcoming:
                return
        if group_greetings:
            if not welcoming:
                return
            msg_id = group_greetings["wel_msg_id"] 
            msg = await Alishan.get_messages(DATABASE, ids=msg_id)
        text = msg.text if msg.text else None
        if text:
            text = text.format_map(safe_data)
        media = msg.media if msg.media else None
        buttons_list = msg.buttons if msg.buttons else None
        await event.reply(
            message=text, 
            file=media, 
            buttons=buttons_list, 
            parse_mode="html"
        )