from AlishanBot.core.bot import Alishan
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantCreator, ChannelParticipantAdmin
from datetime import timedelta, datetime
from AlishanBot import config
from AlishanBot.core.decorators import add_command
from AlishanBot.__init__ import BOT_ID

BAN_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)
UNBAN_RIGHTS = ChatBannedRights(until_date=None, view_messages=False)

async def has_ban_permission(chat, user_id):
    try:
        participant = await Alishan(GetParticipantRequest(chat.id, user_id))
        participant = participant.participant
        if isinstance(participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            return participant.admin_rights and participant.admin_rights.ban_users
    except Exception as e:
        print(f"[has_ban_permission error] {e}")
    return False
    
async def get_target_user(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        user = await Alishan.get_entity(reply_msg.sender_id)
        return user 
    else:
        args = event.raw_text.split()
        if len(args) >= 2:
            try:
                user = await Alishan.get_entity(args[1])
                return user
            except:
                return None
    return None    

@add_command("ban")
async def ban_user(event, command_used, args):
    if not event.is_group:
        return await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs.")
    
    if not args and not event.is_reply:
        return await event.reply("ɪ ᴅᴏᴜʙᴛ ᴛʜᴀᴛ's ᴀ ᴜsᴇʀ.")
        
    chat = await event.get_chat()
    sender = await event.get_sender()
    user = await get_target_user(event)    
    reply = await event.get_reply_message()
    if not user:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")
    try:
        user.first_name
    except:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")
    if user.id == BOT_ID:
        return await event.reply("ᴏʜ ʏᴇᴀʜ, ʙᴀɴ ᴍʏsᴇʟғ, ɴᴏᴏʙ!")
    if user.id == config.OWNER_ID:
        return await event.reply("ᴛʀʏɪɴɢ ᴛᴏ ᴘᴜᴛ ᴍᴇ ᴀɢᴀɪɴsᴛ ᴀ ɢᴏᴅ ʟᴇᴠᴇʟ ᴅɪsᴀsᴛᴇʀ ʜᴜʜ? ")
    if not await has_ban_permission(chat, BOT_ID):
        return await event.reply("ᴏʜʜ sʜɪᴛ!! ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʙᴀɴ ᴜsᴇʀs ʀɪɢʜᴛs")    
    if not (sender.id in config.sudo_list or await has_ban_permission(chat, sender.id)):
        return await event.reply("ᴄᴀɴ'ᴛ ʙᴀɴ! ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʙᴀɴ ᴘᴇʀᴍɪssɪᴏɴ")
    args = event.raw_text.split(maxsplit=2)
    reason = args[2] if len(args) >= 3 else "ɴᴏ ʀᴇᴀsᴏɴ."
    try:
        await Alishan(EditBannedRequest(chat.id, user.id, BAN_RIGHTS))
    except Exception as e:
        if "tried to ban an admin" in str(e):
            return await event.reply(f"ʟᴏʟ, ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ʙᴀɴ ᴀᴅᴍɪɴ? ")
        return await event.reply(f"Failed to ban: {e}")

    text = (
        f"<code>❕</code><b>ʙᴀɴ ᴇᴠᴇɴᴛ</b>\n"
        f"<code> </code><b>•  ʙᴀɴɴᴇᴅ ʙʏ:</b> <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
        f"<code> </code><b>•  ᴜsᴇʀ:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>"
    )
    if reason:
        text += f"\n<code> </code><b>•  ʀᴇᴀsᴏɴ:</b> \n{reason}"

    await event.reply(text, parse_mode="html")


@add_command("tban")
async def temp_ban_user(event, command_used, args):
    if not event.is_group:
        return await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs.")
    chat = await event.get_chat()
    sender = await event.get_sender()
    if not await has_ban_permission(chat, BOT_ID):
        return await event.reply("ᴏʜʜ sʜɪᴛ!! ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʙᴀɴ ᴜsᴇʀs ʀɪɢʜᴛs")
    if not (sender.id in config.sudo_list or await has_ban_permission(chat, sender.id)):
        return await event.reply("ᴄᴀɴ'ᴛ ʙᴀɴ! ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʙᴀɴ ᴘᴇʀᴍɪssɪᴏɴ")   
    if not args and not event.is_reply:
        return await event.reply("ᴏʜʜ sʜɪᴛ!! ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴅᴏɪɴɢ?")
    if event.is_reply and not args:
        return await event.reply("Yoᴜ ʜᴀᴠᴇɴ'ᴛ sᴘᴇᴄɪғɪᴇᴅ ᴀ ᴛɪᴍᴇ ᴛᴏ ʙᴀɴ ᴛʜɪs ᴜsᴇʀ ғᴏʀ!")
    user = await get_target_user(event)
    if not user:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")
    try:
        user.first_name
    except:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")   
    if user.id == BOT_ID:
        return await event.reply("ᴏʜ ʏᴇᴀʜ, ʙᴀɴ ᴍʏsᴇʟғ, ɴᴏᴏʙ!")
    if user.id == config.OWNER_ID:
        return await event.reply("ᴛʀʏɪɴɢ ᴛᴏ ᴘᴜᴛ ᴍᴇ ᴀɢᴀɪɴsᴛ ᴀ ɢᴏᴅ ʟᴇᴠᴇʟ ᴅɪsᴀsᴛᴇʀ ʜᴜʜ? ")    
    if user.id == BOT_ID:
        return await event.reply("ᴏʜ ʏᴇᴀʜ, ʙᴀɴ ᴍʏsᴇʟғ, ɴᴏᴏʙ!")
    chat = await event.get_chat()
    parts = args.split()
    try:
        value_unite = parts[1]
        value = int("".join(filter(str.isdigit, value_unite)))
        unite = "".join(filter(str.isalpha, value_unite)) 
        reason = parts[2] if len(parts) >2 else None
    except Exception as e:
        print(str(e))
        return await event.reply("ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ ғᴏʀᴍᴀᴛ. ᴇxᴀᴍᴘʟᴇ: `/tban 10m Reason`")

    try:
        if unit == "m":
            until_date = datetime.now() + timedelta(minutes=value)
        elif unit == "h":
            until_date = datetime.now() + timedelta(hours=value)
        elif unit == "d":
            until_date = datetime.now() + timedelta(days=value)
        else:
            return await event.reply("ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ ғᴏʀᴍᴀᴛ. ᴜsᴇ m/h/d (e.g., 10m, 2h, 1d).")
    except Exception as e:
        print(str(e))
        return await event.reply("ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ ғᴏʀᴍᴀᴛ. ᴇxᴀᴍᴘʟᴇ: `/tban 10m Reason`")
    rights = ChatBannedRights(until_date=until_date, view_messages=True)
    await Alishan(EditBannedRequest(chat.id, user.id, rights))

    text = (
        f"<b>{chat.title}:</b>\n"
        "ᴛᴇᴍᴩ ʙᴀɴ\n"
        f"<b>ʙᴀɴɴᴇᴅ ʙʏ:</b> <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
        f"<b>ᴜsᴇʀ:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
        f"<b>ᴛɪᴍᴇ:</b> {time_val}"
    )
    if reason:
        text += f"\n<b>ʀᴇᴀsᴏɴ:</b> {reason}"

    await event.reply(text, parse_mode="html")


@add_command("unban")
async def unban_user(event, command_used, args):
    if not event.is_group:
        return await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs.")
    chat = await event.get_chat()
    sender = await event.get_sender()
    if not await has_ban_permission(chat, BOT_ID):
        return await event.reply("ᴏʜʜ sʜɪᴛ!! ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʙᴀɴ ᴜsᴇʀs ʀɪɢʜᴛs")
    if not (sender.id in config.sudo_list or await has_ban_permission(chat, sender.id)):
        return await event.reply("ᴄᴀɴ'ᴛ ʙᴀɴ! ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʙᴀɴ ᴘᴇʀᴍɪssɪᴏɴ")   
    if not args and not event.is_reply:
        return await event.reply("ᴏʜʜ sʜɪᴛ!! ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴅᴏɪɴɢ?")
    user = await get_target_user(event)
    if not user:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")
    try:
        user.first_name
    except:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")    
    try:
        await Alishan(EditBannedRequest(chat.id, user.id, UNBAN_RIGHTS))
    except Exception as e:
        return await event.reply(str(e))
    await event.reply(f"ʏᴇᴘ, ᴛʜɪs ᴜsᴇʀ ᴄᴀɴ ᴊᴏɪɴ!\n\n✅ ᴜɴʙᴀɴɴᴇᴅ <a href='tg://user?id={user.id}'>{user.first_name}</a>", parse_mode="html")


@add_command("kick")
async def kick_user(event, command_used, args):
    if not event.is_group:
        return await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs.")
    chat = await event.get_chat()
    sender = await event.get_sender()
    if not await has_ban_permission(chat, BOT_ID):
        return await event.reply("ᴏʜʜ sʜɪᴛ!! ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʙᴀɴ ᴜsᴇʀs ʀɪɢʜᴛs")
    if not (sender.id in config.sudo_list or await has_ban_permission(chat, sender.id)):
        return await event.reply("ᴄᴀɴ'ᴛ ʙᴀɴ! ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʙᴀɴ ᴘᴇʀᴍɪssɪᴏɴ")   
    if not reply:
        return await event.reply("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴛᴏ ᴋɪᴄʜ.")
        
    user = await get_target_user(event)
    if not user:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")
    try:
        user.first_name
    except:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")
    if user.id == BOT_ID:
        return await event.reply("ᴏʜ ʏᴇᴀʜ, ᴋɪᴄᴋ ᴍʏsᴇʟғ, ɴᴏᴏʙ!")
    if user.id == config.OWNER_ID:
        return await event.reply("ᴛʀʏɪɴɢ ᴛᴏ ᴘᴜᴛ ᴍᴇ ᴀɢᴀɪɴsᴛ ᴀ ɢᴏᴅ ʟᴇᴠᴇʟ ᴅɪsᴀsᴛᴇʀ ʜᴜʜ? ")
    if not user:
        return await event.reply("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")
    chat = await event.get_chat()
    try:
        await Alishan(EditBannedRequest(chat.id, user.id, BAN_RIGHTS))
        await Alishan(EditBannedRequest(chat.id, user.id, UNBAN_RIGHTS))
    except Exception as e:
        return await event.reply(str(e))
    text = (
        f"<b>{chat.title}:</b>\n"
        f"ᴋɪᴄᴋᴇᴅ\n"
        f"<b>ᴋɪᴄᴋᴇᴅ ʙʏ:</b> <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
        f"<b>ᴜsᴇʀ:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>"
    )
    await event.reply(text, parse_mode="html")


@add_command("kickme")
async def kick_me(event, command_used, args):
    if not event.is_group:
        return await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs.")
    if not await has_ban_permission(chat, BOT_ID):
        return await event.reply("ᴏʜʜ sʜɪᴛ!! ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʙᴀɴ ᴜsᴇʀs ʀɪɢʜᴛs")   

    user = await event.get_sender()
    chat = await event.get_chat()
    try:
        await Alishan(EditBannedRequest(chat.id, user.id, BAN_RIGHTS))
        await Alishan(EditBannedRequest(chat.id, user.id, UNBAN_RIGHTS))
    except Exception as e:
        print(str(e))
        return   
    await event.reply("**ᴋɪᴄᴋss ʏᴏᴜ ouᴛ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ**")