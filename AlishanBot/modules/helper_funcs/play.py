from AlishanBot.core.bot import music
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality


async def Play_Audio(chat_id, url):
    await music.play(
        chat_id,
        MediaStream(
            url,
            video_flags=MediaStream.Flags.IGNORE,
            audio_parameters=AudioQuality.STUDIO, 
            )
        )
        
async def Play_Video(chat_id, url):
    await music.play(
        chat_id, 
        MediaStream(
            url, 
            video_parameters=VideoQuality.UHD_4K, 
        )
    )