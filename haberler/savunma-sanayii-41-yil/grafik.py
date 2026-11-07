#!/usr/bin/env python3
"""Savunma sanayiinin 41 yılı dosyası için infografikler (Envanter lacivert/altın stili)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
GOLD, N1, N2, W, MUT, LINE = (201, 162, 74), (11, 22, 42), (22, 36, 60), (240, 244, 252), (150, 165, 190), (34, 50, 78)


def f(p, s):
    return ImageFont.truetype(p, s)


def base(w, h):
    im = Image.new("RGB", (w, h), N1)
    d = ImageDraw.Draw(im)
    for y in range(h):
        k = y / h
        d.line([(0, y), (w, y)], fill=tuple(int(N1[i] + (N2[i] - N1[i]) * k) for i in range(3)))
    d.rectangle([0, 0, w, 8], fill=GOLD)
    return im, d


def footer(d, w, h, src):
    d.text((40, h - 34), src, font=f(R, 18), fill=MUT, anchor="lm")
    d.text((w - 40, h - 34), "ENVANTER MEDYA", font=f(B, 20), fill=GOLD, anchor="rm")


def wrap(d, text, font, maxw):
    out, cur = [], ""
    for wd in text.split():
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            out.append(cur)
            cur = wd
    if cur:
        out.append(cur)
    return out


def kronoloji():
    items = [
        ("1985", "3238 sayılı Kanun kabul edildi; SAGEB ve Savunma Sanayii Destekleme Fonu kuruldu"),
        ("1987", "TUSAŞ tesislerinde F-16 ortak üretimi; ilk yerli montaj uçak teslim edildi"),
        ("1989", "İdare, Savunma Sanayii Müsteşarlığına (SSM) dönüştü"),
        ("1990'lar", "Ortak üretim modelleri: zırhlı araç, helikopter, fırkateyn, füze"),
        ("2004", "SSİK; tank, ATAK ve İHA ihalelerini iptal edip yerli ana yüklenici modeline geçti"),
        ("2007–2008", "ATAK ve ALTAY sözleşmeleri imzalandı"),
        ("2011", "MİLGEM'in ilk gemisi TCG Heybeliada hizmete girdi"),
        ("2018", "Kurum, Cumhurbaşkanlığı Savunma Sanayii Başkanlığı (SSB) oldu"),
        ("2019–2022", "AKINCI (2019) ve KIZILELMA (2022) ilk uçuşlarını yaptı"),
        ("2023", "TCG Anadolu hizmete girdi; HÜRJET ilk kez uçtu"),
        ("2024", "KAAN ilk uçuşunu yaptı; Çelik Kubbe kararı alındı"),
        ("2025", "Savunma ve havacılık ihracatı ilk kez 10 milyar doları aştı"),
        ("2026", "SSB 41 yaşında: ~1.500 proje, 4 binden fazla firma"),
    ]
    w, h = 1200, 1700
    im, d = base(w, h)
    d.text((w / 2, 70), "DOSYA · 1985–2026", font=f(B, 24), fill=GOLD, anchor="mm")
    d.text((w / 2, 125), "Savunma sanayiinin 41 yılı: kilometre taşları", font=f(B, 40), fill=W, anchor="mm")
    x0, y, step = 300, 220, 112
    d.line([(x0, y - 20), (x0, y + step * (len(items) - 1) + 20)], fill=GOLD, width=4)
    ft = f(R, 25)
    for yr, txt in items:
        d.ellipse([x0 - 13, y - 13, x0 + 13, y + 13], fill=N1, outline=GOLD, width=5)
        d.text((x0 - 40, y), yr, font=f(B, 30), fill=GOLD, anchor="rm")
        lines = wrap(d, txt, ft, 800)
        yy = y - (len(lines) - 1) * 17
        for ln in lines:
            d.text((x0 + 40, yy), ln, font=ft, fill=W, anchor="lm")
            yy += 34
        y += step
    footer(d, w, h, "Kaynak: SSB, TBMM/Mevzuat, şirket açıklamaları · Derleme: Envanter Medya")
    im.save(HERE / "kronoloji.png", optimize=True)


def kurumsal():
    w, h = 1600, 560
    im, d = base(w, h)
    d.text((w / 2, 70), "Bir kurum, üç isim", font=f(B, 40), fill=W, anchor="mm")
    boxes = [("1985", "SAGEB", "Savunma Sanayii Geliştirme ve", "Destekleme İdaresi Başkanlığı"),
             ("1989", "SSM", "Savunma Sanayii", "Müsteşarlığı"),
             ("2018", "SSB", "Cumhurbaşkanlığı Savunma", "Sanayii Başkanlığı")]
    bw, gap = 420, 110
    x = (w - (3 * bw + 2 * gap)) / 2
    for i, (yr, ab, l1, l2) in enumerate(boxes):
        d.rounded_rectangle([x, 150, x + bw, 450], radius=14, outline=GOLD, width=3, fill=(16, 30, 52))
        d.text((x + bw / 2, 200), yr, font=f(B, 30), fill=GOLD, anchor="mm")
        d.text((x + bw / 2, 285), ab, font=f(B, 72), fill=W, anchor="mm")
        d.text((x + bw / 2, 370), l1, font=f(R, 24), fill=MUT, anchor="mm")
        d.text((x + bw / 2, 405), l2, font=f(R, 24), fill=MUT, anchor="mm")
        if i < 2:
            ax = x + bw + 20
            d.line([(ax, 300), (ax + gap - 40, 300)], fill=GOLD, width=6)
            d.polygon([(ax + gap - 40, 284), (ax + gap - 18, 300), (ax + gap - 40, 316)], fill=GOLD)
        x += bw + gap
    footer(d, w, h, "Kaynak: Savunma Sanayii Başkanlığı")
    im.save(HERE / "kurumsal.png", optimize=True)


def karsilastirma():
    rows = [("Proje sayısı", "62", "~1.500"), ("Firma sayısı", "56", "4.000+"),
            ("Proje hacmi", "5,5 mlr $", "100+ mlr $"), ("Sektör cirosu", "~1,1 mlr $", "~25 mlr $"),
            ("Yıllık Ar-Ge", "49 mn $", "3,5+ mlr $"), ("Yerlilik oranı", "~%20", "%80+"),
            ("İhracat", "248 mn $", "10,05 mlr $"), ("İstihdam", "—", "135.000+")]
    w, h = 1600, 1000
    im, d = base(w, h)
    d.text((w / 2, 70), "2002 ve bugün: sekiz göstergede dönüşüm", font=f(B, 40), fill=W, anchor="mm")
    cols, cw, ch, gx, gy = 4, 350, 360, 30, 30
    x0 = (w - (cols * cw + (cols - 1) * gx)) / 2
    for i, (lab, a, b) in enumerate(rows):
        cx = x0 + (i % cols) * (cw + gx)
        cy = 140 + (i // cols) * (ch + gy)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=14, fill=(16, 30, 52), outline=LINE, width=2)
        d.rectangle([cx, cy, cx + cw, cy + 6], fill=GOLD)
        d.text((cx + cw / 2, cy + 50), lab.upper(), font=f(B, 22), fill=GOLD, anchor="mm")
        d.text((cx + cw / 2, cy + 115), "2002", font=f(R, 20), fill=MUT, anchor="mm")
        d.text((cx + cw / 2, cy + 155), a, font=f(B, 34), fill=MUT, anchor="mm")
        d.polygon([(cx + cw / 2 - 14, cy + 195), (cx + cw / 2 + 14, cy + 195), (cx + cw / 2, cy + 213)], fill=GOLD)
        d.text((cx + cw / 2, cy + 250), "BUGÜN", font=f(R, 20), fill=MUT, anchor="mm")
        d.text((cx + cw / 2, cy + 300), b, font=f(B, 46), fill=W, anchor="mm")
    footer(d, w, h, "Kaynak: SSB, 41. yıl açıklaması (7 Kasım 2026). İhracat 'bugün' değeri 2025 yılına aittir.")
    im.save(HERE / "karsilastirma.png", optimize=True)


def ihracat():
    data = [("2002", 0.248), ("2021", 3.224), ("2022", 4.4), ("2023", 5.5), ("2024", 7.154), ("2025", 10.054),
            ("2026*", 8.05)]
    w, h = 1600, 900
    im, d = base(w, h)
    d.text((80, 70), "Savunma ve havacılık ihracatı (milyar $)", font=f(B, 40), fill=W, anchor="lm")
    d.text((80, 118), "2002'den 2025'e yaklaşık 40 kat", font=f(R, 26), fill=GOLD, anchor="lm")
    left, right, top, bot = 120, w - 80, 190, h - 130
    vmax = 11
    for v in (0, 2, 4, 6, 8, 10):
        y = bot - (bot - top) * v / vmax
        d.line([(left, y), (right, y)], fill=LINE, width=1)
        d.text((left - 15, y), str(v), font=f(R, 20), fill=MUT, anchor="rm")
    n = len(data)
    slot = (right - left) / n
    bwid = slot * 0.58
    for i, (lab, v) in enumerate(data):
        cx = left + slot * (i + 0.5)
        y = bot - (bot - top) * v / vmax
        partial = lab.endswith("*")
        fill = (120, 98, 50) if partial else GOLD
        d.rectangle([cx - bwid / 2, y, cx + bwid / 2, bot], fill=fill)
        if partial:
            for k in range(int(y), int(bot), 14):
                d.line([(cx - bwid / 2, k), (cx + bwid / 2, k)], fill=GOLD, width=2)
        txt = f"{v:.2f}".replace(".", ",") if v < 1 else f"{v:.2f}".rstrip("0").rstrip(",").replace(".", ",")
        d.text((cx, y - 22), txt, font=f(B, 28), fill=W, anchor="mm")
        d.text((cx, bot + 30), lab.replace("*", ""), font=f(B, 24), fill=W, anchor="mm")
        if partial:
            d.text((cx, bot + 60), "Ocak–Ekim", font=f(R, 18), fill=MUT, anchor="mm")
    # 2002 ile 2021 arasında boşluk işareti
    gx = left + slot * 1.0
    d.text((gx, bot + 30), "//", font=f(B, 24), fill=MUT, anchor="mm")
    footer(d, w, h, "Kaynak: SSB ve TİM verileri. 2003–2020 yılları grafikte gösterilmemiştir.")
    im.save(HERE / "ihracat.png", optimize=True)


if __name__ == "__main__":
    kronoloji(); kurumsal(); karsilastirma(); ihracat()
    print("tamam")
