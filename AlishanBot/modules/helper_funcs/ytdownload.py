import os
from yt_dlp import YoutubeDL
from AlishanBot import config
from AlishanBot.__init__ import BOT_USERNAME

os.makedirs("downloads", exist_ok=True)
COOKIE_FILE = "cookies/cookies.txt"


def is_youtube_url(text):
    text = text.strip().lower()
    if not (text.startswith("http://") or text.startswith("https://")):
        return False

    YT_DOMAINS = [
        "youtube.com",
        "youtu.be",
        "www.youtube.com",
        "m.youtube.com",
        "music.youtube.com"
    ]

    try:
        from urllib.parse import urlparse
        parsed = urlparse(text)
        domain = parsed.netloc.lower()

        return domain in YT_DOMAINS
    except:
        return False
    
def is_playlist(url):
    return "list=" in url    
    
def YTDownload(song_name, query_format, title=None, artist=None):
    file_path = ""
    if query_format == "video":
        ydl_opts = {
            "format": "best[height<=720]",
            "cookiefile": COOKIE_FILE,
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "geo_bypass": True,
            
            "nocheckcertificate": True,
            "quiet": True,
            "addmetadata": True, 
            "no_warnings": True,
            "noplaylist": True,
            "marge_output_format": "mp4", 
        }
    else:
        ydl_opts = {
            "format": "best[height<=720]",
            "cookiefile": COOKIE_FILE,
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "geo_bypass": True,
            
            "nocheckcertificate": True,
            "quiet": True,
            "addmetadata": True, 
            "no_warnings": True,
            "noplaylist": True,
            "merge_output_format": "mp4", 
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio", 
                    "preferredcodec": "mp3", 
                    "preferredquality": "192", 
                },
                {
                    "key": "FFmpegMetadata", 
                    "add_metadata": {
                        "artist": artist or "Unknown Artist", 
                        "title": title or "Unknown Title", 
                        "album": "Youtube", 
                        "comment": f"Download via {BOT_USERNAME}"
                    }, 
                }, 
                ], 
        }
    if (song_name.startswith("http://") or song_name.startswith("https://")) and not is_youtube_url(song_name):
        return "URLERROR"
    query = song_name if is_youtube_url(song_name) else f"ytsearch1:{song_name}"       
    if is_youtube_url(song_name) and is_playlist(song_name):
        with YoutubeDL({"quiet": True, "extract_flat": True}) as ydl:
            playlist_info = ydl.extract_info(song_name, download=False)
            entries = playlist_info.get("entries", [])
            if not entries:
                return "PLAYLISTERROR"
            else:
                vid = entries[0]
                query = vid.get("url") or vid.get("webpage_url")
                
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=False)
        if "entries" in result and result["entries"]:
            info = result["entries"][0]
        else:
            info = result
        duration = info.get("duration")
        if duration > config.DURATION_LIMIT:
            return "DURATIONERROR"
        else:
            ydl.download([query]) 
            file_path = ydl.prepare_filename(info)
            if query_format == "audio":
                base, ext = os.path.splitext(file_path)
                file_path = f"{base}.mp3"
    return file_path