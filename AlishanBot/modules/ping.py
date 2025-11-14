from AlishanBot.core.bot import Alishan, music
from AlishanBot.core.decorators import add_command, callback_query
from AlishanBot.modules.helper_funcs.system import get_system_stats
from AlishanBot.modules.helper_funcs.uptime import get_uptime
from AlishanBot.modules.helper_funcs.ping import get_ping
from AlishanBot import config
from telethon import Button, types
import asyncio
from telethon.tl.functions.messages import SendReactionRequest
from AlishanBot.__init__ import BOT_MENTION, BOT_USERNAME
import time


@add_command("ping")
async def Ping(event, command_used, args):
    await Alishan(SendReactionRequest(
        peer=event.chat_id,
        msg_id=event.id,
        reaction=[types.ReactionEmoji(
            emoticon='🔥'
        )]
    ))
    user = await event.get_sender()
    user_id = user.id
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    full_name = (first_name + " " + last_name).strip()
    start = time.time()
    msg = await event.reply("**🏓 ᴘɪɴɢɪɴɢ...**")
    end = time.time()
    latency = round((end - start) * 1000, 2)
    uptime = get_uptime()
    ping = get_ping()
    ram, cpu, disk = get_system_stats()
    pytgcalls_ping = music.ping
    await Alishan.send_file(
        event.chat_id,
        file=config.START_IMG, 
        caption=f"ʜᴇʏ <a href=\"tg://user?Id={user_id}\">{full_name}</a>.\n\nᴛʜɪs ɪs {BOT_MENTION}.\n\n<b>🏓 ᴘᴏɴɢ : </b>{ping}\n<b>➭ ʟᴀᴛᴇɴᴄʏ :</b> {latency}ᴍs\n\n<b>➥ sʏsᴛᴇᴍ sᴛᴀᴛs :</b>\n<b>➭ ᴜᴘᴛɪᴍᴇ :</b> {uptime}\n<b>➭ ʀᴀᴍ :</b> {ram:.1f}%\n<b>➭ ᴄᴘᴜ :</b> {cpu:.1f}%\n<b>➭ ᴅɪsᴋ :</b> {disk:.1f}%\n<b>➭ ᴘʏ-ᴛɢᴄᴀʟʟs :</b> {pytgcalls_ping:.1f}ᴍs", 
        buttons = [
            [
                Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],
            [
                Button.inline("ʀᴇғʀᴇsʜ", data=b"refresh_ping")
            ], 
            [
                Button.url("sᴜᴘᴘᴏʀᴛ", f"https://t.me/{config.SUPPORT_CHAT}"), 
                Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}")
            ]
        ], 
        parse_mode="html"
    )
    await msg.delete()
    
@callback_query("refresh_ping")    
async def Refresh(event):
     start = time.time() 
     msg = await event.respond("**♻️ ʀᴇғʀᴇsʜɪɴɢ...**")
     end = time.time()
     latency = round((end - start) * 1000, 2)
     uptime = get_uptime()
     ping = get_ping()
     ram, cpu, disk = get_system_stats()
     pytgcalls_ping = music.ping
     user = await event.get_sender()
     user_id = user.id
     first_name = user.first_name or ""
     last_name = user.last_name or ""
     full_name = (first_name + " " + last_name).strip()
     await event.edit(
         f"ʜᴇʏ <a href=\"tg://user?Id={user_id}\">{full_name}</a>.\n\nᴛʜɪs ɪs {BOT_MENTION}.\n\n<b>🏓 ᴘᴏɴɢ : </b>{ping}\n<b>➭ ʟᴀᴛᴇɴᴄʏ :</b> {latency}ᴍs\n\n<b>➥ sʏsᴛᴇᴍ sᴛᴀᴛs :</b>\n<b>➭ ᴜᴘᴛɪᴍᴇ :</b> {uptime}\n<b>➭ ʀᴀᴍ :</b> {ram:.1f}%\n<b>➭ ᴄᴘᴜ :</b> {cpu:.1f}%\n<b>➭ ᴅɪsᴋ :</b> {disk:.1f}%\n<b>➭ ᴘʏ-ᴛɢᴄᴀʟʟs :</b> {pytgcalls_ping:.1f}ᴍs", 
         buttons= [
                [
                    Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],
                [
                    Button.inline("ʀᴇғʀᴇsʜ", data=b"refresh_ping")
                ], 
                [
                    Button.url("sᴜᴘᴘᴏʀᴛ", f"https://t.me/{config.SUPPORT_CHAT}"), 
                    Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}")
                ]
            ], 
         parse_mode="html"
         )
     await msg.delete()