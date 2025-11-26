from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command, callback_query
from AlishanBot.utils.database import users, groups
from AlishanBot.modules.helper_funcs.add_user import add_user
from AlishanBot.modules.helper_funcs.info import get_info
from AlishanBot.modules.helper_funcs.uptime import get_uptime
from AlishanBot.modules.helper_funcs.ping import get_ping
from AlishanBot import config
from telethon import Button, types
import asyncio
from telethon.tl.functions.messages import SendReactionRequest

@add_command("start")
async def Start(event, command_used, args):
    await Alishan(SendReactionRequest(
        peer=event.chat_id,
        msg_id=event.id,
        reaction=[types.ReactionEmoji(
            emoticon='❤️'
        )]
    ))
    user = await event.get_sender()
    user_id = user.id
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    full_name = (first_name + " " + last_name).strip()
    if not users.find_one({"user_id": user_id}):
        await add_user(event)
    info = get_info() 
    BOT_MENTION = info["BOT_MENTION"]
    BOT_USERNAME = info["BOT_USERNAME"]
    emoji = await event.reply("💫")
    uptime = get_uptime()
    ping = get_ping()
    if event.is_private:
        await Alishan.send_file(
            event.chat_id, 
            file=config.START_IMG, 
            caption=f"ʜᴇʏ <a href=\"tg://user?Id={user_id}\">{full_name}</a>.\n\nɪ ᴀᴍ {BOT_MENTION} ᴛʜᴇ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ᴀɴᴅ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ᴡʜɪᴄʜ ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴀɴᴅ sᴇᴄᴜʀᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ\n\n<b>➺ ᴘɪɴɢ : </b>{ping}\n<b>➺ ᴜᴘᴛɪᴍᴇ :</b> {uptime}\n\n<b>ᴄʟɪᴄᴋ ᴏɴ ʜᴇʟᴘ ᴛᴏ ʟᴇᴀʀɴ ᴍᴏʀᴇ. </b>", 
            buttons = [
                [
                    Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],
                [
                    Button.inline("ʜᴇʟᴘ ᴍᴇɴᴜ", data=b"help_menu")
                ], 
                [
                    Button.inline("ᴀʙᴏᴜᴛ ᴍᴇ", data=b"about_help"), 
                    Button.inline("ʀᴇғʀᴇsʜ", data=b"refresh")
                ], 
                [
                    Button.url("sᴜᴘᴘᴏʀᴛ", f"https://t.me/{config.SUPPORT_CHAT}"), 
                    Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}")
                ],
                [
                    Button.url("Source Code",
                    "https://github.com/inialiyaar/AlishanRobot.git"),
                ]
            ], 
            parse_mode="html"
        )
    else:
        await Alishan.send_file(
            event.chat_id,
            file=config.START_IMG,
            caption=f"ʜᴇʏ ᴛʜᴇʀᴇ <a href=\"tg://user?Id={user_id}\">{full_name}</a>.\n\n{BOT_MENTION} ɪs ᴀʟɪᴠᴇ ʙᴀʙʏ! \n\nᴀ ғᴀsᴛ ᴀɴᴅ ᴘᴏᴡᴇʀғᴜʟ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ᴘʟᴜs ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ!\nᴡɪᴛʜ sᴏᴍᴇ ᴀᴡᴇsᴏᴍᴇ Ғᴇᴜᴛᴜʀᴇs.\n\n<b>➺ ᴘɪɴɢ :</b> {ping}\n<b>➺ ᴜᴘᴛɪᴍᴇ :</b> {uptime}\n\n<b>ᴄʟɪᴄᴋ ᴏɴ ʜᴇʟᴘ ᴛᴏ ʟᴇᴀʀɴ ᴍᴏʀᴇ. </b>",
            buttons = [
                [
                    Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],
                [
                    Button.url("sᴜᴘᴘᴏʀᴛ", f"https://t.me/{config.SUPPORT_CHAT}"), 
                    Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}")
                ]
            ], 
            parse_mode="html"
        )
    await emoji.delete() 
    
@callback_query("refresh")    
async def Refresh(event):
     msg = await event.respond("**♻️ ʀᴇғʀᴇsʜɪɴɢ...**")
     uptime = get_uptime()
     ping = get_ping()
     info = get_info() 
     BOT_MENTION = info["BOT_MENTION"]
     BOT_USERNAME = info["BOT_USERNAME"]
     user = await event.get_sender()
     user_id = user.id
     first_name = user.first_name or ""
     last_name = user.last_name or ""
     full_name = (first_name + " " + last_name).strip()
     await event.edit(
         f"ʜᴇʏ <a href=\"tg://user?Id={user_id}\">{full_name}</a>.\n\nɪ ᴀᴍ {BOT_MENTION} ᴛʜᴇ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ᴀɴᴅ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ᴡʜɪᴄʜ ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴀɴᴅ sᴇᴄᴜʀᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ\n\n<b>➺ ᴘɪɴɢ :</b> {ping}\n<b>➺ ᴜᴘᴛɪᴍᴇ :</b> {uptime}\n\n<b>ᴄʟɪᴄᴋ ᴏɴ ʜᴇʟᴘ ᴛᴏ ʟᴇᴀʀɴ ᴍᴏʀᴇ. </b>", 
         buttons= [
                [
                    Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],
                [
                    Button.inline("ʜᴇʟᴘ ᴍᴇɴᴜ", data=b"help_menu")
                ], 
                [
                    Button.inline("ᴀʙᴏᴜᴛ ᴍᴇ", data=b"about_help"), 
                    Button.inline("ʀᴇғʀᴇsʜ", data=b"refresh")
                ], 
                [
                    Button.url("sᴜᴘᴘᴏʀᴛ", f"https://t.me/{config.SUPPORT_CHAT}"), 
                    Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}")
                ],
                [
                    Button.url("Source Code",
                    "https://github.com/inialiyaar/AlishanRobot.git"),
                ]
            ], 
         parse_mode="html"
         )
     await msg.delete()