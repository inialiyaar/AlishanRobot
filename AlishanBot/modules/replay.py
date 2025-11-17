from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command, callback_query
from AlishanBot.modules.helper_funcs.queue import replay
from AlishanBot.modules.helper_funcs.helpers import is_admin

@add_command("replay")
async def replay_handler(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    if not await is_admin(user, event):
        await event.reply("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.")
        return
    try:
        await event.delete()
    except:
        pass    
    if event.is_group or event.is_channel:
    	await replay(event)
    else:
        await event.reply("𝖸ᴏᴜ ᴄᴀɴ ᴜsᴇ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ!.")
    
@callback_query("replay")
async def replay_callback(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    rights = await Alishan.get_permissions(chat.id, user.id)
    if not await is_admin(user, event):
        await event.answer("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.", alert=True)
        return
    if event.is_group or event.is_channel:
    	await replay(event)
    else:
        await event.reply("𝖸ᴏᴜ ᴄᴀɴ ᴜsᴇ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ!.")