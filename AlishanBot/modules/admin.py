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
        return await event.reply("» This command can be used in groups only.")
    chat = await event.get_chat()
    sender = await event.get_sender()
    
    if not await check_rights(event, BOT_ID, "change_info"):
        return await event.reply("» I don't have permission to change group info.")    
    if not await check_rights(event, sender, "change_info"):
        return await event.reply("» You don't have permission to change group info.")

    reply = await event.get_reply_message()
    if not reply or not reply.sticker:
        return await event.reply("» Reply to a sticker to set it as group sticker pack.")

    sticker_attr = next((a for a in reply.document.attributes if isinstance(a, types.DocumentAttributeSticker)), None)
    if not sticker_attr or not sticker_attr.stickerset:
        return await event.reply("» Couldn't detect the sticker set from that sticker.")

    if isinstance(sticker_attr.stickerset, types.InputStickerSetShortName):
        set_name = sticker_attr.stickerset.short_name
    elif isinstance(sticker_attr.stickerset, types.InputStickerSetID):
        set_id = sticker_attr.stickerset.id
        access_hash = sticker_attr.stickerset.access_hash
        sticker_attr.stickerset = types.InputStickerSetID(id=set_id, access_hash=access_hash)
        set_name = None
    else:
        return await event.reply("» Couldn't detect the sticker set from that sticker.")

    try:
        full_chat = await Alishan(functions.channels.GetFullChannelRequest(channel=chat))
        current_set = full_chat.full_chat.stickerset
        if current_set:
            if isinstance(current_set, types.StickerSet):
                if isinstance(sticker_attr.stickerset, types.InputStickerSetID):
                    if current_set.id == sticker_attr.stickerset.id:
                        return await event.reply("This sticker pack is already set in this group.")
                elif isinstance(sticker_attr.stickerset, types.InputStickerSetShortName):
                    if current_set.short_name == sticker_attr.stickerset.short_name:
                        return await event.reply(f"» <b>{sticker_attr.stickerset.short_name}</b> is already set for this group.")
    except Exception:
        pass 

    try:
        await Alishan(functions.channels.SetStickersRequest(
            channel=chat,
            stickerset=sticker_attr.stickerset
        ))

        if set_name:
            await event.reply(f"» Successfully set <b>{set_name}</b> as group sticker <b>{chat.title}</b>!", parse_mode="html")
        else:
            await event.reply(f"» Successfully set a sticker pack in <b>{chat.title}</b>!", parse_mode="html")

    except RPCError as e:
        if "Participants_too_few" in str(e):
            await event.reply("» Your group needs minimum 100 members to set a sticker pack.")
        else:
            await event.reply(f"Error: {e}")

@add_command("setgpic")
async def set_chat_pic(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command can be used in groups only.")
    chat = await event.get_chat()
    sender = await event.get_sender()
    
    if not await check_rights(event, BOT_ID, "change_info"):
        return await event.reply("» I don't have permission to change group info.")    
    if not await check_rights(event, sender, "change_info"):
        return await event.reply("» You don't have permission to change group info.")

    reply = await event.get_reply_message()
    if not reply or not (reply.photo or reply.document):
        return await event.reply("» Reply to a photo or file to set it as group profile pic.")

    dl = await event.reply("» Changing group profile picture..")
    file_path = await Alishan.download_media(reply, "gpic.png")

    try:
        file = await Alishan.upload_file(file_path)
        await Alishan(EditPhotoRequest(chat.id, InputChatUploadedPhoto(file)))
        await event.reply("» Successfully set group profile picture.")
    except PhotoCropSizeSmallError:
        await event.reply("» The photo is too small to be set as group profile pic.")
    except ChatAdminRequiredError:
        await event.reply("» I don't have permission to change group photo.")
    except Exception as e:
        await event.reply(f"Error: {e}")
    finally:
        await dl.delete()
        if os.path.exists(file_path):
            os.remove(file_path)


@add_command("rmpic")
async def rm_chat_pic(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command can be used in groups only.")
    chat = await event.get_chat()
    sender = await event.get_sender()
    
    if not await check_rights(event, BOT_ID, "change_info"):
        return await event.reply("» I don't have permission to change group info.")    
    if not await check_rights(event, sender, "change_info"):
        return await event.reply("» You don't have permission to change group info.")

    try:
        await Alishan(EditPhotoRequest(chat.id, InputChatPhotoEmpty()))
        await event.reply("» Successfully deleted group's profile picture.")
    except ChatAdminRequiredError:
        await event.reply("» I don't have permission to delete group photo.")
    except Exception as e:
        await event.reply(f"Error: {e}")


@add_command("setdes")
async def set_desc(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command can be used in groups only.")
    chat = await event.get_chat()
    sender = await event.get_sender()
    if not await check_rights(event, BOT_ID, "change_info"):
        return await event.reply("» I don't have permission to change group info baby!")    
    if not await check_rights(event, sender, "change_info"):
        return await event.reply("» You don't have permission to change group info baby!")
    reply = await event.get_reply_message()
    if not args and not reply:
        return await event.reply("» What do you want to set as description, huh?")
    if args:
        pass
    elif reply:
        if reply.media:
            return await event.reply(" Wait.. what?? You trying to set media as description 🙃")
        args = reply.text 

    desc = " ".join(args)
    if len(desc) > 255:
        return await event.reply("» Description must be less than 255 characters!")

    try:
        await Alishan(EditChatAboutRequest(chat.id, desc))
        
        await event.reply(f"» Successfully updated group description in {chat.title}!")
    except Exception as e:
        await event.reply(f"Error: {e}")

@add_command("setgtitle")
async def set_title(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command can be used in groups only.")
    reply = await event.get_reply_message()
    sender = await event.get_sender()
    if not args and not reply:
        return await event.reply("» What do you want to set as title, huh?")
    if not await check_rights(event, BOT_ID, "change_info"):
        return await event.reply("» I don't have permission to change group info baby!")    
    if not await check_rights(event, sender, "change_info"):
        return await event.reply("» You don't have permission to change group info baby!")    

    if not event.is_group:
        return await event.reply("» This command is for groups only.")
    if args:
        title = args
    else:
        if reply.media:
            return await event.reply(" Wait.. what?? You trying to set media as title 🙃")
        title = reply.text 
    chat = await event.get_chat()

    if chat.title == title:
        return await event.reply("» This title is already set ✨")

    try:
        if getattr(chat, "megagroup", False) or getattr(chat, "broadcast", False):
            await Alishan(EditTitleRequest(chat, title))
        else:
            await Alishan(EditChatTitleRequest(chat_id=chat.id, title=title))

        await event.reply(
            f"» Successfully set <b>{title}</b> as new chat title!",
            parse_mode="html",
        )
    except Exception as e:
        if "wasn't modified" in str(e):
            await event.reply("» This title is already active ✨")
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
        return await event.reply("» This command works in groups only")

    user = await get_target_user(event)    
    if not user:
        return await event.reply("» What the hell 😒 provide user plz..")

    if not await check_rights(event, event.sender.id, "add_admins"):
        return await event.reply("» You don't have permissions to full promote")

    bot_id = BOT_ID
    effective = await _build_effective_rights(event, FULL_ADMIN_RIGHTS, bot_id, event.sender_id)

    if await is_admin(user, event):
        return await event.reply("» According to me that user is already an admin here !")
        
    try:
        await event.client.edit_admin(event.chat_id, user.id, **effective)
        chat = await event.get_chat()
        await event.reply(
            f"» Fullpromoting a user in <b>{chat.title}</b>\n\n"
            f"User : ➥ <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
            f"Promoter : ➥ <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
            f"Chat : ➥ {chat.title}",
            parse_mode="html"
        )
    except ChatAdminRequiredError:
        await event.reply("» Failed: You don't have rights to full promote")
    except Exception as e:
        await event.reply(f"» Failed !\n<b>Reason :</b> {e}")


@add_command("promote")
async def promote(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command works in groups only")

    user = await get_target_user(event)
    if not user:
        return await event.reply("» What the hell 😒 provide user plz..")

    if not await check_rights(event, event.sender_id, "add_admins"):
        return await event.reply("» You don't have permissions to promote")

    bot_id = BOT_ID
    effective = await _build_effective_rights(event, PROMOTE_RIGHTS, bot_id, event.sender_id)

    if await is_admin(user, event):
        return await event.reply("» According to me that user is already an admin here !")

    try:
        await event.client.edit_admin(event.chat_id, user.id, **effective)
        chat = await event.get_chat()
        await event.reply(
            f"» Promoting a user in <b>{chat.title}</b>\n\n"
            f"User : ➥ <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
            f"Promoter : ➥ <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
            f"Chat : ➥ {chat.title}",
            parse_mode="html"
        )
    except Exception as e:
        await event.reply(f"» Failed !\n<b>Reason :</b> {e}")


@add_command("lowpromote")
async def lowpromote(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command works in groups only")
        
    user = await get_target_user(event)
    if not user:
        return await event.reply("» What the hell 😒 provide user plz..")
    if not await check_rights(event, event.sender_id, "add_admins"):
        return await event.reply("» You don't have permissions to low promote")

    bot_id = BOT_ID
    effective = await _build_effective_rights(event, LOW_ADMIN_RIGHTS, bot_id, event.sender_id)
    if await is_admin(user, event):
        return await event.reply("» According to me that user is already an admin here !")
    try:
        await event.client.edit_admin(event.chat_id, user.id, **effective)
        chat = await event.get_chat()
        await event.reply(
            f"» Lowpromoting a user in <b>{chat.title}</b>\n\n"
            f"User : ➥ <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
            f"Promoter : ➥ <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
            f"Chat : ➥ {chat.title}",
            parse_mode="html"
        )
    except Exception as e:
        await event.reply(f"» Failed !\n<b>Reason :</b> {e}")


@add_command("demote")
async def demote(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command works in groups only")

    user = await get_target_user(event)
    if not user:
        return await event.reply("» What the hell 😒 provide user plz..")

    if not await check_rights(event, BOT_ID, "add_admins"):
        return await event.reply("» I don't have permissions to demote users")

    if not await check_rights(event, event.sender_id, "add_admins"):
        return await event.reply("» You don't have permissions to demote users")

    try:
        if not await is_admin(user, event):
            return await event.reply("» According to me that user is not an admin here !")

        await event.client.edit_admin(event.chat_id, user.id, is_admin=False)
        chat = await event.get_chat()
        await event.reply(
            f"» Demoting a user in <b>{chat.title}</b>\n\n"
            f"User : ➥ <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
            f"Demoter : ➥ <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a>\n"
            f"Chat : ➥ {chat.title}",
            parse_mode="html"
        )
    except Exception as e:
        await event.reply(f"» Failed: {e}")

@add_command("pin")
async def pin_message(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command can be used in groups only.")

    if not await check_rights(event, BOT_ID, "pin_messages"):
        return await event.reply("» I don't have permissions to pinned messages")
    if not await check_rights(event, event.sender_id, "pin_messages"):
        return await event.reply("» You don't have permissions to pin messages")
    reply = await event.get_reply_message()
    if not reply:
        return await event.reply("» Reply to a message to pin it !")

    try:
        await event.client.pin_message(event.chat_id, reply.id, notify=False)
    except Exception as e:
        return await event.reply(f"Error: {e}")

    msg_link = f"https://t.me/c/{str(event.chat_id)[4:]}/{reply.id}"
    await event.reply(
        f"Message pinned.\n"
        f"🔗 <a href='{msg_link}'>View message</a>",
        parse_mode="html",
        link_preview=False,
    )


@add_command("unpin")
async def unpin_message(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command can be used in groups only.")

    reply = await event.get_reply_message()
    if not await check_rights(event, BOT_ID, "pin_messages"):
        return await event.reply("» I don't have permissions to pinned messages")
    if not await check_rights(event, event.sender_id, "pin_messages"):
        return await event.reply("» You don't have permissions to pin messages")
    try:
        if reply:
            await event.client.unpin_message(event.chat_id, reply.id)
            await event.reply("Unpinned that message.")
        else:
            await event.client.unpin_message(event.chat_id)
            await event.reply("Unpinned the last pinned message.")
    except Exception as e:
        await event.reply(f"Error: {e}")


@add_command("pinned")
async def get_pinned(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command can be used in groups only.")
    chat = await event.get_chat()
    group = await Alishan(GetFullChannelRequest(chat))
    pinned_msg_id = group.full_chat.pinned_msg_id
    if not pinned_msg_id:
        return await event.reply("» No message is pinned in this chat.")

    msg_link = f"https://t.me/c/{str(event.chat_id)[4:]}/{pinned_msg_id}"
    await event.reply(
        f"📌 <b>Pinned Message:</b>\n<a href='{msg_link}'>View message</a>",
        parse_mode="html",
        link_preview=False,
    )


@add_command("invite", "link", "givelink")
async def get_invite(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command can be used in groups only.")
    if not await check_rights(event, BOT_ID, "invite_users"):
        return await event.reply("» I don't have permissions to invite users")    
    if not await check_rights(event, event.sender_id, "invite_users"):
        return await event.reply("» You don't have permissions to invite users")
    chat = await event.get_chat()
    if chat.username:
        await event.reply(f"https://t.me/{chat.username}")
    else:
        try:
            invite = await event.client(ExportChatInviteRequest(event.chat_id))
            await event.reply(invite.link)
        except Exception as e:
            await event.reply(f"Error: {e}")

@add_command("adminlist", "admins", "staff", " invitelink")
async def adminlist(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command can be used in groups only.")
    chat = await event.get_chat()
    msg = await event.reply("» Fetching admins list...")
    admins = await Alishan.get_participants(chat, filter=ChannelParticipantsAdmins)
    full_chat = await Alishan(GetFullChannelRequest(chat))
    owner_rank = "Owner"
    owner = None
    admin_list = []
    
    for user in admins:
        participant = user.participant
        if isinstance(participant, ChannelParticipantCreator):
            owner = user
            if getattr(participant, "rank", None):
                owner_rank = participant.rank if participant.rank else "Owner"
            break
    for user in admins:
        participant = user.participant
        if getattr(participant, "admin_rights", None) or getattr(participant, "rank", None):
            rank = participant.rank if participant.rank else "Admin"
            if participant.admin_rights and getattr(participant, "is_admin", True):
                if owner:
                    if user.id == owner.id:
                        continue
                admin_list.append(f"╭⎋ <a href=\"tg://user?id={user.id}\">{user.first_name}</a>\n╰⊚ {rank}\n")
        if getattr(participant, "admin_rights", None) is None and getattr(participant, "rank", None) is None:
            pass
    if owner:      
        text = f"Admins in <b>{chat.title}</b>:\nOwner:\n╭⎋ <a href='tg://user?id={owner.id}'>{owner.first_name}</a>\n╰⊚ {owner_rank}\n\n"    
    else:
        text = f"Admins in <b>{chat.title}</b>:\nOwner:\n╭⎋ Anonymous\n╰⊚ Owner\n\n"    
    if admin_list:
        text += f"Admins:\n" + "\n".join(admin_list)
    await msg.edit(text, parse_mode="html")