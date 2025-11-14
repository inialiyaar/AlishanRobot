import subprocess
import json
from mutagen.mp4 import MP4
from mutagen.easyid3 import EasyID3
from mutagen import File as MutaFile


def get_meta(path):
    ext = path.split(".")[-1].lower()
    if ext == "mp3":
        try:
            audio = EasyID3(path)
            title = audio.get("title", ["Unknown"])[0]
            artist = audio.get("artist", ["Unknown"])[0]

            mut = MutaFile(path)
            duration = int(mut.info.length)

            return title, artist, duration
        except:
            pass
    if ext in ["mp4", "m4a", "mov"]:
        try:
            mp4 = MP4(path)
            title = mp4.tags.get("\xa9nam", ["Unknown"])[0]
            artist = mp4.tags.get("\xa9ART", ["Unknown"])[0]

            mut = MutaFile(path)
            duration = int(mut.info.length)

            return title, artist, duration
        except:
            pass

    try:
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            path
        ]
        output = subprocess.check_output(cmd)
        info = json.loads(output)

        tags = info["format"].get("tags", {})

        title = (
            tags.get("title")
            or tags.get("TITLE")
            or "Unknown"
        )

        artist = (
            tags.get("artist")
            or tags.get("ARTIST")
            or "Unknown"
        )

        duration = int(float(info["format"].get("duration", 0)))

        return title, artist, duration

    except Exception as e:
        return "Unknown", "Unknown", 0