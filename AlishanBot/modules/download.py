from AlishanBot.core.bot import Alishan
from AlishanBot.core.decorators import add_command, callback_query
from AlishanBot.modules.helper_funcs.ytmetadata import meta_data
from AlishanBot.modules.helper_funcs.ytdownload import YTDownload
from AlishanBot.modules.helper_funcs.igdownload import IGDownload, IGMeta
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
        if data == "URLERROR":
            return await status.edit("ᴘʀᴏᴠɪᴅᴇᴅ ᴜʀʟ ɪs ɴᴏᴛ ʏᴏᴜᴛᴜʙᴇ ᴜʀʟ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴏɴ ʏᴏᴜᴛᴜʙᴇ ᴜʀʟ. ")
        if data == "PLAYLISTERROR":    
            return await status.edit("ᴘʀᴏᴠɪᴅᴇᴅ ᴘʟᴀʏʟɪsᴛ ᴀʀᴇ ᴇᴍᴘᴛʏ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴏᴛʜᴇʀ ᴘʟᴀʏʟɪsᴛ.")
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
            caption=f"<blockquote><b>𝖳ɪᴛʟᴇ :</b>\n{title}</blockquote>\n\n<blockquote><b>𝖠ʀᴛɪsᴛ :</b> {artist}\n<b>𝖣ᴜʀᴀᴛɪᴏɴ :</b> {display_duration}</blockquote>",
            buttons = [
                [
                    Button.inline("𝖵ɪᴅᴇᴏ", data=b"ytvideo"),
                    Button.inline("𝖠ᴜᴅɪᴏ", data=b"ytaudio")
                ],
                [
                    Button.url("𝖴ᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}")   
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
        status = await event.respond("🎵 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ...")
        is_downloading = True
        file_path = await asyncio.to_thread(YTDownload, song_name, "audio", title, artist)
        if file_path == "DURATIONERROR":
            return await status.edit("ᴅᴜʀᴀᴛɪᴏɴ ɪs ᴛᴏᴏ ʟᴏɴɢ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴜɴᴅᴇʀ 2 ʜᴏᴜʀ's")
    async with Alishan.action(chat_id, "audio"):
        await status.edit("📤 ᴜᴘʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ...")
        await Alishan.send_file(
            chat_id,
            file=file_path,
            thumb=thumbnail_path,
            caption=f"<blockquote><b>𝖳ɪᴛʟᴇ :</b>\n{title}</blockquote>\n\n<blockquote><b>𝖠ʀᴛɪsᴛ :</b> {artist}\n<b>𝖣ᴜʀᴀᴛɪᴏɴ :</b> {display_duration}</blockquote>",
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

@callback_query("ytvideo")
async def YTDownload_Video(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    song_name, METADATA_MSG, url, title, artist, display_duration, thumbnail_path, is_downloading = download_data[chat_id]
    await METADATA_MSG.delete()
    
    async with Alishan.action(chat_id, "record-video"):
        status = await event.respond("🎬 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...")
        is_downloading = True
        file_path = await asyncio.to_thread(YTDownload, song_name, "video")
        if file_path == "DURATIONERROR":
            return await status.edit("ᴅᴜʀᴀᴛɪᴏɴ ɪs ᴛᴏᴏ ʟᴏɴɢ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴜɴᴅᴇʀ 2 ʜᴏᴜʀs")
    async with Alishan.action(chat_id, "video"):
        await status.edit("📤 ᴜᴘʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...")
        await Alishan.send_file(
            chat_id,
            file=file_path,
            thumb=thumbnail_path, 
            caption=f"<blockquote><b>𝖳ɪᴛʟᴇ :</b>\n{title}</blockquote>\n\n<blockquote><b>𝖠ʀᴛɪsᴛ :</b> {artist}\n<b>𝖣ᴜʀᴀᴛɪᴏɴ :</b> {display_duration}</blockquote>",
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
    
@add_command("insta", "instagram", "ig")
async def IG_handler(event, command_used, url):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)
    if chat_id in download_data:
        old_url, METADATA_MSG, post_url, title, author, duration, thumbnail_path, is_downloading = download_data[chat_id]
        if is_downloading:
            return await event.respond("ᴀʟʀᴇᴀᴅʏ ᴅᴏᴡɴʟᴏᴀᴅ ɪɴ ᴘʀᴏɢʀᴇss, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ.. ")
        else:
            download_data.pop(chat_id, None)

    if not event.is_private:
        return await event.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴʟʏ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ.")

    if not url:
        return await event.reply("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ɪɴsᴛᴀɢʀᴀᴍ ᴘᴏsᴛ ᴜʀʟ ᴀғᴛᴇʀ `/instagram`.")

    async with Alishan.action(chat_id, "photo"):
        status = await event.reply("🔎 sᴇᴀʀᴄʜɪɴɢ ᴘᴏsᴛ...")

        data = IGMeta(url)

        if data == "URLERROR":
            return await status.edit("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɪɴsᴛᴀɢʀᴀᴍ ᴜʀʟ")
        if data == "PRIVATEERROR":
            return await status.edit("ᴀᴄᴄᴏᴜɴᴛ ᴏʀ ᴘᴏsᴛ ɪs ᴘʀɪᴠᴀᴛᴇ. ᴄᴀɴ'ᴛ ᴀᴄᴄᴇss.")
        if isinstance(data, str) and data.startswith("ERROR"):
            return await status.edit(f"ᴇʀʀᴏʀ ғᴇᴛᴄʜɪɴɢ ᴍᴇᴛᴀᴅᴀᴛᴀ:\n{data}")

        post_url, title, author, duration, thumbnail = data

        if duration >= 1:
            minutes, seconds = divmod(int(duration), 60)
            display_duration = f"{minutes}:{seconds:02}"
        else:
            display_duration = "0:00"

        await status.delete()

        thumbnail_path = await Thumbnail(thumbnail, title, author, display_duration)

        METADATA_MSG = await Alishan.send_file(
            chat_id,
            file=thumbnail_path,
            caption=f"<blockquote><b>𝖳ɪᴛʟᴇ :</b>\n{title}</blockquote>\n\n"
                    f"<blockquote><b>𝖠ᴜᴛʜᴏʀ :</b> {author}\n"
                    f"<b>𝖣ᴜʀᴀᴛɪᴏɴ :</b> {display_duration}</blockquote>",
            buttons=[
                [Button.inline("📥 𝖣ᴏᴡɴʟᴏᴀᴅ", data=b"igdownload")],
                [Button.url("𝖴ᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}")]
            ],
            parse_mode="html"
        )

    download_data[chat_id] = [url, METADATA_MSG, post_url, title, author, display_duration, thumbnail_path, False]


@callback_query("igdownload")
async def IG_Download_Handler(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{abs(chat.id)}") if not str(chat.id).startswith("-100") else int(chat.id)

    url, METADATA_MSG, post_url, title, author, display_duration, thumbnail_path, is_downloading = download_data[chat_id]

    await METADATA_MSG.delete()

    async with Alishan.action(chat_id, "record-video"):
        status = await event.respond("📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴘᴏsᴛ...")
        is_downloading = True

        file_path = await asyncio.to_thread(IGDownload, url)

        if file_path == "PRIVATEERROR":
            return await status.edit("ᴘʀɪᴠᴀᴛᴇ ᴘᴏsᴛ ᴅᴏᴡɴʟᴏᴀᴅ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ.")

        if isinstance(file_path, str) and file_path.startswith("ERROR"):
            return await status.edit(f"ᴇʀʀᴏʀ:\n{file_path}")

    async with Alishan.action(chat_id, "video"):
        await status.edit("📤 ᴜᴘʟᴏᴀᴅɪɴɢ...")
        await Alishan.send_file(
            chat_id,
            file=file_path,
            thumb=thumbnail_path,
            caption=f"<blockquote><b>𝖳ɪᴛʟᴇ :</b>\n{title}</blockquote>\n\n"
                    f"<blockquote><b>𝖠ᴜᴛʜᴏʀ :</b> {author}\n"
                    f"<b>𝖣ᴜʀᴀᴛɪᴏɴ :</b> {display_duration}</blockquote>",
            buttons=[[Button.url("ᴜᴘᴅᴀᴛᴇs", f"https://t.me/{config.SUPPORT_CHANNEL}")]],
            parse_mode="html",
            supports_streaming=True
        )

    await status.delete()
    download_data.pop(chat_id, None)

    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)    