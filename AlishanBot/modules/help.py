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
    caption = f"{BOT_MENTION}'s Help Menu\n\nChose the category for which you wanna get help. With {BOT_MENTION}\n<b>Any problem ask your doubts at</b> <a href=\"https://t.me/{SUPPORT_CHAT}\">support chat</a>.\n\nAll commands can be used with : /"
    if event.is_private:
        await Alishan.send_file(
            event.chat_id, 
            file=START_IMG, 
            caption=caption, 
            buttons = [
                [
                    Button.inline("Management", data=b"management_help"), 
                    Button.inline("Music", data=b"music_help"), 
                ], 
                [
                    Button.inline("Games", data=b"games_help")
                ],
                [
                    Button.url("Add me to your Group", f"https://t.me/{BOT_USERNAME}?startgroup=true"), 
                ], 
                
            ], 
            parse_mode="html", 
        )
    else:
        await event.reply(
            "**» Choose an option for getting Help.**", 
            file=START_IMG, 
            buttons = [
                [
                    Button.url("Open in Private", f"https://t.me/{BOT_USERNAME}?start=help"), 
                ], 
                [
                   Button.inline("Open Here", data=b"help_menu"), 
                ], 
            ]
        )
        
@Alishan.on(events.CallbackQuery())
async def callback_help(event):
    data = event.data
    user = await event.get_sender()
    try:
        user_id = user.id
        first_name = user.first_name or ""
        last_name = user.last_name or ""
        full_name = (first_name + " " + last_name).strip()
        mention = f"<a href=\"tg://user?Id={user_id}\">{full_name}</a>"
    except:
        mention = "Anonymous"  
    if data == b"help_menu":
        caption = f"{BOT_MENTION}'s Help Menu\n\nChoose the category you want to help with {BOT_MENTION}\n\n<b>Any problem ask your doubts at</b> <a href=\"https://t.me/{SUPPORT_CHAT}\">support chat</a>."
        buttons = [
            [
                Button.inline("Management", data=b"management_help"), 
                Button.inline("Music", data=b"music_help"), 
            ], 
            [
                Button.inline("Games", data=b"games_help")
            ], 
            [
                Button.url("Add me to your Group", f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ], 
            [
                            
                Button.inline("Home", data=b"back_to_start")
            ]
                        
            ]
    elif data == b"about_help":
        ping = get_ping() 
        uptime = get_uptime()
        total_users = users.count_documents({})
        chats = groups.count_documents({})
        caption = f"<b>Hey</b> {mention},\n<b>This is</b> {BOT_MENTION}\n<b>A powerful group management and music bot built to help you manage your group easily and to protect your group from scammers and spammers.\nWritten in Python with MongoDB as database.</b>\n────────────────────\n<b>➻ Uptime »</b> {uptime}\n<b>➻ Ping »</b> {ping}\n<b>➻ Users »</b> {total_users}\n<b>➻ Chats »</b> {chats}\n────────────────────\n\n➲  I can greet users with customizable welcome messages and even set a group's rules.\n➲ I can play music/video from youtube with control commands.\n\n➻ Click on the buttons given below for getting basic help and info about {BOT_MENTION}."
        buttons = [
            [
                Button.url("Support", f"https://t.me/{SUPPORT_CHAT}"), 
                Button.url("Updates", f"https://t.me/{SUPPORT_CHANNEL}")
            ], 
            [
                Button.inline("Home", data=b"back_to_start")
            ]
        ]
    elif data == b"back_to_start":
        ping = get_ping() 
        uptime = get_uptime()
        if event.is_private:
            caption=f"Hey {mention}.\n\nI am {BOT_MENTION} the most powerful Telegram music and group management bot which can help you to manage and secure your group\n\n<b>➺ Ping :</b> {ping}\n<b>➺ Uptime :</b> {uptime}\n\n<b>Click on help to learn more. </b>"
            buttons = [
                    [
                        Button.url("Add me to your Group", f"https://t.me/{BOT_USERNAME}?startgroup=true")
                    ],
                    [
                        Button.inline("Help Menu", data=b"help_menu")
                    ], 
                    [
                        Button.inline("About Me", data=b"about_help"), 
                        Button.inline("Refresh", data=b"refresh")
                    ], 
                    [
                        Button.url("Support", f"https://t.me/{SUPPORT_CHAT}"), 
                        Button.url("Updates", f"https://t.me/{SUPPORT_CHANNEL}")
                    ],
                ]
        else:
            caption=f"<b>» Choose an option for getting Help.</b>"
            buttons = [
                    [
                        Button.url("Open in Private", f"https://t.me/{BOT_USERNAME}?start=help"), 
                    ], 
                    [
                        Button.inline("Open Here", data=b"help_menu"), 
                    ], 
                ]
    elif data == b"management_help":
        caption = f"<b>{BOT_MENTION}'s Exclusive Features</b>\n\nChose the category for which you wanna get help. With {BOT_MENTION}\n<b>Any problem ask your doubts at</b> <a href=\"https://t.me/{SUPPORT_CHAT}\">support chat</a>.\n\nAll commands can be used with : /"
        buttons = [
            [
                Button.inline("Mute", data=b"mute_help"), 
                Button.inline("Download", data=b"download_help"),
                Button.inline("Bans", data=b"ban_help"), 
                
            ], 
            [
                Button.inline("Fun", data=b"fun_help"), 
                Button.inline("Admins", data=b"admins_help"), 
                Button.inline("Chatbot", data=b"chatbot_help")
            ],
            [
                Button.inline("Infos", data=b"info_help"), 
                Button.inline("Greetings", data=b"greetings_help"), 
                Button.inline("Afk", data=b"afk_help")
            ], 
            [
           Button.inline("Preview", data=b"management_preview"), 
           Button.inline("Back", data=b"help_menu"), 
           Button.inline("Next", data=b"management_next"), 
           ], 
        ]
    elif data == b"management_next":
        pass
    elif data == b"management_preview":
        pass  
    elif data == b"mute_help":
        caption = f"<b>» Available commands for Mute :\n\nAdmins Only</b>\n\n❍ /mute <userhandle>: Silences a user. Can also be used as a reply, muting the replied to upass. \n❍ /tmute <userhandle> x(m/h/d): Mutes a user for x time. (via handle, or reply). M = minutes, h = hours, d = days.\n❍ /unmute <userhandle>: Unmutes a user. Can also be used as a reply, muting the replied to user." 
        buttons = [
            [
                Button.inline("Back", data=b"management_help")
            ]
        ]
    elif data == b"ban_help":
        caption = f"<b>» Available commands for Bans :</b>\n\n❍ /kickme: Kicks the user who issued the command.\n\n<b>Admins Only:</b>\n❍ /ban <userhandld>: Bans a user. (via handle, or reply).\n❍ /sban <userhandle>: Silently ban a user. Deletes command, replied message and doesn't reply. (via handle, or reply).\n❍ /tban <userhandle> x(m/h/d): Bans a user for x time. (via handle, or reply). M = minutes, h = hours, d = days.\n❍ /unban <userhandle>: Unbans a user. (via handle, or reply).\n❍ /kick <userhandle>: Kicks a user our of the group, (via handle, or reply)."
        buttons = [
            [
                Button.inline("Back", data=b"management_help")
            ]
        ]
    elif data == b"download_help":
        caption = f"<b>» Available commands for Download :\n\nPrivate Only</b>\n❍ /download <SongName/YoutubeUrl> : Fetch download options for a song or video by providing a name or a direct Url."
        buttons = [
            [
                Button.inline("Back", data=b"management_help")
            ]
        ]
    elif data == b"fun_help":
        caption = f"<b>» Available commands for Fun :</b>\n\n❍ /truth : To give a random truth. \n❍ /dare : To give a random dare.\n❍ /slap : To slap repliad user.\n❍ /punch : To puncg repliad user.\n ❍ /hug : To hug repliad user.\n❍ /pat : To pat repliad user.\n❍ /kiss : To kiss repliad user.\n❍ /cry : To cry repliad user.\n❍ /dance : To dance with repliad user.\n❍ /wink : To wink repliad user.\n❍ /bite : To bite repliad user.\n❍ /blush : To blush repliad user.\n❍ /smile : To smile with repliad user.\n❍ /love : To love repliad user.\n❍ /highfive : To highfive repliad user.\n❍ /wave : To wave repliad user."
        buttons = [
            [
                Button.inline("Back", data=b"management_help")
            ]
        ]
    elif data == b"admins_help":
        caption = f"<b>» Available commands for Admins :\n\nUser commands</b>\n❍ /admins: List of admins in the chat.\n❍ /pinned: To get the current pinned message.\n\n<b>Admins Only</b>\n❍ /pin: Silently pins the message replied to - add 'loud' or 'notify' to give notifs to users. \n❍ /unpin: Unpins the currently pinned message.\n❍ /invitelink: Gets invitelink.\n❍ /promote: Promotes the user replied to.\n❍ /lowpromote: Promotes the user replied to with half rights.\n❍ /fullpromote: Promotes the user replied to with full rights.\n❍ /demote: Demotes the user replied to.\n❍ /setgtitle <text>: Set group title.\n❍ /setgpic: Reply to an image to set as group photo.\n❍ /setdes: Set group description.\n❍ /setsticker: Set group sticker."
        buttons = [
            [
                Button.inline("Back", data=b"management_help")
            ]
        ]
    elif data == b"chatbot_help":
        caption = f"<b>» Available commands for Chatbot :\n\nGroup Only</b>\n{BOT_MENTION} has an chatbot which provides you a seemingleess chatting experience :\n\n❍  /chatbot : Shows chatbot control pannel."
        buttons = [
            [
                Button.inline("Back", data=b"management_help")
            ]
        ]
    elif data == b"afk_help":
        caption = f"<b>» Available commands for Afk:\n\nGroup Only</b>\n❍  /afk or /brb : Announced your afk! ."
        buttons = [
            [
                Button.inline("Back", data=b"management_help")
            ]
        ]
    elif data == b"info_help":
        caption = f"<b>» Available commands for Info:\n</b>❍ /Id : To show your id or chat id and repliad user id. \n\n<b>Group Only</b>\n❍  /info : To show the repliad user or your information.."
        buttons = [
            [
                Button.inline("Back", data=b"management_help")
            ]
        ]
    elif data == b"greetings_help":
        caption = f"<b>» Available commands for Greetings:\n\nGroup Only</b>\n❍ /welcome or /wel(on|yes/off|no) : To show current welcome status and on or off welcoming.\n❍ /goodbye or /gb (on|yes/off|no) : To show current goodbye status and on or off goodbying\n❍ /setwelcome or /setwel (message or reply message) : To set custome welcome text oramedia. \n❍ /setgoodbye or /setgoodbye (message or reply message) : To set custome goodbye text or media. \n❍ /cleanservice (on|yes/off|no) : To delete old greetings message make your group clean."
        buttons = [
            [
                Button.inline("Back", data=b"management_help"), 
                Button.inline("Markdown", data=b"markdown_help"), 
            ]
        ]
    elif data == b"music_help":
         caption = f"<b>{BOT_MENTION} The Ultimate Music Bot</b>\n\nChose the category for which you wanna get help. With {BOT_MENTION}\n<b>Any problem ask your doubts at</b> <a href=\"https://t.me/{SUPPORT_CHAT}\">support chat</a>.\n\nAll commands can be used with : /"
         buttons = [
             [
                 Button.inline("Admin", data=b"music_admin_help"), 
                 Button.inline("Play", data=b"play_help"), 
             ], 
             [
                 Button.inline("Preview", data=b"music_preview"), 
                 Button.inline("Back", data=b"help_menu"), 
                 Button.inline("Next", data=b"music_next")
             ]
         ]
    elif data == b"play_help":
        caption = f"<b>» Available commands for Play:\n\nv : Stands for video play.\nforce : Stands for force play.</b>\n\n❍ /play or /vplay : Starts streaming the requested track on videochat.\n\n<b>Admins Only</b>\n❍ /playforce or /vplayforce : Stops the ongoing stream and starts streaming the requested track."
        buttons = [
            [
                Button.inline("Back", data=b"music_help")
            ]
        ] 
    elif data == b"music_admin_help":
        caption= f"<b>» Available commands for Admin:</b>\n\n❍ /pause : Pause the current playing stream.\n\n❍ /resume : Resume the paused stream.\n\n❍ /skip : Skip the current playing stream and start streaming the next track in queue.\n\n/end or /stop : Clears the queue and end the current playing stream.\n\n❍ /replay : Replay the current playing stream." 
        buttons = [
            [
                Button.inline("Back", data=b"music_help")
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
        
