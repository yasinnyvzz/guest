#!/usr/bin/env python3
"""Envanter Medya / Defence Arabia başlık kartı (1200x675). Kullanım: kapak.py out.png "etiket" "manşet" [brand] [rtl]"""
import sys
from PIL import Image, ImageDraw, ImageFont

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
GOLD, NAVY1, NAVY2, WHITE = (201, 162, 74), (11, 22, 42), (22, 36, 60), (240, 244, 252)


def wrap(draw, text, font, maxw, rtl):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font, direction="rtl" if rtl else None) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make(out, label, headline, brand="ENVANTER MEDYA", rtl=False):
    W, H = 1200, 675
    im = Image.new("RGB", (W, H), NAVY1)
    d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(NAVY1[i] + (NAVY2[i] - NAVY1[i]) * k) for i in range(3)))
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(24, 38, 62))
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=(24, 38, 62))
    d.rectangle([0, 0, W, 9], fill=GOLD)
    direction = "rtl" if rtl else None
    lab = ImageFont.truetype(BOLD, 26)
    d.text((W / 2, 150), label.upper() if not rtl else label, font=lab, fill=GOLD, anchor="mm", direction=direction)
    d.rectangle([W / 2 - 50, 185, W / 2 + 50, 189], fill=GOLD)
    size = 56
    while size > 30:
        f = ImageFont.truetype(BOLD, size)
        lines = wrap(d, headline, f, 960, rtl)
        if len(lines) <= 4:
            break
        size -= 4
    lh = int(size * 1.3)
    y = 340 - lh * (len(lines) - 1) / 2 + 20
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=WHITE, anchor="mm", direction=direction)
        y += lh
    d.text((W / 2, 630), brand, font=ImageFont.truetype(BOLD, 22), fill=GOLD, anchor="mm")
    im.save(out)


if __name__ == "__main__":
    a = sys.argv
    make(a[1], a[2], a[3], a[4] if len(a) > 4 else "ENVANTER MEDYA", len(a) > 5)
