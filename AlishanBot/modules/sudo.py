from AlishanBot.core.decorators import add_command
from AlishanBot.core.bot import Alishan
from AlishanBot.utils.database import sudo_users 
from AlishanBot.modules.helper_funcs.helpers import get_target_user
from AlishanBot import config
from AlishanBot.__init__ import BOT_MENTION, BOT_ID


@add_command("addsudo")
async def Show_Sudo_User(event, command, used):
    sender = await event.get_sender()
    if not sender:
        return await event.reply("You're anonymous, I don't know who are you?")
    if not sender.id == config.OWNER_ID:
        return await event.reply("What? Who are you? Only my owner can control me!")
    user = await get_target_user(event)
    if not user:
        return await event.reply("This user not found! I guess this user not started me.")
    if user.id == BOT_ID:
        return await event.reply("Oh yeah, add myself, noob!")
    if user.id == config.OWNER_ID:
        return await event.reply("What the hell? You trying to add yourself?")
    if sudo_users.find_one({"user_id": user.id}):
        return await event.reply("This user is already added in sudo users.")
    sudo_users.insert_one({"user_id": user.id})    
    mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    owner = await Alishan.get_entity(config.OWNER_ID)
    await event.reply(f"{mention} successfully added to sudo users. \n\nAdded by: <a href='tg://user?id={owner.id}'>{owner.first_name}</a>", parse_mode="html")
    
@add_command("delsudo")
async def Show_Sudo_User(event, command, used):
    sender = await event.get_sender()
    if not sender:
        return await event.reply("You're anonymous, I don't know who are you?")
    if not sender.id == config.OWNER_ID:
        return await event.reply("What? Who are you? Only my owner can control me!")
    user = await get_target_user(event)
    if not user:
        return await event.reply("This user not found! I guess this user not started me.")
    if user.id == BOT_ID:
        return await event.reply("Oh yeah! Delete myself, noob!")
    if user.id == config.OWNER_ID:
        return await event.reply("What the hell? You trying to delete yourself?")
    if not sudo_users.find_one({"user_id": user.id}):
        return await event.reply("This user is not exist in sudo users!")
    sudo_users.delete_one({"user_id": user.id})    
    mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    owner = await Alishan.get_entity(config.OWNER_ID)
    await event.reply(f"{mention} successfully deleted from sudo users. \n\nDeleted by: <a href='tg://user?id={owner.id}'>{owner.first_name}</a>", parse_mode="html") 
    
@add_command("sudolist")
async def Show_Sudo_User(event, command, used):
    sender = await event.get_sender()
    if not sender:
        return await event.reply("You're anonymous, I don't know who are you?")
    if not (sender.id == config.OWNER_ID) and not (sudo_users.find_one({"user_id": sender.id})):
        return await event.reply("What? Who are you? Only my owner and sudo users can control me!")
    mentions = []
    users_docs = sudo_users.find({})
    for doc in users_docs:
        user_id = doc["user_id"]
        user = await Alishan.get_entity(user_id)
        mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        mentions.append(mention)
    owner = await Alishan.get_entity(config.OWNER_ID)
    display_users = "\n".join(mentions)
    text = f"Here is your list of {BOT_MENTION} sudo users: \n\nOwner: \n<a href='tg://user?Id={config.OWNER_ID}'>{owner.first_name}</a>\n\nSudo Users: \n{display_users}"
    await event.reply(text, parse_mode="html")
    