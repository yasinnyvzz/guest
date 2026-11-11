#!/usr/bin/env python3
"""Tablo A–F'yi üretir: RAPOR_TABLOLARI.md + KONU_ARSIVLERI_2026-11-11.xlsx.
Girdi: veri klasörü (cek.py, sadele.py, hub_esle.py, kuru_calistir.py, canli_durum.py çıktıları).
Kullanım: rapor_uret.py <veri_klasoru>"""
import csv, gzip, html, json, os, re, sys, collections, random, urllib.parse as up
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

D = sys.argv[1]
KOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SOZ = json.load(open(f"{KOK}/sozluk/varliklar.json", encoding="utf-8"))
V = {v["id"]: v for v in SOZ["varliklar"]}
SEO = json.load(open(f"{KOK}/sozluk/seo_metinleri.json", encoding="utf-8"))
HUB = json.load(open(f"{D}/hublar.json"))
CANLI = json.load(open(f"{D}/canli40.json"))
OZET = json.load(open(f"{D}/kuru/ozet.json"))
SITE_AD = {"ev": "Envanter Medya", "dm": "DefenceMENA", "da": "Defence Arabia"}
DOMAIN = {"ev": "https://envantermedya.com", "dm": "https://defencemena.com", "da": "https://defencearabia.com"}
DIL_RX = {"ev": (r"https://envantermedya\.com/(en|es|ar|ru|zh)/", "tr"), "dm": (r"https://defencemena\.com/(fr|pt)/", "en"),
          "da": (r"https://defencearabia\.com/(en)/", "ar")}
TAG_ROBOTS = {"ev": "noindex (tüm etiketler, site geneli)", "dm": "index; 1 yazılı etiketler noindex", "da": "index; 1 yazılı etiketler noindex"}
SITEMAP = {"ev": {"category": "var (6 dosya)", "post_tag": "yok"}, "dm": {"category": "var", "post_tag": "var (2 dosya)"},
           "da": {"category": "var", "post_tag": "var"}}
tables = {}


def rel(u):
    u = up.unquote(u)
    for d in DOMAIN.values():
        u = u.replace(d, "")
    return u


def lang_of(site, link):
    rx, base = DIL_RX[site]
    m = re.match(rx, link)
    return m.group(1) if m else base


def proj(site, lang, eid):
    o = OZET[site]["varlik"]
    g = lambda d: o.get(f"{lang}|{eid}|{d}", 0)
    return g("zaten_bagli"), g("eklenecek"), g("editor_onayi"), g("kopya_terime_bagli"), g("hub_yok")


# ---------------- TABLO A ----------------
A = []
for site in ("ev", "dm", "da"):
    for tax, f in (("category", "categories"), ("post_tag", "tags")):
        terms = {t["id"]: t for t in json.load(open(f"{D}/{site}_{f}.json"))}.values()
        by = collections.defaultdict(list)
        for t in terms:
            by[lang_of(site, t["link"])].append(t)
        for lang, ts in sorted(by.items(), key=lambda x: -len(x[1])):
            c = [t["count"] for t in ts]
            thin = sum(1 for x in c if x <= 1)
            sample = sorted(ts, key=lambda t: -t["count"])[0]
            names = collections.Counter(re.sub(r"\s+", " ", html.unescape(t["name"]).strip().lower()) for t in ts if t["count"] > 0)
            dup = sum(n - 1 for n in names.values() if n > 1)
            sorun = []
            if thin:
                sorun.append(f"{thin}/{len(ts)} terim ≤1 yazılı (%{round(100 * thin / len(ts))})")
            if dup:
                sorun.append(f"{dup} aynı adlı kopya terim")
            nodesc = sum(1 for t in ts if t["count"] >= 20 and not t["description"].strip())
            if nodesc:
                sorun.append(f"20+ yazılı {nodesc} terimde açıklama yok")
            robots = "index" if tax == "category" else TAG_ROBOTS[site]
            A.append([SITE_AD[site], f"{tax} ({lang})", rel(sample["link"]).rsplit("/", 2)[0] + "/…", len(ts), sum(c),
                      robots + f"; sitemap: {SITEMAP[site][tax]}", "; ".join(sorun) or "—"])
# Elle doğrulanmış bulgular (canlı HTML ve REST'ten)
ev_desc_bos = sum(1 for k, v in CANLI.items() if k.startswith("ev:") and v and not v["desc"])
ev_slogan = sum(1 for k, v in CANLI.items() if k.startswith("ev:en:") and v and "Savunma Sanayii Haberleri" in v["title"])
A += [
    ["Envanter Medya", "category (tr)", "/category/projeler/altay-tanki/ · /category/envanter/bmc/altay/ · /category/envanter/otokar/altay-otokar/ · /category/turk-savunma-sanayi/kara-sistemleri/altay-tank/", "4", "6+1+0+0", "index", "ALTAY için 4 ayrı kategori; yazılar dağılmış, hiçbiri güçlü değil → tek arşivde toplanmalı (birleştirme onayı)"],
    ["Envanter Medya", "category (tr)", "/category/envanter/tusas/mmu/ · /category/projeler/milli-muharip-ucak/ · /tag/kaan/ · /tag/milli-muharip-ucak/ · /tag/tf-x/", "5", "17+1+49+11+6", "kategori index, etiket noindex", "KAAN beş terime bölünmüş; başlığında KAAN geçen 85 TR haberin yalnız 15'i KAAN kategorisinde"],
    ["Envanter Medya", "category (en/tr)", "20 hedef arşivin canlı <title>/meta denetimi", "20", "—", "index", f"{ev_desc_bos}/20 arşivde meta açıklama boş; {ev_slogan}/10 İngilizce arşivin başlığına Türkçe site sloganı ekleniyor (\"– Envanter Medya – Savunma Sanayii Haberleri\")"],
    ["Envanter Medya", "post_tag (en)", "/en/tag/kaan-en/", "1", "34", "noindex", "İngilizce KAAN arşivinin tek adresi noindex etiket; 'kaan fighter jet news' niyetine indekslenebilir sayfa yok"],
    ["Envanter Medya", "post_tag (tr)", "/tag/المخزون-العسكري/ vb.", "—", "72", "noindex", "TR dil grubunda Arapça/İngilizce adlı etiketler (dil karışması); hreflang ve eşleştirmeyi bozar"],
    ["Envanter Medya", "tema (ar)", "body.rtl { direction: ltr !important }", "—", "—", "—", "Arapça sayfalarda tema genel yönü LTR'ye zorluyor; yalnız lang=\"ar\" öğeler RTL. Eklenti kutuları kendi dir=rtl özniteliğini taşır"],
    ["Envanter Medya", "yazı dili", "URL dili ≠ metin dili", "—", "108", "—", "108 yazıda metin dili URL dilinden farklı (ör. /en/ altında Türkçe metin); eşleştirmeden çıkarıldı"],
    ["Envanter Medya", "şablon", "tekil haber", "—", "—", "—", "Haber şablonu etiketleri hiç göstermiyor; konu arşivlerine haberden bağlantı yok ('Benzer Yazılar' kategori kartı)"],
    ["DefenceMENA", "site", "defencemena.com", "—", "981 yazı", "index", "Site Afrika odaklı (EN/FR/PT); 'MENA' adı Orta Doğu arşivlerini zayıf bırakıyor. REST yönetici erişimi bu oturumda yok (401) → yalnız herkese açık veri"],
    ["DefenceMENA / Defence Arabia", "post_tag", "/tag/2025-ekonomik-beklentiler/", "1", "0", "noindex", "Türkçe artık etiket iki sitede de var (içe aktarma kalıntısı) — silinmeli/birleştirilmeli"],
    ["Defence Arabia", "category", "298 kategori", "298", "2.747", "index", "158 kategori boş (0 yazı) ama kategori site haritasında olup olmadıkları ayrıca kontrol edilmeli"],
]
tables["A"] = (["Site", "Taksonomi", "Mevcut URL", "Terim sayısı", "Haber sayısı (atama)", "İndeks durumu", "SEO sorunu"], A)

# ---------------- TABLO B ----------------
B = []
GSC_KANIT = {"ev:tr:kaan", "ev:en:aselsan"}  # 24 saatlik GSC'de talep kanıtı olanlar (Tablo E)
ELLE = json.load(open(f"{KOK}/sozluk/hub_elle.json", encoding="utf-8"))
KAPSAM = {("ev", "tr"), ("ev", "en"), ("ev", "ar"), ("dm", "en"), ("da", "ar")}
ilk40 = json.load(open(f"{KOK}/motor/ilk40.json"))
for i, key in enumerate(ilk40, 1):
    site, lang, eid = key.split(":")
    h, c, s = HUB.get(key), CANLI.get(key) or {}, SEO.get(key, {})
    zb, ek, eo, kp, _ = proj(site, lang, eid)
    mevcut = h["count"] if h else 0
    rb = c.get("robots") or ""
    robots = ("noindex" if "noindex" in rb else "index") if rb else ""
    islem = "Mevcut arşiv korunur + hub modülleri" if robots == "index" else "Etiket hub'a dönüşür; kalite kapısı geçince index"
    B.append([SITE_AD[site], lang, s.get("h1", eid), ", ".join(s.get("hedef_sorgu", [])[:3]), rel(h["link"]) if h else "—",
              mevcut, ek, eo, mevcut + ek, robots or "—",
              "P1" if (mevcut + ek >= 40 or key in GSC_KANIT) else ("P2" if mevcut + ek >= 10 else "P3"), islem])
# Arşivi olmayan güçlü varlıklar (yeni arşiv adayı)
yeni = []
for site in ("ev", "dm", "da"):
    for k, n in OZET[site]["varlik"].items():
        lang, eid, d = k.split("|")
        if d == "hub_yok" and n >= 15 and eid in V and (site, lang) in KAPSAM and ELLE.get(f"{site}:{lang}:{eid}") != "yok":
            yeni.append((site, lang, eid, n))
for site, lang, eid, n in sorted(yeni, key=lambda x: -x[3])[:25]:
    ad = V[eid]["ad"].get(lang) or V[eid]["ad"]["en"]
    slug = re.sub(r"[^a-z0-9]+", "-", eid)
    url = {"ev": ("/tag/" if lang == "tr" else f"/{lang}/tag/") + slug + ("" if lang == "tr" else f"-{lang}") + "/",
           "dm": ("/" if lang == "en" else f"/{lang}/") + "tag/" + slug + "/", "da": "/tag/" + up.quote(ad.replace(" ", "-")) + "/"}[site]
    B.append([SITE_AD[site], lang, ad + " (YENİ)", "—", up.unquote(url), 0, "—", "—", f"{n} (yüksek+orta eşleşme)", "yeni etiket (noindex başlar)",
              "P2" if n >= 40 else "P3", "Yeni terim: yalnız onayla açılır; ≥5 yazı + özgün tanıtım olmadan index'e alınmaz"])
tables["B"] = (["Site", "Dil", "Arşiv adı (H1)", "Hedef sorgu (birleşik niyet)", "Önerilen URL (mevcut korunur)",
                "Mevcut haber", "Eklenecek (yüksek güven)", "Editör kuyruğu", "Sınıflandırma sonrası", "Canlı robots",
                "Öncelik", "İşlem"], B)

# ---------------- TABLO C ----------------
C = []
for v in SOZ["varliklar"]:
    for lang in ("tr", "en", "ar"):
        al = [a["t"] for a in v["alias"] if (re.search(r"[\u0600-\u06ff]", a["t"]) is not None) == (lang == "ar")]
        if lang != "ar":
            al = [a for a in al if True]
        site = "ev" if lang in ("tr", "en") else "da"
        h = HUB.get(f"{site}:{lang}:{v['id']}") or (HUB.get(f"ev:ar:{v['id']}") if lang == "ar" else None)
        ilgili = [V[x]["ad"].get(lang, x) for x in (v.get("yapan", []) + v.get("ust", []) + v.get("ilgili", [])) if x in V]
        C.append([v["ad"].get(lang, v["ad"]["en"]), ", ".join(dict.fromkeys(al)) if lang != "en" else ", ".join(dict.fromkeys(a["t"] for a in v["alias"] if not re.search(r"[\u0600-\u06ff]", a["t"]))),
                  lang, (SITE_AD["ev" if not h else h["site"]] + " " + rel(h["link"])) if h else "— (Tablo B)",
                  ", ".join(dict.fromkeys(ilgili))[:200], V[v["id"]]["tip"]])
tables["C"] = (["Ana varlık", "Alternatif adlar (eşleştirme)", "Dil", "Tekil arşiv", "İlişkili arşivler", "Tür"], C)

# ---------------- TABLO D ----------------
random.seed(11)
Dr = []
ONAY = {"eklenecek": "Toplu eklenebilir (yönetici onayı sonrası)", "editor_onayi": "Editör kuyruğu (orta güven)",
        "zaten_bagli": "Zaten bağlı", "kopya_terime_bagli": "Kopya terime bağlı (birleştirme kararı)",
        "hub_yok": "Arşiv yok (Tablo B)", "dil_uyumsuz": "Atlandı: dil uyumsuz"}
for site, quota in (("ev", {"tr": 40, "en": 25, "ar": 15}), ("da", {"ar": 15}), ("dm", {"en": 10})):
    rows = list(csv.DictReader(gzip.open(f"{D}/kuru/eslestirme_{site}.csv.gz", "rt", encoding="utf-8")))
    byp = collections.defaultdict(list)
    for r in rows:
        byp[(r["dil"], r["yazi_id"])].append(r)
    for lang, n in quota.items():
        ids = [k for k, rs in byp.items() if k[0] == lang and any(r["durum"] in ("eklenecek", "editor_onayi") for r in rs)]
        for k in random.sample(ids, min(n, len(ids))):
            rs = byp[k]
            Dr.append([SITE_AD[site], rs[0]["yazi_id"], rs[0]["baslik"][:120],
                       "; ".join(f"{r['varlik']}({r['guven'][0].upper()})" for r in rs if r["varlik"]),
                       "/".join(sorted({r["guven"] for r in rs if r["guven"]})),
                       "; ".join(sorted({ONAY[r["durum"]] for r in rs})), rs[0]["url"]])
tables["D"] = (["Site", "Haber ID", "Haber başlığı", "Önerilen arşivler (Y=yüksek, O=orta)", "Güven düzeyi", "Onay durumu", "URL"], Dr)

# ---------------- TABLO E ----------------
E = [
    ["KAAN (TR) — /category/envanter/tusas/mmu/", "1.845 (sorgu: 'tusaş kaan')", "25", "%1,36", "3,79",
     "Sorgu bir haber sayfasına (/kaan-1-prototipi-yetenekleri-gokvatan/) düşüyor; arşivin kendisi 1.000 sayfalık listede yok. Hub kurulduktan sonra 'kaan haberleri' / 'tusaş kaan' için sorgu→sayfa eşleşmesi izlenmeli."],
    ["ASELSAN (EN) — /en/category/inventory-en/aselsan-en/", "1.202 (sorgu: 'aselsan')", "4", "%0,33", "4,15",
     "Marka sorgusu 'ASELSAN competitors' yazısına düşüyor; EN arşivde meta açıklama yok ve başlıkta Türkçe slogan var. Hub başlık/açıklaması + iç bağlantı ile arşiv hedef sayfa olmalı."],
    ["Diğer 38 arşiv", "veri yok", "veri yok", "veri yok", "veri yok",
     "Elde yalnız 6 Kasım'a ait 24 saatlik GSC dışa aktarımı var; ilk 100 sayfa listesinde hiçbir kategori/etiket arşivi yok. 28 gün ve 3 ay 'Sayfa × Sorgu' dışa aktarımı (her site, ülke filtresiyle) gerekiyor. Rakam üretilmedi."],
    ["DefenceMENA / Defence Arabia (tümü)", "veri yok", "veri yok", "veri yok", "veri yok",
     "Bu oturumda iki sitenin GSC verisine erişim yok (GSC API yetkisi yok, Frase denemesi bitmiş, Semrush API birimi yok)."],
]
tables["E"] = (["Arşiv", "Gösterim", "Tıklama", "CTR", "Ortalama konum", "İşlem / not (gerçek veri: GSC 24 saat, 05–06.11.2026)"], E)

# ---------------- TABLO F ----------------
F = [
    ["Tümü", "Eklenti kurulumu (envanter-konu-arsivleri), varsayılan ayarlarla", "WP ≥6.0, PHP ≥7.4; Rank Math + Polylang ile test edildi", "Düşük: hub işaretlenmedikçe robots/URL değişmez", "Yerel test sitesinde geçti (TR/EN/AR, 499 gerçek yazı)"],
    ["Envanter Medya", "hub_esle.py çıktısını içe aktar: wp eka hub-ice-aktar hublar.json --site=ev --uygula", "Yönetici WP-CLI ya da Code Snippets ile tek seferlik", "Düşük: yalnız seçenek + eka_varlik terim meta'sı", "Test sitesinde eşdeğer eşleme ile geçti"],
    ["Envanter Medya", "İlk 20 arşivi hub yap: wp eka hub-kur seo_metinleri.json --dil=tr|en --uygula", "Rank Math başlık/açıklaması boşsa doldurulur, doluysa ezilmez", "Orta: başlık değişimi CTR'yi etkiler → 30/60/90 gün izleme", "Test sitesinde geçti (title/description/H1/intro/related)"],
    ["Envanter Medya", "Toplu sınıflandırma: önce kuru rapor, sonra --guven=yuksek --uygula, parti parti (--varlik=kaan,tusas,…)", "wp eka siniflandir; 200'lük partiler; term sayımı ertelenir", "Orta: ~23 bin ekleme; birincil kategori korunur; Polylang eşitlemesi günlüğe yazılır; geri alma hazır", "Test: 1.557 ekleme uygulandı → geri alındı → fazladan terim 0"],
    ["Envanter Medya", "Kopya terimleri birleştir (ALTAY×4, KAAN×5, Lockheed Martin×2, Hava Savunma×2 …)", "Rank Math Redirections ile 301; Polylang çeviri grupları", "Yüksek: URL değişikliği — yalnız onayla, önce GSC kontrolü", "Yapılmadı (onay bekliyor)"],
    ["Envanter Medya", "EN başlıklardaki Türkçe slogan ve boş meta açıklamalar", "Rank Math başlık şablonu (EN/AR/ES/RU için ayrı ayırıcı/slogan)", "Düşük", "Tespit edildi; düzeltme onay bekliyor"],
    ["Envanter Medya", "Hub etiketleri için site haritası (eka-konu-sitemap.xml) Rank Math dizinine eklenir", "Yalnız INDEX kararı alan hub etiketleri", "Düşük", "Test: dizinde görünüyor, 2 URL"],
    ["Defence Arabia", "Aynı eklenti; 10 Arapça hub (ülke etiketleri + 4 kategori)", "Yönetici erişimi gerekli (bu oturumda yalnız okuma)", "Düşük", "Metinler hazır; canlı kurulum yapılmadı"],
    ["DefenceMENA", "Aynı eklenti; 10 bölgesel hub; FR/PT için sözlük ad genişletmesi", "Yönetici erişimi gerekli (bu oturumda REST 401)", "Düşük", "Metinler hazır; canlı kurulum yapılmadı"],
    ["Tümü", "Kademeli açılış: 1. dalga 40 hub → 30/60/90 gün GSC ölçümü → 2. dalga", "GSC 28g/3a dışa aktarımı", "—", "Bekliyor"],
]
tables["F"] = (["Site", "Yapılacak iş", "Teknik gereksinim", "Risk", "Test durumu"], F)

# ---------------- ÇIKTI ----------------
def md_cell(x):
    return str(x).replace("|", "\\|").replace("\n", " ")


basliklar = {"A": "TABLO A — Mevcut taksonomi denetimi", "B": "TABLO B — Yeni arşiv önerileri (ilk 40 + yeni aday)",
             "C": "TABLO C — Eşanlamlılar", "D": "TABLO D — Toplu haber eşleştirme (örneklem; tamamı veri/eslestirme_*.csv.gz)",
             "E": "TABLO E — SEO performansı", "F": "TABLO F — Uygulama planı"}
with open(f"{KOK}/RAPOR_TABLOLARI.md", "w", encoding="utf-8") as f:
    for k, (hdr, rows) in tables.items():
        f.write(f"\n## {basliklar[k]}\n\n| " + " | ".join(hdr) + " |\n|" + "---|" * len(hdr) + "\n")
        for r in rows:
            f.write("| " + " | ".join(md_cell(x) for x in r) + " |\n")
wb = Workbook()
wb.remove(wb.active)
for k, (hdr, rows) in tables.items():
    ws = wb.create_sheet(f"Tablo {k}")
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F3864")
    for r in rows:
        ws.append(r)
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = min(60, max(10, max(len(str(c.value or "")) for c in col[:60]) * 0.9))
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
ws = wb.create_sheet("Özet dry-run")
ws.append(["Site", "Yazı", "Yüksek güven (eklenecek)", "Editör kuyruğu", "Zaten bağlı", "Kopya terime bağlı", "Arşiv yok", "Dil uyumsuz", "Yazı başına öneri"])
for s in ("ev", "dm", "da"):
    o = OZET[s]
    d = o["durum"]
    ws.append([SITE_AD[s], o["yazi"], d.get("eklenecek", 0), d.get("editor_onayi", 0), d.get("zaten_bagli", 0),
               d.get("kopya_terime_bagli", 0), d.get("hub_yok", 0), d.get("dil_uyumsuz", 0), o["ort_oneri"]])
ws = wb.create_sheet("SEO metinleri")
ws.append(["Anahtar", "H1", "SEO title", "Meta description", "Tanıtım", "Hedef sorgular", "Canlı title (önce)", "Canlı meta (önce)"])
for k, s in SEO.items():
    c = CANLI.get(k) or {}
    ws.append([k, s["h1"], s["seo_title"], s["meta_description"], s["tanitim"], ", ".join(s["hedef_sorgu"]), c.get("title", ""), c.get("desc", "")])
wb.save(f"{KOK}/KONU_ARSIVLERI_2026-11-11.xlsx")
print({k: len(v[1]) for k, v in tables.items()})
