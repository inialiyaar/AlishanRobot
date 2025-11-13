import os
import re
import json
import asyncio
from telethon import events, Button
from telethon.tl.functions.channels import GetParticipantRequest
from openai import AsyncOpenAI
from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command
from AlishanBot.utils.database import chat_bot_groups
from AlishanBot import config

client = AsyncOpenAI(
    api_key=config.ROUTER_API,
    base_url="https://openrouter.ai/api/v1" 
)

async def send_typing_action(chat_id, duration):
    end_time = asyncio.get_event_loop().time() + duration
    while asyncio.get_event_loop().time() < end_time:
        async with Alishan.action(chat_id, "typing"):
            await asyncio.sleep(4)


async def is_admin(user_id, chat_id, bot):
    try:
        participant = await bot(GetParticipantRequest(chat_id, user_id))
        if getattr(participant.participant, "admin_rights", None) or getattr(participant.participant, "rank", None):
            return True
    except Exception:
        pass
    return False


async def router_reply(user_text: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Mitsuri — a soft-spoken, real girl who replies naturally like a human. "
                        "You never use asterisks (*), tildes (~), or act out actions. "
                        "Your tone is gentle, kind, and realistic — like texting a close friend. "
                        "Keep replies short and natural (1–2 sentences). "
                        "If the user talks in Hindi, reply in Hindi. If in English, reply in English. "
                        "Avoid emojis unless it feels truly natural, and never overuse them. "
                        "Speak like a normal person — not overly sweet or exaggerated."
                    ),
                },
                {"role": "user", "content": user_text},
            ],
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Aww, I'm sorry~ something went wrong 😢💔"


@add_command("chatbot")
async def chatbot_toggle(event, command_used, args):
    if not event.is_group:
        return await event.reply("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘ")

    user = await event.get_sender()
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)

    if not await is_admin(user.id, event.chat_id, event.client):
        return await event.reply("» ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴄʜᴀᴛʙᴏᴛ")

    keyboard = [
        [
            Button.inline("ᴇɴᴀʙʟᴇ", data=f"enable_chatbot({event.chat_id})"),
            Button.inline("ᴅɪsᴀʙʟᴇ", data=f"disable_chatbot({event.chat_id})"),
        ]
    ]
    await event.reply("• ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ", buttons=keyboard)


@Alishan.on(events.CallbackQuery(pattern=r"enable_chatbot\((.+)\)"))
async def enable_chatbot(event):
    user = await event.get_sender()
    chat_id = int(event.pattern_match.group(1))

    if not await is_admin(user.id, chat_id, event.client):
        return await event.answer("ᴏɴʟʏ ᴀᴅᴍɪɴ ᴄᴀɴ ᴇɴᴀʙʟᴇ ᴄʜᴀᴛ ʙᴏᴛ", alert=True)

    chat_bot_groups.update_one({"chat_id": chat_id}, {"$set": {"enabled": True}}, upsert=True)
    await event.edit(f"ᴄʜᴀᴛ ʙᴏᴛ ᴇɴᴀʙʟᴇ ᴅ ʙʏ {user.first_name}~!")


@Alishan.on(events.CallbackQuery(pattern=r"disable_chatbot\((.+)\)"))
async def disable_chatbot(event):
    user = await event.get_sender()
    chat_id = int(event.pattern_match.group(1))

    if not await is_admin(user.id, chat_id, event.client):
        return await event.answer("ᴏɴʟʏ ᴀᴅᴍɪɴ ᴄᴀɴ ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ", alert=True)

    chat_bot_groups.update_one({"chat_id": chat_id}, {"$set": {"enabled": False}}, upsert=True)
    await event.edit(f"ᴄʜᴀᴛʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ ʙʏ {user.first_name}...")



@Alishan.on(events.NewMessage(incoming=True))
async def chatbot_reply(event):
    if event.sender_id == (await event.client.get_me()).id or (event.text and event.text.startswith("/")):
        return

    text = event.raw_text
    if not text:
        return

    if event.is_private:
        typing_task = asyncio.create_task(send_typing_action(event.chat_id, 15))
        reply = await router_reply(text)
        typing_task.cancel()
        if reply:
            await event.reply(reply)
        return

    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    data = chat_bot_groups.find_one({"chat_id": chat_id, "enabled": True})
    if not data:
        return

    me = await event.client.get_me()
    if (
        (event.is_reply and (await event.get_reply_message()).sender_id == me.id)
        or re.search(fr"@{me.username}", text, re.IGNORECASE)
    ):
        clean_text = text.replace(f"@{me.username}", "").strip()
        if not clean_text:
            return
        typing_task = asyncio.create_task(send_typing_action(event.chat_id, 15))
        reply = await router_reply(clean_text)
        typing_task.cancel()
        if reply:
            await event.reply(reply)