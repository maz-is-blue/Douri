"""Generates simple placeholder photography for local dev and seed data.

Douri's real photography isn't available in this repo — staff will replace
every one of these through the admin's image fields. Keeping this local and
dependency-free (Pillow only) avoids seeding from external hotlinked URLs.
"""

import hashlib
import io

from PIL import Image, ImageDraw, ImageFont

PALETTE = ['#0092D4', '#222222', '#29A1E2', '#54595F', '#2A2A2A']


def _color_for(label):
    index = int(hashlib.md5(label.encode('utf-8')).hexdigest(), 16) % len(PALETTE)
    return PALETTE[index]


def make_placeholder(label, width=1200, height=800):
    """Returns (filename, ContentFile-ready bytes) for a labelled placeholder photo."""
    bg = _color_for(label)
    img = Image.new('RGB', (width, height), bg)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype('arial.ttf', size=max(18, width // 28))
    except OSError:
        font = ImageFont.load_default()

    text = label
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    max_width = width * 0.82
    while tw > max_width and len(text) > 4:
        text = text[:-4].rstrip() + '…'
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    draw.text(((width - tw) / 2, (height - th) / 2), text, fill='#FFFFFF', font=font)

    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=82)
    buffer.seek(0)
    return buffer
