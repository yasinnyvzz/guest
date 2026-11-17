# Envanter Medya — Tabanca & Silah Markaları SEO Araştırması (1. Döngü)

Hazırlanma tarihi: 2026-11-17 · Durum: **TASLAK — yayın öncesi insan editör onayı gerekir**

Bu dosya ana rapordur. Yanındaki dosyalar:

| Dosya | İçerik |
|---|---|
| `01_konu_firsatlari_100plus.csv` | 140 konu fırsatı; mevcut URL eşleşmesi, durum, potansiyel, öncelik |
| `mke_tabanca_listesi_2026-11-17.csv/.json` | MKE resmî satış sayfasından 17.11.2026 tarihli 542 tabanca kaydı |
| `02_TASLAK_dunyanin-en-taninmis-tabanca-markalari.md` | İlk sıradaki yazının tam yayın taslağı |

---

## 0. Bu araştırmada neyi yapabildim, neyi yapamadım (dürüst sınırlar)

| Veri kaynağı | Durum |
|---|---|
| Envanter XML sitemap (tüm dillerde 20 567 URL, TR 7 249) | ✅ tarandı |
| Mevcut ana sayfaların başlık/boyut/güncelleme tarihi | ✅ 5 ana sayfa için kontrol edildi |
| MKE Silah Satış sayfası (tabanca: yerli/ithal markalar, ürünler, fiyatlar) | ✅ sayfanın kendi uç noktalarından alındı, tarih damgalı |
| **Semrush** (hacim, KD, ilgili sorgular) | ❌ hesapta API birimi yok — **hiçbir arama hacmi uydurulmadı** |
| **Google Search Console** (gösterim, CTR, pozisyon) | ❌ erişim yok. Bu oturumda CTR/pozisyon verisi **yoktur** |
| Google Trends | ❌ erişilmedi |
| Rakip SERP analizi | ❌ yapılmadı (web araması bu döngüde kullanılmadı) |
| Görsel lisansı | ⚠ Wikimedia Commons için aday dosyalar bulundu; API hız sınırına takıldı, **görsel eşleşme doğrulaması yapılmadı** |

Sonuç: CSV'deki "SEO potansiyeli" **editoryal tahmindir** (konu genişliği, niyet netliği, sitede boşluk). Arama hacmi değildir. Search Console verisi sağlandığında tablo yeniden sıralanmalıdır.

**Gerekli girdiler:** (1) Search Console dışa aktarımı (Sorgular + Sayfalar, son 16 ay), (2) Semrush API birimi veya anahtar kelime dışa aktarımı, (3) editör onayı.

---

## 1. Mevcut Envanter durumu — kritik bulgu

Sitede tabanca konusu **sıfırdan başlamıyor**. Sitemap'ten çıkan ve bu araştırmaya konu olan mevcut sayfalar:

**Büyük sıralama/liste sayfaları (hepsi 7 000–19 000 kelime, 56–74 görsel; son güncelleme Eylül 2026)**
- `/dunyanin-en-iyi-10-tabancasi-canik-zirvede-glock-sig-sauer-beretta-karsilastirmasi/` — title: "En İyi Tabanca Markaları Hangileridir? Karşılaştırma"
- `/turk-tabanca-markalari/` — "Türk Tabanca Markaları: Tam Liste 2026"
- `/tarihin-en-unlu-10-tabancasi/`, `/abdnin-en-unlu-10-tabancasi/`, `/avrupanin-en-taninmis-10-tabancasi/`, `/turkiyede-uretilen-en-taninmis-10-tabanca/`
- `/dunyanin-en-iyi-10-pompali-tufegi/`, `/dunyada-en-cok-kullanilan-10-askeri-tabanca/`, `/dunyanin-en-uzun-suredir-uretilen-10-tabancasi/`, `/dunyanin-en-hafif-tabancalari/`

**Sarsılmaz kümesi:** `sarsilmaz-nedir-sahibi-urunleri-fabrikalari`, `sarsilmaz-tabancalari-guncel-modeller-ozellikleri`, `sarsilmaz-urunleri-tabancalar-tufekler-sistemler`, `sar9-nedir-ozellikleri-teknik-verileri`, `sar9-nedir-ozellikleri`, `sar9-vs-glock-19-…`, `sar9-vs-canik-tp9-…`, `sarsilmaz-k2-45-…`, `sarsilmaz-kilinc-2000-…`, `sarsilmaz-duzce-fabrikasi-…`, `sarsilmaz-hangi-ulkelere-ihracat-yapiyor`, `sarsilmaz-av-tufekleri-magic-vertu-modelleri`, `turkiye-hafif-silah-sanayiinde-sarsilmazin-yeri` + `/envanter/sar9-mete-tabanca/`.

**Diğer Türk üreticiler:** `girsan-tabanca-modelleri`, `tisas-zigana-tabanca-nedir`, `tisas-zigana-tabanca-galeri`, `canik-tp9-nedir`, `canik-mete-serisi-nedir`, `turk-tabanca-ihracati-canik-sarsilmaz`, firma kartları (Tisaş, Yavuz Firearms, Derya, Akdaş).

**Yasal küme:** `silah-ruhsati-nasil-alinir`, `silah-tasima-ruhsati-sartlari`, `silah-bulundurma-ruhsati-nasil-alinir`, `silah-ruhsati-yenileme`, `silah-ruhsati-harclari`, `yivsiz-tufek-ruhsati-nasil-alinir`, `kurusiki-tabanca-ruhsati-ve-cezasi` vb.

**Sitede bulunmayan (sitemap ve URL taramasıyla doğrulandı):**
- 7,65 mm içeriği (hiç yok)
- "9×19 mm nedir" / 9 mm model rehberi (yalnız `medef-9x19-tabanca-fisekleri` mühimmat sayfası var)
- Glock, Beretta, SIG Sauer, Walther, H&K, CZ, Colt, S&W, FN, Browning, Ruger, Kimber için **marka profili** (yalnız haber düzeyinde HK416/M27/M2 Browning var)
- Ülke bazlı kümeler (Alman/İtalyan/Fransız/İngiliz/Avusturya/Çek/İsviçre/Belçika)
- Lüks/pahalı/müzayede/koleksiyon
- MKE yerli–ithal marka kataloğu
- Osmanlı ve erken Cumhuriyet dönemi tabancaları
- "Taşıma ve bulundurma ruhsatı farkı" karşılaştırma sayfası

> Not: Sitemap sayfanın varlığını gösterir, içerik kalitesini değil. Yukarıdaki "mevcut" sayfaların güncel sıralama/CTR performansı bilinmiyor. "Sitede yok" yalnızca yukarıdaki boşluklar için ve URL taramasına dayanarak söylenmiştir.

### Anahtar kelime çakışması riski (acil)
1. `best` (dünyanın en iyi tabanca markaları) ↔ `tarihin-en-unlu-10` ↔ `avrupanin-en-taninmis-10` ↔ `abdnin-en-unlu-10` ↔ `turkiyede-uretilen-en-taninmis-10`: dört–beş "en ünlü/en iyi 10" sayfası birbirine yakın niyet taşıyor. **Yeni "dünya markaları" sayfası açmak yerine**, `best` sayfasını pillar yapıp diğerlerini niyet bazlı ayırmak (tarih / ülke / yerli) daha doğru. Search Console'da aynı sorguyu hangi URL'nin aldığına bakılmadan birleştirme/yönlendirme yapılmamalı.
2. `sar9-nedir-ozellikleri` ↔ `sar9-nedir-ozellikleri-teknik-verileri`: iki sayfa aynı sorguyu hedefliyor görünüyor → birleştirme adayı (**DOĞRULAMA GEREKLİ**, GSC verisi şart).
3. `turk-tabanca-markalari` ↔ `turkiyede-uretilen-en-taninmis-10-tabanca`: rol ayrımı gerekli (marka hub'ı / model listesi).

---

## 2. MKE resmî listesi — 17.11.2026 tarihli ölçüm

Kaynak: `https://mke.gov.tr/urunsatis` (sayfa kendi `UrunSatisMarkaListesi` / `UrunSatisWebUrunler` uç noktalarını kullanıyor; "Tabanca" ürün türü). Fiyatlar sayfada TL olarak listeleniyor (bir kayıt farklı para birimiyle; CSV'de sütun var). **Stok/satış durumu hakkında bilgi yoktur ve tahmin yapılmamıştır.**

- **Yerli (MKE etiketi) — 24 marka:** Aselkon, Ata Arms, Balıklı Silah, Balistik Defence, Barak, Bays, BRG9, Canik, Derya, Ermox Silah, Eşrefoğlu, Girsan, GYES, Kor, Kral, Radikal, Ranger Arms, Reximex, Sarıçam, **Sarsılmaz**, Stoeger, System Defence, **Tisaş**, Tori.
- **İthal — 13 marka:** Arex, Beretta, Bernardelli, Česká zbrojovka, Colt, Glock, Kel-Tec, Kimber, Para Ordnance, Springfield, Springfield (HS Produkt), Tanfoglio, Walther.
- **Toplam 542 tabanca kaydı.** Kalibre dağılımı (ürün adından, otomatik sınıflama; editör kontrolü gerekir): 9×19 ≈ 452 · .45 ACP ≈ 62 · .380 ACP 3 · .22 LR 2 · **7,65 mm: 4** · diğer 19.
- Kayıt sayısı en yüksek markalar: Tisaş 82 · Sarsılmaz 74 · Girsan 67 · Canik 57 · Stoeger 31.
- 7,65 mm kayıtları: Girsan Yavuz 13 Defender (2), Sarsılmaz B6 C (1), Tanfoglio FT.7 Defence (1).

İçerik riski: "Yerli" etiketi MKE'nin satış sınıflamasıdır. Marka ≠ üretici ≠ üretim yeri; Stoeger gibi uluslararası ticari markaların Türkiye üretimi için **üretici resmî kaynakla doğrulanmadan** "Türk markası" denmemelidir.

---

## 3. En yüksek potansiyelli 30 konu (editoryal tahmin)

Seçim ölçütü: sitede boşluk × niyet netliği × Envanter'in sahip olduğu veri (MKE, Türk üretici) × doğrulanabilirlik. Sıra önceliği gösterir.

| # | Konu | Durum | Hedef |
|---|---|---|---|
| 1 | 9×19 mm ne anlama gelir + 9 mm tabancalar rehberi | YENİ | pillar `/9-mm-tabancalar/` |
| 2 | En iyi 9 mm tabancalar (ölçütlü "öne çıkan") | YENİ | pillar altı |
| 3 | 7,65 mm Browning (.32 ACP) vs diğer 7,65 fişekler | YENİ | `/7-65-mm-tabancalar/` |
| 4 | Eski 7,65 tabancalar (Walther PP, FN 1910, Browning 1903…) | YENİ | alt sayfa |
| 5 | MKE tabanca kataloğu: yerli ve ithal markalar | YENİ | `/mke-tabanca-katalogu/` |
| 6 | MKE tabanca fiyat tablosu (tarihli) | YENİ | aynı hub, ayrı güncelleme |
| 7 | Dünyanın en iyi tabanca markaları — metodoloji ile yenileme | MEVCUT-KAPSAM | `best` |
| 8 | En iyi Türk tabanca markaları — CTR/Discover | MEVCUT-CTR | `turk-tabanca-markalari` |
| 9 | Sarsılmaz marka dosyası (hub) | MEVCUT-KAPSAM | `sarsilmaz-nedir…` |
| 10 | SAR9 GEN3 aile rehberi (varyant tablosu) | MEVCUT-KAPSAM | `sar9-…` |
| 11 | Sarsılmaz tabanca modelleri (MKE 74 kayıtla) | MEVCUT-GÜNCELLE | `sarsilmaz-tabancalari…` |
| 12 | Sarsılmaz B6 serisi tarihçesi | YENİ | alt sayfa |
| 13 | Sarsılmaz SAR7/24 | YENİ | alt sayfa |
| 14 | Dünyanın en eski tabanca üreticileri | YENİ | evergreen |
| 15 | Glock marka profili | YENİ | marka kümesi |
| 16 | Beretta marka profili | YENİ | marka kümesi |
| 17 | SIG Sauer marka profili | YENİ | marka kümesi |
| 18 | Colt marka profili + 1911 tarihçesi | YENİ | marka kümesi |
| 19 | Alman tabanca markaları | YENİ | ülke kümesi |
| 20 | İtalyan tabanca markaları | YENİ | ülke kümesi |
| 21 | Fransız tabanca markaları (tarihî/aktif ayrımlı) | YENİ | ülke kümesi |
| 22 | İngiliz silah markaları (tarihî/aktif ayrımlı) | YENİ | ülke kümesi |
| 23 | Taşıma ve bulundurma ruhsatı farkı | YENİ | hukuki, resmî kaynaklı |
| 24 | Türkiye'de tabanca üretiminin tarihçesi | YENİ | tarih |
| 25 | Osmanlı döneminde kullanılan tabancalar | YENİ | tarih |
| 26 | Türk pompalı av tüfeği üreticileri | MEVCUT-KAPSAM | `yerli-pompali-av-tufegi-2026` |
| 27 | Dünyanın en pahalı tabancaları (yalnız doğrulanmış müzayede) | YENİ — **doğrulama sürmeden yayınlanmaz** | koleksiyon |
| 28 | Walther / H&K / CZ marka profilleri | YENİ | marka kümesi |
| 29 | Güvenli silah saklama kuralları | YENİ | güvenlik |
| 30 | Silah markaları ve fotoğrafları (görsel hub) | YENİ | galeri |

Tüm 140 satır `01_konu_firsatlari_100plus.csv` içinde.

---

## 4. Yeni açılması gereken sayfalar (net)

- Yeni kümeler: 9 mm pillar (+3 alt sayfa), 7,65 mm pillar (+2), MKE tabanca kataloğu hub'ı, 12 yabancı marka profili, 9 ülke sayfası, lüks/müzayede (doğrulanırsa), Osmanlı/Cumhuriyet tarihi (2), hukuk karşılaştırması (2), Sarsılmaz alt sayfaları (B6, SAR7/24, SAR9 tarihçesi).
- Mevcut sayfalarla çözülecekler: "2026 tabanca markaları", "dünyanın önde gelen 10…", "en çok tanınan…" → yeni URL açılmaz.

---

## 5. 30 günlük yayın planı (haftada 5 içerik + 5 güncelleme hedefi; kaliteye göre azaltılabilir)

**Hafta 1 — Temel ve çakışma düzeni**
1. GSC dışa aktarımı al → çakışma tablosu (best/tarihin/avrupanin/abdnin; sar9 ikilisi).
2. YENİ: **Dünyanın en tanınmış tabanca markaları** (bkz. taslak) — `best` ile rolü ayrılmış pillar karar sonrası.
3. YENİ: **9×19 mm nedir + 9 mm tabancalar** pillar.
4. YENİ: **MKE tabanca kataloğu** (yerli/ithal marka; tarihli).
5. GÜNCELLE: `turk-tabanca-markalari` (başlık varyantı, MKE 24 marka tablosu).
6. GÜNCELLE: `sarsilmaz-tabancalari-guncel-modeller-ozellikleri` (MKE model ailesi tablosu).

**Hafta 2 — Küçük kalibreler ve Sarsılmaz**
1. YENİ: **7,65 mm tabancalar** (fişek ayrımı).
2. YENİ: **Eski 7,65 tabancalar** (galeri).
3. YENİ: Sarsılmaz **B6 serisi**.
4. YENİ: Sarsılmaz **SAR9 ailesinin gelişimi**.
5. GÜNCELLE: SAR9 sayfa ikilisi (GSC'ye göre birleştir/ayır), `sar9-vs-glock-19`.

**Hafta 3 — Yabancı markalar ve ülkeler**
1. YENİ: Glock, Beretta, SIG Sauer, Colt profilleri (haftada 2–3).
2. YENİ: Alman ve İtalyan tabanca markaları.
3. YENİ: **Dünyanın en eski tabanca üreticileri.**
4. GÜNCELLE: `best` (metodoloji bölümü ve kriter ağırlıkları).

**Hafta 4 — Tarih, hukuk, galeri**
1. YENİ: Fransız ve İngiliz markalar (tarihî/aktif ayrımı).
2. YENİ: Osmanlı dönemi tabancaları; Türkiye'de tabanca üretimi tarihçesi.
3. YENİ: Taşıma–bulundurma ruhsatı farkı; güvenli saklama (resmî kaynaklı).
4. Aylık kontrol: görsel indeksleme, CTR, kategori iç bağlantıları.
5. Yalnız doğrulanabilirse: müzayede "en pahalı" araştırması.

Haftalık ek: 1 Türk üretici derin analizi (Sarsılmaz/Canik/Girsan/Tisaş sırayla), 1 Google Görseller kontrolü.

---

## 6. İlk 10 galeri için içerik brifi

Her brif ortak iskeleti kullanır: SEO başlığı · 40–60 kelime spot · giriş · metodoloji · görselli öğeler (marka/model, gerçek görsel, ülke, tarihçe, teknik kategori, doğrulanmış özellik, bağımsız test varsa, kaynak) · karşılaştırma tablosu · Türk üreticilerin konumu · sonuç · SSS · kaynakça. Aşağıda yalnız farklar var.

| # | Galeri | Önerilen başlıklar | Kapsam / kriter | Kritik doğrulama |
|---|---|---|---|---|
| 1 | Dünyanın en tanınmış tabanca markaları | Genel: "Dünyanın en tanınmış 10 tabanca markası: tarih, ürün ve üretim ülkesi" · Discover: "Bir tabanca markasını tanınmış yapan nedir?" | Ölçütler: tarih, ürün çeşitliliği, resmî standart/ihale, uluslararası varlık, belgelenmiş yenilik | Köken ülke ≠ üretim ülkesi; şirket yapısı |
| 2 | 9 mm tabanca modelleri | "9 mm tabanca modelleri: markalar, fişek ve teknik özellikler" | 9×19 tanımı, model tablosu (tutarlı ölçü) | Sürüm farkları (Gen3 vs Gen5 vb.) |
| 3 | 7,65 mm tabancalar | "7,65 mm tabancalar: tarihçe, modeller ve fotoğraflar" | .32 ACP / 7,65 Parabellum / 7,65 Borchardt ayrımı | Fişek–model eşleşmesi |
| 4 | Türk tabanca markaları galeri | "Türk tabanca markaları: Sarsılmaz, Canik, Girsan, Tisaş" | MKE yerli listesi + doğrulanan üreticiler | Üretici/ticari marka ayrımı |
| 5 | MKE katalog görselli | "MKE tabanca kataloğu: yerli ve ithal markalar" | Marka tablosu, tarihli fiyat | MKE fotoğraf hakkı (izin gerekli) |
| 6 | Alman tabanca markaları | "Alman tabanca markaları: Walther, H&K, SIG Sauer (Almanya) ve tarihî üreticiler" | Aktif/tarihî ayrımı | Marka kökeni vs güncel üretim |
| 7 | Fransız tabanca markaları | "Fransız tabanca markaları: geçmişten günümüze" | MAS, Manurhin, Chapuis vb. | Hangileri hâlâ aktif? |
| 8 | Eski 7,65 modelleri | "Tarihî 7,65 mm tabancalar" | PP/PPK, FN 1910, Browning 1903, Mauser HSc… | Üretim yılları |
| 9 | Pompalı av tüfekleri | "Dünyanın tanınmış pompalı av tüfeği markaları" | Tarih, mekanizma, üretim ülkesi | Av yönlendirmesi/öldürücülük anlatısı yok |
| 10 | Dünyanın en eski tabanca üreticileri | "Hâlâ üretim yapan en eski tabanca markaları" | Kuruluş yılı belgesi, süreklilik | "En eski" iddiası kaynakla; Beretta 1526 iddiası şirket kaynağı |

---

## 7. Türk üreticilerin görünürlüğü (editoryal ilke)

1. **Aynı ölçüt, aynı tablo:** Türk markalar (Sarsılmaz, Canik, Girsan, Tisaş) yabancı markalarla aynı kriter tablosuna girer; avantaj varsa ölçüte dayalıdır (ör. MKE listesindeki ürün çeşitliliği, ihracat verisi, resmî ihale).
2. Her yabancı marka sayfasına doğal bir "Türkiye'de karşılığı / yerli alternatifler" bölümü (örnek: Glock 19 ↔ SAR9/TP9 karşılaştırması mevcut).
3. Her ülke sayfasında "Türkiye" sütunu; "Türk tabanca" kümesi hub'dan beslenir.
4. Karşılaştırmalarda yalnızca üretici kataloğu + bağımsız test; "üstün", "en iyi" yok. Başka markalar kötülenmez.
5. Sponsorlu/ücretli işbirliği varsa sayfa üstünde etiketlenir.

---

## 8. Sarsılmaz özel dosyası — planlanan yapı

Hub: mevcut `sarsilmaz-nedir-sahibi-urunleri-fabrikalari` → hub'a dönüştürülür.

| Sayfa | Durum | Kaynak |
|---|---|---|
| Sarsılmaz tarihi, şirket yapısı, tesisler | güncelle | şirket sitesi, resmî kayıt, KAP/ticaret sicili (doğrula) |
| Tabanca ürün aileleri (SAR9, K2000, K2 45, B6, SAR7/24, P8, SR38, SOCOM…) | güncelle | MKE listesi + üretici kataloğu |
| SAR9 ailesinin gelişimi + GEN3 varyant tablosu | yeni | katalog |
| B6 serisi (.22 LR, 7,65, 9×19) | yeni | katalog + MKE kayıtları |
| SAR7/24 | yeni | katalog |
| Sarsılmaz vs rakipler | güncelle | yalnız resmî veri/test |
| İhracat ve kullanım | güncelle | resmî ihracat verisi (tarihli) |

MKE'de **74 Sarsılmaz tabanca kaydı** görüldü (SAR9 GEN3 C/SC/T/Sport varyantları, K.2000 serisi, SAR7/24, P8, B6, SR38 revolver, K2 .45, SAR2023, SAR9 Socom). Bu adlandırma doğrudan "model ailesi tablosu"nun omurgası. Bağımsız test verisi bu döngüde **bulunmadı**; test yoksa yazıda "bağımsız test verisi bulunamadı" notu yer alır.

---

## 9. Görsel kaynak araştırması (ilk geçiş)

Wikimedia Commons'ta lisanslı aday dosyalar (API; yalnız lisans alanı okundu, **modelle görsel eşleşme henüz doğrulanmadı**):

| Model | Aday dosya | Lisans (Commons alanı) |
|---|---|---|
| Beretta 92 | `File:Beretta 92S (cropped).jpg` | Public domain |
| CZ 75 | `File:CZ 75 Champion.jpg` | CC0 |
| Canik TP9 | `File:Canik-TP9-SFx.jpg` | CC BY-SA 4.0 |
| Mossberg 500 | `File:Mossberg 500 shotgun & Federal Riot Gun of the Bermuda Regiment.jpg` | CC BY-SA 3.0 |
| Remington 870 | `File:Remington 870 Wingmaster (55416542561).jpg` | CC BY-SA 4.0 |
| S&W | `File:Smith & Wesson Model 61 Pocket Escort.jpg` | CC BY-SA 4.0 |

Eksik: Glock, SIG Sauer, Walther, Colt 1911, Sarsılmaz SAR9, Tisaş Zigana, Girsan Yavuz için sorgular hız sınırına takıldı; yeniden denenecek. Türk üreticiler için **basın kiti/izin yazısı talebi** başlatılmalı (görsel yoksa: "Görsel için lisanslı kaynak araştırması gerekli."). CC BY-SA görsellerde atıf + aynı lisans şartı yayın notunda yer almalı. Yapay görsel gerçek ürün fotoğrafının yerine kullanılmaz.

Görsel metadata şablonu (her görsel): model · üretici · üretim ülkesi · açıklama · dosya adı (`sarsilmaz-sar9-gen3-tabanca.webp`) · alt metin · kaynak URL · lisans · tarih.

---

## 10. İç bağlantı mimarisi

Ana kategori **Tabancalar ve Silah Markaları** → alt kategoriler (Türk Tabanca Markaları, Dünya Tabanca Markaları, Tabanca Modelleri, 9 mm, 7,65 mm, Av Tüfekleri, Silah Üreticileri, Tarihî Silahlar, Koleksiyonluk, Teknik Rehberler, MKE Katalog İncelemeleri).

Çekirdek bağlantılar:
- `/9-mm-tabancalar/` → SAR9, TP9, Zigana, Glock 19 karşılaştırmaları + MKE hub
- `/7-65-mm-tabancalar/` → Sarsılmaz B6, Yavuz 13, eski modeller
- Sarsılmaz hub → SAR9 aile, B6, SAR7/24, tarih, ihracat, fabrika
- MKE hub → her marka profili (yalnız MKE listesinde olanlar)
- Ülke sayfaları → ilgili marka profilleri → pillar `best`
- Hukuk sayfaları ↔ güvenli saklama; **av tüfeği sayfaları → mevzuat** (silah seçimi/öldürücülük anlatısı yok)

Alakasız (savunma sanayii haberi) sayfalara SEO amaçlı bağlantı verilmez.

---

## 11. Önerilen başlık/meta (ilk sıradaki yazı)

1. Genel: **Dünyanın En Tanınmış 10 Tabanca Markası: Tarih, Ürünler ve Üretim Ülkeleri**
2. Discover: **Bir Tabanca Markası Nasıl "Efsane" Olur? Dünyanın Tanınmış 10 Üreticisi**
3. Galeri: **Dünyanın Öne Çıkan 10 Tabanca Markası (Fotoğraflı Galeri)**
4. Teknik: **Tabanca Markalarının Karşılaştırması: Kuruluş, Üretim Ülkesi ve Ürün Aileleri**
5. Tarihî: **Tabanca Markaları Tarihi: 1526'dan Günümüze Hâlâ Üretim Yapanlar** *(1526 yalnız Beretta kaynağı doğrulanırsa)*

Meta açıklama (≤155 krk): "Beretta'dan Glock'a, Colt'tan Sarsılmaz'a: tanınmış tabanca markalarını kuruluş yılı, üretim ülkesi ve ürün ailesine göre ölçütlü karşılaştırıyoruz."

Yıl bilgisi başlığa **eklenmedi**; evergreen URL: `/dunyanin-en-taninmis-tabanca-markalari/`.

---

## 12. Puanlama özeti

CSV'deki iki alan:
- **SEO potansiyeli (1–5):** hacim değil. 5 = geniş, net niyet + sitede boşluk/zayıf kapsam; 3 = orta; 1 = niş.
- **Yayın önceliği:** P1 (32 konu) → ilk 30 gün · P2 (53) → 30–60 gün · P3 (55) → 60 gün+.
Search Console + Semrush verisi geldiğinde puanlar yeniden hesaplanmalıdır.

---

## 13. Politika ve güvenlik duruşu

- Yazılar tanıtıcı, tarihî, teknik ve hukuki bilgi çerçevesindedir.
- Av içeriklerinde hedef türüne göre silah seçimi / öldürücülüğü artırma / silah gizleme / denetimden kaçınma anlatısı **yer almaz**.
- Mevzuat bilgisi yayın günü resmî kaynaktan (Resmî Gazete, mevzuat.gov.tr, İçişleri/Emniyet) doğrulanır.
- Fiyat ve stok bilgisi tarihlidir; MKE verisi "kontrol tarihi: 2026-11-17" ibaresiyle verilir.
- **Yayın öncesi insan editör onayı zorunludur.** Hiçbir içerik yayına alınmamıştır.
