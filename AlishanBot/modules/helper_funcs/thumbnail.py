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
    thumb_path = await download_thumbnail(thumb_url)
    bg = Image.open(thumb_path).convert("RGBA").resize((1280, 720), Image.LANCZOS)
    blurred_bg = bg.filter(ImageFilter.GaussianBlur(radius=6))
    overlay = Image.new("RGBA", blurred_bg.size, (0, 0, 0, 100))
    blurred_bg = Image.alpha_composite(blurred_bg, overlay)
    card_w, card_h = 460, 230
    card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle([(0, 0), (card_w, card_h)], radius=30, fill=(30, 30, 30, 200))
    thumb = Image.open(thumb_path).convert("RGBA").resize((120, 120), Image.LANCZOS)
    mask = Image.new('L', thumb.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, 120, 120], radius=20, fill=255)
    thumb.putalpha(mask)
    card.paste(thumb, (20, 20), thumb)
    title_font = ImageFont.truetype("fonts/Bold.otf", 20)
    artist_font = ImageFont.truetype("fonts/Regular.otf", 17)
    small_font = ImageFont.truetype("fonts/Regular.otf", 16)
    zhunehra_font = ImageFont.truetype("fonts/Regular.otf", 18)
    draw.text((160, 20), f"{BOT_NAME}", font=zhunehra_font, fill="white")
    wrapped_title = wrap(title, width=26)[:2]
    for i, line in enumerate(wrapped_title):
        draw.text((160, 40 + i * 20), line, font=title_font, fill="white")
    draw.text((160, 90), artist, font=artist_font, fill=(255, 255, 255, 160))
    bar_y = 120
    bar_start = 160
    bar_end = card_w - 30
    draw.line([(bar_start, bar_y), (bar_end, bar_y)], fill="white", width=2)
    draw.text((bar_start, bar_y + 6), "0:00", font=small_font, fill="white")
    draw.text((bar_end - 35, bar_y + 6), duration, font=small_font, fill="white")
    btn_y = bar_y + 60
    btn_size = 16
    gap = 50
    center_x = (bar_start + bar_end) // 2
    prev_x = center_x - gap - btn_size - 10
    draw.polygon([
        (prev_x, btn_y),
        (prev_x + btn_size, btn_y - btn_size),
        (prev_x + btn_size, btn_y + btn_size)
    ], fill="white")
    draw.rectangle([(center_x - 8, btn_y - btn_size), (center_x - 2, btn_y + btn_size)], fill="white")
    draw.rectangle([(center_x + 2, btn_y - btn_size), (center_x + 8, btn_y + btn_size)], fill="white")
    next_x = center_x + gap + 10
    draw.polygon([
        (next_x, btn_y - btn_size),
        (next_x, btn_y + btn_size),
        (next_x + btn_size, btn_y)
    ], fill="white")
    final = blurred_bg.copy()
    final.paste(card, ((1280 - card_w) // 2, (720 - card_h) // 2), card)
    output_path = thumb_path.replace(".png", "_final.png")
    final.save(output_path, format="PNG")
    try:
        os.remove(thumb_path)
    except:   
        pass   
    return output_path