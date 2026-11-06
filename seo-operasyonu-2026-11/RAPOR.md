# Envanter Medya — Çok dilli GSC SEO operasyonu (ilk teslimat, 6 Kasım 2026)

Ayrıntılı tablolar: `ENVANTER_SEO_2026-11-06.xlsx` (sekmeler: Kapsam, T1–T5, Top100, Yayın takvimi önerisi). Taslak JSON'ları: `taslaklar/`.

## Veri kapsamı ve sınırlar

- GSC dosyası **son 24 saat** (05.11 06:00 → 06.11 05:00, UTC+3), Web arama. Toplam 1.628 tık / 144.112 gösterim / CTR %1,13. Bu rakamlar aylık hacim değildir; SINKEX 26 ve KAAN-1 haber zirveleri tabloyu şişiriyor.
- Sorgular sekmesi toplamın yalnız %27'sini (39.322 gösterim) gösteriyor (anonim sorgular). Sorgu ↔ sayfa eşleşmesi dosyada yok; eşleştirme URL dili + içerik başlık/slug eşleşmesiyle yapıldı.
- 28 gün / 3 ay GSC verisine erişim yok → bir sonraki adımda bu iki aralığın dışa aktarımı gerekli.
- WordPress: 17.932 yayımlanmış yazı + 3.093 CPT (sözlük, sistem, firma, fuar, sayfa) herkese açık REST ile; 322 taslak ve 3.600 zamanlanmış yazı yönetici uygulama parolasıyla (salt okuma) tarandı. Yazma işlemi yalnız 15 yeni taslak + 15 kapak görseli.

## Kritik teknik bulgular (onay gerektiren işler dahil)

- **İki ayrı yayın hattı aynı olayı iki URL'de yayımlıyor.** `es-…` önekli Polylang hattı ile `…-es` sonekli hat. Sonekli hattın **3.526 yazısının Polylang dili yok** (EN 1.273, AR 1.352, ES 441, RU 342, ZH 118). Örnek: Isaac Peral haberi EN'de 7.434 + 3.135 gösterime bölünmüş; hreflang grubu yanlış URL'de.
- **Otomasyon aynı konuyu tekrar üretiyor:** ES'de 14 'ejército más poderoso de Latinoamérica' URL'si, TR'de 7 'KAAN nedir' ve 7 'ASELSAN nedir', EN'de aynı gün 6 'F-22 nedir'. Zamanlanmış kuyrukta da tekrar var (TR S-80 iki kez).
- **Rank Math `%sep%` boş render ediliyor:** başlıklar '…SINKEX 26 Envanter Medya - Savunma Sanayii Haberleri' şeklinde çıkıyor. EN/ES/RU/AR başlıklarına Türkçe site sloganı ekleniyor (yerelleştirme hatası).
- **481 sözlük sayfasında meta açıklama boş;** otomatik açıklamalar bozuk Türkçe ('Geminin taşırdığı suyun ton cisminden hacmi'). 'X ne demek' sorgularında 5–10. sıra, ~0 tık.
- **RU'nun en çok gösterim alan URL'si 404:** HQ-9 sayfasının silinmiş '-2' kopyası 940 gösterim alıyor. Canlı sayfanın başlığında 'Долговременная' yanlış çeviri (doğrusu 'большой дальности').
- Birden çok sayfada çift H1 (ES SEMAR, ES S-80, EN/RU HQ-9). EN APFSDS sayfasında 'Image suggestions' ve 'An analogy for kids' gibi editoryal taslak başlıkları yayında.
- Zamanlanmış kuyrukta talebi **şimdi** olan içerikler aylar sonraya atanmış: EN S-80 açıklayıcısı 28.03.2027, Elbit profili 14.12.2026 → öne çekme önerisi.

## TABLO 1 — Dil bazlı SEO performansı (GSC son 24 saat + WordPress envanteri)

| Dil | GSC sayfa | Tıklama | Gösterim | CTR | Ort. konum | Yayında | Taslak | Zamanlanmış | Son 30 gün | Dil atanmamış | En güçlü konular | En büyük eksikler |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TR | 414 | 821 | 36.564 | %2.25 | 5.6 | 5.828 | 188 | 1.211 | 762 | 0 | TUSAŞ, KAAN’ın Yeni Prototipi KAAN-1’in  (35/2.491); Jandarma 2026 Memur Alımı: 30 Kadro, Baş (31/767) | KAAN/ASELSAN mükerrerleri; sözlükte 'ne demek' başlıkları; harç/ücret başlık uyumu |
| EN | 353 | 547 | 51.658 | %1.06 | 5.8 | 6.016 | 50 | 903 | 500 | 1.273 | KDF Recruitment 2026: Dates, Requirement (81/10.700); Spanish Navy submarine Isaac Peral (S-81 (31/7.434) | Ülke sayfalarında 'Ecuadorian/Tunisian army' ifadesi yok; HK416/SAR 56/MPT-55, BAE/Elbit/Fincantieri profilleri yok |
| ES | 66 | 102 | 6.356 | %1.6 | 4.6 | 1.673 | 17 | 514 | 468 | 441 | ¿Cuánto Gana un Marino de la SEMAR en 20 (13/834); El submarino Isaac Peral (S-81) hunde al (13/323) | Ülke dosyası yok; Indra/Naval Group profili, 'qué es un misil/fragata' yok; 14+5 mükerrer |
| AR | 52 | 74 | 3.455 | %2.14 | 5.1 | 2.930 | 44 | 957 | 592 | 1.352 | أقوى الجيوش في أفريقيا 2026: الترتيب الك (11/1.127); القوة العسكرية المصرية 2026: العدد والقد (6/209) | 'كم عدد الجيش …' sorgularına doğrudan cevap yok; genel radar/fırkateyn rehberi yok |
| RU | 65 | 95 | 4.720 | %2.01 | 6.8 | 1.215 | 19 | 15 | 382 | 342 | EDGE Спустила на Воду Второй Корвет BR71 (14/81); Программа ALTAY с 2007 по 2026 год: реше (5/23) | HQ-9 404 + yanlış çeviri; 'что такое БТР/корвет' yok |
| ZH | 2 | 2 | 2 | %100.0 | 2.5 | 270 | 4 | 0 | 40 | 118 | ASELSAN 电台与通信系统 (1/1); ASELSAN 通信系统与电台 (1/1) | Talep kanıtı yok (2 gösterim) — yeni ZH üretimi önerilmez |

Ülke grupları (gösterim): Türkiye 53.785 · İspanyolca konuşan ülkeler 10.812 (İspanya 4.497, Meksika 2.409, Arjantin 1.012, Şili 990) · Arap ülkeleri 9.684 · BDT 7.472 · diğer 61.384. Sorgu dili tahmini: EN 28.269, TR 8.922, ES 1.018, RU 754, AR 359 gösterim.

## TABLO 2 — Mevcut haber iyileştirmeleri (30)

Önce → sonra başlık/meta, içerik eklemeleri ve teknik işler Excel'de (T2). Canlı yazılar **değiştirilmedi**.

| # | Dil | Mevcut URL | Hedef sorgu | Gösterim | Tık | Konum | Sorun (özet) | Önerilen SEO başlığı | Öncelik / Karar |
|---|---|---|---|---|---|---|---|---|---|
| 1 | en | /en/en-spanish-navy-submarine-isaac-peral-sinks-infanta-elena-sinkex-26/ | spanish navy sinks infanta elena | 9.604 | 31 | 6.13 | Aynı olay için ikinci EN URL (84756, 3.135 gösterim, konum 3,2) var; iki sayfa birbirini yiyor. 84960 Polylang grubunda değil (hreflang yok), 84756 is… | Spanish Navy Sinks Infanta Elena: Isaac Peral S-81 Torpedo Shot | P1 · UPDATE + MERGE REVIEW |
| 2 | en | /en/en-kenya-defence-forces-recruitment-2026/ | kdf recruitment 2026 | 905 | 9 | 5.31 | 'Latest status — Updated 13 September 2026' başlığı 7 haftalık; '2026/2027', 'deadline', 'dates and centres pdf', 'online application' varyantları 9–1… | KDF Recruitment 2026/2027: Dates, Centres, Status and How to Apply | P1 · UPDATE + VERIFY |
| 3 | en | /en/en-kdf-recruitment-requirements/ | kdf recruitment 2026 requirements | 52 | 2 | 5.46 | Sayfa 2.105 gösterim, konum 8,5, CTR %0,3. Durum kutusu 13 Eylül'de kalmış; 'pdf' ve 'by category' varyantları zayıf.… | KDF Requirements 2026: Age Limit, KCSE Grade, Height by Category | P1 · UPDATE + VERIFY |
| 4 | en | /en/en-ecuador-military-inventory/ | ecuadorian army | 1.025 | 0 | 8.01 | 'ecuadorian army' sorgusunda 1.025 gösterim, 0 tık. Başlık 'Ecuador's Military Strength' kalıbında; 'Ecuadorian Army' ifadesi başlıkta/H1'de yok. Rank… | Ecuadorian Army 2026: Military Strength, Tanks, Aircraft, Navy | P1 · UPDATE |
| 5 | en | /en/en-tunisia-military-inventory/ | tunisian army | 899 | 0 | 5.64 | 'tunisian army' 899 gösterim, konum 5,6, 0 tık. Başlık sorgu ifadesini içermiyor; otomatik açıklama 303 karakter.… | Tunisian Army 2026: Military Strength, Tanks, Jets and Navy | P1 · UPDATE |
| 6 | en | /en/en-bolivia-military-inventory/ | bolivian army | 294 | 0 | 7.05 | 'bolivian army' 294 gösterim, 0 tık; aynı başlık kalıbı sorunu.… | Bolivian Army 2026: Military Strength, Tanks, Aircraft, Navy | P1 · UPDATE |
| 7 | en | /en/en-strongest-military-africa-2026/ | top 20 military in africa | 54 | 0 | 6.24 | Sayfa 1.039 gösterim, konum 5,3. 'top 20/top 50 military in africa' sorguları gelir ama tablo Top 15. Aynı niyette 3 EN URL daha var (en-strongest-arm… | Strongest Military in Africa 2026: Top 20 Ranking by Country | P1 · UPDATE + MERGE REVIEW |
| 8 | en | /en/aselsan-competitors/ | aselsan | 1.202 | 4 | 4.15 | Sayfa 725 gösterim, konum 3,0, 0 tık — 'aselsan' marka sorgusunda gösterim alıyor ama başlık 'competitors' niyetinde. EN'de ASELSAN hub sayfası belirs… | ASELSAN Competitors 2026: Thales, Leonardo, Elbit, Hensoldt | P1 · UPDATE |
| 9 | en | /en/en-what-is-apfsds-a-breakdown-of-modern-tank-ammunition/ | apfsds | 238 | 0 | 6.82 | Canlı sayfada 'Image suggestions' ve 'An analogy for kids' gibi editoryal taslak başlıkları yayında. Aynı niyette 2 EN URL daha var. 560 gösterim, 0 t… | What Is APFSDS? How Armour-Piercing Sabot Rounds Work | P1 · UPDATE + MERGE REVIEW |
| 10 | en | /en/en-what-is-hq-9-chinas-long-range-air-defense-system/ | hq-9 | 947 | 4 | 7.49 | İki EN HQ-9 açıklayıcısı var (15455 ve 15487 'HQ-9 what is it? A long-range air defense system of China' — makine çevirisi başlık). Sayfada iki H1, te… | HQ-9 Air Defence System: Range, Variants (HQ-9B, HQ-9BE), Users | P1 · UPDATE + MERGE REVIEW |
| 11 | tr | /kaan-1-prototipi-yetenekleri-gokvatan/ | tusaş kaan | 1.845 | 25 | 3.79 | Genel 'tusaş kaan' sorgusu bir haber sayfasına düşüyor; TR'de 7 ayrı 'KAAN nedir' sayfası var ve hiçbiri bu sorguda öne çıkmıyor. Haberde tek H2 ('İlg… | TUSAŞ KAAN-1 Prototipi: Açıklanan Yetenekler ve Son Durum | P1 · UPDATE |
| 12 | tr | /aselsan-nedir/ | aselsan nedir | 472 | 0 | 8.8 | 'aselsan nedir' + 'kısaca/ne iş yapar/ne üretiyor/ne demek' varyantları 6–9. sırada, ~0 tık. TR'de 7 ASELSAN-nedir URL'si var (savunma-sozluk/aselsan-… | ASELSAN Nedir, Ne İş Yapar? Kısaca Ürünleri ve Ortakları (2026) | P1 · UPDATE + MERGE REVIEW |
| 13 | tr | /silah-ruhsati-harclari/ | bulundurma ruhsat harcı 2026 | 81 | 0 | 1.0 | 1.012 gösterim, konum 6,4, CTR %0,6. 'bulundurma ruhsat harcı 2026' 1. sırada ama 0 tık → snippet cevabı veriyor ama başlık 'taşıma' öncelikli. Varyan… | Silah Ruhsatı Harcı 2026 Ne Kadar? Taşıma ve Bulundurma Tablosu | P1 · UPDATE |
| 14 | tr | /avcilik-belgesi-nasil-alinir/ | avcılık belgesi ücreti | 34 | 0 | 7.65 | 774 gösterim, konum 6,9; 'avcılık belgesi ücreti/harcı' sorguları 5–8. sırada. Ücret bilgisi açıklamada var ama başlık 'nasıl alınır' odaklı.… | Avcılık Belgesi Nasıl Alınır? 2026 Ücreti, Kurs ve Sınav | P1 · UPDATE |
| 15 | tr | /silah-ruhsati-yenileme/ | tüfek ruhsatı yenileme için gerekli belgeler 2026 | 45 | 0 | 6.07 | 661 gösterim, konum 6,3. Tüfek (yivsiz) yenileme belgeleri sorgularında 6–7. sıra; sayfada tüfek bölümü tek H2 altında.… | Silah ve Tüfek Ruhsatı Yenileme 2026: Gerekli Belgeler, Ücret | P1 · UPDATE |
| 16 | tr | /aselsan-mercan-100-denizalti-optronik-mast-euronaval-2026/ | aselsan gökdeniz / denizaltı | 1.271 | 5 | 4.03 | 1.271 gösterim, CTR %0,4. SEO title'da %sep% boş render ediliyor ('…Özellikleri Envanter Medya - Savunma…'). Başlık ürün adı odaklı, 'denizaltı perisk… | ASELSAN MERCAN 100: Denizaltı Optronik Mastı EURONAVAL'de | P1 · UPDATE |
| 17 | tr | /savunma-sozluk/deplasman-nedir/ | deplasman ne demek | 235 | 0 | 9.15 | 261 gösterim, konum 9,1, 0 tık. Meta açıklama boş; otomatik açıklama hatalı ve bozuk Türkçe ('Geminin taşırdığı suyun ton cisminden hacmi'). Başlıkta … | Deplasman Ne Demek? Gemilerde Deplasman Nedir, Nasıl Hesaplanır | P1 · UPDATE |
| 18 | tr | /savunma-sozluk/muhimmat-nedir/ | mühimmat ne demek | 172 | 0 | 5.02 | 235 gösterim, konum 5,2, 0 tık. Aynı sözlük şablonu sorunları (meta boş, başlıkta 'ne demek' yok, FAQ şeması yok).… | Mühimmat Ne Demek? Cephane ile Farkı ve Mühimmat Türleri | P1 · UPDATE |
| 19 | tr | /dunyanin-en-iyi-10-tabancasi-canik-zirvede-glock-sig-sauer-beretta-karsilastirmasi/ | en iyi tabanca markaları | 24 | 0 | 6.38 | 457 gösterim, CTR %0,7. H2'ler yalnızca '#10…#1' — içerik iskeleti anlamsız; 'en iyi tabanca markaları', 'türk tabanca markaları' niyetleri ayrışmıyor… | Dünyanın En İyi 10 Tabancası (2026): Canik, Glock, SIG Sauer | P1 · UPDATE |
| 20 | es | /es/cuanto-gana-marino-semar-2026/ | tabla de haberes sedena 2026 | 25 | 0 | 8.64 | 834 gösterim (ES'nin en çok gösterim alan sayfası). Aynı niyette 5 ES URL'si var (SEDENA/SEMAR maaş). Sayfada iki H1. Rank Math meta boş. Polylang dil… | ¿Cuánto gana un marino en México 2026? Tabla de sueldos SEMAR | P1 · UPDATE + MERGE REVIEW |
| 21 | es | /es/es-indra-prisma-s-radar-euronaval-2026/ | indra | 355 | 0 | 2.66 | 609 gösterim, konum 3,3, 0 tık. Marka sorgusu 'indra' bu habere düşüyor; ES'de Indra profil sayfası yok (yeni taslak hazırlandı). Haberde hiç H2 yok.… | Indra Prisma-S: el nuevo radar naval AESA presentado en Euronaval | P1 · UPDATE |
| 22 | es | /es/es-s80-isaac-peral-submarino-caracteristicas/ | clase s-80 plus | 19 | 0 | 11.47 | Isaac Peral haberi 'submarino' sorgusunda 392 gösterim alırken kalıcı S-80 rehberi konum 8,8'de (69 gösterim). Rehber 18 Ekim'den beri güncellenmedi; … | Submarino S-80 Plus (Isaac Peral): características y estado 2026 | P1 · UPDATE |
| 23 | es | /es/f-16-en-chile-cuantos-tiene-la-fach-de-donde-vinieron-y-que-papel-cumplen-2026/ | cuantos f16 tiene chile | 15 | 0 | 2.87 | 151 gösterim, 0 tık. Rank Math başlığı kelime ortasında kesilmiş ('…de dónde vinieron y'). Polylang dili atanmamış.… | ¿Cuántos F-16 tiene Chile? La flota de la FACh en 2026 | P1 · UPDATE |
| 24 | es | /es/ejercito-mas-poderoso-de-latinoamerica-ranking-2026/ | mejores ejércitos de latinoamérica 2026 | 2 | 1 | 1.5 | 213 gösterim, konum 4,6. Aynı niyette 3 ES URL'si (62984, 62781 es-…, ejercito-mas-poderoso-latinoamerica-ranking-militar-2026). Rank Math meta boş; d… | Ejércitos más poderosos de Latinoamérica 2026: ranking completo | P1 · UPDATE + MERGE REVIEW |
| 25 | es | /es/es-submarino-isaac-peral-hunde-infanta-elena-sinkex-26/ | submarino isaac peral | 54 | 1 | 1.02 | Aynı olay için ikinci ES URL (espana-s81-isaac-peral-submarino-hunde-buque-sinkex-26-es, 284 gösterim). %sep% boş render; Türkçe site sloganı. 'patrul… | El submarino Isaac Peral hunde al patrullero Infanta Elena | P1 · UPDATE + MERGE REVIEW |
| 26 | ar | /ar/ar-africa-strongest-armies-2026/ | اقوى جيش في افريقيا | 19 | 0 | 4.05 | AR'nin en güçlü sayfası (1.127 gösterim, konum 4,1, CTR %1). Aynı başlıkla ikinci AR URL'si (ar-strongest-army-africa-2026) ve 'لماذا تمتلك مصر أقوى ج… | أقوى جيش في أفريقيا 2026: ترتيب أقوى 15 جيشاً بالأرقام | P1 · UPDATE + MERGE REVIEW |
| 27 | ar | /ar/ar-egypt-military-strength-2026/ | كم عدد الجيش المصري 2026 | 13 | 1 | 1.92 | 209 gösterim, konum 5,9. 'كم عدد الجيش المصري / عدد افراد الجيش المصرى / تسليح الجيش المصري 2026' sorguları geliyor; başlık 'العدد' diyor ama ilk para… | كم عدد الجيش المصري 2026؟ الأفراد والتسليح والقدرات | P1 · UPDATE |
| 28 | ar | /ar/ar-morocco-algeria-military-comparison-2026/ | مقارنة عسكرية بين الجزائر والمغرب 2026 | 4 | 1 | 3.0 | 209 gösterim; aynı niyette ikinci AR URL (ar-morocco-vs-algeria-military-2026, 154 gösterim, konum 6,5). EN'de de ayrı sayfa var (en-morocco-vs-algeri… | مقارنة عسكرية بين الجزائر والمغرب 2026: من الأقوى؟ | P1 · UPDATE + MERGE REVIEW |
| 29 | ru | /ru/ru-hq-9-что-такое-долговременная-система-пр/ | HQ-9 (RU) | 940 | 4 | 7.59 | RU'nun en çok gösterim alan URL'si (940) '…-пр-2/' sonekli ve 404 dönüyor; canlı sayfa 15457. Başlık yanlış çeviri: 'Долговременная' (kalıcı/uzun süre… | ЗРК HQ-9: характеристики, дальность и операторы | P1 · UPDATE + VERIFY (teknik) |
| 30 | ru | /ru/ru-samyy-bystryy-istrebitel-v-mire/ | самый быстрый истребитель в мире | 47 | 0 | 6.34 | 240 gösterim, konum 6,9; anchor URL'leri ayrıca ~250 gösterim. Aynı niyette 'samye-bystrye-boevye-samolety-v-mire' (152 gösterim) var. Açıklamada 'Дан… | Самый быстрый истребитель в мире 2026: рейтинг по скорости | P1 · UPDATE + MERGE REVIEW |

## TABLO 3 — Yeni SEO haber/rehber fırsatları

Kalıcı içerik: 35 yeni/yeni açı fırsatı + 16 güncel haber adayı (İspanya Bakanlar Kurulu'nun 4 kalemi tek haberde birleştirildi → 13 ayrı haber). Toplam **48 ayrı makale fırsatı**; ayrıca 9 satır öne çekme/güncelleme/atlama kararıdır. Tümü yayında + taslak + zamanlanmış kuyruğa karşı kontrol edildi.

| Dil | Önerilen başlık | Hedef ülke | Ana sorgu | Talep kanıtı (24s) | Kaynak | Mükerrerlik kontrolü | Öncelik | Karar | Durum |
|---|---|---|---|---|---|---|---|---|---|
| en | HK416 Rifle Explained: Specs, Variants and Who Uses It | Global/UK/US | hk416 | hk416 55 @6,8; hk 416 19 @7,7 | heckler-koch.com, USMC/DGA duyuruları | EN'de 0 sayfa (6.016 EN yazı + sözlük tarandı) | P2 | NEW | **taslak yazıldı** |
| en | SAR 56: Sarsılmaz's 5.56 mm Assault Rifle Explained | Global | sar 56 | sar 56 106 @6,5; sar56 34 @8,6 | sarsilmaz.com ürün sayfası | EN'de yok; TR /sar-56-nedir-…/ var (hreflang) | P2 | NEW | **taslak yazıldı** |
| en | MPT-55: MKE's 5.56 mm National Infantry Rifle | Global | mpt 55 | mpt 55 71 @9,5 | mke.gov.tr | EN'de yok; TR /mpt-55-nedir/ var | P2 | NEW | **taslak yazıldı** |
| es | Indra: qué es, qué hace y quién es su propietario | España | indra | indra 355 @2,7; indra sistemas 32; noticias indra 41 @1,0 | indracompany.com, CNMV, SEPI | ES'de profil yok (yalnız haberler) | P2 | NEW | **taslak yazıldı** |
| es | Naval Group: qué es, qué hace y quién es su propietario | España/Chile/Brasil | naval group | naval group 91 @4,5 | navalgroup.com | ES'de profil yok (4 haber var) | P2 | NEW | **taslak yazıldı** |
| es | ¿Qué es un misil? Tipos, cómo funciona y diferencia con un cohete | España/LatAm | misil | misil 246 @3,6 (bir habere düşüyor) | Üretici sayfaları, Ministerio de Defensa | ES'de genel rehber yok (balístico/crucero haberleri var) | P2 | NEW | **taslak yazıldı** |
| es | Fuerzas Armadas de México 2026: efectivos, aviones, buques y presupuesto | México | fuerzas armadas de méxico | Meksika'dan 2.409 gösterim; SEDENA/SEMAR maaş sorguları | gob.mx/sedena, gob.mx/semar, DOF, IISS | Yayında/taslakta/zamanlanmışta ES México dosyası yok (EN/AR'de var) | P4 | NEW | **taslak yazıldı** |
| es | Fuerzas Armadas de Argentina 2026: F-16, Pampa III, Armada y Ejército | Argentina | fuerza aérea argentina | Arjantin'den 1.012 gösterim; 'fuerza aérea argentina', 'cuantos pampa 3 tiene argentina' | argentina.gob.ar/defensa, FAA, IISS | Zamanlanmış ES 84644 (10.11) yalnız Fuerza Aérea → taslak Ejército/Armada ağırlıklı NEW ANGLE olarak yazıldı | P4 | NEW ANGLE | **taslak yazıldı** |
| ru | Что такое БТР: устройство, назначение и известные модели | Rusya/BDT | бтр | бтр 72 @10,2 | Üretici sayfaları, STANAG 4569 | RU'da tanım sayfası yok (yalnız BTR-4 görüş yazısı) | P2 | NEW | **taslak yazıldı** |
| ru | Что такое корвет и чем он отличается от фрегата | Rusya/BDT | корвет | корвет 38 @8,55 (12 tık habere); карвет 9 | Donanma/tersane kaynakları | RU'da tanım yok; 13 korvet haberi var (iç link) | P2 | NEW | **taslak yazıldı** |
| tr | İHA ve SİHA'larda termal iz yönetimi nedir? | Türkiye | iha siha termal iz yönetimi | 23 @28 (sayfa yok) | Akademik/kurumsal yayınlar | TR'de yok | P4 | NEW | **taslak yazıldı** |
| es | Fuerzas Armadas de Chile 2026 (ficha país) | Chile | fuerzas armadas de chile | Şili 990 gösterim; 'cuantos f16 tiene chile' | FACh, Armada de Chile, IISS | Zamanlanmış: es-inventario-fuerza-aerea-chile (15.11, yalnız hava kuvveti) → tüm kuvvetler NEW ANGLE | P4 | NEW ANGLE | havuz |
| es | Fuerzas Armadas de Perú 2026 (ficha país) | Perú | fuerzas armadas del perú | Peru 406 gösterim; F-16 Block 70 haberleri | mindef.gob.pe, FAP, IISS | Zamanlanmış: es-inventario-fuerza-aerea-peru (16.11, yalnız hava) → tüm kuvvetler NEW ANGLE | P4 | NEW ANGLE | havuz |
| es | Fuerzas Armadas de Colombia 2026 (ficha país) | Colombia | fuerzas militares de colombia | Gripen/Black Hawk ES sayfaları gösterim alıyor | mindefensa.gov.co, IISS | Zamanlanmış: es-inventario-fuerza-aerea-colombiana (08.11, yalnız hava) → tüm kuvvetler NEW ANGLE | P4 | NEW ANGLE | havuz |
| es | Fuerzas Armadas de Ecuador 2026 (ficha país) | Ecuador | fuerzas armadas del ecuador | 'ecuadorian army' 1.025 @8,0 (EN); Ekvador 242 gösterim | midena.gob.ec, IISS | Zamanlanmış: es-inventario-fuerzas-armadas-ecuador (11.11) → aynı niyet | P5 | SKIP (zamanlanmış) | havuz |
| es | Fuerzas Armadas de Venezuela 2026 (ficha país) | Venezuela | fuerza armada nacional bolivariana | Venezuela 284 gösterim; 'venezuela military strength' | IISS, SIPRI | Zamanlanmış: es-inventario-militar-venezuela (12.11) → aynı niyet | P5 | SKIP (zamanlanmış) | havuz |
| es | Fuerzas Armadas de España 2026: efectivos, flota y presupuesto | España | fuerzas armadas españolas | İspanya 4.497 gösterim; 'armada española', 'spanish navy' 148 | defensa.gob.es, armada.defensa.gob.es | Zamanlanmış: es-inventario-ejercito-del-aire-espana (14.11, yalnız hava) → Armada+Ejército NEW ANGLE | P4 | NEW ANGLE | havuz |
| es | Patrullero Infanta Elena (P-76): historia del buque hundido en el SINKEX 26 | España | patrullero infanta elena | 91 @4,4 | armada.defensa.gob.es | Yeni URL yerine mevcut ES haberine bölüm olarak eklenmeli | P5 | NEW ANGLE → mevcut habere ekle | havuz |
| en | What Is a Helicopter Carrier? LHD, LHA and Light Carriers Explained | Global | helicopter carrier | 82 @9,7 (ülke sıralaması sayfası alıyor) | Donanma kaynakları | EN'de tanım sayfası yok; sıralama sayfası farklı niyet | P2 | NEW ANGLE | havuz |
| en | İMECE: Türkiye's Earth-Observation Satellite Explained | Global | imece | 14 @4,9 | TÜBİTAK UZAY, SSB | EN'de yok; TR'de 3 URL (TR'de de MERGE REVIEW) | P4 | NEW | havuz |
| en | Bistatic and Passive Radar Explained | Global | bistatic radar | 16 @3,4 | Akademik/üretici | EN'de yok | P4 | NEW | havuz |
| en | Syrian Navy 2026: Ships and Status | MENA | syrian navy | 14 @3,9 | IISS | EN'de yok | P5 | NEW | havuz |
| ar | ما هو الصاروخ؟ أنواع الصواريخ العسكرية وكيف تعمل | MENA | صاروخ | 63 @2,1 (Exocet haberine düşüyor) | Üretici kaynakları | AR'de genel tanım yok (balistik ve kruz alt sayfaları var) | P2 | NEW | havuz |
| ar | كم عدد الجيش العراقي 2026؟ (mevcut sayfaya başlık/ilk paragraf) | Irak | كم عدد الجيش العراقي 2026 | 4 @4,75 + 1 @3 | IISS | /ar/ar-iraq-military-strength-2026/ var | P1 | UPDATE (yeni URL değil) | havuz |
| ar | كم عدد الجيش الأردني 2026؟ (mevcut sayfaya) | Ürdün | كم عدد الجيش الاردني 2026 | 2 @3,5 | IISS | /ar/ar-jordan-military-strength-2026/ var | P1 | UPDATE | havuz |
| tr | F-35 fiyatı ne kadar? Lot bazında birim maliyet | Türkiye | f35 fiyatı | 16 @5,4 | F-35 JPO / Lockheed Martin lot duyuruları | TR'de yok | P2 | NEW | havuz |
| tr | Askerî helikopter fiyatları 2026 | Türkiye | helikopter fiyatları 2026 | 12 @3,7 | Resmî FMS/DSCA bildirimleri | TR'de yok; EN 'most expensive helicopters' var (NEW ANGLE) | P4 | NEW | havuz |
| tr | Pedestal nedir? (Savunma Sözlüğü) | Türkiye | pedestal nedir | 25 @6,8 | Üretici dokümanları | Sözlükte yok; ALTINAY haberi gösterim alıyor | P2 | NEW | havuz |
| tr | Komuta ne demek? (Savunma Sözlüğü) | Türkiye | komuta ne demek | 12 @1,0 | TDK, askerî terim sözlükleri | Sözlükte yok; 'komuta-kontrol nedir' yazısı var | P2 | NEW | havuz |
| tr | Hipersonik füzelerde termal koruma nasıl sağlanır? | Türkiye | hipersonik termal koruma | 13 @10,2 | Akademik/kurumsal | TR'de yok | P4 | NEW | havuz |
| ru | Новости Польши: армия и ВПК (тематическая страница) | Polonya/BDT | новости польши | 23 @1,0; польша новости 23 @1,0; польша 23 | — | 24 RU Polonya haberi var; hub/etiket sayfası yok | P4 | NEW (hub) | havuz |
| zh | — | Çin | — | ZH: 2 gösterim (son 24 saat) | — | 270 ZH içerik; talep kanıtı yok → yeni ZH içerik üretilmemeli | P5 | SKIP | havuz |
| en | BAE Systems: What It Makes, Revenue and Key Programmes | Global/UK | bae systems | 164 @4,6 | baesystems.com yıllık rapor | EN'de profil yok (yalnız haberler) | P2 | NEW | havuz |
| en | Elbit Systems: Company Profile, Products and Exports | Global | elbit systems | 149 @5,3; elbit 27 @4,1 | elbitsystems.com yıllık rapor | EN profil 14.12.2026'ya zamanlanmış (ID 72185) → talep şimdi var, yayını öne çek | P2 | RESCHEDULE | havuz |
| en | Fincantieri: Italy's Shipbuilder Explained | Global | fincantieri | 98 @2,2 | fincantieri.com | EN'de profil yok | P2 | NEW | havuz |
| en | Airbus Defence and Space: Divisions and Programmes | Global | airbus defence and space | 12 @6,7; airbus 132 @2,7 | airbus.com | EN'de profil yok | P4 | NEW | havuz |
| es | ¿Qué es una fragata? Diferencias con corbeta y destructor | España/LatAm | fragata | fragata 21 @2,1; corbeta 21 @2,1 | Armada Española, Navantia | ES'de genel tanım yok (yayın+taslak+zamanlanmış); haber sayfaları sıralanıyor | P2 | NEW | havuz |
| en | Corvette vs Frigate vs Destroyer: What's the Difference? | Global | corvettes / destroyer | corvettes 30 @4,6; destroyer 16 @1,8 | Donanma kaynakları | EN'de genel karşılaştırma yok (yalnız MİLGEM korvet sayfası) | P2 | NEW | havuz |
| en | What Is Radar and How Does It Work? (AESA, PESA, bands) | Global | radar | radar 106 @6,4 | Üretici/akademik | EN'de yalnız ürün bazlı radar açıklayıcıları var | P2 | NEW | havuz |
| ar | ما هو الرادار العسكري وكيف يعمل؟ | MENA | رادار | 10 @4,9 | Üretici/akademik | AR'de yalnız ürün bazlı radar sayfaları var | P2 | NEW | havuz |
| ar | ما هي الفرقاطة؟ الفرق بين الفرقاطة والكورفيت والمدمرة | MENA | فرقاطة | 13 @6,8 | Donanma kaynakları | AR'de genel tanım yok | P2 | NEW | havuz |
| ar | أنواع المروحيات العسكرية ومهامها | MENA | مروحية | 7 @1,4 | Üretici kaynakları | AR'de genel rehber yok | P4 | NEW | havuz |
| en | What Is the S-80 Submarine? (zamanlanmış 26215 — 28.03.2027) | İspanya/Global | isaac peral (s-81) | isaac peral (s-81) 51 @2,9; spanish navy sinks infanta elena 9.604; submarine 885 @2,0 | Navantia, Armada | EN açıklayıcı Mart 2027'ye zamanlanmış; talep şimdi | P1 | RESCHEDULE (öne çek, SINKEX haberine bağla) | havuz |
| ar | ما هي الغواصة S-80؟ (zamanlanmış 26217 — 28.03.2027) | MENA | S-80 | SINKEX 26 ilgisi | Navantia | AR açıklayıcı Mart 2027'ye zamanlanmış | P3 | RESCHEDULE | havuz |
| es,en | Spain authorises €2.3 billion programme for robust positioning, navigation and timing (PNT) systems for its armed forces | Spain | haber (2026-11-03) | güncel gelişme | La Moncloa – Referencia del Consejo de Ministros, 3 Nov 2026 (Defensa section) | eksik: tr,en,es,ar,ru | P3 | NEW | **taslak yazıldı** |
| es,en | Spain approves €1.438 billion programme to modernise Air and Space Force aircraft | Spain | haber (2026-11-03) | güncel gelişme | La Moncloa – Referencia del Consejo de Ministros, 3 Nov 2026 | eksik: tr,en,es,ar,ru | P3 | NEW | **taslak yazıldı** |
| es,en | Spain authorises €269 million framework agreement for extended-range 155 mm artillery ammunition | Spain | haber (2026-11-03) | güncel gelişme | La Moncloa – Referencia del Consejo de Ministros, 3 Nov 2026 | eksik: tr,en,es,ar,ru | P3 | NEW | **taslak yazıldı** |
| es,en | Spain adds €38 million to Navy MH-60R Seahawk programme; first helicopter still due by end-2026 | Spain | haber (2026-11-03) | güncel gelişme | La Moncloa – Referencia del Consejo de Ministros, 3 Nov 2026 | eksik: tr,en,es,ar,ru | P3 | NEW | **taslak yazıldı** |
| es,en | Spanish Air and Space Force wraps up its largest exercise of 2026, Sirio-Dragón-Tormenta 26: 278 sorties, 2,500+ personnel | Spain | haber (2026-11-04) | güncel gelişme | Infodefensa | eksik: tr,en,es,ar,ru | P3 | NEW | havuz |
| es,en | Spain awards €3.6 million R&D contract for a national fuel cell for the S-80 submarines' AIP | Spain | haber (2026-11-05) | güncel gelişme | Infodefensa | eksik: tr,en,es,ar,ru | P3 | VERIFY | havuz |
| es,en | Peru's Congress approves funds for first payment on second batch of 12 F-16 Block 70 fighters | Peru | haber (2026-11-01) | güncel gelişme | Infodefensa | eksik: es,en,tr,ar,ru | P3 | NEWS UPDATE | havuz |
| es,en | Peru awards Leonardo €40.4 million to support the Air Force's four C-27J Spartans | Peru | haber (2026-11-02) | güncel gelişme | Infodefensa | eksik: tr,en,es,ar,ru | P3 | VERIFY | havuz |
| ar,en,tr,es,ru | Türkiye's parliament ratifies the Makkah Joint Defence Agreement with Saudi Arabia and Pakistan | Türkiye, Saudi Arabia, Pakistan | haber (2026-11-05) | güncel gelişme | Arab News (Reuters reporting) | eksik: tr,en,ar,es,ru | P3 | NEWS UPDATE | **taslak yazıldı** |
| ar,en,tr | Saudi Arabia and Syria sign a defence cooperation agreement in Riyadh | Saudi Arabia, Syria | haber (2026-11-04) | güncel gelişme | Asharq Al-Awsat (English) | eksik: tr,en,es,ar,ru | P3 | VERIFY | havuz |
| ar,en,es | Saudi air defences intercept Houthi ballistic missile fired towards Madinah region | Saudi Arabia, Yemen | haber (2026-11-05) | güncel gelişme | Asharq Al-Awsat (English) | eksik: tr,en,es,ar,ru | P3 | VERIFY | havuz |
| ru,en,tr | Poland tenders multi-year support to keep its Soviet-origin Kub and Osa air defence systems operational | Poland | haber (2026-11-06) | güncel gelişme | Defence24.pl | eksik: tr,en,es,ar,ru | P3 | VERIFY | havuz |
| ru,en,tr | Romania and Moldova launch their first joint military procurement: 62 IVECO trucks for the Moldovan Army | Romania, Moldova | haber (2026-11-02) | güncel gelişme | Romanian Ministry of National Defence (MApN) press release | eksik: tr,en,es,ar,ru | P3 | NEW | **taslak yazıldı** |
| en,es,ar,ru | ASELSAN signs $1.1 billion air defence export contract with an undisclosed international customer | Türkiye | haber (2026-11-03) | güncel gelişme | KAP – ASELSAN disclosure (New Business Relation) | eksik: en,es,ar,ru | P3 | NEW | **taslak yazıldı** |
| en,ar,es,ru | Türkiye's defence and aerospace exports jump 61% in October 2026 to $1.14 billion | Türkiye | haber (2026-11-03) | güncel gelişme | Anadolu Agency (via Foreks), quoting SSB President Haluk Görgün | eksik: en,es,ar,ru | P3 | NEW | havuz |
| en | MKE presents TOLGA 20mm Dual naval close-in gun system at Euronaval 2026 after first warship firing | Türkiye | haber (2026-11-05) | güncel gelişme | Naval News | eksik: en | P3 | NEW | havuz |

## TABLO 4 — Mükerrer içerik

Hiçbir URL silinmedi, yönlendirilmedi veya birleştirilmedi; aşağıdakiler onay bekleyen önerilerdir.

| Dil | URL 1 | URL 2 | Benzerlik | Arama niyeti | Önerilen işlem |
|---|---|---|---|---|---|
| en | /en/en-spanish-navy-submarine-isaac-peral-sinks-infanta-elena-sinkex-26/ (7.434 gös., 31 tık, konum 7,1) | /en/spain-s81-isaac-peral-submarine-sinks-target-ship-sinkex-26-en/ (3.135 gös., 13 tık, konum 3,2) | Aynı olay, iki hat (önekli Polylang + sonekli dil atanmamış) | Haber: SINKEX 26 Isaac Peral | 84960 ana; 84756 canonical→84960, hreflang grubunu 84960'a taşı (onay) |
| es | /es/es-submarino-isaac-peral-hunde-infanta-elena-sinkex-26/ (323 gös., 13 tık) | /es/espana-s81-isaac-peral-submarino-hunde-buque-sinkex-26-es/ (284 gös., 1 tık) | Aynı olay | Haber: SINKEX 26 | 84958 ana; sonekli kopya canonical (onay) |
| en | /en/en-what-is-hq-9-chinas-long-range-air-defense-system/ (15455) | /en/en-hq-9-what-is-it-a-long-range-air-defense-system-of-china/ (15487) | Aynı gün üretilmiş iki açıklayıcı | HQ-9 nedir | 15455 ana; 15487 canonical/301 (onay) |
| ru | /ru/ru-hq-9-что-такое-…-пр/ (15457, canlı) | /ru/ru-hq-9-что-такое-…-пр-2/ (404, 940 gös.) | Silinmiş kopya hâlâ gösterim alıyor | HQ-9 что такое | 404 URL'yi 15457'ye 301 (onay) — RU'da en hızlı kazanım |
| en | /en/en-what-is-the-f-22-raptor-americas-5th-gen-air-superiority-fighter/ (48568) | 48567, 48571, 48575, 48576, 48577 (aynı gün 6 URL) | Başlıklar neredeyse aynı (Jaccard ≥0,8) | What is the F-22 Raptor | Tek URL seç; diğer 5'i canonical/301 (onay). Otomasyonda tekrar üretimi durdur |
| en | /en/what-is-k9-thunder-self-propelled-howitzer-explained/ (15137) | /en/k9-thunder-explained/ (16554), /en/en-what-is-k9-thunder-the-story-…/ (16544) | 3 açıklayıcı | K9 Thunder nedir ('samsung k9 thunder' 49 gös., konum 8,5) | 15137 ana; diğer 2 canonical (onay) |
| en | /en/en-what-is-apfsds-a-breakdown-of-modern-tank-ammunition/ (560 gös.) | /en/en-what-is-an-apfsds-shell-…/ (70 gös.), /en/en-what-is-apfsds/ | 3 açıklayıcı aynı gün | What is APFSDS | 21865 ana (en çok gösterim); diğer 2 canonical |
| en | /en/en-strongest-military-africa-2026/ (1.039 gös.) | /en/en-strongest-army-africa-2026/ (118), /en/en-africas-strongest-militaries-2026/ (80), /en/en-why-egypt-strongest-military-africa/ | Aynı sıralama niyeti | Strongest military in Africa | 67765 ana; 'why Egypt' farklı açı (NEW ANGLE) kalabilir, diğer 2 canonical |
| en | /en/bayraktar-tb2-baykar-en/ (370 gös., konum 1,2) | /en/what-is-bayraktar-tb2-turkish-combat-drone-explained/ | Aynı açıklayıcı niyet | What is Bayraktar TB2 | Biri ana seçilmeli; ikisi de dil atanmamış |
| en | /en/bayraktar-akinci-specifications-operators/ (50 gös.) | /en/en-what-is-bayraktar-akinci-turkiye-heavy-strike-drone/ (78 gös.) | Aynı ürün açıklayıcısı | What is AKINCI | Specs + 'what is' tek sayfada birleşsin |
| en | /en/en-kenya-defence-forces-recruitment-2026/ (10.700 gös.) | /en/en-next-kdf-recruitment-date/, /en/en-is-there-kdf-recruitment-2026/ | 'when/is there' alt niyetleri ana sayfa ile çakışıyor | KDF recruitment 2026 status | Ana sayfa korunur; alt sayfalar farklı soru odaklı kalabilir ama 'latest status' kutusu yalnız ana sayfada; iç linkle bağla |
| en | /en/europe-strongest-armies-2026-russia-france-turkey/ | /en/nato-strongest-armies-2026-usa-france-turkey/ | Kısmi örtüşme | Europe vs NATO ranking | SKIP — farklı kapsam (Avrupa ≠ NATO); iç link yeterli |
| tr | /aselsan-nedir/ (1.250 gös., konum 8,0) | /savunma-sozluk/aselsan-nedir/ (391), /aselsan-nedir-ne-is-yapar/ (canonical→/aselsan-nedir/ ✓), /aselsan-nedir-ne-is-yapar-ne-uretiyor/, /aselsan-savunma-nedir/ | 5 URL aynı soru | ASELSAN nedir | 3457 ana; sözlük kaydı kısa tanım + ana rehbere link; diğer 2 post canonical (onay) |
| tr | /kaan-nedir/ (hub) | /kaan-ucagi-nedir/, /kaan-nedir-turkiye-milli-muharip-ucagi/, /kaan-nedir-ne-ise-yarar-…/, /kaan-milli-muharip-ucak/ | 5 'KAAN nedir' yazısı | KAAN nedir | /kaan-nedir/ hub; diğerleri canonical (onay). 'tusaş kaan' sorgusu şu an haber sayfasına düşüyor |
| tr | /aselsan-kimin-sahibi/ (465 gös.) | /aselsan-devletin-mi-ozel-sirket-mi/ (162), /aselsan-kimin-devletin-mi/ | Aynı soru | ASELSAN kimin, devletin mi | 40904 ana; diğerleri canonical |
| tr | /aselsan-ne-zaman-neden-kuruldu/ (198 gös.) | /aselsan-ne-zaman-ve-neden-kuruldu/ (aynı başlık), /aselsan-ne-zaman-kuruldu-tarihcesi/ | Birebir aynı başlık | ASELSAN ne zaman kuruldu | Tek URL; diğerleri canonical |
| tr | /aselsan-fabrikalari-yerleskeleri/ (263 gös.) | /aselsan-nerede-merkez-fabrikalari/ (123), /aselsan-nerede-merkez-kampusler/ | Aynı soru | ASELSAN nerede | 41092 ana |
| tr | /aselsan-maaslari-2026/ (1.519 gös.) | /aselsan-maaslari-2026-2/, /aselsan-maaslari/ (2025), /aselsan-muhendis-maaslari-2026-…/ | Aynı yıl, aynı soru | ASELSAN maaşları 2026 | 22991 ana; '-2' canonical; mühendis maaşı alt niyet olarak kalabilir |
| tr | /tusas-maaslari-2026-muhendis-teknisyen-ve-isci-ucretleri-ne-kadar/ (312) | /tusas-maaslari-2026/ (110) — birebir aynı başlık | Aynı başlık | TUSAŞ maaşları 2026 | 10277 ana |
| tr | /aselsan-mulakat-sureci-asamalari/ | /aselsan-is-basvurusu-mulakat-sureci/, /aselsan-is-basvurusu-mulakat/ | Aynı süreç | ASELSAN mülakat | Tek rehber |
| tr | /silah-ruhsati-nasil-alinir/ (156) | /silah-bulundurma-ruhsati-nasil-alinir/ (195) | Kısmi (bulundurma alt niyet) | Silah ruhsatı nasıl alınır | SKIP — alt niyet ayrı; karşılıklı link |
| tr | /sar9-nedir-ozellikleri/ (204) | /sar9-nedir-ozellikleri-teknik-verileri/ (35) | Aynı ürün | SAR9 nedir | 73533 ana |
| es | /es/cuanto-gana-marino-semar-2026/ (834) | /es/es-sueldo-sedena-semar-mexico-2026/ (463), /es/cuanto-gana-soldado-sedena-2026/ (250), /es/es-sueldo-soldado-mexico-sedena-semar-2026/ (91), /es/cuanto-gana-un-soldado-en-mexico-sueldos-sedena-semar-2026/ | 5 URL; ikisi SEMAR+SEDENA birlikte | Sueldos SEMAR / SEDENA 2026 | İki ana sayfa: SEMAR (63220) + SEDENA (63103); 'SEDENA y SEMAR' karma 3 URL canonical (onay) |
| es | /es/ejercito-mas-poderoso-de-latinoamerica-ranking-2026/ (213) | /es/es-ejercito-mas-poderoso-latinoamerica-ranking-2026/ (64), /es/ejercito-mas-poderoso-latinoamerica-ranking-militar-2026/ (39) | 14 ES URL aynı başlık/niyet (64191, 64986, 65952, 66480, 66891, 67185, 67451, 68228 … — 2–23 Eylül arası otomasyon tekrarları) | Ranking militar Latinoamérica | 62984 ana (213 gös.); diğer 13 canonical/301 (onay). Otomasyonda aynı konu kontrolü |
| es | /es/navantia-que-es-que-hace-y-quien-es-su-propietario-perfil-2026/ (105) | /es/es-navantia-que-es-propietario/ (60) | Aynı profil | Navantia qué es | Biri ana (105 gösterimli) |
| es | /es/ia-63-pampa-iii-caracteristicas-historia-modernizacion-argentina/ (169) | /es/pampa-iii-avion-entrenador-argentino-caracteristicas-programa-2026/ | Aynı ürün | Pampa III | Birincisi ana |
| ar | /ar/ar-africa-strongest-armies-2026/ (1.127) | /ar/ar-strongest-army-africa-2026/ | Aynı sıralama | أقوى جيش في أفريقيا | 66932 ana |
| ar | /ar/ar-morocco-algeria-military-comparison-2026/ (209) | /ar/ar-morocco-vs-algeria-military-2026/ (154) | Aynı karşılaştırma | المغرب والجزائر مقارنة | 57406 ana |
| ar | /ar/ar-saudi-arabia-military-strength-2026/ (164) | /ar/ar-saudi-military-strength-2026/ — birebir aynı başlık | Aynı başlık | القوة العسكرية السعودية | 66652 ana |
| ru | /ru/ru-samyy-bystryy-istrebitel-v-mire/ (240+anchor) | /ru/samye-bystrye-boevye-samolety-v-mire/ (152) | Aynı sıralama niyeti | Самый быстрый истребитель | 72671 ana |
| ru | /ru/что-такое-баллистическая-ракета-как-о-ru/ (112) | /ru/ballisticheskaya-raketa/ (55) | Aynı tanım | Баллистическая ракета это | Biri ana |
| ru | /ru/chto-takoe-radar/ (215) | /ru/chto-takoe-radar-aesa/ | Kısmi (AESA alt konu) | Что такое радар | SKIP — AESA ayrı niyet; karşılıklı link |
| en | /en/kf-21-boramae-what-is-south-korea-fighter/ (28255) | /en/what-is-kf-21-boramae-korean-fighter-explained/ (15307) | İki açıklayıcı | What is KF-21 Boramae | Biri ana; diğeri canonical |
| es | /es/es-s80-isaac-peral-submarino-caracteristicas/ (64254) | /es/s-80-isaac-peral-el-submarino-espanol-con-propulsion-aip-que-renueva-la-armada/ (63615) | Aynı ürün rehberi | Submarino S-80 | 64254 ana |
| tr | /sar-56-nedir-ozellikleri-teknik-verileri/ (212 gös.) | /sar-56-nedir/ | Aynı ürün açıklayıcısı | SAR 56 nedir | 67126 ana (GSC gösterimi olan); diğeri canonical |
| en | /en/rocket-vs-missile-difference/ | /en/en-rocket-vs-missile-difference/ | Aynı başlık niyeti, iki hat | Rocket vs missile | Biri ana; diğeri canonical |
| tr | ZAMANLANMIŞ 26740 'Navantia S-80 Plus Denizaltısı Nedir?' (12.11.2026) | ZAMANLANMIŞ 26213 'S-80 Denizaltısı Nedir?' (23.04.2027) | Kuyrukta aynı niyet iki kez | S-80 nedir (TR) | 26213'ü kuyruktan çıkar/taslağa al (onay) — 26740 yeterli |

## TABLO 5 — WordPress taslakları (15)

Hepsi `draft`, dil atanmış, kapak = Envanter başlık kartı (gerçek fotoğraf ya da yapay zekâ görseli değil). Polylang çeviri grubuna **bağlanmadı**: grupta meta/kapak eşitlemesi yayındaki eşdeğer sayfaları değiştirebileceği için gruplama yayın anında editörde.

| Dil | Makale başlığı | Post ID | URL | Durum | Hedef sorgu | Kaynak doğrulaması |
|---|---|---|---|---|---|---|
| en | HK416 Explained: Heckler & Koch's Piston-Driven 5.56 mm Assault Rifle | 84997 | https://envantermedya.com/wp-admin/post.php?post=84997&action=edit | draft | hk416 | 12 kaynak; Heckler & Koch – HK416 product page (overview, variants, compare); Heckler & Koch – HK417 product page; Heckl |
| en | MPT-55 Rifle: MKE's 5.56 mm National Infantry Rifle Explained | 84999 | https://envantermedya.com/wp-admin/post.php?post=84999&action=edit | draft | mpt 55 | 5 kaynak; MKE – Small Arms catalogue (2025); CNN Türk / Anadolu Agency – 'Hassas görevlerin güçlü silahı MPT-55' (22 Aug |
| en | SAR 56 Rifle: Sarsılmaz's 5.56 mm Infantry Rifle Explained | 85001 | https://envantermedya.com/wp-admin/post.php?post=85001&action=edit | draft | sar 56 | 9 kaynak; Sarsılmaz – SAR 56 14.5" product page; Sarsılmaz – SAR 56 11" product page; Sarsılmaz – SAR 56 7.5" product pa |
| ru | Что такое БТР: устройство, назначение и известные модели бронетранспортёров | 85003 | https://envantermedya.com/wp-admin/post.php?post=85003&action=edit | draft | бтр | 8 kaynak; ARTEC GmbH — BOXER Armoured Personnel Carrier brochure (03/2025); Patria — Patria AMV XP product page; General |
| ru | Что такое корвет: чем корвет отличается от фрегата и эсминца | 85005 | https://envantermedya.com/wp-admin/post.php?post=85005&action=edit | draft | корвет | 9 kaynak; Naval News — Turkish Navy Ada-class corvette called in France for the first time (11/2023); Baird Maritime — V |
| tr | İHA ve SİHA'larda termal iz yönetimi nedir? Kızılötesi imza nasıl azaltılır? | 85007 | https://envantermedya.com/wp-admin/post.php?post=85007&action=edit | draft | iha siha termal iz yönetimi | 6 kaynak; Kelly, L. C. (Defence Science & Technology Group, Australia) — Low-Emissivity Topcoats for the Reduction of Th |
| es | Fuerzas Armadas de Argentina 2026: Ejército, Armada, Fuerza Aérea y presupuesto | 85009 | https://envantermedya.com/wp-admin/post.php?post=85009&action=edit | draft | fuerzas armadas argentinas 2026 | 15 kaynak; Ministerio de Defensa (21-08-2026) – LOA por 235 Stryker; Ministerio de Defensa (20-12-2024) – primer escuadr |
| es | Fuerzas Armadas de México 2026: efectivos, aviones, buques y presupuesto | 85011 | https://envantermedya.com/wp-admin/post.php?post=85011&action=edit | draft | fuerzas armadas de mexico 2026 | 12 kaynak; Cámara de Diputados – Presupuesto de Egresos de la Federación 2026 (DOF 21-11-2025); Ley de la Guardia Nacion |
| es | Indra: qué es, qué hace y quién es su propietario (2026) | 85013 | https://envantermedya.com/wp-admin/post.php?post=85013&action=edit | draft | indra | 13 kaynak; Indra Group – Comunicado de resultados del ejercicio 2025 (25/02/2026); Indra Group – Comunicado de resultado |
| es | Naval Group: qué es, qué hace y quién es su propietario | 85015 | https://envantermedya.com/wp-admin/post.php?post=85015&action=edit | draft | naval group | 13 kaynak; Naval Group – Gouvernance / Actionnariat; Naval Group – Discover the group; Naval Group – History; Naval Grou |
| es | ¿Qué es un misil? Tipos, cómo funciona y diferencia con un cohete | 85017 | https://envantermedya.com/wp-admin/post.php?post=85017&action=edit | draft | misil | 12 kaynak; Arms Control Association – Missile Defense Systems at a Glance; NASIC / DIBMAC – Ballistic and Cruise Missile |
| es | El Consejo de Ministros autoriza 2.302 millones para dotar a las Fuerzas Armadas de capacidad PNT robusta | 85019 | https://envantermedya.com/wp-admin/post.php?post=85019&action=edit | draft | consejo de ministros defensa 3 noviembre 2026 PNT | 5 kaynak; La Moncloa – Referencia del Consejo de Ministros, 3 de noviembre de 2026; Infodefensa – PNT; Infodefensa – aer |
| ar | البرلمان التركي يصادق على اتفاقية مكة للدفاع المشترك مع السعودية وباكستان | 85021 | https://envantermedya.com/wp-admin/post.php?post=85021&action=edit | draft | البرلمان التركي يصادق على اتفاقية مكة للدفاع المشترك | 4 kaynak; TBMM (official) – 'Mekke Anlaşması'nın onaylanmasının uygun bulunduğuna dair kanun teklifi TBMM Genel Kurulund |
| en | ASELSAN Signs $1.1 Billion Air Defence Export Contract With an Undisclosed Customer | 85023 | https://envantermedya.com/wp-admin/post.php?post=85023&action=edit | draft | aselsan 1.1 billion air defense export | 2 kaynak; KAP – ASELSAN 'New Business Relation' disclosure, 03.11.2026 10:07:49; Türkiye Today |
| ru | Румыния и Молдова впервые провели совместную военную закупку: 62 грузовика IVECO для Национальной армии | 85025 | https://envantermedya.com/wp-admin/post.php?post=85025&action=edit | draft | Молдова IVECO грузовики Румыния совместная закупка | 2 kaynak; MApN (Ministerul Apărării Naționale) – joint procurement press release, 2 Nov 2026; MApN – Oprea–Nosatîi meeti |

Her taslağın `verification_notes` alanında editörün yayın öncesi kontrol etmesi gereken maddeler var (ör. SAR 56 kullanıcı ülkeleri doğrulanamadı → metne yazılmadı; MPT-55 adetleri 2019 AA haberine dayanıyor; Mekke anlaşması oy sayısı resmî kayıtta yok).

## Yayın takvimi önerisi (onay sonrası)

Otomasyonun zamanlanmış saatleriyle çakışmayan, o gün o dilde yükü az olan slotlar. Haberler onaydan hemen sonra; rehberler 8–16 Kasım arasına yayıldı. Hiçbir taslak zamanlanmadı.

| Slot | Dil | Post ID | Başlık | O gün o dilde zamanlanmış | Not |
|---|---|---|---|---|---|
| 2026-11-06 18:30 | ar | 85021 | البرلمان التركي يصادق على اتفاقية مكة للدفاع المشترك مع السعودية وباكس | 0 | Haber: onaydan hemen sonra (güncelliği kaybetmeden) |
| 2026-11-06 18:30 | en | 85023 | ASELSAN Signs $1.1 Billion Air Defence Export Contract With an Undiscl | 2 | Haber: onaydan hemen sonra (güncelliği kaybetmeden) |
| 2026-11-06 18:30 | es | 85019 | El Consejo de Ministros autoriza 2.302 millones para dotar a las Fuerz | 1 | Haber: onaydan hemen sonra (güncelliği kaybetmeden) |
| 2026-11-06 18:30 | ru | 85025 | Румыния и Молдова впервые провели совместную военную закупку: 62 грузо | 0 | Haber: onaydan hemen sonra (güncelliği kaybetmeden) |
| 2026-11-08 10:30 | ru | 85003 | Что такое БТР: устройство, назначение и известные модели бронетранспор | 0 |  |
| 2026-11-09 10:30 | es | 85011 | Fuerzas Armadas de México 2026: efectivos, aviones, buques y presupues | 1 |  |
| 2026-11-09 10:30 | ru | 85005 | Что такое корвет: чем корвет отличается от фрегата и эсминца | 0 |  |
| 2026-11-09 10:30 | tr | 85007 | İHA ve SİHA'larda termal iz yönetimi nedir? Kızılötesi imza nasıl azal | 5 |  |
| 2026-11-10 10:30 | en | 84999 | MPT-55 Rifle: MKE's 5.56 mm National Infantry Rifle Explained | 1 |  |
| 2026-11-10 10:30 | es | 85013 | Indra: qué es, qué hace y quién es su propietario (2026) | 1 |  |
| 2026-11-11 10:30 | es | 85015 | Naval Group: qué es, qué hace y quién es su propietario | 1 |  |
| 2026-11-12 10:30 | es | 85009 | Fuerzas Armadas de Argentina 2026: Ejército, Armada, Fuerza Aérea y pr | 1 | 84644 (Fuerza Aérea Argentina, 10.11) yayımlandıktan sonra; ona link eklenecek |
| 2026-11-12 12:30 | en | 84997 | HK416 Explained: Heckler & Koch's Piston-Driven 5.56 mm Assault Rifle | 0 | talep var (hk416 74 gös./24s); erken |
| 2026-11-13 10:30 | en | 85001 | SAR 56 Rifle: Sarsılmaz's 5.56 mm Infantry Rifle Explained | 1 |  |
| 2026-11-16 10:30 | es | 85017 | ¿Qué es un misil? Tipos, cómo funciona y diferencia con un cohete | 1 |  |

## 30 / 60 / 90 gün performans takibi (dil bazında ayrı)

- **Temel çizgi:** bu dosya (24 saat) + 28 gün ve 3 ay GSC dışa aktarımı (Sayfa × Sorgu, ülke filtresiyle). URL listesi: T2'deki 30 sayfa, T5'teki 15 taslak, Top100.
- **Ölçülecekler (her dil ayrı):** organik tık ve gösterim değişimi; CTR değişimi (T2 sayfalarında hedef: konum sabitken CTR artışı); ilk 3 / ilk 10 sorgu sayısı; yeni içeriklerin ilk 30 gündeki gösterimi; güncellenen içeriklerin önce/sonra karşılaştırması (aynı 28 günlük pencere); ülke bazlı görünürlük (İspanya, Meksika, Arjantin, Şili ayrı); Kapsam raporundaki 404/indekslenmeyen URL'ler; mükerrer kümelerde hangi URL'nin gösterim aldığı (çakışma takibi).
- **30. gün:** T2 başlık/meta değişikliklerinin CTR etkisi; Polylang dili atanmamış yazılarda dil ataması yapıldıysa hreflang hataları. **60. gün:** yeni rehberlerin sıralaması; mükerrer kümelerde canonical sonrası gösterimin tek URL'de toplanması. **90. gün:** dil bazlı yeniden önceliklendirme — talep kanıtı zayıf kalan dillerde (ZH) üretim durdurulur, güçlü olanlara (ES ülke dosyaları, EN şirket profilleri) kaydırılır.

## Onay bekleyen kararlar

- Mükerrer kümeler için canonical/301 (T4) — URL değişikliği ve yönlendirme yapılmadı.
- RU HQ-9 404 URL'sinin canlı sayfaya 301'i (en hızlı RU kazanımı).
- Sonekli hattın 3.526 yazısına toplu Polylang dil ataması ve otomasyonda 'aynı konu var mı' kontrolü.
- Rank Math ayırıcı karakter + EN/ES/AR/RU başlık şablonundan Türkçe sloganın çıkarılması.
- T2'deki 30 revizyonun canlıya alınması (önce/sonra metinleri hazır).
- 15 taslağın editör kontrolü, çeviri gruplaması ve takvime alınması; zamanlanmış EN S-80 ve Elbit yazılarının öne çekilmesi.

## Büyüme havuzu notu

Önceki '300 İspanyolca konu' listesi repoda ve WordPress'te bulunamadı; havuz bu teslimatta GSC verisi + envanter karşılaştırmasından kuruldu (Top100 mevcut sayfa: Excel 'Top100' sekmesi; yeni fırsatlar: T3). Liste paylaşılırsa aynı mükerrerlik kontrolünden geçirilip havuza eklenecek.
