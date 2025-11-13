from AlishanBot.core.bot import music
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality


async def Play_Audio(chat_id, url):
    try:
        await music.play(
            chat_id,
            MediaStream(
                url,
                video_flags=MediaStream.Flags.IGNORE,
                audio_parameters=AudioQuality.STUDIO, 
                )
            )
    except Exception as e:
        print(str(e))
        
async def Play_Video(chat_id, url):
    try:
        await music.play(
            chat_id, 
            url
        )
    except Exception as e:
        print(str(e)) 