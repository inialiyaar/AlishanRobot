from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command
from AlishanBot.modules.helper_funcs.helpers import is_admin


Unknown_Pic = "https://i.ibb.co/8gPXfNPW/x.jpg"

@add_command("id", "info")
async def Info_Handler(event, command_used, args):
    sender = await event.get_sender()
    if command_used == "info":
        if event.is_private:
            return await event.reply("This command is only for groups.")
        if event.is_reply:
            repliad = await event.get_reply_message()
            user = await Alishan.get_entity(repliad.sender_id)
            if not user:
                return await event.reply("I don't have information about anonymous users!")
        else:
            if not sender:
                return await event.reply("I don't have information about anonymous users!")
            else:
                user = sender
        first = user.first_name or ""
        last = user.last_name or ""
        full_name = first + " " + last
        username = user.username or ""
        user_id = user.id
        chat = await event.get_chat()
        photos = await Alishan.get_profile_photos(user_id, limit=1)
        if await is_admin(user, event):
            admin_stats = f"Yes!"
        else:
            admin_stats = f"No!"
        if photos:
            photo = photos[0]
        else:    
            photo = Unknown_Pic
        text = f"{full_name} Information.\n\nFirst Name: {first}\nLast Name: {last}\nFull Name: {full_name}\nUsername: @{username}\nUser ID: {user_id}\nLink: <a href='tg://user?id={user_id}'>{first}</a>\n\nIs Admin: {admin_stats}"
        await Alishan.send_file(chat.id, file=photo, caption=text, parse_mode="html")
    if command_used == "id":
        if event.is_private:
            first = sender.first_name or ""
            last = sender.last_name or ""
            full_name = first + " " + last
            return await event.reply(f"Here is {full_name}'s ID: `{sender.id}`")
        else:
            if event.is_reply:
                repliad = await event.get_reply_message()
                user = await Alishan.get_entity(repliad.sender_id)
                if not user:
                    return await event.reply("I don't have information about anonymous users!")
                if not sender:
                    return await event.reply(f"Here is {user.first_name}'s ID: `{user.id}`\nChat ID: `{event.chat_id}`")    
                else:
                    return await event.reply(f"Here is {user.first_name}'s ID: `{user.id}`\nChat ID: `{event.chat_id}`\nYour ID: `{sender.id}`")    
            else:
                if not sender:
                    return await event.reply(f"You are anonymous: \nChat ID: `{event.chat_id}`")
                else:
                    return await event.reply(f"Your ID: `{sender.id}`\nChat ID: `{event.chat_id}`")
                    