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
            caption=f"Hey <a href=\"tg://user?Id={user_id}\">{full_name}</a>.\n\nI am {BOT_MENTION} the most powerful Telegram music and group management bot which can help you to manage and secure your group\n\n<b>➺ Ping: </b>{ping}\n<b>➺ Uptime:</b> {uptime}\n\n<b>Click on Help to learn more. </b>", 
            buttons = [
                [
                    Button.url("Add Me to Your Group", f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],
                [
                    Button.inline("Help Menu", data=b"help_menu")
                ], 
                [
                    Button.inline("About Me", data=b"about_help"), 
                    Button.inline("Refresh", data=b"refresh")
                ], 
                [
                    Button.url("Support", f"https://t.me/{config.SUPPORT_CHAT}"), 
                    Button.url("Updates", f"https://t.me/{config.SUPPORT_CHANNEL}")
                ],
            ], 
            parse_mode="html"
        )
    else:
        await Alishan.send_file(
            event.chat_id,
            file=config.START_IMG,
            caption=f"Hey there <a href=\"tg://user?Id={user_id}\">{full_name}</a>.\n\n{BOT_MENTION} is alive baby! \n\nA fast and powerful Telegram music plus management bot!\nWith some awesome features.\n\n<b>➺ Ping:</b> {ping}\n<b>➺ Uptime:</b> {uptime}\n\n<b>Click on Help to learn more. </b>",
            buttons = [
                [
                    Button.url("Add Me to Your Group", f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],
                [
                    Button.url("Support", f"https://t.me/{config.SUPPORT_CHAT}"), 
                    Button.url("Updates", f"https://t.me/{config.SUPPORT_CHANNEL}")
                ]
            ], 
            parse_mode="html"
        )
    await emoji.delete() 
    
@callback_query("refresh")    
async def Refresh(event):
     msg = await event.respond("**♻️ Refreshing...**")
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
         f"Hey <a href=\"tg://user?Id={user_id}\">{full_name}</a>.\n\nI am {BOT_MENTION} the most powerful Telegram music and group management bot which can help you to manage and secure your group\n\n<b>➺ Ping:</b> {ping}\n<b>➺ Uptime:</b> {uptime}\n\n<b>Click on Help to learn more. </b>", 
         buttons= [
                [
                    Button.url("Add Me to Your Group", f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],
                [
                    Button.inline("Help Menu", data=b"help_menu")
                ], 
                [
                    Button.inline("About Me", data=b"about_help"), 
                    Button.inline("Refresh", data=b"refresh")
                ], 
                [
                    Button.url("Support", f"https://t.me/{config.SUPPORT_CHAT}"), 
                    Button.url("Updates", f"https://t.me/{config.SUPPORT_CHANNEL}")
                ],
            ], 
         parse_mode="html"
         )
     await msg.delete()
     