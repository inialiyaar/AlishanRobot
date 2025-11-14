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



@add_command("download")
async def Download(event, command_used, song_name):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    if chat_id in download_data:
        song_name, METADATA_MSG, url, title, artist, duration, thumbnail_path, is_downloading = download_data[chat_id]
        if is_downloading:
            return await event.respond("ᴀʟʀᴇᴀᴅʏ ᴅᴏᴡɴʟᴏᴀᴅ ɪɴ ᴘʀᴏɢʀᴇss, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ.. ")
        else:
            download_data.pop(chat_id, None)
            
    if not event.is_private:
        await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴʟʏ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ.")
        return

    if not song_name:
        await event.reply("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ʏᴏᴜᴛᴜʙᴇ ɴᴀᴍᴇ ᴏʀ ᴜʀʟ ᴀғᴛᴇʀ `/download`.")
        return
    async with Alishan.action(chat_id, "photo"):
        status = await event.reply(f"🔎 sᴇᴀʀᴄʜɪɴɢ ғᴏʀ **{song_name}** ...")
        data = await meta_data(song_name)
        url, title, artist, duration, thumbnail_url = data
        if duration >= 3600:
            hours, remainder = divmod(duration, 3600)
            minutes, secs = divmod(remainder, 60)
            duration_text = f"{hours}:{minutes:02}:{secs:02}"
        else:
            minutes, secs = divmod(duration, 60)
            display_duration = f"{minutes}:{secs:02}"
        await status.delete()
        thumbnail_path = await Thumbnail(thumbnail_url, title, artist, display_duration)
        METADATA_MSG = await Alishan.send_file(
            chat_id,
            file=thumbnail_path,
            caption=f"<pre><b>𝖳ɪᴛʟᴇ :</b>\n{title}</pre>\n\n<pre><b>𝖠ʀᴛɪsᴛ :</b> {artist}\n<b>𝖣ᴜʀᴀᴛɪᴏɴ :</b> {display_duration}</pre>",
            buttons = [
                [
                    Button.inline("𝖵ɪᴅᴇᴏ", data=b"video"),
                    Button.inline("𝖠ᴜᴅɪᴏ", data=b"audio")
                ],
                [
                    Button.url("𝖴ᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}")   
                ]
            ],
            parse_mode="html"
        )
    download_data[chat_id] = [song_name, METADATA_MSG, url, title, artist, display_duration, thumbnail_path, False]


@callback_query("audio")
async def Download_Audio(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    song_name, METADATA_MSG, url, title, artist, display_duration, thumbnail_path, is_downloading = download_data[chat_id]
    await METADATA_MSG.delete()
    async with Alishan.action(chat_id, "record-video"):
        status = await event.respond("🎵 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ...")
        is_downloading = True
        file_path = await asyncio.to_thread(YTDownload, song_name, "audio", title, artist)
        if file_path == "ERROR":
            return await status.edit("ᴅᴜʀᴀᴛɪᴏɴ ɪs ᴛᴏᴏ ʟᴏɴɢ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴜɴᴅᴇʀ 2 ʜᴏᴜʀ's")
    async with Alishan.action(chat_id, "video"):
        await status.edit("📤 ᴜᴘʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ...")
        await Alishan.send_file(
            chat_id,
            file=file_path,
            thumb=thumbnail_path,
            caption=f"<pre><b>𝖳ɪᴛʟᴇ :</b>\n{title}</pre>\n\n<pre><b>𝖠ʀᴛɪsᴛ :</b> {artist}\n<b>𝖣ᴜʀᴀᴛɪᴏɴ :</b> {display_duration}</pre>",
            buttons = [
                [Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}")]
                ],
            supports_streaming=True,
            parse_mode="html"
        )
    await status.delete()
    download_data.pop(chat_id, None)
    os.remove(file_path)
    os.remove(thumbnail_path)

@callback_query("video")
async def Download_Video(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    song_name, METADATA_MSG, url, title, artist, display_duration, thumbnail_path, is_downloading = download_data[chat_id]
    await METADATA_MSG.delete()
    
    async with Alishan.action(chat_id, "record-video"):
        status = await event.respond("🎬 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...")
        is_downloading = True
        file_path = await asyncio.to_thread(YTDownload, song_name, "video")
        if file_path == "ERROR":
            return await status.edit("ᴅᴜʀᴀᴛɪᴏɴ ɪs ᴛᴏᴏ ʟᴏɴɢ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴜɴᴅᴇʀ 2 ʜᴏᴜʀs")
    async with Alishan.action(chat_id, "video"):
        await status.edit("📤 ᴜᴘʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...")
        await Alishan.send_file(
            chat_id,
            file=file_path,
            thumb=thumbnail_path, 
            caption=f"<pre><b>𝖳ɪᴛʟᴇ :</b>\n{title}</pre>\n\n<pre><b>𝖠ʀᴛɪsᴛ :</b> {artist}\n<b>𝖣ᴜʀᴀᴛɪᴏɴ :</b> {display_duration}</pre>",
            buttons = [
                [Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}")]
                ],
            supports_streaming=True,
            parse_mode="html"
        )
    
    await status.delete()
    download_data.pop(chat_id, None)
    os.remove(file_path)
    os.remove(thumbnail_path)