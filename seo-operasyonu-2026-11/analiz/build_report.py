import json, sys, os, glob, re, collections
sys.path.insert(0, os.path.dirname(__file__))
from rev30 import REV
from dup_table import DUP
from opp_evergreen import OPP
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

S = os.path.dirname(os.path.dirname(__file__))
OUT = sys.argv[1]
R = json.load(open(f"{S}/data/report_data.json"))
NP = json.load(open(f"{S}/data/nonpublic.json"))
NEWS = json.load(open(f"{S}/out/news_candidates.json"))
UP = json.load(open(f"{S}/out/upload_log.json")) if os.path.exists(f"{S}/out/upload_log.json") else []
G = json.load(open(f"{S}/data/gsc.json"))
INV = json.load(open(f"{S}/data/inv.json"))

L = ["tr", "en", "es", "ar", "ru", "zh"]
LN = {"tr": "Türkçe", "en": "İngilizce", "es": "İspanyolca", "ar": "Arapça", "ru": "Rusça", "zh": "Çince"}

def pl(link, slug):
    m = re.search(r"/(en|es|ar|ru|zh)/", link)
    if m: return m.group(1)
    m = re.match(r"(en|es|ar|ru|zh)-", slug); return m.group(1) if m else "tr"

npc = {st: collections.Counter(pl(p["link"], p["slug"]) for p in NP[st]) for st in NP}
pub = collections.Counter(p["lang"] for p in INV if p["type"] == "post")
nopll = collections.Counter(p["lang"] for p in INV if p["type"] == "post" and p["pll"] is None)
last30 = collections.Counter(p["lang"] for p in INV if p["type"] == "post" and p["date"] >= "2026-10-07")
cpt = collections.Counter(p["lang"] for p in INV if p["type"] != "post")

GAPS = {
 "tr": "KAAN/ASELSAN'da 7'şer mükerrer URL; sözlük 'X ne demek' başlıkları; harç/ücret sorgularında başlık uyumu",
 "en": "Ülke sayfalarında 'Ecuadorian/Tunisian/Bolivian army' ifadesi yok; HK416, SAR 56, MPT-55, BAE/Elbit/Fincantieri profilleri yok; 1.273 yazı dil atanmamış",
 "es": "Ülke dosyası yok (México, Argentina…); Indra/Naval Group profili ve 'qué es un misil' rehberi yok; 5 SEDENA/SEMAR mükerreri",
 "ar": "'كم عدد الجيش …' sorgularına doğrudan cevap yok; 'ما هو الصاروخ' genel rehberi yok; 3 mükerrer çift",
 "ru": "HQ-9 404 + yanlış çeviri; 'что такое БТР/корвет' rehberi yok; 342 yazı dil atanmamış",
 "zh": "Talep kanıtı yok (2 gösterim); 118 yazı dil atanmamış — yeni ZH üretimi önerilmez",
}
TOPS = {l: "; ".join(f"{t[:55]} ({c:.0f} tık/{i:.0f} gös.)" for t, c, i in R["T1"][l]["top"][:3]) for l in L}

wb = openpyxl.Workbook()
H = Font(bold=True, color="FFFFFF"); F = PatternFill("solid", fgColor="1F2A44")
def sheet(name, head, rows, widths=None):
    ws = wb.create_sheet(name); ws.append(head)
    for c in ws[1]: c.font = H; c.fill = F; c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows: ws.append(list(r))
    for i, w in enumerate(widths or [], 1): ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"; return ws
wb.remove(wb.active)

# ---- Tablo 0: kapsam
G_rows = [("Kaynak dosya", "https___envantermedya.com_-Performance-on-Search-2026-11-06.xlsx"),
          ("Arama türü", "Web (metin tabanlı)"), ("Zaman aralığı", "Son 24 saat (2026-11-05 06:00 → 2026-11-06 05:00, UTC+3)"),
          ("Toplam (Grafik)", "1.628 tık / 144.112 gösterim / CTR %1,13"),
          ("Sorgular sekmesi", "1.000 satır; 584 tık / 39.322 gösterim (anonim sorgular hariç → toplamla eşleşmez)"),
          ("Sayfalar sekmesi", "1.000 satır; anchor (#) URL'ler ayrı satır, burada temel URL'de toplandı"),
          ("Uyarı", "24 saatlik veri aylık hacim değildir; haber zirveleri (SINKEX 26, KAAN-1) tabloyu şişirir. 28 gün / 3 ay GSC erişimi yok."),
          ("WordPress", "Herkese açık REST + yönetici uygulama parolası ile taslak/zamanlanmış tarandı (salt okuma; yalnız yeni taslaklar oluşturuldu)")]
sheet("Kapsam", ["Alan", "Değer"], G_rows, [24, 110])

# ---- Tablo 1
t1 = []
for l in L:
    a = R["T1"][l]
    t1.append((LN[l], a["pages"], a["clicks"], a["impr"], f"%{a['ctr']}", a["pos"], pub[l], npc["draft"][l], npc["future"][l],
               last30[l], nopll[l], cpt[l], TOPS[l], GAPS[l]))
sheet("T1 Dil performansı", ["Dil", "GSC sayfa sayısı", "Tıklama", "Gösterim", "CTR", "Ort. konum", "Yayında yazı", "Taslak", "Zamanlanmış",
      "Son 30 gün yayın", "Dil atanmamış yazı", "Sözlük/sistem/sayfa (CPT)", "En güçlü konular", "En büyük eksikler"],
      t1, [11, 9, 9, 10, 7, 8, 9, 8, 10, 9, 10, 10, 60, 60])
sheet("T1b Sorgu dili", ["Sorgu dili (tahmini)", "Sorgu", "Tıklama", "Gösterim", "CTR %", "Konum"],
      [(LN.get(l, l), v["queries"], v["clicks"], v["impr"], v["ctr"], v["pos"]) for l, v in R["T1q"].items()], [18, 8, 8, 9, 8, 8])
sheet("T1c Ülke grupları", ["Grup", "Tıklama", "Gösterim"], [(k, v[0], v[1]) for k, v in R["countries"].items()]
      + [("— " + n, c, i) for n, c, i, p in R["hisp"]], [30, 9, 10])

# ---- Tablo 2
pages = {}
for a in R["top100"]: pages[a["url"].rstrip("/")] = a
t2 = []
for r in REV:
    t2.append((r["lang"], r["url"], r["id"], r["query"], r["q_impr"], r["q_clicks"], r["q_pos"], r["issue"],
               f"BAŞLIK: {r['old_title']}  →  {r['new_title']}\nMETA: {r['old_desc']}  →  {r['new_desc']}\nİÇERİK: {r['content']}\nİÇ LİNK: {r['links']}\nTEKNİK: {r['tech']}",
               r["prio"], r["decision"]))
sheet("T2 Mevcut iyileştirme (30)", ["Dil", "Mevcut URL", "Post ID", "Hedef sorgu", "Gösterim", "Tıklama", "Konum", "Sorun", "SEO revizyonu (önce → sonra)", "Öncelik", "Karar"],
      t2, [5, 45, 8, 24, 8, 7, 7, 55, 100, 7, 18])

# ---- Tablo 3
t3 = []
for o in OPP:
    lang, title, country, q, ev, src, dup, prio, dec, draft = o
    t3.append((lang, title, country, q, ev, src, dup, prio, dec, "Tam taslak (bu teslimat)" if draft else "Havuz"))
news_draft = {"spain-pnt-pem-2-3bn","spain-ea-aircraft-modernisation-1-438bn","spain-155mm-extended-range-269m","spain-mh60r-loa-amendment-38m","turkiye-parliament-ratifies-makkah-defence-pact","aselsan-1-1bn-air-defence-export","romania-moldova-joint-procurement-iveco-trucks"}
for n in NEWS:
    t3.append((",".join(n["target_langs"]), n["headline_en"], ", ".join(n.get("target_countries", [])), n["id"], f"Güncel gelişme {n['date']}; ilgili GSC: ülke gösterimi",
               f"{n['primary_source']['name']} — {n['primary_source']['url']}", "Eksik: " + ", ".join(n["envanter_coverage"].get("missing_in", [])) + " (yayında+taslak+zamanlanmış kontrol)",
               "P3", "NEWS UPDATE" if n["id"] in ("turkiye-parliament-ratifies-makkah-defence-pact", "peru-congress-funds-second-f16-block70-batch") else ("VERIFY" if n["confidence"] != "high" else "NEW"),
               "Tam taslak (bu teslimat)" if n["id"] in news_draft else "Havuz"))
sheet("T3 Yeni fırsatlar", ["Dil", "Önerilen başlık", "Hedef ülke", "Ana sorgu", "Talep kanıtı", "Kaynak", "Mükerrerlik kontrolü", "Öncelik", "Karar", "Durum"],
      t3, [8, 55, 16, 24, 32, 45, 50, 7, 16, 16])

# ---- Tablo 4
sheet("T4 Mükerrer", ["Dil", "URL 1", "URL 2", "Benzerlik", "Arama niyeti", "Önerilen işlem (onay gerekli)"], DUP, [5, 55, 60, 30, 28, 50])

# ---- Tablo 5
t5 = [(u["lang"], u["title"], u["post_id"], u["link"], u["status"], u["target_query"], u["source_check"]) for u in UP]
sheet("T5 WP taslakları", ["Dil", "Makale başlığı", "Post ID", "URL (taslak önizleme)", "Durum", "Hedef sorgu", "Kaynak doğrulaması"], t5, [5, 60, 8, 50, 8, 26, 70])

# ---- Top 100
sheet("Top100 mevcut sayfa", ["Dil", "URL", "Başlık", "Gösterim", "Tıklama", "Konum", "Ek tık potansiyeli (tahmin)", "Polylang dili", "Özel meta açıklama"],
      [(a["lang"], a["url"], a["title"], a["impr"], a["clicks"], a["pos"], a["score"], "var" if a["pll"] else "YOK", "var" if a["rm_desc"] else "yok") for a in R["top100"]],
      [5, 60, 60, 9, 8, 7, 10, 9, 9])
CAL = json.load(open(f"{S}/out/calendar.json"))
sheet("Yayın takvimi önerisi", ["Önerilen slot (TR saati)", "Dil", "Post ID", "Başlık", "Tür", "O gün o dilde zamanlanmış", "Not"],
      [(c["slot"], c["lang"], c["post_id"], c["title"], c["type"], c["existing_that_day"], c.get("note", "")) for c in CAL], [18, 5, 8, 70, 8, 10, 50])
wb.save(OUT)
print("saved", OUT, len(t2), len(t3), len(DUP), len(t5))
