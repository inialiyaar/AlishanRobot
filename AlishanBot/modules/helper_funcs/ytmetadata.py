from yt_dlp import YoutubeDL
import time

cookie = "cookies/cookies.txt"
CACHE = {}
CACHE_EXPIRY = 3600

async def is_youtube_url(text):
    return text.startswith("http://") or text.startswith("https://")

async def meta_data(song_name):
    title = "Unknown Title"
    artist = "Unknown Artist"
    raw_duration = 0
    display_duration = "0:00"
    now = time.time()
    if song_name in CACHE:
        cache_entry = CACHE[song_name]
        if now - cache_entry["timestamp"] < CACHE_EXPIRY:
            return cache_entry["data"]    
        else:
            del CACHE[song_name]    
    ydl_opts = {
            "format": "best",
            "quiet": True,
            "no_warnings": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "noplaylist": True,
            "cookiefile": cookie,
            "skip_download": True,
        }
    
    with YoutubeDL(ydl_opts) as ydl:
        query = song_name if await is_youtube_url(song_name) else f"ytsearch1:{song_name}"
        result = ydl.extract_info(query, download=False)
    
        if "entries" in result:
            info = result["entries"][0]
        else:
            info = result
    
        title = info.get("title", "Unknown Title")
        if len(title) > 50:
            title = title[:50]
        artist = info.get("uploader", "Unknown Artist")
        duration = int(info.get("duration", 0))
        thumbnail_url = info.get("thumbnail")
        url = info.get("url")

        data = [url, title, artist, duration, thumbnail_url]
        CACHE[song_name] = {
            "timestamp": now,
            "data": data
        }
                
        return data