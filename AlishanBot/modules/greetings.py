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
last_sent = {} 
  
DEFAULT_WELCOME_TEXT = "Hey there {first}, and welcome to {chatname}! How are you?"  
DEFAULT_GOODBYE_TEXT = "Nice Knowing you {fullname}! See you soon later."  
  
@add_command("welcome", "wel")  
async def Welcome_Handler(event, command_used, args):  
    if event.is_private:  
        return await event.reply("This command is made to be used in groups! ")  
    user = await event.get_sender()  
    if not user:  
        return await event.reply("Anonymous can't use these commands.")  
    if not await is_admin(user, event):  
        return await event.reply("You need to be an admin to do this.")  
    chat = await event.get_chat()  
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)      
    group_greetings = greetings.find_one({"chat_id": chat_id})       
    if not group_greetings:  
        welcoming = True  
        wel_clean_up = False  
        msg_id = None  
    else:  
        welcoming = group_greetings.get("welcoming", True)  
        wel_clean_up = group_greetings.get("wel_clean_up", False)  
        msg_id = group_greetings.get("wel_msg_id", None)  
    if not args:  
        stats = await event.reply(f"I am currently welcoming users: {welcoming}\nI am currently deleting old welcomes: {wel_clean_up}\n\nMembers are currently welcome with:")  
        if not msg_id:  
            text = DEFAULT_WELCOME_TEXT  
        else:      
            msg = await Alishan.get_messages(DATABASE, ids=msg_id)  
            text = msg.text  
        await stats.reply(  
            message=text,  
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
            return await event.reply("Okay!! I'll greet members when they join.")  
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
            return await event.reply("I'll go loaf around and not welcome anyone then.")  
        else:  
            return await event.reply("I understand only 'on/yes' or 'off/no'")  
              
@add_command("goodbye", "gb")  
async def Welcome_Handler(event, command_used, args):  
    if event.is_private:  
        return await event.reply("This command is made to be used in groups! ")  
    user = await event.get_sender()  
    if not user:  
        return await event.reply("Anonymous can't use these commands.")  
    if not await is_admin(user, event):  
        return await event.reply("You need to be an admin to do this.")      
    chat = await event.get_chat()  
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)      
    group_greetings = greetings.find_one({"chat_id": chat_id})       
    if not group_greetings:  
        goodbye = True  
        gb_clean_up = False  
        msg_id = None  
    else:  
        goodbye = group_greetings.get("goodbye", True)  
        gb_clean_up = group_greetings.get("gb_clean_up", False)  
        msg_id = group_greetings.get("gb_msg_id", None)  
    if not args:  
        stats = await event.reply(f"I am currently goodbye to users: {goodbye}\nI am currently deleting old goodbyes: {gb_clean_up}\n\nMembers are currently goodbye with:")  
        if not msg_id:  
            text = DEFAULT_GOODBYE_TEXT  
        else:      
            msg = await Alishan.get_messages(DATABASE, ids=msg_id)  
            text = msg.text  
        await stats.reply(  
            message=text,  
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
            return await event.reply("Okay!! I'll greet members when they join.")  
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
            return await event.reply("I'll go loaf around and not welcome anyone then.")  
        else:  
            return await event.reply("I understand only 'on/yes' or 'off/no'")              
              
@add_command("setwelcome", "setwel")     
async def set_new_welcome(event, command_used, args):  
    if event.is_private:  
        return await event.reply("This command is made to be used in groups!")  
    user = await event.get_sender()  
    if not user:  
        return await event.reply("Anonymous can't use these commands.")  
    if not await is_admin(user, event):  
        return await event.reply("You need to be an admin to do this.")      
    chat = await event.get_chat()  
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)         
    sender = await event.get_sender()  
    if not sender:  
        return await event.reply("Anonymous can't use these commands. ")  
    if sender.bot:  
        return  
    if not args and not event.is_reply:  
        return await event.reply("You need to give the welcome message some content.")  
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
        msg_id = group_greetings.get("wel_msg_id", None)   
        if not msg_id:  
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
    return await event.reply("Yes!! This new welcome message has been saved in my database.")   
      
@add_command("setgoodbye", "setgb")
async def set_new_goodbye(event, command_used, args):
    if event.is_private:
        return await event.reply("This command is made to be used in groups!")

    sender = await event.get_sender()
    if not sender:
        return await event.reply("Anonymous can't use these commands.")
    if not await is_admin(sender, event):
        return await event.reply("You need to be an admin to do this.")

    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)

    if not args and not event.is_reply:
        return await event.reply("You need to give the welcome message some content.")

    if event.is_reply:
        replied = await event.get_reply_message()
        text = replied.message or ""
        media = replied.media or None
        buttons = replied.buttons or None
    else:
        text = args
        media = event.media or None
        buttons = None

    group_greetings = greetings.find_one({"chat_id": chat_id})

    if not group_greetings or not group_greetings.get("gb_msg_id"):
        if not media:
            msg = await Alishan.send_message(DATABASE, text, buttons=buttons)
        else:
            msg = await Alishan.send_file(DATABASE, caption=text, file=media, buttons=buttons)
    else:
        msg_id = group_greetings["gb_msg_id"]
        old = await Alishan.get_messages(DATABASE, ids=msg_id)

        if old.media:
            await old.delete()
            if not media:
                msg = await Alishan.send_message(DATABASE, text, buttons=buttons)
            else:
                msg = await Alishan.send_file(DATABASE, caption=text, file=media, buttons=buttons)
        else:
            await Alishan.edit_message(DATABASE, msg_id, text=text, file=media, buttons=buttons)
            msg = await Alishan.get_messages(DATABASE, ids=msg_id)

    greetings.update_one(
        {"chat_id": chat_id},
        {"$set": {"gb_msg_id": msg.id}},
        upsert=True,
    )

    return await event.reply("Yes!! This new goodbye message has been saved in my database.") 
      
@Alishan.on(events.ChatAction)
async def Greetings_Handler(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    user = await event.get_user()
    if not user:
        return

    if not (event.user_left or event.user_kicked or event.user_joined or event.user_added):
        return

    now = time.time()
    last_greetings.setdefault(chat_id, {})
    if user.id in last_greetings[chat_id] and now - last_greetings[chat_id][user.id] < 5:
        return
    last_greetings[chat_id][user.id] = now

    first = user.first_name or ""
    last = user.last_name or ""
    fullname = (first + " " + last).strip()
    username = f"@{user.username}" if user.username else ""
    mention = f"<a href='tg://user?Id={user.id}'>{first}</a>"
    chatname = chat.title or ""

    safe_data = SafeDict(
        chatname=chatname,
        mention=mention,
        fullname=fullname,
        last=last,
        first=first,
        username=username,
        id=user.id,
        chatid=chat_id,
    )

    group_greetings = greetings.find_one({"chat_id": chat_id}) or {}
    if event.user_left or event.user_kicked:
        if user.id == BOT_ID:
            return
    
        goodbye = group_greetings.get("goodbye", True) if group_greetings else True
        if not goodbye:
            return
    
        wel_clean_up = group_greetings.get("wel_clean_up", False)
    
        msg_id = group_greetings.get("gb_msg_id") if group_greetings else None
    
        if not msg_id:
            text = DEFAULT_GOODBYE_TEXT
            media = None
            buttons = None
        else:
            temp = await Alishan.get_messages(DATABASE, ids=msg_id)
            text = temp.text or DEFAULT_GOODBYE_TEXT
            media = temp.media
            buttons = temp.buttons
    
        text = text.format_map(safe_data)
    
        sent = await event.reply(message=text, file=media, buttons=buttons, parse_mode="html")
    
        if wel_clean_up:
            old = last_sent.get(chat_id)
            if old:
                try:
                    await Alishan.delete_messages(chat_id, old)
                except:
                    pass
    
            last_sent[chat_id] = sent.id
    
        return
    if event.user_joined or event.user_added:
        if user.id == BOT_ID:
            return
    
        welcoming = group_greetings.get("welcoming", True) if group_greetings else True
        if not welcoming:
            return
    
        wel_clean_up = group_greetings.get("wel_clean_up", False)
    
        msg_id = group_greetings.get("wel_msg_id") if group_greetings else None
    
        if not msg_id:
            text = DEFAULT_WELCOME_TEXT
            media = None
            buttons = None
        else:
            temp = await Alishan.get_messages(DATABASE, ids=msg_id)
            text = temp.text or DEFAULT_WELCOME_TEXT
            media = temp.media
            buttons = temp.buttons
    
        text = text.format_map(safe_data)
    
        sent = await event.reply(message=text, file=media, buttons=buttons, parse_mode="html")
    
        if wel_clean_up:
            old = last_sent.get(chat_id)
            if old:
                try:
                    await Alishan.delete_messages(chat_id, old)
                except:
                    pass
    
            last_sent[chat_id] = sent.id
    
        return
        
@add_command("cleanservice")
async def clean_service(event, command_used, args):
    if event.is_private:
        return await event.reply("This command is made to be used in groups!")

    user = await event.get_sender()
    if not user:
        return await event.reply("Anonymous can't use these commands.")
    if not await is_admin(user, event):
        return await event.reply("You need to be an admin to do this.")

    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)

    if not args:
        return await event.reply("I understand only 'on/yes' or 'off/no'")
    if args.lower() in ["yes", "on"]:
        enable = True
    elif args.lower() in ["off", "no"]:
        enable = False
    else:
        return await event.reply("I understand only 'on/yes' or 'off/no'")
    greetings.update_one(
        {"chat_id": chat_id},
        {"$set": {"wel_clean_up": enable}},
        upsert=True,
    )

    if enable:
        return await event.reply("Service cleanup enabled.")
    else:
        return await event.reply("Service cleanup disabled.")
        