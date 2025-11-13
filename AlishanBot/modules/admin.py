import os
from telethon import Button, events, functions, types
from telethon.errors import ChatAdminRequiredError, PhotoCropSizeSmallError, RPCError, UserNotParticipantError
from telethon.tl.functions.channels import (
    EditPhotoRequest,
    EditTitleRequest,
    EditBannedRequest,
    GetParticipantRequest,
    EditAdminRequest,
    GetFullChannelRequest
)

from telethon.tl.functions.messages import (
    EditChatTitleRequest,
    EditChatAboutRequest,
    EditChatPhotoRequest,
    ExportChatInviteRequest,
    EditChatTitleRequest
)

from telethon.tl.types import (
    InputChatUploadedPhoto,
    ChatAdminRights,
    ChannelParticipantAdmin,
    ChannelParticipantCreator, 
    InputChatPhotoEmpty, 
    ChatBannedRights,
    ChannelParticipantsAdmins, 
    ChannelParticipantSelf, 
)

from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command
from AlishanBot.modules.helper_funcs.check_rights import check_rights, _build_effective_rights
import html
from AlishanBot. __init__ import BOT_USERNAME, BOT_ID


@add_command("setsticker")
async def set_sticker(event, command_used, args):
    chat = await event.get_chat()
    sender = await event.get_sender()
    
    if not await check_rights(event, BOT_ID, "change_info"):
        return await event.reply("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ ʙᴀʙʏ!")    
    if not await check_rights(event, sender, "change_info"):
        return await event.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴩ ɪɴғᴏ ʙᴀʙʏ !")

    reply = await event.get_reply_message()
    if not reply or not reply.sticker:
        return await event.reply("» ʀᴇᴩʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ɢʀᴏᴜᴩ sᴛɪᴄᴋᴇʀ ᴩᴀᴄᴋ !")

    sticker_attr = next((a for a in reply.document.attributes if isinstance(a, types.DocumentAttributeSticker)), None)
    if not sticker_attr or not sticker_attr.stickerset:
        return await event.reply("» ᴄᴏᴜʟᴅɴ'ᴛ ᴅᴇᴛᴇᴄᴛ ᴛʜᴇ sᴛɪᴄᴋᴇʀ sᴇᴛ ғʀᴏᴍ ᴛʜᴀᴛ sᴛɪᴄᴋᴇʀ !")

    if isinstance(sticker_attr.stickerset, types.InputStickerSetShortName):
        set_name = sticker_attr.stickerset.short_name
    elif isinstance(sticker_attr.stickerset, types.InputStickerSetID):
        set_id = sticker_attr.stickerset.id
        access_hash = sticker_attr.stickerset.access_hash
        sticker_attr.stickerset = types.InputStickerSetID(id=set_id, access_hash=access_hash)
        set_name = None
    else:
        return await event.reply("» ᴄᴏᴜʟᴅɴ'ᴛ ᴅᴇᴛᴇᴄᴛ ᴛʜᴇ sᴛɪᴄᴋᴇʀ sᴇᴛ ғʀᴏᴍ ᴛʜᴀᴛ sᴛɪᴄᴋᴇʀ !")

    try:
        full_chat = await Alishan(functions.channels.GetFullChannelRequest(channel=chat))
        current_set = full_chat.full_chat.stickerset
        if current_set:
            if isinstance(current_set, types.StickerSet):
                if isinstance(sticker_attr.stickerset, types.InputStickerSetID):
                    if current_set.id == sticker_attr.stickerset.id:
                        return await event.reply("» ᴛʜɪs sᴛɪᴄᴋᴇʀ ᴩᴀᴄᴋ ɪs ᴀʟʀᴇᴀᴅʏ sᴇᴛ ғᴏʀ ᴛʜɪs ɢʀᴏᴜᴩ !")
                elif isinstance(sticker_attr.stickerset, types.InputStickerSetShortName):
                    if current_set.short_name == sticker_attr.stickerset.short_name:
                        return await event.reply(f"» <b>{sticker_attr.stickerset.short_name}</b> ɪs ᴀʟʀᴇᴀᴅʏ sᴇᴛ ғᴏʀ ᴛʜɪs ɢʀᴏᴜᴩ !")
    except Exception:
        pass 

    try:
        await Alishan(functions.channels.SetStickersRequest(
            channel=chat,
            stickerset=sticker_attr.stickerset
        ))

        if set_name:
            await event.reply(f"» sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ <b>{set_name}</b> ᴀs ɢʀᴏᴜᴩ sᴛɪᴄᴋᴇʀs ɪɴ <b>{chat.title}</b>!", parse_mode="html")
        else:
            await event.reply(f"» sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ᴀ sᴛɪᴄᴋᴇʀ ᴩᴀᴄᴋ ɪɴ <b>{chat.title}</b>!", parse_mode="html")

    except RPCError as e:
        if "Participants_too_few" in str(e):
            await event.reply("» ʏᴏᴜʀ ɢʀᴏᴜᴩ ɴᴇᴇᴅs ᴍɪɴɪᴍᴜᴍ 100 ᴍᴇᴍʙᴇʀs ᴛᴏ sᴇᴛ ᴀ sᴛɪᴄᴋᴇʀ ᴩᴀᴄᴋ !")
        else:
            await event.reply(f"Error: {e}")

@add_command("setchatpic")
async def set_chat_pic(event, command_used, args):
    chat = await event.get_chat()
    sender = await event.get_sender()
    
    if not await check_rights(event, BOT_ID, "change_info"):
        return await event.reply("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ ʙᴀʙʏ!")    
    if not await check_rights(event, sender, "change_info"):
        return await event.reply("» ʏᴏʏ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ ʙᴀʙʏ!")

    reply = await event.get_reply_message()
    if not reply or not (reply.photo or reply.document):
        return await event.reply("» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ғɪʟᴇ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ɢʀᴏᴜᴘ ᴘʀᴏғɪʟ ᴘɪᴄ")

    dl = await event.reply("» ᴄʜᴀɴɢɪɴɢ ɢʀᴏᴜᴘ's ᴘʀᴏғɪʟᴇ ᴘɪᴄᴛᴜʀᴇ...")
    file_path = await Alishan.download_media(reply, "gpic.png")

    try:
        file = await Alishan.upload_file(file_path)
        await Alishan(EditPhotoRequest(chat.id, InputChatUploadedPhoto(file)))
        await event.reply("» sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ grouᴘ ᴘʀᴏғɪʟᴇ ᴘɪᴄ!")
    except PhotoCropSizeSmallError:
        await event.reply("» ᴛʜᴇ ᴘʜᴏᴛᴏ ɪs ᴛᴏᴏ sᴍᴀʟʟ ᴛᴏ ʙᴇ sᴇᴛ ᴀs ɢʀᴏᴜᴘ ᴘʀᴏғɪʟᴇ ᴘɪᴄ!")
    except ChatAdminRequiredError:
        await event.reply("» ɪ ᴅᴏɴ’ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ!")
    except Exception as e:
        await event.reply(f"Error: {e}")
    finally:
        await dl.delete()
        if os.path.exists(file_path):
            os.remove(file_path)


@add_command("rmchatpic")
async def rm_chat_pic(event, command_used, args):
    chat = await event.get_chat()
    sender = await event.get_sender()
    
    if not await check_rights(event, BOT_ID, "change_info"):
        return await event.reply("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ ʙᴀʙʏ!")    
    if not await check_rights(event, sender, "change_info"):
        return await event.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴩ ɪɴғᴏ ʙᴀʙʏ !")

    try:
        await Alishan(EditPhotoRequest(chat.id, InputChatPhotoEmpty()))
        await event.reply("» sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ɢʀᴏᴜᴘ’s ᴘʀᴏғɪʟᴇ ᴘɪᴄᴛᴜʀᴇ!")
    except ChatAdminRequiredError:
        await event.reply("» ɪ ᴅᴏɴ’ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴅᴇʟᴇᴛᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ!")
    except Exception as e:
        await event.reply(f"Error: {e}")


@add_command("setdesc")
async def set_desc(event, command_used, args):
    chat = await event.get_chat()
    sender = await event.get_sender()
    if not await check_rights(event, BOT_ID, "change_info"):
        return await event.reply("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ ʙᴀʙʏ!")    
    if not await check_rights(event, sender, "change_info"):
        return await event.reply("» ʏᴏʏ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ ʙᴀʙʏ!")

    if not args:
        return await event.reply("» ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇᴛ ᴀs ᴅᴇsᴄʀɪᴘᴛɪᴏɴ, ʜᴜʜ?")

    desc = " ".join(args)
    if len(desc) > 255:
        return await event.reply("»ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴍᴜsᴛ ʙᴇ ʟᴇss ᴛʜᴀɴ 255 ᴄʜᴀʀᴀᴄᴛᴇʀs!")

    try:
        await Alishan(EditChatAboutRequest(chat.id, desc))
        
        await event.reply(f"» sᴜᴄᴄᴇssғᴜʟʟʏ ᴜᴘᴅᴀᴛᴇᴅ ɢʀᴏᴜᴘ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ɪɴ {chat.title}!")
    except Exception as e:
        await event.reply(f"Error: {e}")


@Alishan.on(events.NewMessage(pattern=r"^/settitle(@\w+)? (.+)$"))
async def set_title(event):
    match = event.pattern_match
    mention = match.group(1)
    title = match.group(2).strip()

    if mention and mention.lower() != f"@{BOT_USERNAME.lower()}":
        return 
    if not await check_rights(event, BOT_ID, "change_info"):
        return await event.reply("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ ʙᴀʙʏ!")    
    if not await check_rights(event, sender, "change_info"):
        return await event.reply("» ʏᴏʏ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ ʙᴀʙʏ!")    

    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ғᴏʀ ɢʀᴏᴜᴘs ᴏɴʟʏ.")

    chat = await event.get_chat()

    if chat.title == title:
        return await event.reply("» ᴛʜɪs ᴛɪᴛʟᴇ ɪs ᴀʟʀᴇᴀᴅʏ sᴇᴛ ✨")

    try:
        if getattr(chat, "megagroup", False) or getattr(chat, "broadcast", False):
            await Alishan(EditTitleRequest(chat, title))
        else:
            await Alishan(EditChatTitleRequest(chat_id=chat.id, title=title))

        await event.reply(
            f"» sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ <b>{title}</b> ᴀs ɴᴇᴡ ᴄʜᴀᴛ ᴛɪᴛʟᴇ!",
            parse_mode="html",
        )
    except Exception as e:
        if "wasn't modified" in str(e):
            await event.reply("» ᴛʜɪs ᴛɪᴛʟᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴄᴛɪᴠᴇ ✨")
        else:
            await event.reply(f"Error: {e}")

    
FULL_ADMIN_RIGHTS = {
    "change_info": True,
    "post_messages": True,
    "edit_messages": True,
    "delete_messages": True,
    "ban_users": True,
    "invite_users": True,
    "pin_messages": True,
    "add_admins": True,
    "manage_call": True,
    "anonymous": False,
}

PROMOTE_RIGHTS = {
    "change_info": True,
    "post_messages": False,
    "edit_messages": True,
    "delete_messages": True,
    "ban_users": True,
    "invite_users": True,
    "pin_messages": True,
    "add_admins": False,
    "manage_call": True,
    "anonymous": False,
}

LOW_ADMIN_RIGHTS = {
    "change_info": False,
    "post_messages": False,
    "edit_messages": False,
    "delete_messages": True,
    "ban_users": False,
    "invite_users": True,
    "pin_messages": True,
    "add_admins": False,
    "manage_call": True,
}    

@add_command("fullpromote")
async def fullpromote(event, command_used, args):
    sender = await event.get_sender()
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ")

    reply = await event.get_reply_message()
    if not reply:
        return await event.reply("» ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴛᴏ ғᴜʟʟ ᴩʀᴏᴍᴏᴛᴇ")

    if not await check_rights(event, event.sender.id, "add_admins"):
        return await event.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ғᴜʟʟ ᴩʀᴏᴍᴏᴛᴇ")

    bot_id = BOT_ID
    effective = await _build_effective_rights(event, FULL_ADMIN_RIGHTS, bot_id, event.sender_id)

    if not await is_admin(sender, event):
        return await event.reply("» ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ ʜᴇʀᴇ !")
        
    try:
        await event.client.edit_admin(event.chat_id, reply.sender_id, **effective)
        chat = await event.get_chat()
        await event.reply(
            f"» ғᴜʟʟᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ <b>{chat.title}</b>\n\n"
            f"ᴜsᴇʀ : ➥ <a href='tg://user?id={reply.sender_id}'>{reply.sender.first_name}</a>\n"
            f"ᴩʀᴏᴍᴏᴛᴇʀ : ➥ <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
            f"ᴄʜᴀᴛ : ➥ {chat.title}",
            parse_mode="html"
        )
    except ChatAdminRequiredError:
        await event.reply("» ғᴀɪʟᴇᴅ: ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʀɪɢʜᴛs ᴛᴏ ғᴜʟʟ ᴩʀᴏᴍᴏᴛᴇ")
    except Exception as e:
        await event.reply(f"» ғᴀɪʟᴇᴅ !\n<b>ʀᴇᴀsᴏɴ :</b> {e}")


@add_command("promote")
async def promote(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ")

    reply = await event.get_reply_message()
    if not reply:
        return await event.reply("» ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴛᴏ ᴩʀᴏᴍᴏᴛᴇ")

    if not await check_rights(event, event.sender_id, "add_admins"):
        return await event.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴩʀᴏᴍᴏᴛᴇ")

    bot_id = BOT_ID
    effective = await _build_effective_rights(event, PROMOTE_RIGHTS, bot_id, event.sender_id)

    try:
        part = await event.client.get_participant(event.chat_id, reply.sender_id)
        if getattr(part.participant, "admin_rights", None):
            return await event.reply("» ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ ʜᴇʀᴇ !")
    except Exception:
        pass

    try:
        await event.client.edit_admin(event.chat_id, reply.sender_id, **effective)
        chat = await event.get_chat()
        await event.reply(
            f"» ᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ <b>{chat.title}</b>\n\n"
            f"ᴜsᴇʀ : ➥ <a href='tg://user?id={reply.sender_id}'>{reply.sender.first_name}</a>\n"
            f"ᴩʀᴏᴍᴏᴛᴇʀ : ➥ <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
            f"ᴄʜᴀᴛ : ➥ {chat.title}",
            parse_mode="html"
        )
    except Exception as e:
        await event.reply(f"» ғᴀɪʟᴇᴅ !\n<b>ʀᴇᴀsᴏɴ :</b> {e}")


@add_command("lowpromote")
async def lowpromote(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ")

    reply = await event.get_reply_message()
    if not reply:
        return await event.reply("» ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴛᴏ ʟᴏᴡ ᴩʀᴏᴍᴏᴛᴇ")

    if not await check_rights(event, event.sender_id, "add_admins"):
        return await event.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ʟᴏᴡ ᴩʀᴏᴍᴏᴛᴇ")

    bot_id = BOT_ID
    effective = await _build_effective_rights(event, LOW_ADMIN_RIGHTS, bot_id, event.sender_id)

    try:
        part = await event.client.get_participant(event.chat_id, reply.sender_id)
        if getattr(part.participant, "admin_rights", None):
            return await event.reply("» ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ ʜᴇʀᴇ !")
    except Exception:
        pass

    try:
        await event.client.edit_admin(event.chat_id, reply.sender_id, **effective)
        chat = await event.get_chat()
        await event.reply(
            f"» ʟᴏᴡᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ <b>{chat.title}</b>\n\n"
            f"ᴜsᴇʀ : ➥ <a href='tg://user?id={reply.sender_id}'>{reply.sender.first_name}</a>\n"
            f"ᴩʀᴏᴍᴏᴛᴇʀ : ➥ <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
            f"ᴄʜᴀᴛ : ➥ {chat.title}",
            parse_mode="html"
        )
    except Exception as e:
        await event.reply(f"» ғᴀɪʟᴇᴅ !\n<b>ʀᴇᴀsᴏɴ :</b> {e}")


@add_command("demote")
async def demote(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ")

    reply = await event.get_reply_message()
    if not reply:
        return await event.reply("» ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴛᴏ ᴅᴇᴍᴏᴛᴇ")

    if not await check_rights(event, BOT_ID, "add_admins"):
        return await event.reply("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴜsᴇʀs")

    if not await check_rights(event, event.sender_id, "add_admins"):
        return await event.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴜsᴇʀs")

    try:
        part = await event.client.get_participant(event.chat_id, reply.sender_id)
        if not getattr(part.participant, "admin_rights", None):
            return await event.reply("» sᴜᴄᴄᴇssғᴜʟʟʏ: ᴜsᴇʀ ɪs ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ")

        promoter = getattr(part.participant, "promoted_by", None)
        if promoter and promoter != event.sender_id:
            sender_part = await event.client.get_participant(event.chat_id, event.sender_id)
            if getattr(sender_part.participant, "admin_rights", None) == getattr(part.participant, "admin_rights", None):
                return await event.reply("» ᴇQᴜᴀʟ ʀɪɢʜᴛs ᴅᴇᴛᴇᴄᴛᴇᴅ, ᴄᴀɴ'ᴛ ᴅᴇᴍᴏᴛᴇ ᴇQᴜᴀʟ ʀᴀɴᴋ ᴀᴅᴍɪɴ !")

        await event.client.edit_admin(event.chat_id, reply.sender_id, is_admin=False)
        chat = await event.get_chat()
        await event.reply(
            f"» ᴅᴇᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ <b>{chat.title}</b>\n\n"
            f"ᴜsᴇʀ : ➥ <a href='tg://user?id={reply.sender_id}'>{reply.sender.first_name}</a>\n"
            f"ᴅᴇᴍᴏᴛᴇʀ : ➥ <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
            f"ᴄʜᴀᴛ : ➥ {chat.title}",
            parse_mode="html"
        )
    except Exception as e:
        await event.reply(f"» ғᴀɪʟᴇᴅ: {e}")
        
@add_command("refreshadmin")
async def refresh_admin(event, command_used, args):
    await event.reply("» sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇғʀᴇsʜᴇᴅ ᴀᴅᴍɪɴ ᴄᴀᴄʜᴇ !") 

@add_command("pin")
async def pin_message(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ.")

    if not await check_rights(event, BOT_ID, "pinned_messages"):
        return await event.reply("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇs")
    if not await check_rights(event, event.sender_id, "pin_messages"):
        return await event.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴘɪɴ ᴍᴇssᴀɢᴇs")
    reply = await event.get_reply_message()
    if not reply:
        return await event.reply("» ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴩɪɴ ɪᴛ !")

    try:
        await event.client.pin_message(event.chat_id, reply.id, notify=False)
    except Exception as e:
        return await event.reply(f"ᴇʀʀᴏʀ: {e}")

    msg_link = f"https://t.me/c/{str(event.chat_id)[4:]}/{reply.id}"
    await event.reply(
        f"ᴍᴇssᴀɢᴇ ᴘɪɴɴᴇᴅ.\n"
        f"🔗 <a href='{msg_link}'>ᴠɪᴇᴡ ᴍᴇssᴀɢᴇ</a>",
        parse_mode="html",
        link_preview=False,
    )


@add_command("unpin")
async def unpin_message(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ.")

    reply = await event.get_reply_message()
    if not await check_rights(event, BOT_ID, "pinned_messages"):
        return await event.reply("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇs")
    if not await check_rights(event, event.sender_id, "pin_messages"):
        return await event.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴘɪɴ ᴍᴇssᴀɢᴇs")
    try:
        if reply:
            await event.client.unpin_message(event.chat_id, reply.id)
            await event.reply("ᴜɴᴩɪɴɴᴇᴅ ᴛʜᴀᴛ ᴍᴇssᴀɢᴇ.")
        else:
            await event.client.unpin_message(event.chat_id)
            await event.reply("ᴜɴᴩɪɴɴᴇᴅ ᴛʜᴇ ʟᴀsᴛ ᴩɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ.")
    except Exception as e:
        await event.reply(f"ᴇʀʀᴏʀ: {e}")


@add_command("pinned")
async def get_pinned(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ.")
    chat = await event.get_chat()
    if not chat.pinned_msg_id:
        return await event.reply("» ɴᴏ ᴍᴇssᴀɢᴇ ɪs ᴩɪɴɴᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.")

    msg_link = f"https://t.me/c/{str(event.chat_id)[4:]}/{chat.pinned_msg_id}"
    await event.reply(
        f"📌 <b>ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ:</b>\n<a href='{msg_link}'>ᴠɪᴇᴡ ᴍᴇssᴀɢᴇ</a>",
        parse_mode="html",
        link_preview=False,
    )


@add_command("invite")
async def get_invite(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ.")
    if not await check_rights(event, BOT_ID, "invite_users"):
        return await event.reply("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ɪɴᴠɪᴛᴇ ᴜsᴇʀs")    
    if not await check_rights(event, event.sender_id, "invite_users"):
        return await event.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ɪɴᴠɪᴛᴇ ᴜsᴇʀs")
    chat = await event.get_chat()
    if chat.username:
        await event.reply(f"https://t.me/{chat.username}")
    else:
        try:
            invite = await event.client(ExportChatInviteRequest(event.chat_id))
            await event.reply(invite.link)
        except Exception as e:
            await event.reply(f"ᴇʀʀᴏʀ: {e}")



@add_command("adminlist", "admins")
async def adminlist(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ.")

    msg = await event.reply("» ғᴇᴛᴄʜɪɴɢ ᴀᴅᴍɪɴs ʟɪsᴛ...")
    admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
    chat_title = html.escape((await event.get_chat()).title)
    text = f"ᴀᴅᴍɪɴs ɪɴ: 𝗔𝘀𝘁𝗿𝗮𝗕𝗼𝘁𝘇 𝗖𝗵𝗮𝘁\n\n"

    owner_text = "Owner:\n"
    admins_text = "Admins:\n"

    owner_found = False

    for admin in admins:
        mention = f"<a href='tg://user?id={admin.id}'>{html.escape(admin.first_name)}</a>"
        title = getattr(admin.participant, "rank", "ADMIN") 

        is_creator = getattr(admin.participant, "creator", False)
        is_anonymous = getattr(admin.participant, "anonymous", False)

        if is_creator and not owner_found:
            owner_found = True
            if is_anonymous:
                owner_text += f"Anonymous\n    —\n"
            else:
                owner_text += f"{title}\n    {mention}\n"
        else:
            admins_text += f"{title}\n    {mention}\n"

    if not owner_found:
        owner_text += "—\n"

    if admins_text.strip() == "Admins:":
        admins_text += "—\n"

    text += f"{owner_text}\n{admins_text}"

    await msg.edit(text, parse_mode="html")