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
        return await event.reply("ʏᴏᴜ'ʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ᴀʀᴇ ʏᴏᴜ? ")
    if not sender.id == config.OWNER_ID:
        return await event.reply("ᴡʜᴀᴛ? ᴡʜᴏ ᴀʀᴇ ʏᴏᴜ ᴏɴʟʏ ᴍʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴄᴏɴᴛʀᴏʟ ᴍᴇ! ")
    user = await get_target_user(event)
    if not user:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ! ɪ ɢᴜᴇss ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ sᴛᴀʀᴛᴇᴅ ᴍᴇ. ")
    if user.id == BOT_ID:
        return await event.reply("ᴏʜ ʏᴇᴀʜ, ᴀᴅᴅ ᴍʏsᴇʟғ, ɴᴏᴏʙ!")
    if user.id == config.OWNER_ID:
        return await event.reply("ᴡʜᴀᴛ ᴛʜᴇ ʜᴇʟʟ? ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ᴀᴅᴅ ʏᴏᴜʀsᴇʟғ?")
    if sudo_users.find_one({"user_id": user.id}):
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴅᴅᴇᴅ ɪɴ sᴜᴅᴏ ᴜsᴇʀs. ")
    sudo_users.insert_one({"user_id": user.id})    
    mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    owner = await Alishan.get_entity(config.OWNER_ID)
    await event.reply(f"{mention} sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ sᴜᴅᴏ users. \n\nᴀᴅᴅᴇᴅ ʙʏ : <a href='tg://user?id={owner.id}'>{owner.first_name}</a>", parse_mode="html")
    
@add_command("delsudo")
async def Show_Sudo_User(event, command, used):
    sender = await event.get_sender()
    if not sender:
        return await event.reply("ʏᴏᴜ'ʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ᴀʀᴇ ʏᴏᴜ? ")
    if not sender.id == config.OWNER_ID:
        return await event.reply("ᴡʜᴀᴛ? ᴡʜᴏ ᴀʀᴇ ʏᴏᴜ ᴏɴʟʏ ᴍʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴄᴏɴᴛʀᴏʟ ᴍᴇ! ")
    user = await get_target_user(event)
    if not user:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ! ɪ ɢᴜᴇss ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ sᴛᴀʀᴛᴇᴅ ᴍᴇ. ")
    if user.id == BOT_ID:
        return await event.reply("ᴏʜ ʏᴇᴀʜ! ᴅᴇʟᴇᴛᴇ ᴍʏsᴇʟғ, ɴᴏᴏʙ!")
    if user.id == config.OWNER_ID:
        return await event.reply("ᴡʜᴀᴛ ᴛʜᴇ ʜᴇʟʟ? ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀsᴇʟғ?")
    if not sudo_users.find_one({"user_id": user.id}):
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ᴇxɪsᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs! ")
    sudo_users.delete_one({"user_id": user.id})    
    mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    owner = await Alishan.get_entity(config.OWNER_ID)
    await event.reply(f"{mention} sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇ ᴛᴏ sᴜᴅᴏ users. \n\nᴅᴇʟᴇᴛᴇᴅ ʙʏ : <a href='tg://user?id={owner.id}'>{owner.first_name}</a>", parse_mode="html") 
    
@add_command("sudolist")
async def Show_Sudo_User(event, command, used):
    sender = await event.get_sender()
    if not sender:
        return await event.reply("ʏᴏᴜ'ʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ᴀʀᴇ ʏᴏᴜ? ")
    if not (sender.id == config.OWNER_ID) and not (sudo_users.find_one({"user_id": sender.id})):
        return await event.reply("ᴡʜᴀᴛ? ᴡʜᴏ ᴀʀᴇ ʏᴏᴜ ᴏɴʟʏ ᴍʏ ᴏᴡɴᴇʀ ᴀɴᴅ sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ ᴄᴏɴᴛʀᴏʟ ᴍᴇ! ")
    mentions = []
    users_docs = sudo_users.find({})
    for doc in users_docs:
        user_id = doc["user_id"]
        user = await Alishan.get_entity(user_id)
        mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        mentions.append(mention)
    owner = await Alishan.get_entity(config.OWNER_ID)
    display_users = "\n".join(mentions)
    text = f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪsᴛ ᴏғ {BOT_MENTION} sᴜᴅᴏ ᴜsᴇʀs: \n\nᴏᴡɴᴇʀ: \n<a href='tg://user?Id={config.OWNER_ID}'>{owner.first_name}</a>\n\nsᴜᴅᴏ ᴜsᴇʀs: \n{display_users}"
    await event.reply(text, parse_mode="html")     