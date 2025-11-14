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
    EditChatTitleRequest, 
)

from telethon.tl.types import (
    InputChatUploadedPhoto,
    ChatAdminRights,
    ChannelParticipantCreator, 
    InputChatPhotoEmpty, 
    ChatBannedRights,
    ChannelParticipantsAdmins, 
    ChannelParticipantSelf, 
)

from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command
from AlishanBot.modules.helper_funcs.helpers import check_rights, _build_effective_rights, is_admin, get_target_user
import html
from AlishanBot. __init__ import BOT_USERNAME, BOT_ID


@add_command("setsticker")
async def set_sticker(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ.")
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

@add_command("setgpic")
async def set_chat_pic(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ.")
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


@add_command("rmpic")
async def rm_chat_pic(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ.")
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


@add_command("setdes")
async def set_desc(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ.")
    chat = await event.get_chat()
    sender = await event.get_sender()
    if not await check_rights(event, BOT_ID, "change_info"):
        return await event.reply("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ ʙᴀʙʏ!")    
    if not await check_rights(event, sender, "change_info"):
        return await event.reply("» ʏᴏʏ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ ʙᴀʙʏ!")
    reply = await event.get_reply_message()
    if not args and not reply:
        return await event.reply("» ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇᴛ ᴀs ᴅᴇsᴄʀɪᴘᴛɪᴏɴ, ʜᴜʜ?")
    if args:
        pass
    elif reply:
        if reply.media:
            return await event.reply(" ᴡᴀɪᴛ.. ᴡʜᴀᴛ?? ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ sᴇᴛ ᴍᴇᴅɪᴀ ᴀs ᴅᴇsᴄʀɪᴘᴛɪᴏɴ 🙃")
        args = reply.text 

    desc = " ".join(args)
    if len(desc) > 255:
        return await event.reply("»ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴍᴜsᴛ ʙᴇ ʟᴇss ᴛʜᴀɴ 255 ᴄʜᴀʀᴀᴄᴛᴇʀs!")

    try:
        await Alishan(EditChatAboutRequest(chat.id, desc))
        
        await event.reply(f"» sᴜᴄᴄᴇssғᴜʟʟʏ ᴜᴘᴅᴀᴛᴇᴅ ɢʀᴏᴜᴘ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ɪɴ {chat.title}!")
    except Exception as e:
        await event.reply(f"Error: {e}")

@add_command("setgtitle")
async def set_title(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ.")
    reply = await event.get_reply_message()
    sender = await event.get_sender()
    if not args and not reply:
        return await event.reply("» ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇᴛ ᴀs ᴛɪᴛʟᴇ, ʜᴜʜ?")
    if not await check_rights(event, BOT_ID, "change_info"):
        return await event.reply("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ ʙᴀʙʏ!")    
    if not await check_rights(event, sender, "change_info"):
        return await event.reply("» ʏᴏʏ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ ʙᴀʙʏ!")    

    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ғᴏʀ ɢʀᴏᴜᴘs ᴏɴʟʏ.")
    if args:
        title = args
    else:
        if reply.media:
            return await event.reply(" ᴡᴀɪᴛ.. ᴡʜᴀᴛ?? ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ sᴇᴛ ᴍᴇᴅɪᴀ ᴀs ᴛɪᴛʟᴇ 🙃")
        title = reply.text 
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

    user = await get_target_user(event)    
    if not user:
        return await event.reply("» ᴡʜᴀᴛ ᴛʜᴇ ʜᴇʟʟ 😒 ᴘʀᴏᴠɪᴅᴇ ᴜsᴇʀ ᴘʟᴢ..")

    if not await check_rights(event, event.sender.id, "add_admins"):
        return await event.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ғᴜʟʟ ᴩʀᴏᴍᴏᴛᴇ")

    bot_id = BOT_ID
    effective = await _build_effective_rights(event, FULL_ADMIN_RIGHTS, bot_id, event.sender_id)

    if await is_admin(user, event):
        return await event.reply("» ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ ʜᴇʀᴇ !")
        
    try:
        await event.client.edit_admin(event.chat_id, user.id, **effective)
        chat = await event.get_chat()
        await event.reply(
            f"» ғᴜʟʟᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ <b>{chat.title}</b>\n\n"
            f"ᴜsᴇʀ : ➥ <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
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

    user = await get_target_user(event)
    if not user:
        return await event.reply("» ᴡʜᴀᴛ ᴛʜᴇ ʜᴇʟʟ 😒 ᴘʀᴏᴠɪᴅᴇ ᴜsᴇʀ ᴘʟᴢ..")

    if not await check_rights(event, event.sender_id, "add_admins"):
        return await event.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴩʀᴏᴍᴏᴛᴇ")

    bot_id = BOT_ID
    effective = await _build_effective_rights(event, PROMOTE_RIGHTS, bot_id, event.sender_id)

    if await is_admin(user, event):
        return await event.reply("» ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ ʜᴇʀᴇ !")

    try:
        await event.client.edit_admin(event.chat_id, user.id, **effective)
        chat = await event.get_chat()
        await event.reply(
            f"» ᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ <b>{chat.title}</b>\n\n"
            f"ᴜsᴇʀ : ➥ <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
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
        
    user = await get_target_user(event)
    if not user:
        return await event.reply("» ᴡʜᴀᴛ ᴛʜᴇ ʜᴇʟʟ 😒 ᴘʀᴏᴠɪᴅᴇ ᴜsᴇʀ ᴘʟᴢ..")
    if not await check_rights(event, event.sender_id, "add_admins"):
        return await event.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ʟᴏᴡ ᴩʀᴏᴍᴏᴛᴇ")

    bot_id = BOT_ID
    effective = await _build_effective_rights(event, LOW_ADMIN_RIGHTS, bot_id, event.sender_id)
    if await is_admin(user, event):
        return await event.reply("» ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ ʜᴇʀᴇ !")
    try:
        await event.client.edit_admin(event.chat_id, user.id, **effective)
        chat = await event.get_chat()
        await event.reply(
            f"» ʟᴏᴡᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ <b>{chat.title}</b>\n\n"
            f"ᴜsᴇʀ : ➥ <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
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

    user = await get_target_user(event)
    if not user:
        return await event.reply("» ᴡʜᴀᴛ ᴛʜᴇ ʜᴇʟʟ 😒 ᴘʀᴏᴠɪᴅᴇ ᴜsᴇʀ ᴘʟᴢ..")

    if not await check_rights(event, BOT_ID, "add_admins"):
        return await event.reply("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴜsᴇʀs")

    if not await check_rights(event, event.sender_id, "add_admins"):
        return await event.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴜsᴇʀs")

    try:
        if not await is_admin(user, event):
            return await event.reply("» ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ʜᴇʀᴇ !")

        await event.client.edit_admin(event.chat_id, user.id, is_admin=False)
        chat = await event.get_chat()
        await event.reply(
            f"» ᴅᴇᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ <b>{chat.title}</b>\n\n"
            f"ᴜsᴇʀ : ➥ <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
            f"ᴅᴇᴍᴏᴛᴇʀ : ➥ <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
            f"ᴄʜᴀᴛ : ➥ {chat.title}",
            parse_mode="html"
        )
    except Exception as e:
        await event.reply(f"» ғᴀɪʟᴇᴅ: {e}")

@add_command("pin")
async def pin_message(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ.")

    if not await check_rights(event, BOT_ID, "pin_messages"):
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
    if not await check_rights(event, BOT_ID, "pin_messages"):
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
    group = await Alishan(GetFullChannelRequest(chat))
    pinned_msg_id = group.full_chat.pinned_msg_id
    if not pinned_msg_id:
        return await event.reply("» ɴᴏ ᴍᴇssᴀɢᴇ ɪs ᴩɪɴɴᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.")

    msg_link = f"https://t.me/c/{str(event.chat_id)[4:]}/{pinned_msg_id}"
    await event.reply(
        f"📌 <b>ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ:</b>\n<a href='{msg_link}'>ᴠɪᴇᴡ ᴍᴇssᴀɢᴇ</a>",
        parse_mode="html",
        link_preview=False,
    )


@add_command("invite", "link", "givelink")
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



@add_command("adminlist", "admins", "staff", " invitelink")
async def adminlist(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴏɴʟʏ.")
    chat = await event.get_chat()
    msg = await event.reply("» ғᴇᴛᴄʜɪɴɢ ᴀᴅᴍɪɴs ʟɪsᴛ...")
    admins = await Alishan.get_participants(chat, filter=ChannelParticipantsAdmins)
    full_chat = await Alishan(GetFullChannelRequest(chat))
    owner_rank = "ᴏᴡɴᴇʀ"
    owner = None
    admin_list = []
    
    for user in admins:
        participant = user.participant
        if isinstance(participant, ChannelParticipantCreator):
            owner = user
            if getattr(participant, "rank", None):
                owner_rank = participant. rank if participant.rank else "ᴏᴡɴᴇʀ"
            break
    for user in admins:
        participant = user.participant
        if getattr(participant, "admin_rights", None) or getattr(participant, "rank", None):
            rank = participant.rank if participant.rank else "ᴀᴅᴍɪɴ"
            if participant.admin_rights and getattr(participant, "is_admin", True):
                if owner:
                    if user.id == owner.id:
                        continue
                admin_list.append(f"╭⎋ <a href=\"tg://user?id={user.id}\">{user.first_name}</a>\n╰⊚ {rank}\n")
        if getattr(participant, "admin_rights", None) is None and getattr(participant, "rank", None) is None:
            pass
    if owner:      
        text = f"ᴀᴅᴍɪɴs ɪɴ <b>{chat.title}</b>:\nᴏᴡɴᴇʀ:\n╭⎋ <a href='tg://user?id={owner.id}'>{owner.first_name}</a>\n╰⊚ {owner_rank}\n\n"    
    else:
        text = f"ᴀᴅᴍɪɴs ɪɴ <b>{chat.title}</b>:\nᴏᴡɴᴇʀ:\n╭⎋ ᴀɴᴏɴʏᴍᴏᴜs\n╰⊚ ᴏᴡɴᴇʀ\n\n"    
    if admin_list:
        text += f"ᴀᴅᴍɪɴs:\n" + "\n".join(admin_list)
    await msg.edit(text, parse_mode="html") 