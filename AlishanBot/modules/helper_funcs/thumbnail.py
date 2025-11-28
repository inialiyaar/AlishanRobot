from PIL import Image, ImageDraw, ImageFont, ImageFilter
from textwrap import wrap
import os
import requests
from AlishanBot import config
import uuid
from AlishanBot.__init__ import BOT_USERNAME

import re

os.makedirs("downloads", exist_ok=True)
cleaned = BOT_USERNAME.replace("_", " ")
cleaned = re.sub(r"(?i)\b(robot|bot)\b", "", cleaned)
BOT_NAME = " ".join(cleaned.split())

async def download_thumbnail(thumb_url):
    save_path = f"downloads/{uuid.uuid4().hex[:8]}.png"
    response = requests.get(thumb_url, stream=True, timeout=10)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    return save_path                  

async def Thumbnail(thumb_url, title, artist, duration):
    if title is None:
        title = "Unknown Title"
    if artist is None:
        artist = "Unknown Artist"
    thumb_path = await download_thumbnail(thumb_url)
    earphones_path = "earphones.png"
    bg = Image.open(thumb_path).convert("RGBA").resize((1280, 720), Image.LANCZOS)
    blurred = bg.filter(ImageFilter.GaussianBlur(18))
    dim = Image.new("RGBA", (1280, 720), (0, 0, 0, 120))
    blurred = Image.alpha_composite(blurred, dim)
    card_w, card_h = 1050, 350
    card = Image.new("RGBA", (card_w, card_h), (255,255,255,0))
    cx = (1280 - card_w) // 2
    cy = (720 - card_h) // 2
    cut = blurred.crop((cx, cy, cx+card_w, cy+card_h))
    cut = cut.filter(ImageFilter.GaussianBlur(10))
    cut.putalpha(160)

    mask = Image.new("L", (card_w, card_h), 0)
    m = ImageDraw.Draw(mask)
    m.rounded_rectangle((0, 0, card_w, card_h), radius=40, fill=255)

    card = Image.composite(cut, card, mask)
    draw = ImageDraw.Draw(card)

    title_font = ImageFont.truetype("fonts/Bold.otf", 46)
    artist_font = ImageFont.truetype("fonts/Regular.otf", 33)
    small_font = ImageFont.truetype("fonts/Regular.otf", 26)
    bot_font = ImageFont.truetype("fonts/Bold.otf", 28)

    thumb = Image.open(thumb_path).convert("RGBA").resize((300, 300), Image.LANCZOS)

    glow = Image.new("RGBA", (300, 300), (255,255,255,0))
    g = ImageDraw.Draw(glow)
    g.ellipse((0, 0, 300, 300), fill=(255,255,255,120))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    card.paste(glow, (40, 25), glow)

    tmask = Image.new("L", (300, 300), 0)
    ImageDraw.Draw(tmask).rounded_rectangle((0,0,300,300), radius=40, fill=255)
    thumb.putalpha(tmask)
    card.paste(thumb, (40, 25), thumb)

    if os.path.exists(earphones_path):
        ear = Image.open(earphones_path).convert("RGBA").resize((240, 240), Image.LANCZOS)
        ear.putalpha(200)
        card.paste(ear, (250, 40), ear)

    draw.text((370, 30), BOT_NAME, font=bot_font, fill="white")

    wrapped = wrap(title, 20)[:2]
    for i, line in enumerate(wrapped):
        draw.text((370, 80 + (i*50)), line, font=title_font, fill="white")

    draw.text((370, 180), artist, font=artist_font, fill=(240,240,240,230))
    bar_y = 260
    bar_s = 370
    bar_e = card_w - 60

    draw.line([(bar_s, bar_y), (bar_e, bar_y)], fill=(255,255,255,180), width=5)

    cursor_x = bar_s + 200
    draw.ellipse((cursor_x-12, bar_y-12, cursor_x+12, bar_y+12), fill=(255,255,255,200))
    draw.ellipse((cursor_x-8, bar_y-8, cursor_x+8, bar_y+8), fill="white")

    draw.text((bar_s, bar_y+15), "0:00", font=small_font, fill="white")
    draw.text((bar_e-70, bar_y+15), duration, font=small_font, fill="white")
    final = blurred.copy()
    final.paste(card, (cx, cy), card)

    output = thumb_path.replace(".png", "_final.png")
    final.save(output, "PNG")
    return output