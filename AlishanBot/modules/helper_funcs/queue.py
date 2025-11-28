from AlishanBot.modules.helper_funcs.play import Play_Stream, join_call
from AlishanBot.core.bot import music, Alishan
from AlishanBot.modules.helper_funcs.ytmetadata import meta_data
from pytgcalls import filters
from pytgcalls.types import Update
from telethon import Button
import os
from asyncio import create_task, sleep, Lock
from AlishanBot.__init__ import player_stats, BOT_USERNAME, ASSISTANT_MENTION, BOT_MENTION, update_time
from AlishanBot.modules.helper_funcs.thumbnail import Thumbnail
from AlishanBot.modules.helper_funcs.metadata import get_meta
from AlishanBot import config
import asyncio
from collections import defaultdict
import re
from AlishanBot.modules.helper_funcs.ErrorLog import send_error
import traceback
from AlishanBot.utils.database import stream_mode
import time

queues = {}  
queue_position = {}  
current_ind = {}
queue_locks = defaultdict(asyncio.Lock)
progress_bar = {}


async def add_to_queue(song_name, chat_id, query_format, mention, download, force_play):
    async with queue_locks[chat_id]:
        queues.setdefault(chat_id, [])
        queue_position.setdefault(chat_id, 0)
        current_ind.setdefault(chat_id, 0)  
        settings = stream_mode.find_one({"chat_id": chat_id})
        if settings:
            play_mode = settings.get("play_mode", "normal")
        else:
            play_mode = "normal"
        status = await Alishan.send_message(chat_id, f"**sᴇᴀʀᴄʜɪɴɢ...🔎**")
        if download:
            stream_url = song_name
            title,  artist, duration = get_meta(song_name)
            thumbnail = "https://i.ibb.co/gLNS8hC1/x.jpg"
        if not download:
            data = await meta_data(song_name)
            if data == "URLERROR":
                return await Alishan.send_message(chat_id, "ᴘʀᴏᴠɪᴅᴇᴅ ᴜʀʟ ɪs ɴᴏᴛ ʏᴏᴜᴛᴜʙᴇ ᴜʀʟ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴏɴ ʏᴏᴜᴛᴜʙᴇ ᴜʀʟ. ")
            if data == "PLAYLISTERROR":    
                return await Alishan.send_message(chat_id, "ᴘʀᴏᴠɪᴅᴇᴅ ᴘʟᴀʏʟɪsᴛ ᴀʀᴇ ᴇᴍᴘᴛʏ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴏᴛʜᴇʀ ᴘʟᴀʏʟɪsᴛ.")
            stream_url, title, artist, duration, thumbnail = data
        
        if chat_id not in player_stats:
            await Play_Stream(chat_id, stream_url, query_format, play_mode)
            player_stats[chat_id] = {
               "is_playing": True,
               "duration": duration,
               "current_time": 0,
               "last_update": time.time(),
               "play_mode": play_mode
           }    
            create_task(playing_message(title, artist, duration, query_format, thumbnail, chat_id, mention, download))
            queues[chat_id].append((stream_url, title, artist, duration, thumbnail, mention, query_format, download)) 
            try:
                await status.delete()
            except Exception:
                pass
            return       
        if force_play:
            await Play_Stream(chat_id, stream_url, query_format, play_mode)
            player_stats[chat_id] = {
               "is_playing": True,
               "duration": duration,
               "current_time": 0,
               "last_update": time.time(),
               "play_mode": play_mode
           }    
            create_task(playing_message(title, artist, duration, query_format, thumbnail, chat_id, mention, download))
            queues[chat_id].append((stream_url, title, artist, duration, thumbnail, mention, query_format, download)) 
            try:
                await status.delete()
            except Exception:
                pass
            return       
        queues[chat_id].append((stream_url, title, artist, duration, thumbnail, mention, query_format, download)) 
        queue_position[chat_id] +=1
        create_task(queue_message(title, artist, duration, query_format, chat_id, queue_position[chat_id], mention))
        try:
            await status.delete()
        except Exception:
            pass

async def play_next(chat_id):
    if chat_id not in queues or not queues[chat_id]:
        player_stats.pop(chat_id, None)
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
        player_stats.pop(chat_id, None)
        return
    try:
        queue_position[chat_id] -=1
        
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        settings = stream_mode.find_one({"chat_id": chat_id})
        if settings:
            play_mode = settings.get("play_mode", "normal")
        else:
            play_mode = "normal"
        await Play_Stream(chat_id, stream_url, query_format, play_mode)
        player_stats[chat_id] = {
               "is_playing": True,
               "duration": duration,
               "current_time": 0,
               "last_update": time.time(),
               "play_mode": play_mode,
           }
        create_task(playing_message(title, artist, duration, query_format, thumbnail, chat_id, mention, download))
    except Exception as e:
        await Alishan.send_message(chat_id, f"Error: {str(e)}")

@music.on_update(filters.stream_end())
async def stream_end(_, update: Update):
    try:
        pass
    except:
        return   
    try:
        chat_id = update.chat_id
        chat_id = int(f"-100{chat_id}" if not str(chat_id).startswith("-100") else chat_id)
        if chat_id in queues:
            await play_next(chat_id)
    except:
        pass
        
async def playing_message(title, artist, duration, query_format, thumbnail, chat_id, mention, download):
    duration = int(duration)
    if duration >= 3600:
        hours, remainder = divmod(duration, 3600)
        minutes, secs = divmod(remainder, 60)
        duration_text = f"{hours}:{minutes:02}:{secs:02}"
    else:
        minutes, secs = divmod(duration, 60)
        duration_text = f"{minutes}:{secs:02}"
    if not download:
        thumbnail_path = await Thumbnail(thumbnail, title, artist, duration_text)
    else:
        thumbnail_path = thumbnail  
    if query_format == "video":
        query_format = "𝖵ɪᴅᴇᴏ"
    else:
        query_format = "𝖠ᴜᴅɪᴏ"

    msg = await Alishan.send_file(
        chat_id,
        file=thumbnail_path,
        caption=f"<blockquote>‣ 𝖳ɪᴛʟᴇ:\n{title}</blockquote>\n"
                f"<blockquote><b>‣ 𝖠ʀᴛɪsᴛ:<b> {artist}\n"
                f"<b>‣ 𝖣ᴜʀᴀᴛɪᴏɴ:<b> {duration_text}\n"
                f"<b>‣ 𝖲ᴛʀᴇᴀᴍ 𝖳ʏᴘᴇ :</b> {query_format}\n"
                f"<b>𝖱ᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {mention}</blockquote>\n",
        buttons=[
            [
                Button.inline("▷", data=b"resume"),
                Button.inline("II", data=b"pause"),
                Button.inline("♫", data=b"modes"), 
                Button.inline("‣‣I", data=b"skip"),
                Button.inline("▢", data=b"stop"),
            ],
            [
                Button.inline("≪ -20s", data=b"seek_backward"), 
                Button.inline("↻", data=b"replay"),
                Button.inline("+20s ≫", data=b"seek_forward")
            ], 
            [
                Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ]
        ],
        parse_mode="html"
    )

    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
    progress_bar[chat_id] = msg
    create_task(update_bar())
    
async def update_bar():
    while True:
        await asyncio.sleep(10)

        for chat_id, msg in list(progress_bar.items()):
            if chat_id not in player_stats:
                progress_bar.pop(chat_id, None)
                continue

            stats = player_stats[chat_id]

            duration = stats["duration"]
            current = stats["current_time"]
            last_up = stats["last_update"]
            is_playing = stats["is_playing"]
            if duration is None or duration == 0:
                continue
            if is_playing:
                elapsed = time.time() - last_up
                current += elapsed
                if current > duration:
                    current = duration
                stats["current_time"] = current
                stats["last_update"] = time.time()

            TOTAL = 10
            filled = int((current / duration) * TOTAL)
            if filled < 0: filled = 0
            if filled > TOTAL: filled = TOTAL
            
            empty = TOTAL - filled
            bar = "─" * filled + "ꕥ" + "─" * empty

            def fmt(sec):
                sec = int(sec)
                m, s = divmod(sec, 60)
                return f"{m:02}:{s:02}"
            text = f"{fmt(current)} {bar} {fmt(duration)}"
            buttons=[
                [Button.inline(f"{text}", data=b"progress_bar")], 
                [
                    Button.inline("▷", data=b"resume"),
                    Button.inline("II", data=b"pause"),
                    Button.inline("♫", data=b"modes"), 
                    Button.inline("‣‣I", data=b"skip"),
                    Button.inline("▢", data=b"stop"),
                ],
                [
                    Button.inline("≪ -20s", data=b"seek_backward"), 
                    Button.inline("↻", data=b"replay"),
                    Button.inline("+20s ≫", data=b"seek_forward")
                ], 
                [
                    Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ]
            ]
            try:
                await msg.edit(buttons=buttons)
            except:
                pass
    
    
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
        f"<b>➲ 𝖠ᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ ᴀᴛ #{queue_pos}</b>\n\n<blockquote><b>‣ 𝖳ɪᴛʟᴇ :</b> {title}</blockquote>\n<blockquote><b>‣ 𝖠ʀᴛɪsᴛ :</b> {artist}\n<b>‣ 𝖣ᴜʀᴀᴛɪᴏɴ :</b> {duration_text}\n<b>‣ 𝖲ᴛʀᴇᴀᴍ 𝖳ʏᴘᴇ :</b> {query_format}\n<b>𝖱ᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {mention}</blockquote>",
        buttons = [
        [
            Button.inline("‣‣I", data=b"skip"),
            Button.inline("▢", data=b"stop")
        ],
        [
            Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ]
    ],
    parse_mode="html"
    )