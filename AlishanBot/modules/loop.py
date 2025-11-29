from AlishanBot.core.bot import Alishan, music
from AlishanBot.modules.helper_funcs.queue import queues
from AlishanBot.__init__ import player_stats, BOT_MENTION, update_time
from AlishanBot.core.decorators import add_command
from AlishanBot.modules.helper_funcs.helpers import is_admin
from AlishanBot.utils.database import stream_mode


@add_command("loop")
async def loop_handler(event, command_used, args):
    if not event.is_group:
        return await event.reply("𝖸ᴏᴜ ᴄᴀɴ ᴜsᴇ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ!.")
    user = await event.get_sender()
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "ᴀɴᴏɴʏᴍᴏᴜs"
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    settings = stream_mode.find_one({"chat_id": chat_id})
    if settings:
        admin_cmd = settings.get("admin_cmd", "admins")
    else:
        admin_cmd = "admins"  
    if not await is_admin(user, event) and admin_cmd == "admins":
        await event.reply("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.")
        return
    if chat_id not in player_stats:
        return await event.reply(f"» {BOT_MENTION} ɪsɴ'ᴛ 𝖲ᴛʀᴇᴀᴍɪɴɢ ᴏɴ 𝖵ᴏɪᴄᴇᴄʜᴀᴛ.", parse_mode="html")    
    if not args:
        return await event.reply("ɪ ᴜɴᴅᴇʀsᴛᴀɴᴅ ᴏɴʟʏ 'on/yes' ᴏʀ 'off/no'")
    if args.lower() in ["yes", "on", "enable"]:
        player_stats[chat_id]["loop"] = True
        return await event.reply(f"ʟᴏᴏᴘ ᴇɴᴀʙʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ\nᴇɴᴀʙʟᴇᴅ ʙʏ : {mention}", parse_mode="html")
    elif args.lower() in ["no", "off", "disable"]:
        player_stats[chat_id]["loop"] = False
        return await event.reply(f"ʟᴏᴏᴘ ᴅɪsᴀʙʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ\nᴅɪsᴀʙʟᴇᴅ ʙʏ : {mention}", parse_mode="html")
    else:
        return await event.reply("ɪ ᴜɴᴅᴇʀsᴛᴀɴᴅ ᴏɴʟʏ 'on/yes' ᴏʀ 'off/no'")