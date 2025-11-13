from telethon.tl.types import (
    ChannelParticipantCreator,
    ChannelParticipantAdmin,
)
from telethon.tl.functions.channels import GetParticipantRequest

async def check_rights(event, user, right):
    chat = await event.get_chat()

    if not getattr(chat, "megagroup", False) and not getattr(chat, "gigagroup", False):
        return True

    try:
        participant = await event.client(GetParticipantRequest(chat.id, user))
    except Exception as e:
        print(f"GetParticipantRequest failed: {e}")
        return False

    participant = participant.participant 

    if isinstance(participant, ChannelParticipantCreator):
        return True

    if isinstance(participant, ChannelParticipantAdmin):
        rights = getattr(participant, "admin_rights", None)
        if rights and getattr(rights, right, False):
            return True

    return False
    
async def _build_effective_rights(event, rights_template: dict, bot_id: int, promoter_id: int):
    effective = {}
    for key, want in rights_template.items():
        if not want:
            effective[key] = False
            continue
      
        bot_has = await check_rights(event, bot_id, key)
        promoter_has = await check_rights(event, promoter_id, key)
        effective[key] = bool(bot_has and promoter_has)
    return eeffectiv 
    
async def is_admin(user, event):
    chat = await event.get_chat()

    if not getattr(chat, "megagroup", False) and not getattr(chat, "gigagroup", False):
        return True

    try:
        participant = await event.client(GetParticipantRequest(chat.id, user))
    except Exception as e:
        print(f"GetParticipantRequest failed: {e}")
        return False

    participant = participant.participant 

    if isinstance(participant, ChannelParticipantCreator):
        return True

    if isinstance(participant, ChannelParticipantAdmin):
        rights = getattr(participant, "admin_rights", None)
        if rights:
            return True

    return False       