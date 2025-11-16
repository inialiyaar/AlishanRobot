import instaloader
from urllib.parse import urlparse
import os

def is_instagram_url(url: str):
    url = url.strip().lower()
    return "instagram.com" in url

def IGMeta(url):
    try:
        if not is_instagram_url(url):
            return "URLERROR"

        L = instaloader.Instaloader(
            download_video_thumbnails=False,
            save_metadata=False,
            download_geotags=False,
            download_comments=False,
        )

        parsed = urlparse(url)
        shortcode = parsed.path.strip("/").split("/")[-1]

        if not shortcode:
            return "INVALID_URL"

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        if post.user and post.user.is_private:
            return "PRIVATE_ERROR"

        title = post.title or "Instagram Post"
        author = post.owner_username or "Unknown"
        duration = post.video_duration if post.is_video else 0
        thumbnail = post.url
        return url, title, author, duration, thumbnail

    except Exception as e:
        return f"ERROR: {str(e)}"

os.makedirs("downloads", exist_ok=True)

def IGDownload(url):
    try:
        L = instaloader.Instaloader(
            download_video_thumbnails=False,
            save_metadata=False,
            download_geotags=False,
            download_comments=False,
        )

        parsed = urlparse(url)
        shortcode = parsed.path.strip("/").split("/")[-1]

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        if post.is_private:
            return "PRIVATEERROR"

        if post.is_video:
            filename = f"downloads/{shortcode}.mp4"
        else:
            filename = f"downloads/{shortcode}.jpg"

        L.download_post(post, target="downloads")

        return filename

    except Exception as e:
        return f"ERROR: {str(e)}"        