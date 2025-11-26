from AlishanBot.core.bot import music
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality, Device, ExternalMedia
from pytgcalls.types.raw import AudioParameters
from asyncio import sleep

async def _play_base(chat_id, url, is_video=False, eco=False, seek_offset=None):
    current_ms = await music.time(chat_id) or 0
    current_sec = int(current_ms / 1000)

    if seek_offset:
        new_sec = current_sec + seek_offset
        if new_sec < 0:
            new_sec = 0 
    else:
        new_sec = current_sec

    if eco:
        ff = (
            "-atmid "
            f"-ss {new_sec} "
            "-af asetrate=44100*0.92,aresample=44100,atempo=1.0,"
            "lowpass=f=3800,highpass=f=120,aecho=0.6:0.7:50:0.3,volume=1.15"
            " -atend"
        )
    else:
        ff = f"-ss {new_sec}" if seek_offset else None

    aud = AudioQuality.STUDIO
    vid = VideoQuality.UHD_4K
    if is_video:
        await music.play(
            chat_id,
            MediaStream(
                url,
                audio_parameters=aud,
                video_parameters=vid,
                ffmpeg_parameters=ff,
            )
        )
    else:
        await music.play(
            chat_id,
            MediaStream(
                url,
                audio_parameters=aud,
                video_flags=MediaStream.Flags.IGNORE, 
                ffmpeg_parameters=ff,
            )
        )

async def Play_Audio(chat_id, url, eco=False, seek=False, to_seek=None):
    offset = to_seek if to_seek else (20 if seek else None)
    await _play_base(chat_id, url, is_video=False, eco=eco, seek_offset=offset)
    
async def Play_Video(chat_id, url, eco=False, seek=False, to_seek=None):
    offset = to_seek if to_seek else (20 if seek else None)
    await _play_base(chat_id, url, is_video=True, eco=eco, seek_offset=offset)    
        
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