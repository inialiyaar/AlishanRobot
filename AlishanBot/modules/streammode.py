from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command, callback_query
from AlishanBot.modules.helper_funcs.helpers import is_admin
from AlishanBot.__init__ import BOT_MENTION
from AlishanBot.utils.database import stream_mode
from telethon import events, Button

def get_display_values(vote_mode, play_mode, admin_cmd, can_play):
    admin_cmd_disp = "ᴇᴠᴇʀʏᴏɴᴇ" if admin_cmd == "everyone" else "ᴀᴅᴍɪɴs"
    can_play_disp = "ᴇᴠᴇʀʏᴏɴᴇ" if can_play == "everyone" else "ᴀᴅᴍɪɴs"

    if play_mode == "normal":
        play_mode_disp = "ɴᴏʀᴍᴀʟ"
    elif play_mode == "eco":
        play_mode_disp = "ᴇᴄᴏ"
    else:
        play_mode_disp = "ʟᴏғɪ"

    return admin_cmd_disp, can_play_disp, play_mode_disp


def build_buttons(vote_mode, admin_cmd_disp, can_play_disp, play_mode_disp):
    return [
        [
            Button.inline("ᴠᴏᴛᴇs ➭", data=b"votes_help"),
            Button.inline(f"{vote_mode}", data=b"change_votes")
        ],
        [
            Button.inline("ᴀᴅᴍɪɴ ᴄᴍᴅs ➭", data=b"admin_cmd_help"),
            Button.inline(f"{admin_cmd_disp}", data=b"change_admin_cmd")
        ],
        [
            Button.inline("ᴄᴀɴ ᴘʟᴀʏ ➭", data=b"can_play_help"),
            Button.inline(f"{can_play_disp}", data=b"change_can_play")
        ],
        [
            Button.inline("ᴘʟᴀʏᴍᴏᴅᴇ ➭", data=b"play_mode_help"),
            Button.inline(f"{play_mode_disp}", data=b"change_play_mode")
        ]
    ]


@add_command("streammode", "changemode", "playmode")
async def StreamMode(event, command, args):
    user = await event.get_sender()
    if not await is_admin(user, event):
        return await event.reply("ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs.")

    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    settings = stream_mode.find_one({"chat_id": chat_id}) or {}

    vote_mode = settings.get("vote_mode", 5)
    play_mode = settings.get("play_mode", "normal")
    admin_cmd = settings.get("admin_cmd", "admins")
    can_play = settings.get("can_play", "everyone")

    admin_cmd_disp, can_play_disp, play_mode_disp = get_display_values(
        vote_mode, play_mode, admin_cmd, can_play
    )

    text = (
        f"ʜᴇʀᴇ ɪs {BOT_MENTION}'s sᴛʀᴇᴀᴍ settings\n"
        f"sᴇʟᴇᴄᴛ ᴛʜᴇ ᴍᴏᴅᴇ ɪɴ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘʟᴀʏ ᴛʜᴇ ǫᴜᴇʀɪᴇs\n"
        f"ɪɴsɪᴅᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ : {chat.title}"
    )

    buttons = build_buttons(vote_mode, admin_cmd_disp, can_play_disp, play_mode_disp)
    await event.reply(text, buttons=buttons, parse_mode="html")


@Alishan.on(events.CallbackQuery())
async def change_callback(event):
    data = event.data
    if data not in [b"can_play_help", b"play_mode_help", b"votes_help", b"admin_cmd_help", b"change_admin_cmd", b"change_can_play", b"change_votes", b"change_play_mode"]:
        return
    user = await event.get_sender()
    if not await is_admin(user, event):
        return await event.answer("ᴏɴʟʏ ᴀᴅᴍɪɴ ᴄᴀɴ ᴄʜᴀɴɢᴇ ʜᴇʀᴇ.", alert=True)
    if data == b"can_play_help":
        return await event.answer(
        "ᴇᴠᴇʀʏᴏɴᴇ : ᴀɴʏᴏɴᴇ ᴄᴀɴ ᴘʟᴀʏ.\n\n"
        "ᴀᴅᴍɪɴs : ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴘʟᴀʏ.",
        alert=True
    )
    elif data == b"play_mode_help":
        return await event.answer(
        "ɴᴏʀᴍᴀʟ : ᴅᴇғᴀᴜʟᴛ ᴘʟᴀʏ ᴍᴏᴅᴇ.\n\n"
        "ᴇᴄᴏ : ʟᴏᴡ ʀᴇsᴏᴜʀᴄᴇ ᴍᴏᴅᴇ.\n\n"
        "ʟᴏғɪ : ʟᴏғɪ sᴏɴɢ ᴘʟᴀʏ ᴀs ᴅᴇғᴀᴜʟᴛ.",
        alert=True
    )
    elif data == b"votes_help":
        return await event.answer(
        "ᴠᴏᴛᴇ sʏsᴛᴇᴍ ᴀʟʟᴏᴡs ɴᴏɴ-ᴀᴅᴍɪɴs ᴛᴏ ᴜsᴇ sᴏᴍᴇ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs.",
        alert=True
    )
    elif data == b"admin_cmd_help":
        return await event.answer(
        "ᴇᴠᴇʀʏᴏɴᴇ : ᴀʟʟ ᴍᴇᴍʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴀᴅᴍɪɴ ᴄᴍᴅs.\n\n"
        "ᴀᴅᴍɪɴs : ᴏɴʟʏ ᴀᴅᴍɪɴs ᴀʟʟᴏᴡᴇᴅ.",
        alert=True
    )
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)

    settings = stream_mode.find_one({"chat_id": chat_id}) or {}

    vote_mode = settings.get("vote_mode", 5)
    play_mode = settings.get("play_mode", "normal")
    admin_cmd = settings.get("admin_cmd", "admins")
    can_play = settings.get("can_play", "everyone")

    if data == b"change_admin_cmd":
        admin_cmd = "admins" if admin_cmd == "everyone" else "everyone"

    elif data == b"change_play_mode":
        if play_mode == "normal":
            play_mode = "eco"
        elif play_mode == "eco":
            play_mode = "lofi"
        else:
            play_mode = "normal"

    elif data == b"change_votes":
        vote_mode = 1 if vote_mode >= 5 else vote_mode + 1

    elif data == b"change_can_play":
        can_play = "admins" if can_play == "everyone" else "everyone"

    stream_mode.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "vote_mode": vote_mode,
                "admin_cmd": admin_cmd,
                "play_mode": play_mode,
                "can_play": can_play
            }
        },
        upsert=True
    )
    admin_cmd_disp, can_play_disp, play_mode_disp = get_display_values(
        vote_mode, play_mode, admin_cmd, can_play
    )

    text = (
        f"ʜᴇʀᴇ ɪs {BOT_MENTION}'s sᴛʀᴇᴀᴍ settings\n"
        f"sᴇʟᴇᴄᴛ ᴛʜᴇ ᴍᴏᴅᴇ ɪɴ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘʟᴀʏ ᴛʜᴇ ǫᴜᴇʀɪᴇs\n"
        f"ɪɴsɪᴅᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ : {chat.title}‎"
    )

    buttons = build_buttons(vote_mode, admin_cmd_disp, can_play_disp, play_mode_disp)

    await event.edit(text, buttons=buttons, parse_mode="html")