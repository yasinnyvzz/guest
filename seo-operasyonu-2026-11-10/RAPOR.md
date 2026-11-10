# Envanter Medya — SEO pilot operasyonu, 10 Kasım 2026

Ayrıntılı tablolar: `ENVANTER_SEO_2026-11-10.xlsx` (Özet, 1.000 sorgu, 1.000 sayfa, ülke, cihaz, saatlik, 30 fırsat, CTR paketi, WP taslakları, yayın takvimi önerisi).
Makale kopyaları: `taslaklar/` · CTR paketi: `ctr_revizyonlari.json` · Betikler: `taslak_yukle.py`, `zamanla.py`, `guncelle.py`.

**Hiçbir şey yayımlanmadı veya zamanlanmadı.** Yazma işlemleri yalnızca yeni taslaklar ve görselleridir. Yayındaki sayfalara dokunulmadı.

---

## 1. Performans karşılaştırması (her biri "son 24 saat" kesiti)

| Kesit | Tıklama | Gösterim | CTR |
|---|---|---|---|
| 6 Kasım (önceki rapor) | 1.628 | 144.112 | %1,13 |
| 8 Kasım (sizin verdiğiniz toplam) | 1.151 | 104.422 | %1,10 |
| **10 Kasım** | **1.610** | **125.557** | **%1,28** |

- 8 Kasım'a göre tıklama **+%39,9**, gösterim **+%20,2**, CTR **+0,18 puan**.
- 6 Kasım'a göre tıklama yatay (−%1,1), gösterim −%12,9, CTR +0,15 puan. Yani 8 Kasım bir dipti; 10 Kasım, 6 Kasım seviyesine dönüş. Üç günlük kesitten trend çıkmaz.
- Dosyanın son 3 saati (09:00–11:00) GSC veri gecikmesi nedeniyle neredeyse boş; gerçek günlük toplam bir miktar daha yüksek.
- Sorgular sekmesi toplam gösterimin yalnız **%25'ini** (31.013) gösteriyor; geri kalanı anonim/uzun kuyruk. Sorgu↔sayfa eşleşmesi dosyada yok, eşleştirme URL dili ve başlık/slug ile yapıldı.
- **7/28/90 günlük veri alınamadı:** oturumda Search Console API yetkisi yok (gcloud kimliği yok, Frase'in GSC bağlantısının deneme süresi bitmiş). Bir sonraki adım için GSC'den 28 gün ve 3 ay dışa aktarımı (Sorgular + Sayfalar) veya API erişimi gerekli.

### Neler değişti (6 → 10 Kasım, sayfa düzeyi)
- **Tıklaması artanlar çoğunlukla evergreen sayfalar:** silah ruhsatı sağlık raporu (0→8), EN ana muharebe tankı sıralaması (4→11), EN Fas–Cezayir karşılaştırması (0→7), savunma sanayii maaşları (11→15), KDF salary (1→4), KDF portal (19→21), dünyanın en hızlı tankları (0→3).
- **Düşenler haber kaynaklı:** `tusaş kaan` 1.845 gös./25 tık @3,8 → 726 gös./0 tık @10,4 (KAAN-1 haberi eskidi, ana rehber sıralamada yok); SINKEX 26 EN haberi 7.434 → 71 gösterim; KDF ana sayfası 10.700 → 3.545 gösterim (tıklama 81 → 75, CTR arttı).
- 10 Kasım'ın tık kazandıran yeni haberleri: USS Theodore Roosevelt (21), Pakistan Fa'az (17), Rheinmetall %16 düşüş (17), Lockheed 8 mlr $ (13), Viasat (10), Shield AI–Echodyne (8).

### Yüksek gösterim / düşük tıklama
- **25 sorgu** ≥100 gösterim alıp **0 tık** alıyor (toplam 7.888 gösterim). **103 sorgu** 4–15. sırada ve ≥30 gösterimli (14.107 gösterim) — P2 havuzu.
- Ülke: Meksika 4.042 gösterim / CTR **%0,42** (en zayıf büyük pazar); Kenya %2,34 en iyi. Cihaz: mobil %65 gösterim, CTR %1,19 (masaüstü %1,48).
- Dil (sayfa sekmesi): EN 44.676 gös. / %1,61 · TR 25.577 / %2,70 · ES 8.282 / %1,07 · RU 4.321 / %1,37 · AR 3.324 / %2,11 · ZH 48. PT için tek sorgu yok.

## 2. Öncelikli sorgular: hangi sayfa gösterim alıyor, karar ne?

| Sorgu | Gös. / Tık / Konum | Gösterim alan sayfa | Karar |
|---|---|---|---|
| m27 | 1.394 / 5 / 2,4 | EN M27 sözleşme **haberi** (9 Kasım) | **NEW ANGLE** — M27 IAR açıklayıcısı (pilot) |
| rheinmetall stock | 944 / 8 / 4,5 | EN Rheinmetall %16 düşüş haberi | **UPDATE** — başlık hisse niyetine; Q3 2026 zaten işlenmiş, yeni URL yok |
| kdf recruitment 2026 | 851 / 4 / 5,7 | EN KDF ana sayfası + 3 çapa URL | **UPDATE + VERIFY** — durum kutusu 13 Eylül'de kalmış |
| tusaş kaan | 726 / 0 / 10,4 | KAAN-1 haberi; rehberler yok | **UPDATE** — /kaan-nedir/ ana rehber yeniden yazıldı (pilot) + **MERGE REVIEW** |
| египет | 692 / 0 / 2,3 | RU Dostluk Denizi haberi | **NEW** — RU Mısır silahlı kuvvetleri rehberi (pilot) |
| tunisian army | 601 / 0 / 5,6 | EN Tunus envanteri (0 tık, Rank Math boş) | **UPDATE** — başlık/H1 'Tunisian Army' |
| aselsan (EN) | 577 / 6 / 7,1 | EN 'ASELSAN competitors' | **MERGE REVIEW** — tek EN ASELSAN hub |
| bayraktar akıncı | 509 / 4 / 2,5 | dosyada eşleşme yok (aday: /envanter/bayraktar-akinci/) | **UPDATE + VERIFY** — 13+ AKINCI rehberi var, yeni makale yok |
| gimbal | 490 / 1 / 7,2 | EN Altınay Venüs-4 | **SKIP** (tüketici kamera niyeti) — yalnız meta |
| баллистическая ракета | 476 / 0 / 10,1 | RU 12584 (3,8 bin karakter, ince) | **UPDATE** — kapsamlı yeniden yazım (pilot) + 39449 ile MERGE |
| egipto | 423 / 0 / 5,7 | ES Dostluk Denizi haberi | **NEW** — ES Mısır silahlı kuvvetleri rehberi (pilot) |
| ecuadorian army | 394 / 0 / 8,3 | EN Ekvador envanteri | **UPDATE** — başlık/H1 |
| siper | 344 / 0 / 3,8 | 4 ayrı EN SİPER açıklayıcısı | **MERGE REVIEW** + EN hipersonik radar taslağını yayımla |

**Ana sonuç:** Site evergreen konularda doymuş durumda. TR'de 7 ayrı "KAAN nedir", 5 ayrı "KAAN vs F-35", EN'de 5 KAAN açıklayıcısı, 4 SİPER açıklayıcısı, aynı M1E3 haberinin 9 kopyası var. KAAN, AKINCI, SİPER ve ASELSAN için yeni makale açmak yamyamlığı artırır. Bu konularda doğru hamle güçlendirme ve birleştirme. Yeni makaleler yalnızca gerçek boşluklara yazıldı.

## 3. WordPress arşivi ve 6 Kasım işlerinin akıbeti

- Önbelleğe alınan envanter: **18.410 yayında, 362 taslak, 3.562 zamanlanmış** yazı (son zamanlanmış: 2 Temmuz 2027) + 3.093 sözlük/sistem/firma/sayfa. Site günde **63–101 yazı** yayımlıyor.
- **6 Kasım'ın 15 taslağının hiçbiri yayımlanmamış**; önerilen **30 başlık/meta revizyonunun hiçbiri uygulanmamış** (ör. Tunus sayfası 28 Eylül'den beri değişmedi, KDF 13 Eylül'den beri).
- **85023 (EN, ASELSAN 1,1 mlr $) artık mükerrer:** diğer hat aynı haberi 8 Kasım'da 85328 olarak yayımladı → yayımlanmamalı (silmedim).
- 6 Kasım'ın haber taslakları (ES Bakanlar Kurulu 2.302 M€, RU Romanya–Moldova, AR Mekke anlaşması onayı) 4 gün eskidi → yayımlanacaksa önce güncellik ve mükerrerlik kontrolü.

## 4. Pilot: ilk 10 makale

| # | Dil | Hedef sorgu | Mevcut gösterim | Mevcut tık | Makale başlığı | SEO kararı | WordPress | Önerilen yayın |
|---|---|---|---|---|---|---|---|---|
| 1 | EN | m27 | 1.394 | 5 | M27 IAR Explained: The Marine Corps' HK416-Based Infantry Rifle | NEW ANGLE | taslak 85868 — [önizleme](https://envantermedya.com/?p=85868&preview=true) | 10 Kasım 16:30 |
| 2 | EN | lmt stock | 483 (küme ≈1.030) | 1 (küme 6) | Lockheed Martin Stock (LMT): Q3 2026 Results, a $292 Billion Backlog and the Post-Midterm Sell-Off | NEW | taslak 85835 — [önizleme](https://envantermedya.com/?p=85835&preview=true) | 10 Kasım 17:00 |
| 3 | TR | tusaş kaan | 726 | 0 | TUSAŞ KAAN Nedir? Özellikleri, Motoru, Prototipleri ve Son Durumu (2026) | UPDATE | mevcut post 49720 (yayında; revizyon `taslaklar/tr-kaan-nedir-UPDATE-49720.json`) | onay sonrası uygulanır |
| 4 | RU | баллистическая ракета | 476 | 0 | Баллистическая ракета: что это, как летит, виды и дальность | UPDATE | mevcut post 12584 (yayında; revizyon `taslaklar/ru-ballisticheskaya-raketa-UPDATE-12584.json`) | onay sonrası uygulanır |
| 5 | EN | taurus kepd 350 | 177 | 0 | Taurus KEPD 350 Explained: Range, Warhead, Operators and Taurus Neo | NEW | taslak 85838 — [önizleme](https://envantermedya.com/?p=85838&preview=true) | 10 Kasım 17:50 |
| 6 | RU | пэтриот | 52 | 1 | ЗРК Patriot («Пэтриот»): характеристики, ракеты PAC-2 GEM-T и PAC-3 MSE, страны | NEW ANGLE | taslak 85851 — [önizleme](https://envantermedya.com/?p=85851&preview=true) | 10 Kasım 16:45 |
| 7 | ES | egipto | 423 | 0 | Fuerzas Armadas de Egipto 2026: efectivos, armamento y proveedores | NEW | taslak 85844 — [önizleme](https://envantermedya.com/?p=85844&preview=true) | 10 Kasım 17:20 |
| 8 | RU | египет | 692 | 0 | Вооружённые силы Египта в 2026 году: численность, структура и вооружение | NEW | taslak 85847 — [önizleme](https://envantermedya.com/?p=85847&preview=true) | 10 Kasım 17:35 |
| 9 | ES | ah-64 apache precio | 21 | 0 | Precio del helicóptero Apache AH-64E: cuánto cuesta y por qué varía tanto | NEW ANGLE | taslak 85841 — [önizleme](https://envantermedya.com/?p=85841&preview=true) | 10 Kasım 18:10 |
| 10 | EN | christian freuding | 55 | 0 | Christian Freuding: Career, Ukraine Role and Plans of Germany's Next Chief of Defence | NEW ANGLE | taslak 85832 — [önizleme](https://envantermedya.com/?p=85832&preview=true) | 10 Kasım 18:25 |

Her makalede: doğrudan cevap veren giriş, H2/H3, en az bir karşılaştırma/teknik tablo, SSS, kaynak listesi, "son güncelleme" satırı, 3–8 iç bağlantı (hepsi HTTP 200), Rank Math başlık (≤60) / açıklama / odak anahtar kelime, özgün slug, öne çıkan görsel (WebP, 1200 px) ve alt metin var. Türk savunma toplayıcı siteleri ve Wikipedia kaynak olarak kullanılmadı. Tüm doğrulanamayan noktalar her JSON'un `verification_notes` alanında listelendi.

**Görseller:** 5 makalede ABD hükümeti kamu malı DVIDS fotoğrafı (kredi altyazıda). Freuding ve Taurus için açık lisanslı Wikimedia Commons fotoğrafı seçilmişti, ama Commons yükleme anında hız sınırı (HTTP 429) verdi. Bu yüzden ev başlık kartı kullanıldı (fotoğraf diye sunulmuyor). Commons açılınca değiştirilebilir. Hiçbir yapay görsel fotoğraf gibi kullanılmadı.

**Çeviri grupları kasıtlı olarak bağlanmadı.** Polylang gruplama sırasında meta ve kapağı yayındaki çevirilerle eşitliyor. Taslak aşamasında bağlamak, yayındaki EN/AR/TR sayfaların SEO alanlarını ezebilir. Yayın anında `ENVANTER_YAYIN_REHBERI.md` sırasıyla bağlanmalı:
- Taurus EN ↔ TR 19744
- ES Mısır ↔ EN `en-egypt-military-strength-2026` / AR 64452

## 5. Yayın takvimi önerisi (onay bekliyor)

| Slot (TR) | Dil | Post | Başlık |
|---|---|---|---|
| onay sonrası (guncelle.py icerik) | TR | 49720 | UPDATE: /kaan-nedir/ ana KAAN rehberi |
| onay sonrası (guncelle.py icerik) | RU | 12584 | UPDATE: Баллистическая ракета (RU 12584) |
| 10 Kasım 16:30 | EN | 85868 | M27 IAR Explained: The Marine Corps' HK416-Based Infantry Rifle |
| 10 Kasım 16:45 | RU | 85851 | ЗРК Patriot («Пэтриот»): характеристики, ракеты PAC-2 GEM-T и PAC-3 MSE, страны |
| 10 Kasım 17:00 | EN | 85835 | Lockheed Martin Stock (LMT): Q3 2026 Results, a $292 Billion Backlog and the Post-Midterm Sell-Off |
| 10 Kasım 17:20 | ES | 85844 | Fuerzas Armadas de Egipto 2026: efectivos, armamento y proveedores |
| 10 Kasım 17:35 | RU | 85847 | Вооружённые силы Египта в 2026 году: численность, структура и вооружение |
| 10 Kasım 17:50 | EN | 85838 | Taurus KEPD 350 Explained: Range, Warhead, Operators and Taurus Neo |
| 10 Kasım 18:10 | ES | 85841 | Precio del helicóptero Apache AH-64E: cuánto cuesta y por qué varía tanto |
| 10 Kasım 18:25 | EN | 85832 | Christian Freuding: Career, Ukraine Role and Plans of Germany's Next Chief of Defence |

- Aralıklar 15–20 dakika. Sitenin kendi zamanlanmış kuyruğuyla aynı dakikaya denk gelen slot yok. Aynı dil art arda gelmiyor.
- İki UPDATE yeni URL açmaz; onaydan sonra `guncelle.py icerik …` ile mevcut URL'ye yazılır. Önce yedek alınır, slug korunur.
- Onaydan sonra: `takvim_onerisi.json` içinde onaylanan satırlarda `"onay": true` yapılır, ardından `python3 zamanla.py takvim_onerisi.json --yaz` çalıştırılır. Kuyruk WordPress'te `future` olarak kalıcıdır, tarayıcı kapansa da WP-Cron yayımlar.
- Saat önerileri onay saatine göre kaydırılabilir. Sık yayın sıralamayı kendiliğinden yükseltmez; site zaten günde ~100 yazı yayımlıyor, bu 10 yazı hacmi değil kapsamı artırıyor.

## 6. İkinci parti (önerilen 10)

Yeni yazı üretmek yerine **6 Kasım'dan bekleyen ve talebi kanıtlanmış hazır taslaklar**, yeniden doğrulama sonrası:

1. EN HK416 (84997): `hk416` 57 gös.
2. EN SAR 56 (85001): `sar 56` + `sar56` 107 gös.
3. EN MPT-55 (84999): `mpt 55` 35 gös. @10,1
4. ES ¿Qué es un misil? (85017): `misil` 115 gös. @2,0, 0 tık
5. ES Fuerzas Armadas de México (85011): Meksika 4.042 gös., CTR %0,42
6. ES Fuerzas Armadas de Argentina (85009): `ejercito argentino`
7. EN SİPER hipersonik radar haberi (85050): `siper` 344 gös.
8. EN SUNGUR–BURÇ ilk atış haberi (85058)
9. RU БТР (85003)
10. RU корвет (85005)

Yedekte üç taslak var: ES Indra (85013), ES Naval Group (85015), TR termal iz (85007).

## 7. Mevcut sayfalar: CTR ve sıralama paketi (onay bekliyor)

`ctr_revizyonlari.json` içinde 16 sayfa için mevcut ve önerilen Rank Math başlık ve açıklaması, sorun tespiti ve içerik aksiyonları var. Başlık tek başına yetmeyeceği için her satırda kapsam, doğruluk ve bağlantı işi de yazılı. Uygulama: `python3 guncelle.py meta ctr_revizyonlari.json --yaz`. Önce kuru çalıştırma yapılır, her değişiklikten önce yedek alınır. P1 satırları:

- **Rheinmetall (85083):** "Rheinmetall Stock Falls 16%: Q3 2026 Guidance Cut Explained"
- **KDF ana sayfa (59837) ve şartlar (65052):** durum kutusu güncellenecek. KDF'nin Ekim 2026'daki "şu an alım yok" uyarısı önce resmî kanaldan doğrulanmalı.
- **Tunus (54957) / Ekvador (66753) / Bolivya (64085):** sorgu ifadesi ("Tunisian Army" vb.) başlığa ve H1'e. Rank Math alanları şu an boş.
- **Afrika sıralaması (67765):** Top 20'ye genişletme.
- **APFSDS (21865):** yayındaki taslak artıkları temizlenecek.
- **Silah ruhsatı harçları (66108):** başlık "bulundurma" öne alınarak yeniden yazılacak. Sorguda 1. sıradayız ama 0 tık var.
- **AKINCI sistem kartı (63016):** sorgu↔sayfa eşleşmesi GSC'de doğrulanınca uygulanacak.

## 8. Teknik SEO bulguları

| Konu | Bulgu | Öneri |
|---|---|---|
| Hreflang | Yalnız Polylang grubuna alınmış yazılarda çıkıyor. Ör. M27 haberinin 5 dili (85527–85531) gruplanmamış, hreflang yok. 6 Kasım raporu sonekli hatta 3.526 dili atanmamış yazı saymıştı. | Sonekli hattın yazıları yayın anında gruplanmalı |
| Google News sitemap | 100 URL ile sınırlı, ~20 saati kapsıyor (site günde ~100 yazı). 9 Kasım'ın M27 haberi listeden düşmüş. | Rank Math News sitemap'i 48 saat / 1.000 URL'ye çıkarılmalı |
| Yapılandırılmış veri | Rehberler de (`/kaan-nedir/`, Tunus envanteri) `NewsArticle` olarak işaretli | Evergreen rehberler `Article`/`TechArticle` olmalı |
| Taslak artıkları | 52 EN açıklayıcıda (ID ~19560–19613) 'Image suggestions' başlığı ve ham markdown `#` satırı yayında, APFSDS'de 'An analogy for kids' | Toplu temizlik betiği, onaylı |
| Rank Math | KDF başlığında `&amp;`. Birçok evergreen sayfada başlık/açıklama boş. 6 Kasım'da tespit edilen `%sep%` sorunu sürüyor (ör. 84849). | Şablon düzeltmesi |
| Kanonik / indekslenebilirlik | Kontrol edilen sayfalarda kendi kanoniği var, `index, follow`, tek H1, breadcrumb şeması var | — |
| Sitemap | `sitemap_index.xml` 124 alt sitemap; robots.txt doğru | Yayın sonrası URL'nin post-sitemap'te olduğu kontrol edilmeli (indeksleme süresi garanti edilemez) |
| Mükerrerler | 7 KAAN nedir · 5 KAAN vs F-35 · 5 EN KAAN açıklayıcısı · 4 EN SİPER · 9 EN M1E3 kopyası · 3 ES SEDENA/SEMAR maaş · RU balistik füze 2 sayfa | MERGE REVIEW listesi xlsx'te; 301/kanonik editör onayıyla |

## 9. Yayındaki sayfalarda bulunan hatalar (yazarlar tespit etti)

- **EN Freuding atama haberi (84970):**
  - Pistorius alıntısı yanlış: BMVg aslı "Ihn leitet ein klarer Kompass", "moral" kelimesi yok.
  - Cavo Dragone General değil, Amiral.
  - Ukrayna özel kurmay görevi resmî CV'ye göre 2022–2023.
  - Breuer'in NATO'ya geçişi kaynaklarda "2027 yazı" olarak geçiyor; haber "Temmuz 2027" diyor.
- **ES Dostluk Denizi haberi:** MKE mutabakatı için "septiembre de 2024" yazıyor, büyük olasılıkla 2026.
- **ES İsrail Apache haberleri:** iki haber tarih (14/20 Ekim) ve tutar konusunda birbiriyle çelişiyor.
- **ES "helicópteros más caros":** Fas için 36 adet yazıyor, kesin sipariş 24 (+12 opsiyon).
- **RU balistik füze sayfası 12584:** menzil sınıfları ve Türkiye bilgisi hatalıydı. Yeni metinde düzeltildi.
- **TR /kaan-ile-f-35-fark/:** ilk uçuşu "2023" yazıyor (doğrusu 21 Şubat 2024), kaynak listesi yok, ~330 kelime → MERGE REVIEW'da /kaan-vs-f-35/'e yönlendirilmeli.
- **TR /kaan-nedir/ (mevcut hâli):** "teknik değerlerin çoğu açıklanmadı" diyor; TUSAŞ ürün sayfası boyut/ağırlık/performans değerlerini yayımlıyor. Revizyonda düzeltildi. Revizyon uygulanmadan önce KAAN-1'in ilk uçuşunun duyurulup duyurulmadığı kontrol edilmeli (10 Kasım itibarıyla duyuru yok).
- **ES ikinci "qué es KAAN" sayfası:** /es/es-que-es-kaan-turkiye-caza-nacional-quinta-generacion/ (3 Temmuz) → /es/es-kaan-que-es/ ile birleştirilmeli.
- **Storm Shadow menzili:** Envanter sayfaları 560 km kullanıyor, MBDA resmî ifadesi "250 km üzeri". Hizalanmalı.

## 10. Günlük rapor — bu parti

| Soru | Cevap |
|---|---|
| Kaç yeni makale yazıldı? | **8** (tümü WP'de taslak) |
| Kaç mevcut sayfa iyileştirildi? | **2 tam yeniden yazım hazır** (KAAN hub, RU balistik füze) + **16 sayfalık CTR paketi** hazır; canlıya uygulanan: **0** (onay bekliyor) |
| Kaç makale zamanlandı? | **0** (editoryal onay bekleniyor; takvim önerisi hazır) |
| Kaç fırsat mükerrer olduğu için elendi? | Yeni makale açılmayan 9 konu (KAAN ×2 açı, AKINCI, SİPER, ASELSAN, Rheinmetall, ICBM, Eurofighter AR, Freuding haberi). Ayrıca 85023 taslağı mükerrer. |
| Kaç dilde yayın? | Taslaklar 4 dilde: EN 4, ES 2, RU 3 (biri güncelleme), TR 1 (güncelleme). AR'de yeni boşluk bulunamadı. PT/ZH'de talep yok. |
| Hâlâ tık almayanlar | tunisian army, ecuadorian army, tusaş kaan, египет, egipto, баллистическая ракета, siper, apfsds, bulundurma ruhsat harcı 2026, gimbal |
| Konumu iyileşenler | 6 → 10 Kasım: silah ruhsatı sağlık raporu, EN tank sıralaması, EN Fas–Cezayir, KDF salary, Roketsan fabrikaları (tık artışı; konum yatay). Düşen: tusaş kaan (3,8 → 10,4). |

**İzleme:** pilot URL'leri yayımlandıktan sonra 7, 14 ve 28. günlerde aynı hedef sorgular için GSC karşılaştırması yapılacak. Bu oturumda kalıcı izleme kurulmadı, 28 günlük GSC dışa aktarımı veya API erişimi gerekiyor.

## 11. Onayınızı bekleyen kararlar

1. Pilot taslakların yayın takvimi (bölüm 5) ve iki UPDATE'in canlıya yazılması.
2. CTR paketi (16 sayfa, bölüm 7).
3. MERGE REVIEW listesi: KAAN, SİPER, M1E3, SEDENA/SEMAR, RU balistik füze, Afrika sıralaması için 301 veya kanonik.
4. Mükerrer 85023 taslağının çöpe alınması.
5. 52 EN açıklayıcıda taslak artığı temizliği.
6. News sitemap limiti ve rehber şema türü (site ayarı).
7. İkinci 10'luk parti (bölüm 6).
