from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChatParticipantAdmin,
    ChatParticipantCreator
)
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from AlishanBot.core.bot import Alishan
from AlishanBot.modules.helper_funcs.ErrorLog import send_error
import traceback

async def check_rights(event, user, right):
    try:
        chat = await event.get_chat()
    except:
        chat = await Alishan.get_entity(event)    

    participant = await Alishan(GetParticipantRequest(chat.id, user))
    participant = participant.participant
    
    if isinstance(participant, (ChannelParticipantCreator, ChatParticipantCreator)):
        return True

    if isinstance(participant, (ChannelParticipantAdmin, ChatParticipantAdmin)):
        rights = getattr(participant, "admin_rights", None)
        if rights and getattr(rights, right, False):
            return True

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
    
async def _build_effective_rights(event, rights_template: dict, bot_id: int, promoter_id: int):
    effective = {}
    for key, want in rights_template.items():
        if not want:
            effective[key] = False
            continue
      
        bot_has = await check_rights(event, bot_id, key)
        promoter_has = await check_rights(event, promoter_id, key)
        effective[key] = bool(bot_has and promoter_has)
    return effective
    
async def is_admin(user, event):
    chat = await event.get_chat()

    if not getattr(chat, "megagroup", False) and not getattr(chat, "gigagroup", False):
        return True

    try:
        participant = await event.client(GetParticipantRequest(chat.id, user))
    except Exception as e:
        return False

    participant = participant.participant 

    if isinstance(participant, ChannelParticipantCreator):
        return True

    if isinstance(participant, ChannelParticipantAdmin):
        rights = getattr(participant, "admin_rights", None)
        if rights:
            return True

    return False       