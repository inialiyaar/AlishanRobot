from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command, callback_query
from AlishanBot.modules.helper_funcs.ytmetadata import meta_data
from AlishanBot.modules.helper_funcs.ytdownload import YTDownload
import os
from telethon import events
from AlishanBot.modules.helper_funcs.thumbnail import Thumbnail
from AlishanBot.__init__ import download_data
import asyncio
from AlishanBot import config
from telethon import Button

@add_command("youtube", "yt", "ytdownload")
async def YTDownload_handler(event, command_used, song_name):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    if chat_id in download_data:
        old_song_name, METADATA_MSG, url, title, artist, duration, thumbnail_path, is_downloading = download_data[chat_id]
        if is_downloading:
            return await event.respond("Already download in progress, please wait..")
        else:
            download_data.pop(chat_id, None)
            
    if not event.is_private:
        await event.reply("This command works only in private chat.")
        return

    if not song_name:
        await event.reply("Please provide a YouTube name or URL after `/download`.")
        return
    async with Alishan.action(chat_id, "photo"):
        status = await event.reply(f"🔎 Searching for **{song_name}** ...")
        data = await meta_data(song_name)
        if data == "URLERROR":
            return await status.edit("Provided URL is not a YouTube URL, please try a YouTube URL.")
        if data == "PLAYLISTERROR":    
            return await status.edit("Provided playlist is empty, please try other playlists.")
        url, title, artist, duration, thumbnail_url = data
        if duration >= 3600:
            hours, remainder = divmod(duration, 3600)
            minutes, secs = divmod(remainder, 60)
            display_duration = f"{hours}:{minutes:02}:{secs:02}"
        else:
            minutes, secs = divmod(duration, 60)
            display_duration = f"{minutes}:{secs:02}"
        await status.delete()
        thumbnail_path = await Thumbnail(thumbnail_url, title, artist, display_duration)
        METADATA_MSG = await Alishan.send_file(
            chat_id,
            file=thumbnail_path,
            caption=f"<blockquote><b>Title :</b>\n{title}</blockquote>\n\n<blockquote><b>Artist :</b> {artist}\n<b>Duration :</b> {display_duration}</blockquote>",
            buttons = [
                [
                    Button.inline("Video", data=b"ytvideo"),
                    Button.inline("Audio", data=b"ytaudio")
                ],
                [
                    Button.url("Updates", f"https://t.me/{config.SUPPORT_CHANNEL}")   
                ]
            ],
            parse_mode="html"
        )
    download_data[chat_id] = [song_name, METADATA_MSG, url, title, artist, display_duration, thumbnail_path, False]


@callback_query("ytaudio")
async def YTDownload_Audio(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    song_name, METADATA_MSG, url, title, artist, display_duration, thumbnail_path, is_downloading = download_data[chat_id]
    await METADATA_MSG.delete()
    async with Alishan.action(chat_id, "record-audio"):
        status = await event.respond("🎵 Downloading audio...")
        download_data[chat_id][-1] = True # is_downloading = True
        file_path = await asyncio.to_thread(YTDownload, song_name, "audio", title, artist)
        if file_path == "DURATIONERROR":
            download_data.pop(chat_id, None)
            return await status.edit("Duration is too long, please try under 2 hours.")
    async with Alishan.action(chat_id, "audio"):
        await status.edit("📤 Uploading audio...")
        await Alishan.send_file(
            chat_id,
            file=file_path,
            thumb=thumbnail_path,
            caption=f"<blockquote><b>Title :</b>\n{title}</blockquote>\n\n<blockquote><b>Artist :</b> {artist}\n<b>Duration :</b> {display_duration}</blockquote>",
            buttons = [
                [Button.url("Updates", f"https://t.me/{config.SUPPORT_CHANNEL}")]
                ],
            supports_streaming=True,
            parse_mode="html"
        )
    await status.delete()
    download_data.pop(chat_id, None)
    os.remove(file_path)
    os.remove(thumbnail_path)

@callback_query("ytvideo")
async def YTDownload_Video(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    song_name, METADATA_MSG, url, title, artist, display_duration, thumbnail_path, is_downloading = download_data[chat_id]
    await METADATA_MSG.delete()
    
    async with Alishan.action(chat_id, "record-video"):
        status = await event.respond("🎬 Downloading video...")
        download_data[chat_id][-1] = True # is_downloading = True
        file_path = await asyncio.to_thread(YTDownload, song_name, "video")
        if file_path == "DURATIONERROR":
            download_data.pop(chat_id, None)
            return await status.edit("Duration is too long, please try under 2 hours")
    async with Alishan.action(chat_id, "video"):
        await status.edit("📤 Uploading video...")
        await Alishan.send_file(
            chat_id,
            file=file_path,
            thumb=thumbnail_path, 
            caption=f"<blockquote><b>Title :</b>\n{title}</blockquote>\n\n<blockquote><b>Artist :</b> {artist}\n<b>Duration :</b> {display_duration}</blockquote>",
            buttons = [
                [Button.url("Updates", f"https://t.me/{config.SUPPORT_CHANNEL}")]
                ],
            supports_streaming=True,
            parse_mode="html"
        )
    
    await status.delete()
    download_data.pop(chat_id, None)
    os.remove(file_path)
    os.remove(thumbnail_path)
    