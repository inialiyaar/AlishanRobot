from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command, callback_query
from telethon import Button, types
from AlishanBot.__init__ import BOT_MENTION, BOT_USERNAME
from AlishanBot.modules.helper_funcs.uptime import get_uptime
from AlishanBot.modules.helper_funcs.ping import get_ping
from AlishanBot import config
from telethon.tl.functions.messages import SendReactionRequest
from telethon import events
from AlishanBot.utils.database import users, groups


SUPPORT_CHANNEL = config.SUPPORT_CHANNEL
SUPPORT_CHAT = config.SUPPORT_CHAT
START_IMG = config.START_IMG

@add_command("help")
async def help(event, command, args):
    await Alishan(SendReactionRequest(
        peer=event.chat_id,
        msg_id=event.id,
        reaction=[types.ReactionEmoji(
            emoticon='❤️'
        )]
    ))
    caption = f"{BOT_MENTION}'s ʜᴇʟᴘ ᴍᴇɴᴜ\n\nᴄʜᴏꜱᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ꜰᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴘ. ᴡɪᴛʜ {BOT_MENTION}\n<b>ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ</b> <a href=\"https://t.me/{SUPPORT_CHAT}\">sᴜᴘᴘᴏʀᴛ chat</a>.\n\nᴀʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ ᴄᴀɴ ʙᴇ ᴜꜱᴇᴅ ᴡɪᴛʜ : /"
    if event.is_private:
        await event.reply(
            file=START_IMG, 
            caption=caption, 
            buttons = [
                [
                    Button.inline("ᴍᴀɴᴀɢᴇᴍᴇɴᴛ", data=b"management_help"), 
                    Button.inline("ᴍᴜsɪᴄ", data=b"music_help"), 
                ], 
                [
                    Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ", f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ], 
                
            ], 
            parse_mode="html", 
        )
    else:
        await event.reply(
            "**» ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ғᴏʀ ɢᴇᴛᴛɪɴɢ ʜᴇʟᴩ.**", 
            file=START_IMG, 
            buttons = [
                [
                    Button.url("ᴏᴘᴇɴ ɪɴ ᴘʀɪᴠᴀᴛᴇ", f"https://t.me/{BOT_USERNAME}?start=help"), 
                ], 
                [
                   Button.inline(" ᴏᴘᴇɴ ʜᴇʀᴇ", data=b"help_menu"), 
                ], 
            ]
        )
        
@Alishan.on(events.CallbackQuery())
async def callback_help(event):
    data = event.data
    ping = get_ping() 
    uptime = get_uptime()
    user = await event.get_sender()
    try:
        user_id = user.id
        first_name = user.first_name or ""
        last_name = user.last_name or ""
        full_name = (first_name + " " + last_name).strip()
        mention = f"<a href=\"tg://user?Id={user_id}\">{full_name}</a>"
    except:
        mention = "ᴀɴᴏɴʏᴍᴏᴜs"  
    if data == b"help_menu":
        caption = f"{BOT_MENTION}'s ʜᴇʟᴘ ᴍᴇɴᴜ\n\nᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʜᴇʟᴘ ᴡɪᴛʜ {BOT_MENTION}\n\n<b>ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ</b> <a href=\"https://t.me/{SUPPORT_CHAT}\">sᴜᴘᴘᴏʀᴛ chat</a>."
        buttons = [
            [
                Button.inline("ᴍᴀɴᴀɢᴇᴍᴇɴᴛ", data=b"management_help"), 
                Button.inline("ᴍᴜsɪᴄ", data=b"music_help"), 
            ], 
            [
                Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ", f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ], 
            [
                            
                Button.inline("• ʜᴏᴍᴇ •", data=b"back_to_start")
            ]
                        
            ]
    elif data == b"about_help":
        total_users = users.count_documents({})
        chats = groups.count_documents({})
        caption = f"<b>ʜᴇʏ</b> {mention},\n<b>ᴛʜɪs ɪs</b> {BOT_MENTION}\n<b>ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴀɴᴅ ᴍᴜsɪᴄ ʙᴏᴛ ʙᴜɪʟᴛ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴇᴀꜱɪʟʏ ᴀɴᴅ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ ꜰʀᴏᴍ ꜱᴄᴀᴍᴍᴇʀꜱ ᴀɴᴅ ꜱᴘᴀᴍᴍᴇʀꜱ.\nᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ ᴍᴏɴɢᴏᴅʙ ᴀs ᴅᴀᴛᴀʙᴀsᴇ.</b>\n────────────────────\n<b>➻ ᴜᴩᴛɪᴍᴇ »</b> {uptime}\n<b>➻ ᴘɪɴɢ »<b> {ping}\n<b>➻ ᴜsᴇʀs »</b> {total_users}\n<b>➻ ᴄʜᴀᴛs »</b> {chats}\n────────────────────\n\n➲  ɪ ᴄᴀɴ ɢʀᴇᴇᴛ ᴜꜱᴇʀꜱ ᴡɪᴛʜ ᴄᴜꜱᴛᴏᴍɪᴢᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇꜱ ᴀɴᴅ ᴇᴠᴇɴ ꜱᴇᴛ ᴀ ɢʀᴏᴜᴘ'ꜱ ʀᴜʟᴇꜱ.\n➲ ɪ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ/ᴠɪᴅᴇᴏ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ᴡɪᴛʜ ᴄᴏɴᴛʀᴏʟ ᴄᴏᴍᴍᴀɴᴅs.\n\n➻ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ғᴏʀ ɢᴇᴛᴛɪɴɢ ʙᴀsɪᴄ ʜᴇʟᴩ ᴀɴᴅ ɪɴғᴏ ᴀʙᴏᴜᴛ {BOT_MENTION}."
        buttons = [
            [
                Button.url("sᴜᴘᴘᴏʀᴛ", f"https://t.me/{SUPPORT_CHAT}"), 
                Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{SUPPORT_CHANNEL}")
            ], 
            [
                Button.inline("• ʜᴏᴍᴇ •", data=b"back_to_start")
            ]
        ]
    elif data == b"back_to_start":
        if event.is_private:
            caption=f"ʜᴇʏ {mention}.\n\nɪ ᴀᴍ {BOT_MENTION} ᴛʜᴇ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ᴀɴᴅ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ᴡʜɪᴄʜ ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴀɴᴅ sᴇᴄᴜʀᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ\n\n<b>➺ ᴘɪɴɢ:</b>{ping}\n<b>➺ ᴜᴘᴛɪᴍᴇ:</b> {uptime}\n\n<b>ᴄʟɪᴄᴋ ᴏɴ ʜᴇʟᴘ ᴛᴏ ʟᴇᴀʀɴ ᴍᴏʀᴇ. </b>"
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
                        Button.url("sᴜᴘᴘᴏʀᴛ", f"https://t.me/{SUPPORT_CHAT}"), 
                        Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{SUPPORT_CHANNEL}")
                    ]
                ]
        else:
            caption=f"<b>» ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ғᴏʀ ɢᴇᴛᴛɪɴɢ ʜᴇʟᴩ.</b>"
            buttons = [
                    [
                        Button.url("ᴏᴘᴇɴ ɪɴ ᴘʀɪᴠᴀᴛᴇ", f"https://t.me/{BOT_USERNAME}?start=help"), 
                    ], 
                    [
                        Button.inline(" ᴏᴘᴇɴ ʜᴇʀᴇ", data=b"help_menu"), 
                    ], 
                ]
    elif data == b"management_help":
        caption = f"<b>{BOT_MENTION}'s ᴇxᴄʟᴜsɪᴠᴇ ғᴇᴀᴛᴜʀᴇs</b>\n\nᴄʜᴏꜱᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ꜰᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴘ. ᴡɪᴛʜ {BOT_MENTION}\n<b>ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ</b> <a href=\"https://t.me/{SUPPORT_CHAT}\">sᴜᴘᴘᴏʀᴛ chat</a>.\n\nᴀʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ ᴄᴀɴ ʙᴇ ᴜꜱᴇᴅ ᴡɪᴛʜ : /"
        buttons = [
            [
                Button.inline("𝖬ᴜᴛᴇ", data=b"mute_help"), 
                Button.inline("Dᴏᴡɴʟᴏᴀᴅ", data=b"download_help"),
                Button.inline("𝖡ᴀɴs", data=b"ban_help"), 
                
            ], 
            [
           Button.inline("◁", data=b"management_preview"), 
           Button.inline("ʙᴀᴄᴋ", data=b"help_menu"), 
           Button.inline("▷", data=b"management_next"), 
           ]
        ]
    elif data == b"management_next":
        pass
    elif data == b"management_preview":
        pass  
    elif data == b"mute_help":
        caption = f"<b>» ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ Mᴜᴛᴇ​ :\n\nᴀᴅᴍɪɴs ᴏɴʟʏ:</b>\n\n❍ /mute <ᴜsᴇʀʜᴀɴᴅʟᴇ>: sɪʟᴇɴᴄᴇs ᴀ ᴜsᴇʀ. ᴄᴀɴ ᴀʟsᴏ ʙᴇ ᴜsᴇᴅ ᴀs ᴀ ʀᴇᴘʟʏ, ᴍᴜᴛɪɴɢ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴜᴘᴀss\n❍ /tmute <ᴜsᴇʀʜᴀɴᴅʟᴇ> x(ᴍ/ʜ/ᴅ): ᴍᴜᴛᴇs ᴀ ᴜsᴇʀ ғᴏʀ x ᴛɪᴍᴇ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ). ᴍ = ᴍɪɴᴜᴛᴇs, ʜ = ʜᴏᴜʀs, ᴅ = ᴅᴀʏs.\n❍ /ᴜɴᴍᴜᴛᴇ <ᴜsᴇʀʜᴀɴᴅʟᴇ>: ᴜɴᴍᴜᴛᴇs ᴀ ᴜsᴇʀ. ᴄᴀɴ ᴀʟsᴏ ʙᴇ ᴜsᴇᴅ ᴀs ᴀ ʀᴇᴘʟʏ, ᴍᴜᴛɪɴɢ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ to ᴜsᴇʀ." 
        buttons = [
            [
                Button.inline("ʙᴀᴄᴋ", data=b"management_help")
            ]
        ]
    elif data == b"ban_help":
        caption = f"<b>» ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ Bᴀɴs :</b>\n\n❍ /kickme: ᴋɪᴄᴋs ᴛʜᴇ ᴜsᴇʀ ᴡʜᴏ ɪssᴜᴇᴅ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ\n\n<b>ᴀᴅᴍɪɴs ᴏɴʟʏ:</b>\n❍ /ban <ᴜsᴇʀʜᴀɴᴅʟᴅ>: ʙᴀɴs ᴀ ᴜsᴇʀ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)\n❍ /sban <ᴜsᴇʀʜᴀɴᴅʟᴇ>: sɪʟᴇɴᴛʟʏ ʙᴀɴ ᴀ ᴜsᴇʀ. ᴅᴇʟᴇᴛᴇs ᴄᴏᴍᴍᴀɴᴅ, ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ᴀɴᴅ ᴅᴏᴇsɴ'ᴛ ʀᴇᴘʟʏ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)\n❍ /tban <ᴜsᴇʀʜᴀɴᴅʟᴇ> x(ᴍ/ʜ/ᴅ): ʙᴀɴs ᴀ ᴜsᴇʀ ғᴏʀ x ᴛɪᴍᴇ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ). ᴍ = ᴍɪɴᴜᴛᴇs, ʜ = ʜᴏᴜʀs, ᴅ = ᴅᴀʏs.\n❍ /unban <ᴜsᴇʀʜᴀɴᴅʟᴇ>: ᴜɴʙᴀɴs ᴀ ᴜsᴇʀ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)\n❍ /kick <ᴜsᴇʀʜᴀɴᴅʟᴇ>: ᴋɪᴄᴋs ᴀ ᴜsᴇʀ ᴏᴜʀ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ, (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)"
        buttons = [
            [
                Button.inline("ʙᴀᴄᴋ", data=b"management_help")
            ]
        ]
    elif data == b"download_help":
        caption = f"<b>» ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ Bᴀɴs :\n\n𝖯ʀɪᴠᴀᴛᴇ ᴏɴʟʏ</b>\n❍ /download <𝖲ᴏɴɢ𝖭ᴀᴍᴇ/𝖸ᴏᴜᴛᴜʙᴇ𝖴ʀʟ> : 𝖥ᴇᴛᴄʜ 𝖣ᴏᴡɴʟᴏᴀᴅ ᴏᴘᴛɪᴏɴs ғᴏʀ ᴀ 𝖲ᴏɴɢ ᴏʀ 𝖵ɪᴅᴇᴏ ʙʏ ᴘʀᴏᴠɪᴅɪɴɢ ᴀ 𝖭ᴀᴍᴇ ᴏʀ ᴀ ᴅɪʀᴇᴄᴛ 𝖴ʀʟ,"
        buttons = [
            [
                Button.inline("ʙᴀᴄᴋ", data=b"management_help")
            ]
        ]
    elif data == b"music_help":
         caption = f"<b>{BOT_MENTION} ᴛʜᴇ ᴜʟᴛɪᴍᴀᴛᴇ ᴍᴜsɪᴄ ʙᴏᴛ</b>\n\nᴄʜᴏꜱᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ꜰᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴘ. ᴡɪᴛʜ {BOT_MENTION}\n<b>ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ</b> <a href=\"https://t.me/{SUPPORT_CHAT}\">sᴜᴘᴘᴏʀᴛ chat</a>.\n\nᴀʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ ᴄᴀɴ ʙᴇ ᴜꜱᴇᴅ ᴡɪᴛʜ : /"
         buttons = [
             [
                 Button.inline("ᴀᴅᴍɪɴ", data=b"music_admin_help"), 
                 Button.inline("ᴘʟᴀʏ", data=b"play_help"), 
             ], 
             [
                 Button.inline("◁", data=b"music_preview"), 
                 Button.inline("ʙᴀᴄᴋ", data=b"help_menu"), 
                 Button.inline("▷", data=b"music_next")
             ]
         ]
    elif data == b"play_help":
        caption = f"<b>» ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ 𝖯ʟᴀʏ:\n\nv : sᴛᴀɴᴅs ғᴏʀ ᴠɪᴅᴇᴏ ᴩʟᴀʏ.</b>\n❍ play ᴏʀ /vplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ."
        buttons = [
            [
                Button.inline("ʙᴀᴄᴋ", data=b"music_help")
            ]
        ] 
    elif data == b"music_admin_help":
        caption= f"» ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ 𝖠ᴅᴍɪɴ:\n\n❍ /pause : ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.\n\n❍ /resume : ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ.\n\n❍ /skip : sᴋɪᴩ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ ɪɴ ǫᴜᴇᴜᴇ.\n\n/end ᴏʀ /stop : ᴄʟᴇᴀʀs ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ᴇɴᴅ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.\n\n❍ /replay : ʀᴇᴘʟᴀʏ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ. " 
        buttons = [
            [
                Button.inline("ʙᴀᴄᴋ", data=b"music_help")
            ]
        ] 
    try:
        await event.edit(
            caption, 
            buttons=buttons, 
            parse_mode="html"
        )
    except:
        pass          