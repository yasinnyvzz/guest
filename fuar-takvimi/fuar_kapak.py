#!/usr/bin/env python3
"""Envanter Medya fuar kapakları (1200x675).

  yeni:    python3 fuar_kapak.py yeni out.png "IQDEX" "IQDEX 2027" "Bağdat · Irak" "Nisan 2027"
  duzelt:  python3 fuar_kapak.py duzelt src.webp out.png "Abu Dabi · BAE" "Ocak 2027" [yeni_yil]

`duzelt` mevcut kapağın alt satırını (konum • tarih) silip yeniden yazar; yeni_yil verilirse
başlıktaki altın renkli yılı da değiştirir. Fotoğraf korunur.
"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

F = "/usr/share/fonts/opentype/inter/"
BLACK, XBOLD, SEMI = F + "Inter-Black.otf", F + "Inter-ExtraBold.otf", F + "Inter-SemiBold.otf"
GOLD, WHITE, BLUE, MUTED = (232, 182, 72), (236, 240, 247), (150, 178, 222), (120, 140, 175)
W, H = 1200, 675


def _spaced(d, xy, text, font, fill, spacing, anchor_center=True):
    widths = [d.textlength(c, font=font) for c in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = xy[0] - total / 2 if anchor_center else xy[0]
    for c, w in zip(text, widths):
        d.text((x, xy[1]), c, font=font, fill=fill, anchor="lm")
        x += w + spacing
    return total


def header(d, y=54):
    f = ImageFont.truetype(XBOLD, 17)
    a, b, c = "ENVANTER", "MEDYA", "   ·   SAVUNMA FUAR TAKVİMİ"
    parts = [(a, (150, 170, 205)), (b, GOLD), (c, (150, 170, 205))]
    sp = 4.2
    total = sum(sum(d.textlength(ch, font=f) + sp for ch in t) for t, _ in parts) - sp
    x = W / 2 - total / 2
    for t, col in parts:
        x += _spaced(d, (x, y), t, f, col, sp, anchor_center=False) + sp


def subline(d, y, konum, tarih, size=26):
    f = ImageFont.truetype(SEMI, size)
    sep = "   •   "
    w = d.textlength(konum, font=f) + d.textlength(sep, font=f) + d.textlength(tarih, font=f)
    x = W / 2 - w / 2
    d.text((x, y), konum, font=f, fill=WHITE, anchor="lm")
    x += d.textlength(konum, font=f)
    d.text((x, y), sep, font=f, fill=MUTED, anchor="lm")
    x += d.textlength(sep, font=f)
    d.text((x, y), tarih, font=f, fill=BLUE, anchor="lm")


def yeni(out, buyuk, baslik, konum, tarih):
    im = Image.new("RGB", (W, H))
    px = im.load()
    for y in range(H):
        for x in range(W):
            dx, dy = (x - 900) / 700, (y - 520) / 600
            r = min(1.0, (dx * dx + dy * dy) ** 0.5)
            base = (10 + 20 * (1 - r), 26 + 34 * (1 - r), 58 + 62 * (1 - r))
            px[x, y] = tuple(int(v) for v in base)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(22, 40, 76))
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=(22, 40, 76))
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    d = ImageDraw.Draw(im)
    header(d)
    fb = ImageFont.truetype(BLACK, 96 if len(buyuk) <= 10 else 74)
    d.text((W / 2, 250), buyuk, font=fb, fill=(245, 247, 252), anchor="mm")
    # başlık: yıl altın
    ad, _, yil = baslik.rpartition(" ")
    ft = ImageFont.truetype(BLACK, 46)
    wa, wy = d.textlength(ad + " ", font=ft), d.textlength(yil, font=ft)
    x = W / 2 - (wa + wy) / 2
    d.text((x, 444), ad + " ", font=ft, fill=(245, 247, 252), anchor="lm")
    d.text((x + wa, 444), yil, font=ft, fill=GOLD, anchor="lm")
    d.rectangle([W / 2 - 48, 512, W / 2 + 48, 516], fill=GOLD)
    subline(d, 556, konum, tarih)
    im.save(out, quality=88)


def _bbox(im, y0, y1, pred):
    px = im.load()
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(W):
            if pred(px[x, y]):
                xs.append(x)
                ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


def _sil(im, box, pad=8):
    """Kutuyu üst ve alt kenardan dikey enterpolasyonla doldurur."""
    x0, y0, x1, y1 = box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad
    px = im.load()
    h = y1 - y0
    for x in range(x0, x1 + 1):
        top, bot = px[x, y0 - 1], px[x, y1 + 1]
        for y in range(y0, y1 + 1):
            k = (y - y0) / h
            px[x, y] = tuple(int(top[i] * (1 - k) + bot[i] * k) for i in range(3))
    reg = im.crop((x0 - 4, y0 - 4, x1 + 5, y1 + 5)).filter(ImageFilter.GaussianBlur(3))
    im.paste(reg, (x0 - 4, y0 - 4))


def duzelt(src, out, konum, tarih, yeni_yil=None):
    im = Image.open(src).convert("RGB")
    parlak = lambda p: max(p) > 140
    alt = _bbox(im, 536, 580, parlak)
    if not alt:
        raise SystemExit("alt satır bulunamadı")
    cy = (alt[1] + alt[3]) / 2
    _sil(im, alt)
    d = ImageDraw.Draw(im)
    subline(d, cy, konum, tarih)
    if yeni_yil:
        altin = lambda p: p[0] > 180 and p[1] > 130 and p[2] < 110 and p[0] - p[2] > 90
        yb = _bbox(im, 410, 480, altin)
        if not yb:
            raise SystemExit("başlık yılı bulunamadı")
        _sil(im, yb, pad=5)
        h = yb[3] - yb[1]
        ft = ImageFont.truetype(BLACK, int(round(h * 1.37)))
        d.text((yb[0] - 1, yb[3] + 1), yeni_yil, font=ft, fill=GOLD, anchor="ls")
    im.save(out, quality=90)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "yeni":
        yeni(*a[1:6])
    elif a[0] == "duzelt":
        duzelt(*a[1:])
