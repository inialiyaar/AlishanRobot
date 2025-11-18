from AlishanBot.modules.helper_funcs.play import Play_Audio, Play_Video, join_call
from AlishanBot.core.bot import music, Alishan
from AlishanBot.modules.helper_funcs.ytmetadata import meta_data
from pytgcalls import filters
from pytgcalls.types import Update
from telethon import Button
import os
from asyncio import create_task, sleep, Lock
from AlishanBot.__init__ import is_playing
from AlishanBot.modules.helper_funcs.thumbnail import Thumbnail
from AlishanBot.modules.helper_funcs.metadata import get_meta
from AlishanBot.__init__ import BOT_USERNAME, ASSISTANT_MENTION, BOT_MENTION
from AlishanBot import config
import asyncio
from collections import defaultdict
import re
from AlishanBot.modules.helper_funcs.ErrorLog import send_error
import traceback

queues = {}  
queue_position = {}  
current_ind = {}
active_bars = {}
queue_locks = defaultdict(asyncio.Lock)

async def add_to_queue(song_name, chat_id, query_format, mention, download, force_play):
    async with queue_locks[chat_id]:
        status = await Alishan.send_message(chat_id, f"**sᴇᴀʀᴄʜɪɴɢ...🔎**")
        if not download:
            data = await meta_data(song_name)
            if data == "URLERROR":
                return await event.reply("ᴘʀᴏᴠɪᴅᴇᴅ ᴜʀʟ ɪs ɴᴏᴛ ʏᴏᴜᴛᴜʙᴇ ᴜʀʟ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴏɴ ʏᴏᴜᴛᴜʙᴇ ᴜʀʟ. ")
            if data == "PLAYLISTERROR":    
                return await event.reply("ᴘʀᴏᴠɪᴅᴇᴅ ᴘʟᴀʏʟɪsᴛ ᴀʀᴇ ᴇᴍᴘᴛʏ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴏᴛʜᴇʀ ᴘʟᴀʏʟɪsᴛ.")
        queues.setdefault(chat_id, [])
        queue_position.setdefault(chat_id, 0)
        current_ind.setdefault(chat_id, 0)
        
        if download:
            stream_url = song_name
            title,  artist, duration = get_meta(song_name)
            thumbnail = "https://i.ibb.co/gLNS8hC1/x.jpg"
        try:
            if force_play:
                is_playing[chat_id] = True
                await join_call(chat_id)
                if not download:
                    stream_url, title, artist, duration, thumbnail = data
                if query_format == "video":
                    await Play_Video(
                        chat_id, 
                        stream_url
                    )
                if query_format == "audio":
                    await Play_Audio(
                        chat_id,
                        stream_url
                        )
                create_task(playing_message(title, artist, duration, query_format, thumbnail, chat_id, mention, download))
                try:
                    await status.delete()
                except Exception:
                    pass    
                return    
                
            if not chat_id in is_playing:
                is_playing[chat_id] = True
                await join_call(chat_id)
                if not download:
                    stream_url, title, artist, duration, thumbnail = data
                if query_format == "video":
                    await Play_Video(
                        chat_id, 
                        stream_url
                    )
                if query_format == "audio":
                    await Play_Audio(
                        chat_id,
                        stream_url
                        )
                queues[chat_id].append((stream_url, title, artist, duration, thumbnail, mention, query_format, download)) 
                create_task(playing_message(title, artist, duration, query_format, thumbnail, chat_id, mention, download))
            else:
                if download:
                    stream_url = song_name
                    title,  artist, duration = get_meta(song_name)
                    thumbnail = "https://i.ibb.co/gLNS8hC1/x.jpg"
                else:
                    stream_url, title, artist, duration, thumbnail = data
                queues[chat_id].append((stream_url, title, artist, duration, thumbnail, mention, query_format, download)) 
                queue_position[chat_id] +=1
                create_task(queue_message(title, artist, duration, query_format, chat_id, queue_position[chat_id], mention))
            try:
                await status.delete()
            except Exception:
                pass    
        except Exception:
            error = traceback.format_exc()
            await send_error(error)

async def play_next(chat_id):
    try:
        await music.mute(chat_id)
    except:
        pass      
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
        queue_position[chat_id] -=1
        
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        if query_format == "video":
            await Play_Video(chat_id, stream_url)
        else:
            await Play_Audio(chat_id, stream_url)
            
        if chat_id in active_bars:
            active_bars[chat_id]["active"] = False  
        create_task(playing_message(title, artist, duration, query_format, thumbnail, chat_id, mention, download))
        is_playing[chat_id] = True
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
    if chat_id in active_bars:
        active_bars[chat_id]["active"] = False
    bar_state = {"active": True}
    active_bars[chat_id] = bar_state
    asyncio.create_task(update_duration_bar(msg, duration, chat_id, bar_state))


async def update_duration_bar(msg, duration, chat_id=None, bar_state=None):
    elapsed = 0
    total_blocks = 9
    
    while elapsed <= duration:
        if chat_id not in is_playing or not bar_state.get("active", False):
            break
    
        if not is_playing.get(chat_id, False):
            await asyncio.sleep(2)
            continue
    
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
        f"<b>➲ 𝖠ᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ ᴀᴛ #{queue_pos}</b>\n\n<blockquote><b>‣ 𝖳ɪᴛʟᴇ :</b> {title}</blockquote>\n<blockquote><b>‣ 𝖠ʀᴛɪsᴛ :</b> {artist}\n<b>‣ 𝖣ᴜʀᴀᴛɪᴏɴ :</b> {duration_text}\n<b>‣ 𝖲ᴛʀᴇᴀᴍ 𝖳ʏᴘᴇ :</b> {query_format}\n<b>𝖱ᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {mention}</blockquote>",
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
    
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    if chat_id in queues and queues[chat_id]:
        try:
            await music.mute(chat_id)
        except:
            pass     
        status = await event.reply("**𝖱ᴇᴘʟᴀʏɪɴɢ ᴄᴜʀʀᴇɴᴛ 𝖳ʀᴀᴄᴋ...**")
        index = current_ind.get(chat_id, 0)
        stream_url, title, artist, duration, thumbnail, mention, query_format, download = queues[chat_id][index]
        try:
            if query_format == "video":
                await Play_Video(chat_id, stream_url)
            else:
                await Play_Audio(chat_id, stream_url)
            if chat_id in active_bars:
                active_bars[chat_id]["active"] = False    
            create_task(playing_message(title, artist, duration, query_format, thumbnail, chat_id, mention, download)) 
            is_playing[chat_id] = True
            try:
                await status.edit(f"<b>➭ 𝖳ʀᴀᴄᴋ ʀᴇᴘʟᴀʏ 𝖲ᴛᴀʀᴛᴇᴅ!\n\n𝖱ᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {mention}", parse_mode="html")
            except Exception:
                await event.reply(f"<b>➭ 𝖳ʀᴀᴄᴋ ʀᴇᴘʟᴀʏ 𝖲ᴛᴀʀᴛᴇᴅ! \n\n𝖱ᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {mention}", parse_mode="html")
        except Exception as e:
            await status.edit(f"Replay failed: {str(e)}")
    else:
        await event.reply(f"» {BOT_MENTION} ɪsɴ'ᴛ 𝖲ᴛʀᴇᴀᴍɪɴɢ ᴏɴ 𝖵ᴏɪᴄᴇᴄʜᴀᴛ.", parse_mode="html")
        
__all__ = ["queues", "queue_position", "current_ind", "queue_locks"]        