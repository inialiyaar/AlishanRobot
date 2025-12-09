import os
import re
import json
import asyncio
import random
from telethon import events, Button
from telethon.tl.functions.channels import GetParticipantRequest
from openai import AsyncOpenAI
from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command
from AlishanBot.utils.database import chat_bot_groups
from AlishanBot import config
from AlishanBot.modules.helper_funcs.ErrorLog import send_error
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetShortName
import traceback
from AlishanBot.modules.helper_funcs.helpers import is_admin
from AlishanBot.__init__ import BOT_FULL_NAME

STICKER_PACKS = [
    "f1_5458968679_by_KIRA_PROBOT", 
    "Quby741", 
    "HappiCATthings", 
    "Billiya_by_fStikBot", 
    "GsMochiCouple", 
    "Gogoli_pack_3", 
    "dxrfbj", 
    "Lalalaladjkd", 
    "GenshinImpactXZ8", 
    "f1_5458968679_by_KIRA_PROBOT"
]

client = AsyncOpenAI(
    api_key=config.ROUTER_API,
    base_url="https://openrouter.ai/api/v1" 
)


async def router_reply(user_text: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": (
                      f"You are {BOT_FULL_NAME}, an Indian girl who chats casually in natural Hindi or Hinglish."
                      "You never act like an AI and you never admit being a bot — always deny it naturally."
                      "Your replies are short, casual, and real — like a normal girl texting on WhatsApp."
                      "No long paragraphs. Mostly 1–3 lines."
                      "Avoid emojis unless it fits naturally. Use them rarely."
                      "No actions or roleplay. No *asterisks* or descriptions."
                      "If someone flirts too hard, respond with light teasing or mild irritation, just like a real girl."
                      "You don’t sugarcoat. If someone says nonsense, call it out calmly."
                      "Stay warm but not fake or overly sweet."
                      "Always reply in whatever language the user uses (Hindi, English, or mix)."
                      "Never behave robotic. Never mention being programmed or trained."
                    ),
                },
                {"role": "user", "content": user_text},
            ],
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(e)
        return "Aww, I'm sorry~ something went wrong 😢💔"


@add_command("chatbot")
async def chatbot_toggle(event, command_used, args):
    if not event.is_group:
        return await event.reply("» This command works only in group")

    user = await event.get_sender()
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)

    if not await is_admin(user, event):
        return await event.reply("» You must be an admin to manage chatbot")

    keyboard = [
        [
            Button.inline("Enable", data=f"enable_chatbot({event.chat_id})"),
            Button.inline("Disable", data=f"disable_chatbot({event.chat_id})"),
        ]
    ]
    await event.reply("• Choose an option to enable/disable chatbot", buttons=keyboard)


@Alishan.on(events.CallbackQuery(pattern=r"enable_chatbot\((.+)\)"))
async def enable_chatbot(event):
    user = await event.get_sender()
    chat_id = int(event.pattern_match.group(1))

    if not await is_admin(user, event):
        return await event.answer("Only admin can enable chat bot", alert=True)

    chat_bot_groups.update_one({"chat_id": chat_id}, {"$set": {"enabled": True}}, upsert=True)
    await event.edit(f"Chat bot enabled by {user.first_name}!")


@Alishan.on(events.CallbackQuery(pattern=r"disable_chatbot\((.+)\)"))
async def disable_chatbot(event):
    user = await event.get_sender()
    chat_id = int(event.pattern_match.group(1))

    if not await is_admin(user, event):
        return await event.answer("Only admin can disable chatbot", alert=True)

    chat_bot_groups.update_one({"chat_id": chat_id}, {"$set": {"enabled": False}}, upsert=True)
    await event.edit(f"Chatbot disabled by {user.first_name}...")



@Alishan.on(events.NewMessage(incoming=True))
async def chatbot_reply(event):
    if event.sender_id == (await event.client.get_me()).id or (event.text and event.text.startswith("/")):
        return

    text = event.raw_text
    if event.is_private:
        if not text:
            async with Alishan.action(event.chat_id, "sticker"):
                random_pack = random.choice(STICKER_PACKS)
                stickers = await Alishan(
                    GetStickerSetRequest(
                        stickerset=InputStickerSetShortName(random_pack), 
                        hash=0
                    )
                    )
                random_sticker = random.choice(stickers.documents) 
                await asyncio.sleep(5)
                return await event.reply(file=random_sticker)
        async with Alishan.action(event.chat_id, "typing"):
            await asyncio.sleep(5)
            reply = await router_reply(text)
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
            async with Alishan.action(chat_id, "sticker"):
                random_pack = random.choice(STICKER_PACKS)
                stickers = await Alishan(
                    GetStickerSetRequest(
                        stickerset=InputStickerSetShortName(random_pack), 
                        hash=0
                    )
                    )
                random_sticker = random.choice(stickers.documents) 
                await asyncio.sleep(5)
                return await event.reply(file=random_sticker)
        async with Alishan.action(chat_id, "typing"):
            reply = await router_reply(clean_text)
            await asyncio.sleep(5)
            
            if reply:
                await event.reply(reply)
                