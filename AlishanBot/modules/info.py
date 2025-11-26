from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command
from AlishanBot.modules.helper_funcs.helpers import is_admin


Unknown_Pic = "https://i.ibb.co/8gPXfNPW/x.jpg"

@add_command("id", "info")
async def Info_Handler(event, command_used, args):
    sender = await event.get_sender()
    if command_used == "info":
        if event.is_private:
            return await event.reply(" ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs. ")
        if event.is_reply:
            repliad = await event.get_reply_message()
            user = await Alishan.get_entity(repliad.sender_id)
            if not user:
                return await event.reply(" ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀɴᴏɴʏᴍᴏᴜs! ")
        else:
            if not sender:
                return await event.reply(" ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀɴᴏɴʏᴍᴏᴜs! ")
            else:
                user = sender
        first = user.first_name or ""
        last = user.last_name or ""
        full_name = first + " " + last
        username = user.username or ""
        user_id = user.id
        chat = await event.get_chat()
        photos = await Alishan.get_profile_photos(user_id, limit=1)
        if await is_admin(user,  event):
            admin_stats = f"ʏᴇs!"
        else:
            admin_stats = f"ɴᴏ!"
        if photos:
            photo = photos[0]
        else:    
            photo = Unknown_Pic
        text = f"{full_name} ɪɴғᴏʀᴍᴀᴛɪᴏɴ!.\n\nғɪʀsᴛ ɴᴀᴍᴇ : {first}\nʟᴀsᴛ ɴᴀᴍᴇ : {last}\nғᴜʟʟ ɴᴀᴍᴇ : {full_name}\nᴜsᴇʀɴᴀᴍᴇ : @{username}\nᴜsᴇʀ ɪᴅ : {user_id}\nʟɪɴᴋ : <a href='tg://user?id={user_id}'>{first}</a>\n\nɪs ᴀᴅᴍɪɴ : {admin_stats}"
        await Alishan.send_file(chat.id, file=photo, caption=text, parse_mode="html")
    if command_used == "id":
        if event.is_private:
            first = sender.first_name or ""
            last = sender.last_name or ""
            full_name = first + " " + last
            return await event.reply(f"ʜᴇʀᴇ ɪs {full_name}'s ɪᴅ : `{sender.id}`")
        else:
            if event.is_reply:
                repliad = await event.get_reply_message()
                user = await Alishan.get_entity(repliad.sender_id)
                if not user:
                    return await event.reply(" ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀɴᴏɴʏᴍᴏᴜs! ")
                if not sender:
                    return await event.reply(f"ʜᴇʀᴇ ɪs {user.first}'s ɪᴅ : `{user.id}`\nᴄʜᴀᴛ ɪᴅ : `{event.chat_id}`")    
                else:
                    return await event.reply(f"ʜᴇʀᴇ ɪs {user.first}'s ɪᴅ : `{user.id}`\nᴄʜᴀᴛ ɪᴅ : `{event.chat_id}`\nʏᴏᴜʀ ɪᴅ : `{sender.id}`")    
            else:
                if not sender:
                    return await event.reply(f" ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜs : \nᴄʜᴀᴛ ɪᴅ : `{chat.id}`")
                else:
                    return await event.reply(f"ʏᴏᴜʀ ɪᴅ : `{sender.id}`\nᴄʜᴀᴛ ɪᴅ : `{event.chat_id}`")