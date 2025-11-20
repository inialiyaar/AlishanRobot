from AlishanBot.core.bot import music
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality, Device, ExternalMedia
from pytgcalls.types.raw import AudioParameters
from asyncio import sleep


async def Play_Audio(chat_id, url, eco=False, seek=False, to_seek=None):
    if to_seek:
          play_sec = await music.time(chat_id)
          if to_seek > 0:
            play_sec += to_seek
          else:
              play_sec = max(0, play_sec, to_seek)
          if eco:
              await music.play(
                    chat_id,
                    MediaStream(
                        url,
                        video_flags=MediaStream.Flags.IGNORE,
                        audio_parameters=AudioQuality.STUDIO, 
                                ffmpeg_parameters=(
                            "-atmid "
                            f"-ss {play_sec} "
                            "-af asetrate=44100*0.92,aresample=44100,atempo=1.0,lowpass=f=3800,highpass=f=120,aecho=0.6:0.7:50:0.3,volume=1.15"
                            " -atend"
                            ),
                        )
                    )    
              return        
          else: 
              await music.play(
                  chat_id,
                  MediaStream(
                      url,
                      video_flags=MediaStream.Flags.IGNORE,
                      audio_parameters=AudioQuality.STUDIO, 
                      ffmpeg_parameters=f"-ss {play_sec}"
                      )
                  )
              return
    if seek:
        play_time = await music.time(chat_id)
        play_sec = max(1, int(play_time / 1000))
        await music.play(
          chat_id,
          MediaStream(
              url,
              video_flags=MediaStream.Flags.IGNORE,
              audio_parameters=AudioQuality.STUDIO, 
              ffmpeg_parameters=f"-ss {play_sec}"
              )
          )
    if not eco: 
        await music.play(
            chat_id,
            MediaStream(
                url,
                video_flags=MediaStream.Flags.IGNORE,
                audio_parameters=AudioQuality.STUDIO, 
                )
            )
    else:
        play_time = await music.time(chat_id)
        play_sec = max(1, int(play_time / 1000))
        await music.play(
            chat_id,
            MediaStream(
                url,
                video_flags=MediaStream.Flags.IGNORE,
                audio_parameters=AudioQuality.STUDIO, 
                ffmpeg_parameters=(
                    "-atmid "
                    f"-ss {play_sec} "
                    "-af asetrate=44100*0.92,aresample=44100,atempo=1.0,lowpass=f=3800,highpass=f=120,aecho=0.6:0.7:50:0.3,volume=1.15"
                    " -atend"
                    ),
                )
            )
        
async def Play_Video(chat_id, url, eco=False, seek=False, to_seek=None):
    if to_seek:
          play_sec = await music.time(chat_id)
          if to_seek > 0:
            play_sec += to_seek
          else:
              play_sec = max(0, play_sec, to_seek)
          if eco:
              await music.play(
                    chat_id,
                    MediaStream(
                        url,
                        audio_parameters=AudioQuality.STUDIO, 
                        video_parameters=VideoQuality.UHD_4K, 
                                ffmpeg_parameters=(
                            "-atmid "
                            f"-ss {play_sec} "
                            "-af asetrate=44100*0.92,aresample=44100,atempo=1.0,lowpass=f=3800,highpass=f=120,aecho=0.6:0.7:50:0.3,volume=1.15"
                            " -atend"
                            ),
                        )
                    )    
              return
          else:   
              await music.play(
                  chat_id,
                  MediaStream(
                      url,
                      audio_parameters=AudioQuality.STUDIO, 
                      video_parameters=VideoQuality.UHD_4K, 
                      ffmpeg_parameters=f"-ss {play_sec}"
                      )
                  )
              return
    if seek:
        play_time = await music.time(chat_id)
        play_sec = max(1, int(play_time / 1000))
        await music.play(
          chat_id,
          MediaStream(
              url,
              audio_parameters=AudioQuality.STUDIO, 
              video_parameters=VideoQuality.UHD_4K, 
              ffmpeg_parameters=f"-ss {play_sec}"
              )
          )
    if not eco: 
        await music.play(
            chat_id,
            MediaStream(
                url,
                audio_parameters=AudioQuality.STUDIO, 
                video_parameters=VideoQuality.UHD_4K, 
                )
            )
    else:
        play_time = await music.time(chat_id)
        play_sec = max(1, int(play_time / 1000))
        await music.play(
            chat_id,
            MediaStream(
                url,
                audio_parameters=AudioQuality.STUDIO,
                video_parameters=VideoQuality.UHD_4K,  
                ffmpeg_parameters=(
                    "-atmid "
                    f"-ss {play_sec} "
                    "-af asetrate=44100*0.92,aresample=44100,atempo=1.0,lowpass=f=3800,highpass=f=120,aecho=0.6:0.7:50:0.3,volume=1.15"
                    " -atend"
                    ),
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
    await sleep(2)