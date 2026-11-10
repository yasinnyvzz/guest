#!/usr/bin/env python3
"""10 Kasım 2026 SEO pilotu: GSC analizi + fırsatlar + CTR paketi + taslak kaydı → ENVANTER_SEO_2026-11-10.xlsx
Kullanım: python3 rapor_xlsx.py <gsc1110.json> <çıktı.xlsx>"""
import json, sys
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

HERE = Path(__file__).resolve().parent.parent
gsc = json.load(open(sys.argv[1]))
wb = Workbook()
H = Font(bold=True, color="FFFFFF"); FILL = PatternFill("solid", fgColor="0B1F3A")


def sheet(title, header, rows, widths=None):
    ws = wb.create_sheet(title)
    ws.append(header)
    for c in ws[1]:
        c.font, c.fill = H, FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(list(r))
    for i, w in enumerate(widths or [], start=1):
        ws.column_dimensions[ws.cell(1, i).column_letter].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    return ws


wb.remove(wb.active)
tot = [("10 Kasım 2026 (son 24 saat)", 1610, 125557, 1.282), ("8 Kasım 2026 (son 24 saat, kullanıcı verisi)", 1151, 104422, 1.102),
       ("6 Kasım 2026 (son 24 saat, önceki rapor)", 1628, 144112, 1.130)]
sheet("Özet", ["Kesit", "Tıklama", "Gösterim", "CTR %"], tot, [44, 12, 12, 10])

Q = sorted(gsc["Q"], key=lambda x: -x["i"])
sheet("Sorgular (1000)", ["Sorgu", "Tahmini dil", "Tıklama", "Gösterim", "CTR %", "Konum", "Segment"],
      [(q["q"], q["lang"], q["c"], q["i"], round(q["ctr"] * 100, 2), q["pos"],
        "Yüksek gösterim / 0 tık" if q["i"] >= 100 and q["c"] == 0 else ("Konum 4–15" if 4 <= q["pos"] <= 15 else ""))
       for q in Q], [42, 10, 9, 10, 8, 8, 22])
P = sorted(gsc["P"], key=lambda x: -x["i"])
sheet("Sayfalar (1000)", ["URL", "Dil", "Tıklama", "Gösterim", "CTR %", "Konum"],
      [(p["u"], p["lang"], p["c"], p["i"], round(p["ctr"] * 100, 2), p["pos"]) for p in P], [90, 6, 9, 10, 8, 8])
sheet("Ülkeler", ["Ülke", "Tıklama", "Gösterim", "CTR", "Konum"], gsc["C"], [28, 10, 10, 10, 10])
sheet("Cihazlar", ["Cihaz", "Tıklama", "Gösterim", "CTR", "Konum"], gsc["D"], [14, 10, 10, 10, 10])
sheet("Saatlik", ["Saat (UTC+3)", "Tıklama", "Gösterim", "CTR", "Konum"], gsc["G"], [22, 10, 10, 10, 10])

F = json.load(open(HERE / "firsatlar_30.json"))
sheet("30 fırsat", ["#", "Öncelik", "Hedef sorgu", "Dil", "Gösterim / Tık / Konum (24s)", "Mevcut URL", "Karar", "Yeni açı / aksiyon",
                    "SEO potansiyeli", "Resmî kaynak", "Parti"],
      [(i + 1, *r) for i, r in enumerate(F)], [4, 7, 30, 6, 20, 48, 16, 70, 26, 30, 12])
C = json.load(open(HERE / "ctr_revizyonlari.json"))
sheet("CTR paketi", ["Post ID", "Dil", "URL", "Hedef sorgu", "GSC 10 Kasım", "Sorun", "Rank Math başlık (önce)", "Rank Math başlık (sonra)",
                     "Açıklama (sonra)", "İçerik aksiyonları", "Öncelik", "Karar"],
      [(x["post_id"], x["lang"], x["url"], x["target_query"], x["gsc_10nov"], x.get("problem", ""), x["rank_math_title"]["from"],
        x["rank_math_title"]["to"], x["rank_math_description"]["to"], " • ".join(x["content_actions"]), x["priority"], x["decision"])
       for x in C], [8, 5, 50, 24, 36, 50, 36, 40, 60, 60, 7, 18])
log = HERE / "taslaklar" / "yukleme_kaydi.json"
if log.exists():
    L = json.load(open(log))
    sheet("WP taslakları", ["Dil", "Post ID", "Başlık", "Hedef sorgu", "Karar", "Tür", "Önizleme", "Görsel", "Kaynak sayısı"],
          [(x["lang"], x["post_id"], x["title"], x["target_query"], x["decision"], x["content_type"], x["preview"], x["image_note"], x["sources"])
           for x in L], [5, 8, 60, 26, 12, 10, 46, 50, 8])
plan = HERE / "takvim_onerisi.json"
if plan.exists():
    sheet("Yayın takvimi (öneri)", ["Slot (TR saati)", "Dil", "Post ID", "Başlık", "Tür", "Onay"],
          [(r["slot"], r["lang"], r["post_id"], r["title"], r["tur"], "BEKLİYOR" if not r.get("onay") else "ONAYLI")
           for r in json.load(open(plan))], [18, 5, 8, 70, 12, 10])
wb.save(sys.argv[2])
print("yazıldı:", sys.argv[2])
