from AlishanBot.core.bot import Alishan, Assistant
from AlishanBot.utils.database import groups
from AlishanBot.__init__ import BOT_MENTION, BOT_FULL_NAME
from AlishanBot import config
from telethon import Button
from AlishanBot.core.decorators import callback_query
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

async def add_group(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    groups.insert_one({"chat_id": chat_id})
    full_chat = await Alishan(GetFullChannelRequest(channel=chat_id))
    channel_obj = full_chat.chats[0]
    full_info = full_chat.full_chat 
    full_name = channel_obj.title
    username = channel_obj.username if channel_obj.username else None
    try:
        result = await Alishan(ExportChatInviteRequest(chat_id))
        invite_link = result.link
        invite_button = [
            [Button.url("ɢʀᴏᴜᴘ", invite_link)]
        ]
    except Exception:
        invite_button = [
            [Button.inline("ɪɴᴠɪᴛᴇ ғᴀɪʟᴇᴅ", data=b"invite_failed")]
        ]
    added_by = await event.get_added_by()    
    if added_by:
        mention = f"<a href=\"tg://user?id={added_by.id}\">{added_by.first_name}</a>"
    else:
        mention = "ᴜɴᴋɴᴏᴡɴ"  
    total_members = full_info.participants_count
    creator_id = channel_obj.creator_id if hasattr(channel_obj, "creator_id") else None
    if creator_id:
        try:
            creator = await Alishan.get_entity(creator_id)
            creator = f"<a href=\"tg://user?id{creator.id}\">{creator.first_name}</a>"
        except:
            creator = "ᴜɴᴋɴᴏᴡɴ"
    else:
        creator = "ᴜɴᴋɴᴏᴡɴ"  
        
    caption = f"#GROUPLOG\n{BOT_MENTION} ʜᴀs ᴀᴅᴅᴇᴅ ᴛᴏ {full_name}.\n\n<b>ᴀᴅᴅᴇᴅ ʙʏ :</b> {mention}\n<b>ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> @{username}\n<b>ᴄʜᴀᴛ ɪᴅ :</b> {chat_id}\n\n<b>ᴏᴡɴᴇʀ : </b>{creator}\n<b>ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs :</b> {total_members}"    
    await Alishan.send_message(
        config.EVENT_LOGS,
        caption,
        buttons=invite_button,
        force_document=False,
        parse_mode="html"
        )
        
@callback_query("invite_failed")
async def invite_failed_callback(event):
    await event.answer(f"{BOT_FULL_NAME} ɪs ɴᴏᴛ ᴀᴅᴍɪɴ", alert=True)