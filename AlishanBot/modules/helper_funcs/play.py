from AlishanBot.core.bot import music
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality, Device, ExternalMedia
from pytgcalls.types.raw import AudioParameters
from asyncio import sleep

async def Play_Audio(chat_id, url):
    try:
        await music.unmute(chat_id)
    except:
        pass    
    await music.play(
        chat_id,
        MediaStream(
            url,
            video_flags=MediaStream.Flags.IGNORE,
            audio_parameters=AudioQuality.STUDIO, 
            )
        )
        
async def Play_Video(chat_id, url):
    try:
        await music.unmute(chat_id)
    except:
        pass    
    await music.play(
        chat_id, 
        MediaStream(
            url, 
            video_parameters=VideoQuality.UHD_4K, 
        )
    )
        
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
    try:
        await music.mute(chat_id)
    except:
        pass     
    await sleep(2)