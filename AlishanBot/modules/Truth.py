from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command, callback_query
from telethon import events, Button
import requests


@add_command("truth", "dare")
async def command_handler(event, command_used, args):
    if command_used == "truth":
        response = requests.get("https://api.truthordarebot.xyz/api/truth")
        if response.status_code == 200:
            question = response.json().get("question")
            await event.reply(f"**ᴛʀᴜᴛʜ:**\n{question}",buttons=[Button.inline("ɴᴇxᴛ ᴛʀᴜᴛʜ", data=b"next_truth")])
        else:
            await event.reply("ᴜɴᴀʙʟᴇ ᴛᴏ ғᴇᴛᴄʜ ᴀ ᴛʀᴜᴛʜ ǫᴜᴇsᴛɪᴏɴ ᴀᴛ ᴛʜᴇ momenᴛ.")
    else:
        response = requests.get("https://api.truthordarebot.xyz/api/dare")
        if response.status_code == 200:
            question = response.json().get("question")
            await event.reply(f"**ᴅᴀʀᴇ:**\n{question}", buttons=[Button.inline("ɴᴇxᴛ ᴅᴀʀᴇ", data=b"next_dare")])
        else:
            await event.reply("ᴜɴᴀʙʟᴇ ᴛᴏ ғᴇᴛᴄʜ ᴀ ᴅᴀʀᴇ ǫᴜᴇsᴛɪᴏɴ ᴀᴛ ᴛʜᴇ momenᴛ.",)
    
        
@callback_query("next_truth")
async def next_truth_callback(event):
    response = requests.get("https://api.truthordarebot.xyz/api/truth")
    if response.status_code == 200:
        question = response.json().get("question")
        await event.reply(f"**ᴛʀᴜᴛʜ:**\n{question}",buttons=[Button.inline("ɴᴇxᴛ ᴛʀᴜᴛʜ", data=b"next_truth")])
    else:
        await event.reply("ᴜɴᴀʙʟᴇ ᴛᴏ ғᴇᴛᴄʜ ᴀ ᴛʀᴜᴛʜ ǫᴜᴇsᴛɪᴏɴ ᴀᴛ ᴛʜᴇ momenᴛ.")
        
@callback_query("next_dare")
async def next_dare_callback(event):
    response = requests.get("https://api.truthordarebot.xyz/api/dare")
    if response.status_code == 200:
        question = response.json().get("question")
        await event.reply(f"**ᴅᴀʀᴇ:**\n{question}", buttons=[Button.inline("ɴᴇxᴛ ᴅᴀʀᴇ", data=b"next_dare")])
    else:
        await event.reply("ᴜɴᴀʙʟᴇ ᴛᴏ ғᴇᴛᴄɢ ᴀ ᴅᴀʀᴇ ǫᴜᴇsᴛɪᴏɴ ᴀᴛ ᴛʜᴇ momenᴛ.",)