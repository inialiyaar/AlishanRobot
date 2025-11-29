from AlishanBot.core.bot import music
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality, ExternalMedia
from asyncio import sleep
from pytgcalls.types.raw import AudioParameters


async def Play_Stream(chat_id, url, stream_format, Play_Mode, seek=None):
    aud = AudioQuality.STUDIO
    vid = VideoQuality.UHD_4K
    if Play_Mode == "lofi":
        if seek:
            ff =(
                "-atmid "
                f"-ss {seek} "
                "-af asetrate=44100*0.92,aresample=44100,atempo=1.0,"
                "lowpass=f=3800,highpass=f=120,aecho=0.6:0.7:50:0.3,volume=1.15"
                " -atend"
            )
        else:   
            ff =(
                "-atmid "
                "-af asetrate=44100*0.92,aresample=44100,atempo=1.0,"
                "lowpass=f=3800,highpass=f=120,aecho=0.6:0.7:50:0.3,volume=1.15"
                " -atend"
            ) 
    elif Play_Mode == "eco":
        if seek:
            ff = (
                "-atmid "
                f"-ss {seek} "
                "-af aecho=0.7:0.65:60:0.22,volume=1.10"
                " -atend"
            )
        else:
            ff = (
                "-atmid "
                "-af aecho=0.7:0.65:60:0.22,volume=1.10"
                " -atend"
            )
    elif seek:
        ff = f"-ss {seek}"
    else:
        ff = None    
    if stream_format == "audio":
        await music.play(
            chat_id,
            MediaStream(
                url,
                audio_parameters=aud,
                video_flags=MediaStream.Flags.IGNORE, 
                ffmpeg_parameters=ff,
            )
        )
    else:
        await music.play(
            chat_id,
            MediaStream(
                url,
                audio_parameters=aud,
                video_parameters=vid,
                ffmpeg_parameters=ff,
            )
        )
    
def join_call(chat_id):
    music.play(
        chat_id,
        MediaStream(
            ExternalMedia.AUDIO,
            AudioParameters(
                bitrate=48000,
                channels=2
            )
        )
    )
    sleep(2)