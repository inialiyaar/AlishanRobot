from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command, callback_query
from telethon import events, Button
from datetime import datetime
import aiohttp
import requests
import random

AFK_USERS = {}
TENOR_API = "https://g.tenor.com/v1/search?q={query}&key=LIVDSRZULELA&limit=25"

ACTION_CMDS = {
    "slap": "slap",
    "punch": "punch",
    "hug": "anime hug",
    "pat": "anime pat",
    "kiss": "anime kiss",
    "cry": "anime cry",
    "dance": "anime dance",
    "wink": "anime wink",
    "bite": "anime bite",
    "blush": "anime blush",
    "smile": "anime smile",
    "love": "anime love",
    "highfive": "anime highfive",
    "wave": "anime wave",
}

TEXT_FUN = ["roll", "decide", "toss", "rlg", "truth", "dare"]

FACES = [
    "└[@∵@]┘", "└[@Ω@]┘", "└[@x@]┘",
    "└[@_@]┘", "└[@-@]┘", "└[@ᴥ@]┘"
]

async def get_random_gif(query):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(TENOR_API.format(query=query)) as resp:
                data = await resp.json()
                results = data.get("results")
                if results:
                    gif = random.choice(results)
                    return gif["media"][0]["gif"]["url"]
    except:
        pass

    return "https://media.tenor.com/HQzD-hMno5UAAAAC/error.gif"


@add_command(
    *list(ACTION_CMDS.keys()),
    *TEXT_FUN
)
async def all_fun_commands(event, command_used, args):

    sender = await event.get_sender()

    if command_used in ACTION_CMDS:
        query = ACTION_CMDS[command_used]
        gif = await get_random_gif(query)

        victim_msg = await event.get_reply_message()

        if victim_msg:
            victim_user = await victim_msg.get_sender()
            msg = f"**{sender.first_name}** {command_used}ed **{victim_user.first_name}**!"
        else:
            msg = f"**{sender.first_name}** {command_used}ed someone!"

        return await event.reply(msg, file=gif)

    if command_used == "roll":
        num = random.randint(1, 6)
        return await event.reply(f"🎲 **{num}**")

    if command_used == "decide":
        return await event.reply(f"🤖 **{random.choice(['Yes', 'No', 'Maybe'])}**")
        
    if command_used == "toss":
        return await event.reply(f"🪙 **{random.choice(['Heads', 'Tails'])}**")

    if command_used == "rlg":
        return await event.reply(random.choice(FACES))

    if command_used == "truth":
        r = requests.get("https://api.truthordarebot.xyz/api/truth").json()
        q = r.get("question", "Error fetching truth.")
        return await event.reply(
            f"**ᴛʀᴜᴛʜ:**\n{q}",
            buttons=[Button.inline("ɴᴇxᴛ ᴛʀᴜᴛʜ", data=b"next_truth")]
        )

    if command_used == "dare":
        r = requests.get("https://api.truthordarebot.xyz/api/dare").json()
        q = r.get("question", "Error fetching dare.")
        return await event.reply(
            f"**ᴅᴀʀᴇ:**\n{q}",
            buttons=[Button.inline("ɴᴇxᴛ ᴅᴀʀᴇ", data=b"next_dare")]
        )


@callback_query("next_truth")
async def next_truth(event):
    r = requests.get("https://api.truthordarebot.xyz/api/truth").json()
    q = r.get("question", "Error fetching truth.")
    await event.edit(
        f"**ᴛʀᴜᴛʜ:**\n{q}",
        buttons=[Button.inline("ɴᴇxᴛ ᴛʀᴜᴛʜ", data=b"next_truth")]
    )

@callback_query("next_dare")
async def next_dare(event):
    r = requests.get("https://api.truthordarebot.xyz/api/dare").json()
    q = r.get("question", "Error fetching dare.")
    await event.edit(
        f"**ᴅᴀʀᴇ:**\n{q}",
        buttons=[Button.inline("ɴᴇxᴛ ᴅᴀʀᴇ", data=b"next_dare")]
    )


@add_command("afk", "brb")
async def set_afk(event, command_used, args):
    user = await event.get_sender()
    reason = args or "No reason provided."

    AFK_USERS[user.id] = {"reason": reason, "since": datetime.now()}

    await event.reply(
        f"ㅤㅤㅤ - {user.first_name}ㅤㅤㅤ ㅤㅤ is now away!"
    )


@Alishan.on(events.NewMessage)
async def remove_afk(event):
    sender = await event.get_sender()
    if not sender:
        return
    if sender.id not in AFK_USERS:
        return

    text = event.raw_text.lower().strip()
    try:
        if text.startswith("/afk") or text.startswith("/brb"):
            return
    except:
        return   

    await event.reply(
        f"ㅤㅤㅤ - {sender.first_name}ㅤㅤㅤ ㅤㅤ is now in the chat!"
    )

    del AFK_USERS[sender.id]


@Alishan.on(events.NewMessage)
async def afk_reply(event):
    if not event.is_group:
        return
    if not event.message.entities:
        return

    for entity in event.message.entities:
        if hasattr(entity, "user_id"):
            uid = entity.user_id
            if uid in AFK_USERS:
                info = AFK_USERS[uid]
                user = await Alishan.get_entity(uid)
                await event.reply(
                    f"• {user.first_name} is AFK.\n"
                    f"• Reason: {info['reason']}"
                )