from AlishanBot.core.bot import music
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality, Device, ExternalMedia
from pytgcalls.types.raw import AudioParameters
from asyncio import sleep

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
        
async def join_call(chat_id):
    await music.play(
        chat_id,
        MediaStream(
            ExternalMedia.AUDIO,
            AudioParameters(
                bitrate=48000,
                channels=2
            )
        )
    )
    await sleep(2)