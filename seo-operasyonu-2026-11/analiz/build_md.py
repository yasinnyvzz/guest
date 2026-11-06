import json, sys, os, collections, re
sys.path.insert(0, os.path.dirname(__file__))
from rev30 import REV
from dup_table import DUP
from opp_evergreen import OPP
S = os.path.dirname(os.path.dirname(__file__))
R = json.load(open(f"{S}/data/report_data.json")); NP = json.load(open(f"{S}/data/nonpublic.json"))
NEWS = json.load(open(f"{S}/out/news_candidates.json")); UP = json.load(open(f"{S}/out/upload_log.json"))
CAL = json.load(open(f"{S}/out/calendar.json")); INV = json.load(open(f"{S}/data/inv.json"))
L = ["tr", "en", "es", "ar", "ru", "zh"]
def pl(link, slug):
    m = re.search(r"/(en|es|ar|ru|zh)/", link)
    if m: return m.group(1)
    m = re.match(r"(en|es|ar|ru|zh)-", slug); return m.group(1) if m else "tr"
npc = {st: collections.Counter(pl(p["link"], p["slug"]) for p in NP[st]) for st in NP}
pub = collections.Counter(p["lang"] for p in INV if p["type"] == "post")
nopll = collections.Counter(p["lang"] for p in INV if p["type"] == "post" and p["pll"] is None)
last30 = collections.Counter(p["lang"] for p in INV if p["type"] == "post" and p["date"] >= "2026-10-07")
def esc(x): return str(x).replace("|", "/").replace("\n", " ")
def fmt(n): return f"{n:,.0f}".replace(",", ".")
o = []
w = o.append
w("# Envanter Medya — Çok dilli GSC SEO operasyonu (ilk teslimat, 6 Kasım 2026)\n")
w("Ayrıntılı tablolar: `ENVANTER_SEO_2026-11-06.xlsx` (sekmeler: Kapsam, T1–T5, Top100, Yayın takvimi önerisi). Taslak JSON'ları: `taslaklar/`.\n")
w("## Veri kapsamı ve sınırlar\n")
w("- GSC dosyası **son 24 saat** (05.11 06:00 → 06.11 05:00, UTC+3), Web arama. Toplam 1.628 tık / 144.112 gösterim / CTR %1,13. Bu rakamlar aylık hacim değildir; SINKEX 26 ve KAAN-1 haber zirveleri tabloyu şişiriyor.")
w("- Sorgular sekmesi toplamın yalnız %27'sini (39.322 gösterim) gösteriyor (anonim sorgular). Sorgu ↔ sayfa eşleşmesi dosyada yok; eşleştirme URL dili + içerik başlık/slug eşleşmesiyle yapıldı.")
w("- 28 gün / 3 ay GSC verisine erişim yok → bir sonraki adımda bu iki aralığın dışa aktarımı gerekli.")
w("- WordPress: 17.932 yayımlanmış yazı + 3.093 CPT (sözlük, sistem, firma, fuar, sayfa) herkese açık REST ile; 322 taslak ve 3.600 zamanlanmış yazı yönetici uygulama parolasıyla (salt okuma) tarandı. Yazma işlemi yalnız 15 yeni taslak + 15 kapak görseli.\n")
w("## Kritik teknik bulgular (onay gerektiren işler dahil)\n")
for t in [
 "**İki ayrı yayın hattı aynı olayı iki URL'de yayımlıyor.** `es-…` önekli Polylang hattı ile `…-es` sonekli hat. Sonekli hattın **3.526 yazısının Polylang dili yok** (EN 1.273, AR 1.352, ES 441, RU 342, ZH 118). Örnek: Isaac Peral haberi EN'de 7.434 + 3.135 gösterime bölünmüş; hreflang grubu yanlış URL'de.",
 "**Otomasyon aynı konuyu tekrar üretiyor:** ES'de 14 'ejército más poderoso de Latinoamérica' URL'si, TR'de 7 'KAAN nedir' ve 7 'ASELSAN nedir', EN'de aynı gün 6 'F-22 nedir'. Zamanlanmış kuyrukta da tekrar var (TR S-80 iki kez).",
 "**Rank Math `%sep%` boş render ediliyor:** başlıklar '…SINKEX 26 Envanter Medya - Savunma Sanayii Haberleri' şeklinde çıkıyor. EN/ES/RU/AR başlıklarına Türkçe site sloganı ekleniyor (yerelleştirme hatası).",
 "**481 sözlük sayfasında meta açıklama boş;** otomatik açıklamalar bozuk Türkçe ('Geminin taşırdığı suyun ton cisminden hacmi'). 'X ne demek' sorgularında 5–10. sıra, ~0 tık.",
 "**RU'nun en çok gösterim alan URL'si 404:** HQ-9 sayfasının silinmiş '-2' kopyası 940 gösterim alıyor. Canlı sayfanın başlığında 'Долговременная' yanlış çeviri (doğrusu 'большой дальности').",
 "Birden çok sayfada çift H1 (ES SEMAR, ES S-80, EN/RU HQ-9). EN APFSDS sayfasında 'Image suggestions' ve 'An analogy for kids' gibi editoryal taslak başlıkları yayında.",
 "Zamanlanmış kuyrukta talebi **şimdi** olan içerikler aylar sonraya atanmış: EN S-80 açıklayıcısı 28.03.2027, Elbit profili 14.12.2026 → öne çekme önerisi.",
]: w(f"- {t}")
w("\n## TABLO 1 — Dil bazlı SEO performansı (GSC son 24 saat + WordPress envanteri)\n")
w("| Dil | GSC sayfa | Tıklama | Gösterim | CTR | Ort. konum | Yayında | Taslak | Zamanlanmış | Son 30 gün | Dil atanmamış | En güçlü konular | En büyük eksikler |")
w("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
GAPS = {"tr": "KAAN/ASELSAN mükerrerleri; sözlükte 'ne demek' başlıkları; harç/ücret başlık uyumu",
 "en": "Ülke sayfalarında 'Ecuadorian/Tunisian army' ifadesi yok; HK416/SAR 56/MPT-55, BAE/Elbit/Fincantieri profilleri yok",
 "es": "Ülke dosyası yok; Indra/Naval Group profili, 'qué es un misil/fragata' yok; 14+5 mükerrer",
 "ar": "'كم عدد الجيش …' sorgularına doğrudan cevap yok; genel radar/fırkateyn rehberi yok",
 "ru": "HQ-9 404 + yanlış çeviri; 'что такое БТР/корвет' yok", "zh": "Talep kanıtı yok (2 gösterim) — yeni ZH üretimi önerilmez"}
for l in L:
    a = R["T1"][l]; top = "; ".join(esc(t[:40]) + f" ({c:.0f}/{fmt(i)})" for t, c, i in a["top"][:2])
    w(f"| {l.upper()} | {a['pages']} | {a['clicks']:.0f} | {fmt(a['impr'])} | %{a['ctr']} | {a['pos']} | {fmt(pub[l])} | {npc['draft'][l]} | {fmt(npc['future'][l])} | {last30[l]} | {fmt(nopll[l])} | {top} | {GAPS[l]} |")
w("\nÜlke grupları (gösterim): Türkiye 53.785 · İspanyolca konuşan ülkeler 10.812 (İspanya 4.497, Meksika 2.409, Arjantin 1.012, Şili 990) · Arap ülkeleri 9.684 · BDT 7.472 · diğer 61.384. Sorgu dili tahmini: EN 28.269, TR 8.922, ES 1.018, RU 754, AR 359 gösterim.\n")
w("## TABLO 2 — Mevcut haber iyileştirmeleri (30)\n")
w("Önce → sonra başlık/meta, içerik eklemeleri ve teknik işler Excel'de (T2). Canlı yazılar **değiştirilmedi**.\n")
w("| # | Dil | Mevcut URL | Hedef sorgu | Gösterim | Tık | Konum | Sorun (özet) | Önerilen SEO başlığı | Öncelik / Karar |")
w("|---|---|---|---|---|---|---|---|---|---|")
for i, r in enumerate(REV, 1):
    w(f"| {i} | {r['lang']} | {esc(r['url'].replace('https://envantermedya.com',''))} | {esc(r['query'])} | {fmt(r['q_impr'])} | {r['q_clicks']} | {r['q_pos']} | {esc(r['issue'][:150])}… | {esc(r['new_title'])} | {r['prio']} · {r['decision']} |")
w("\n## TABLO 3 — Yeni SEO haber/rehber fırsatları\n")
newc = [x for x in OPP if not any(k in x[8] for k in ("SKIP", "UPDATE", "RESCHEDULE", "mevcut habere"))]
w(f"Kalıcı içerik: {len(newc)} yeni/yeni açı fırsatı + 16 güncel haber adayı (İspanya Bakanlar Kurulu'nun 4 kalemi tek haberde birleştirildi → 13 ayrı haber). Toplam **{len(newc)+13} ayrı makale fırsatı**; ayrıca {len(OPP)-len(newc)} satır öne çekme/güncelleme/atlama kararıdır. Tümü yayında + taslak + zamanlanmış kuyruğa karşı kontrol edildi.\n")
w("| Dil | Önerilen başlık | Hedef ülke | Ana sorgu | Talep kanıtı (24s) | Kaynak | Mükerrerlik kontrolü | Öncelik | Karar | Durum |")
w("|---|---|---|---|---|---|---|---|---|---|")
for x in OPP:
    w("| " + " | ".join(esc(v) for v in x[:9]) + f" | {'**taslak yazıldı**' if x[9] else 'havuz'} |")
drafted = {"spain-pnt-pem-2-3bn", "spain-ea-aircraft-modernisation-1-438bn", "spain-155mm-extended-range-269m", "spain-mh60r-loa-amendment-38m",
           "turkiye-parliament-ratifies-makkah-defence-pact", "aselsan-1-1bn-air-defence-export", "romania-moldova-joint-procurement-iveco-trucks"}
for n in NEWS:
    dec = "NEWS UPDATE" if n["id"] in ("turkiye-parliament-ratifies-makkah-defence-pact", "peru-congress-funds-second-f16-block70-batch") else ("NEW" if n["confidence"] == "high" else "VERIFY")
    w(f"| {','.join(n['target_langs'])} | {esc(n['headline_en'])} | {esc(', '.join(n.get('target_countries', [])))} | haber ({n['date']}) | güncel gelişme | {esc(n['primary_source']['name'])} | eksik: {','.join(n['envanter_coverage'].get('missing_in', []))} | P3 | {dec} | {'**taslak yazıldı**' if n['id'] in drafted else 'havuz'} |")
w("\n## TABLO 4 — Mükerrer içerik\n")
w("Hiçbir URL silinmedi, yönlendirilmedi veya birleştirilmedi; aşağıdakiler onay bekleyen önerilerdir.\n")
w("| Dil | URL 1 | URL 2 | Benzerlik | Arama niyeti | Önerilen işlem |")
w("|---|---|---|---|---|---|")
for d in DUP: w("| " + " | ".join(esc(v) for v in d) + " |")
w("\n## TABLO 5 — WordPress taslakları (15)\n")
w("Hepsi `draft`, dil atanmış, kapak = Envanter başlık kartı (gerçek fotoğraf ya da yapay zekâ görseli değil). Polylang çeviri grubuna **bağlanmadı**: grupta meta/kapak eşitlemesi yayındaki eşdeğer sayfaları değiştirebileceği için gruplama yayın anında editörde.\n")
w("| Dil | Makale başlığı | Post ID | URL | Durum | Hedef sorgu | Kaynak doğrulaması |")
w("|---|---|---|---|---|---|---|")
for u in UP: w(f"| {u['lang']} | {esc(u['title'])} | {u['post_id']} | https://envantermedya.com/wp-admin/post.php?post={u['post_id']}&action=edit | {u['status']} | {esc(u['target_query'])} | {esc(u['source_check'][:120])} |")
w("\nHer taslağın `verification_notes` alanında editörün yayın öncesi kontrol etmesi gereken maddeler var (ör. SAR 56 kullanıcı ülkeleri doğrulanamadı → metne yazılmadı; MPT-55 adetleri 2019 AA haberine dayanıyor; Mekke anlaşması oy sayısı resmî kayıtta yok).\n")
w("## Yayın takvimi önerisi (onay sonrası)\n")
w("Otomasyonun zamanlanmış saatleriyle çakışmayan, o gün o dilde yükü az olan slotlar. Haberler onaydan hemen sonra; rehberler 8–16 Kasım arasına yayıldı. Hiçbir taslak zamanlanmadı.\n")
w("| Slot | Dil | Post ID | Başlık | O gün o dilde zamanlanmış | Not |")
w("|---|---|---|---|---|---|")
for c in CAL: w(f"| {c['slot']} | {c['lang']} | {c['post_id']} | {esc(c['title'][:70])} | {c['existing_that_day']} | {esc(c.get('note',''))} |")
w("\n## 30 / 60 / 90 gün performans takibi (dil bazında ayrı)\n")
for t in [
 "**Temel çizgi:** bu dosya (24 saat) + 28 gün ve 3 ay GSC dışa aktarımı (Sayfa × Sorgu, ülke filtresiyle). URL listesi: T2'deki 30 sayfa, T5'teki 15 taslak, Top100.",
 "**Ölçülecekler (her dil ayrı):** organik tık ve gösterim değişimi; CTR değişimi (T2 sayfalarında hedef: konum sabitken CTR artışı); ilk 3 / ilk 10 sorgu sayısı; yeni içeriklerin ilk 30 gündeki gösterimi; güncellenen içeriklerin önce/sonra karşılaştırması (aynı 28 günlük pencere); ülke bazlı görünürlük (İspanya, Meksika, Arjantin, Şili ayrı); Kapsam raporundaki 404/indekslenmeyen URL'ler; mükerrer kümelerde hangi URL'nin gösterim aldığı (çakışma takibi).",
 "**30. gün:** T2 başlık/meta değişikliklerinin CTR etkisi; Polylang dili atanmamış yazılarda dil ataması yapıldıysa hreflang hataları. **60. gün:** yeni rehberlerin sıralaması; mükerrer kümelerde canonical sonrası gösterimin tek URL'de toplanması. **90. gün:** dil bazlı yeniden önceliklendirme — talep kanıtı zayıf kalan dillerde (ZH) üretim durdurulur, güçlü olanlara (ES ülke dosyaları, EN şirket profilleri) kaydırılır.",
]: w(f"- {t}")
w("\n## Onay bekleyen kararlar\n")
for t in ["Mükerrer kümeler için canonical/301 (T4) — URL değişikliği ve yönlendirme yapılmadı.",
 "RU HQ-9 404 URL'sinin canlı sayfaya 301'i (en hızlı RU kazanımı).",
 "Sonekli hattın 3.526 yazısına toplu Polylang dil ataması ve otomasyonda 'aynı konu var mı' kontrolü.",
 "Rank Math ayırıcı karakter + EN/ES/AR/RU başlık şablonundan Türkçe sloganın çıkarılması.",
 "T2'deki 30 revizyonun canlıya alınması (önce/sonra metinleri hazır).",
 "15 taslağın editör kontrolü, çeviri gruplaması ve takvime alınması; zamanlanmış EN S-80 ve Elbit yazılarının öne çekilmesi."]: w(f"- {t}")
w("\n## Büyüme havuzu notu\n")
w("Önceki '300 İspanyolca konu' listesi repoda ve WordPress'te bulunamadı; havuz bu teslimatta GSC verisi + envanter karşılaştırmasından kuruldu (Top100 mevcut sayfa: Excel 'Top100' sekmesi; yeni fırsatlar: T3). Liste paylaşılırsa aynı mükerrerlik kontrolünden geçirilip havuza eklenecek.")
open(sys.argv[1], "w").write("\n".join(o) + "\n"); print("ok", len(o))
