from AlishanBot.modules.helper_funcs.play import Play_Audio, Play_Video
from AlishanBot.core.bot import music, Alishan
from AlishanBot.modules.helper_funcs.ytmetadata import meta_data
from pytgcalls import filters
from pytgcalls.types import Update
from telethon import Button
import os
from asyncio import create_task, sleep
from AlishanBot.__init__ import is_playing
from AlishanBot.modules.helper_funcs.thumbnail import Thumbnail
from AlishanBot.__init__ import BOT_USERNAME, ASSISTANT_MENTION, BOT_MENTION
from AlishanBot import config
import asyncio

queues = {}  
queue_position = {}  
current_ind = {}


async def add_to_queue(song_name, chat_id, query_format, mention, download):
    status = await Alishan.send_message(chat_id, f"**sᴇᴀʀᴄʜɪɴɢ...🔎**")
    queues.setdefault(chat_id, [])
    queue_position.setdefault(chat_id, 0)
    current_ind.setdefault(chat_id, 0)
    if download:
        stream_url = song_name
        title = "𝖳ᴇʟᴇɢʀᴀᴍ ʟᴏᴄᴀʟ ᴘʟᴀʏʙᴀᴄᴋ"
        artist = "ᴛᴇʟᴇɢʀᴀᴍ"
        duration = "ɴᴏɴᴇ"
        thumbnail = "https://i.ibb.co/gLNS8hC1/x.jpg"
    try:
        if not chat_id in is_playing:
            if not download:
                data = await meta_data(song_name)
                stream_url, title, artist, duration, thumbnail = data
            if query_format == "video":
                await Play_Video(chat_id, stream_url)
            else:
                await Play_Audio(chat_id, stream_url)
            is_playing[chat_id] = True
            create_task(playing_message(title, artist, duration, query_format, thumbnail, chat_id, mention))
        else:
            data = await meta_data(song_name)
            stream_url, title, artist, duration, thumbnail = data
            queue_position[chat_id] += 1
            create_task(queue_message(title, artist, duration, query_format, chat_id, queue_position[chat_id], mention))
            
        queues[chat_id].append((stream_url, title, artist, duration, thumbnail, mention, query_format)) 
        try:
            await status.delete()
        except Exception:
            pass    
    except Exception as e:
        await Alishan.send_message(chat_id, f"Error {str(e)}")

async def play_next(chat_id):
    if chat_id not in queues or not queues[chat_id]:
        is_playing.pop(chat_id, None)
        await music.leave_call(chat_id)
        await Alishan.send_message(chat_id, f"<b>𝖰ᴜᴇᴜᴇ ғɪɴɪsʜᴇᴅ,</b> {ASSISTANT_MENTION} ʟᴇᴀᴠɪɴɢ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.", parse_mode="html")
        queues.pop(chat_id, None)
        queue_position.pop(chat_id, None)
        current_ind.pop(chat_id, None)
        return
    current_ind[chat_id] += 1
    index = current_ind[chat_id]
    if index >= len(queues[chat_id]):
        await music.leave_call(chat_id)
        await Alishan.send_message(chat_id, f"<b>𝖰ᴜᴇᴜᴇ ғɪɴɪsʜᴇᴅ,</b> {ASSISTANT_MENTION} ʟᴇᴀᴠɪɴɢ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.", parse_mode="html")
        queues.pop(chat_id, None)
        queue_position.pop(chat_id, None)
        current_ind.pop(chat_id, None)
        is_playing.pop(chat_id, None)
        return
        
    try:
        queue_position[chat_id] -= 1
        
        stream_url, title, artist, duration, thumbnail, mention, query_format = queues[chat_id][index]
            
        if query_format == "video":
            await Play_Video(chat_id, stream_url)
        else:
            await Play_Audio(chat_id, stream_url)
          
        create_task(playing_message(title, artist, duration, query_format, thumbnail, chat_id, mention))
        is_playing[chat_id] = True
    except Exception as e:
        await Alishan.send_message(chat_id, f"Error: {str(e)}")

@music.on_update(filters.stream_end())
async def stream_end(_, update: Update):
    chat_id = update.chat_id
    chat_id = int(f"-100{chat_id}" if not str(chat_id).startswith("-100") else chat_id)
    if chat_id in queues:
        await play_next(chat_id)
        
async def playing_message(title, artist, duration, query_format, thumbnail, chat_id, mention):
    if duration >= 3600:
        hours, remainder = divmod(duration, 3600)
        minutes, secs = divmod(remainder, 60)
        duration_text = f"{hours}:{minutes:02}:{secs:02}"
    else:
        minutes, secs = divmod(duration, 60)
        duration_text = f"{minutes}:{secs:02}"

    thumbnail_path = await Thumbnail(thumbnail, title, artist, duration_text)
    if query_format == "video":
        query_format = "𝖵ɪᴅᴇᴏ"
    else:
        query_format = "𝖠ᴜᴅɪᴏ"

    msg = await Alishan.send_file(
        chat_id,
        file=thumbnail_path,
        caption=f"<pre>‣ 𝖳ɪᴛʟᴇ:\n{title}</pre>\n"
                f"<pre><b>‣ 𝖠ʀᴛɪsᴛ:<b> {artist}\n"
                f"<b>‣ 𝖣ᴜʀᴀᴛɪᴏɴ:<b> {duration_text}\n"
                f"<b>‣ 𝖲ᴛʀᴇᴀᴍ 𝖳ʏᴘᴇ :</b> {query_format}</pre>\n"
                f"<b>𝖱ᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {mention}",
        buttons=[
            [Button.inline("00:00 ▱▱▱▱▱▱▱▱▱ 00:00", data=b"ignore_bar")],
            [
                Button.inline("ᴘᴀᴜsᴇ", data=b"pause"),
                Button.inline("ʀᴇᴘʟᴀʏ", data=b"replay"),
                Button.inline("ʀᴇsᴜᴍᴇ", data=b"resume"),
            ],
            [
                Button.inline("sᴋɪᴘ", data=b"skip"),
                Button.inline("sᴛᴏᴘ", data=b"stop"),
            ],
            [
                Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}"),
            ],
        ],
        parse_mode="html"
    )

    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)

    asyncio.create_task(update_duration_bar(msg, duration))


async def update_duration_bar(msg, duration):
    elapsed = 0
    total_blocks = 9

    while elapsed <= duration:
        filled = int((elapsed / duration) * total_blocks)
        empty = total_blocks - filled
        bar = "▰" * filled + "▱" * empty

        current_min, current_sec = divmod(elapsed, 60)
        total_min, total_sec = divmod(duration, 60)

        progress_text = f"{current_min:02}:{current_sec:02} {bar} {total_min:02}:{total_sec:02}"

        try:
            await msg.edit(
                buttons=[
                    [Button.inline(progress_text, data=b"ignore_bar")],
                    [
                        Button.inline("ᴘᴀᴜsᴇ", data=b"pause"),
                        Button.inline("ʀᴇᴘʟᴀʏ", data=b"replay"),
                        Button.inline("ʀᴇsᴜᴍᴇ", data=b"resume"),
                    ],
                    [
                        Button.inline("sᴋɪᴘ", data=b"skip"),
                        Button.inline("sᴛᴏᴘ", data=b"stop"),
                    ],
                    [
                        Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}"),
                    ],
                ]
            )
        except Exception:
            break 

        await asyncio.sleep(5)
        elapsed += 5

async def queue_message(title, artist, duration, query_format, chat_id, queue_pos, mention):
    if duration >= 3600:
            hours, remainder = divmod(duration, 3600)
            minutes, secs = divmod(remainder, 60)
            duration_text = f"{hours}:{minutes:02}:{secs:02}"
    else:
        minutes, secs = divmod(duration, 60)
        duration_text = f"{minutes}:{secs:02}"
    if query_format == "video":
        query_format = "𝖵ɪᴅᴇᴏ"
    else:
        query_format = "𝖠ᴜᴅɪᴏ"        
    await Alishan.send_message(
        chat_id,
        f"<b>➲ 𝖠ᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ ᴀᴛ #{queue_pos}</b>\n\n<pre><b>‣ 𝖳ɪᴛʟᴇ :</b> {title}</pre>\n<pre><b>‣ 𝖠ʀᴛɪsᴛ :</b> {artist}\n<b>‣ 𝖣ᴜʀᴀᴛɪᴏɴ :</b> {duration_text}\n<b>‣ 𝖲ᴛʀᴇᴀᴍ 𝖳ʏᴘᴇ :</b> {query_format}</pre>\n<b>𝖱ᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {mention}",
        buttons = [
        [
            Button.inline("sᴋɪᴘ", data=b"skip"),
            Button.inline("sᴛᴏᴘ", data=b"stop")
        ],
        [
            Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ]
    ],
    parse_mode="html"
    )

async def replay(event):
    user = await event.get_sender()
    try:
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
    except Exception:
        mention = "ᴀɴᴏɴʏᴍᴏᴜs"
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
    if chat_id in queues and queues[chat_id]:
        status = await event.reply("**𝖱ᴇᴘʟᴀʏɪɴɢ ᴄᴜʀʀᴇɴᴛ 𝖳ʀᴀᴄᴋ...**")
        index = current_ind.get(chat_id, 0)
        stream_url, title, artist, duration, thumbnail, requested_by, query_format = queues[chat_id][index]
        try:
            if query_format == "video":
                await Play_Video(chat_id, stream_url)
            else:
                await Play_Audio(chat_id, stream_url)
            await playing_message(title, artist, duration, query_format, thumbnail, chat_id, requested_by)
            is_playing[chat_id] = True
            try:
                await status.edit(f"<b>➭ 𝖳ʀᴀᴄᴋ ʀᴇᴘʟᴀʏ 𝖲ᴛᴀʀᴛᴇᴅ!\n\n𝖱ᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {mention}", parse_mode="html")
            except Exception:
                await event.reply(f"<b>➭ 𝖳ʀᴀᴄᴋ ʀᴇᴘʟᴀʏ 𝖲ᴛᴀʀᴛᴇᴅ! \n\n𝖱ᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {mention}", parse_mode="html")
        except Exception as e:
            await status.edit(f"Replay failed: {str(e)}")
    else:
        await event.reply(f"» {BOT_MENTION} ɪsɴ'ᴛ 𝖲ᴛʀᴇᴀᴍɪɴɢ ᴏɴ 𝖵ᴏɪᴄᴇᴄʜᴀᴛ.", parse_mode="html")