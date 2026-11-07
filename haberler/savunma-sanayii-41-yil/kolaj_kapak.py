#!/usr/bin/env python3
"""Fotoğraf kolajlı kapak (1200x675). Kullanım: kolaj_kapak.py <çıktı> <foto1> <foto2> <foto3> <foto4>"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
GOLD, NAVY, WHITE = (201, 162, 74), (11, 22, 42), (240, 244, 252)


def cover(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


out, photos = sys.argv[1], sys.argv[2:6]
W, H = 1200, 675
can = Image.new("RGB", (W, H), NAVY)
cw, ch = W // 2, H // 2
for i, p in enumerate(photos):
    can.paste(cover(Image.open(p).convert("RGB"), cw - 2, ch - 2), ((i % 2) * cw + 1, (i // 2) * ch + 1))
# lacivert örtü: ortada koyu bant
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
for y in range(H):
    dist = abs(y - H * 0.55) / (H * 0.55)
    a = int(235 - 140 * min(1, dist))
    d.line([(0, y), (W, y)], fill=NAVY + (a,))
can = Image.alpha_composite(can.convert("RGBA"), ov).convert("RGB")
d = ImageDraw.Draw(can)
d.rectangle([0, 0, W, 9], fill=GOLD)
d.text((W / 2, 235), "DOSYA · 1985–2026", font=ImageFont.truetype(B, 28), fill=GOLD, anchor="mm")
d.rectangle([W / 2 - 50, 265, W / 2 + 50, 269], fill=GOLD)
d.text((W / 2, 340), "SAVUNMA SANAYİİNİN", font=ImageFont.truetype(B, 50), fill=WHITE, anchor="mm")
d.text((W / 2, 425), "41 YILI", font=ImageFont.truetype(B, 92), fill=GOLD, anchor="mm")
d.text((W / 2, 505), "Hazır alımdan teknoloji ihracatına", font=ImageFont.truetype(B, 32), fill=WHITE, anchor="mm")
d.rectangle([0, H - 62, W, H], fill=NAVY)
d.rectangle([0, H - 62, W, H - 59], fill=GOLD)
d.text((W / 2, H - 31), "ENVANTER MEDYA", font=ImageFont.truetype(B, 22), fill=GOLD, anchor="mm")
can.save(out, optimize=True)
