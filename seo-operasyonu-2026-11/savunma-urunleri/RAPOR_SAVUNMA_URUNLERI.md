# Türk savunma sanayii ürünleri SEO operasyonu — durum raporu (7 Kasım 2026)

## Engeller (dürüst durum)
- ssb.gov.tr bu ortamdaki ağ proxy'sinden erişilemiyor → **SSB ürün kataloğu PDF'si işlenemedi**; tekil ürün sayısı çıkarılamadı.
- Frase (deneme bitmiş) ve Semrush (API birimi yok) kullanılamadı → **arama hacmi verisi yok**; Search Console verisine bu oturumda erişilemedi. Öneri sorguları hacim sayılmadı.
- Üretici sitelerinden doğrulama yapılmadı; ürün "durum" sütunu genel evredir, yayın öncesi doğrulanmalı.

## WordPress arşivi (REST ile çekildi)
savunma_sistemi 1.238 · savunma_firma 150 · firma 469 · savunma_terimi 481 · yazı 8.000 (çoğu zamanlanmış).
- "turk-savunma-sanayii-urunleri" ve "yerli-savunma-sanayi-urunleri" slug'ları yoktu; aynı niyette ana katalog sayfası yok → **NEW**.
- KPSS niyetli ayrı rehber yok (yalnız alım haberleri).
- Katalogdaki 32 ürünün 32'sinin ürün dosyası var (/envanter/…); MPT-55 için yazı var (mpt-55-nedir). Eksik: Hisar-O ayrı dosya, MİDLAS/CENK doğrulanacak.
- Kalite bulgusu (UPDATE): ürün sayfası başlıkları bozuk ("Atak Ii", "Bayraktar Tb2 Si̇ha", "Altay Amt Ana Muharebe Tanki"); resmî yazılışa göre düzeltilmeli (URL değişmeden).

## Oluşturulan taslak
- WordPress #85235 (draft, TR): /turk-savunma-sanayii-urunleri/ — 10 kategori, 32 ürün, şirket tablosu, SSS. Kaynak: `taslaklar/tr-turk-savunma-sanayii-urunleri.json`.
- Yayınlanmadı. Kapak/görsel yok; kaynak listesi SSB erişimi sonrası eklenecek.

## Sonuç tablosu
| Hedef sorgu | Mevcut URL | Arama verisi | Karar | Başlık | Öncelik | WP |
|---|---|---|---|---|---|---|
| türk savunma sanayii ürünleri / ürün isimleri | yok | yok | NEW | Türk Savunma Sanayii Ürünleri: … İsimleri | 1 | taslak #85235 |
| yerli savunma sanayi ürünleri KPSS | yok | yok | NEW | KPSS İçin Yerli ve Millî Savunma Sanayii Ürünleri | 2 | yok |
| yerli savunma sanayi şirketleri | savunma_firma sayfaları | yok | NEW+CLUSTER | Türkiye'nin Savunma Sanayii Şirketleri ve Ürünleri | 3 | yok |
| Baykar/ASELSAN/ROKETSAN/TUSAŞ ürünleri | firma sayfaları | yok | VERIFY/UPDATE | şirket başına ürün rehberi | 4 | yok |
| ilk yerli ürünler / tarihçe | yok | yok | NEW | Türk Savunma Sanayiinin Tarihçesi ve İlkleri | 6 | yok |

## 7 günlük plan
1 Ana katalog doğrulama+yayın onayı · 2 KPSS rehberi · 3 Şirketler rehberi · 4 Yerli İHA'lar · 5 Yerli füzeler · 6 Savaş uçakları · 7 Kara araçları. Günde en fazla 2 taslak; hepsi editoryal onaya kadar draft.

## 30 gün
Hafta 1 yukarıdaki 7; hafta 2 helikopter, hava savunma, radar/EH, gemiler, denizaltı; hafta 3 piyade tüfekleri, tabancalar, motorlar, uydu, ihracat; hafta 4 şirket alt rehberleri (ASELSAN, Roketsan, TUSAŞ, Baykar, STM, HAVELSAN, MKE, TEI, Kale), tarihçe, ürün sayfası başlık düzeltmeleri.

## Güncelleme (8 Kasım 2026): SSB kataloğu işlendi
- ssb.gov.tr erişilebilir hâle geldi (önceki hata geçici). PDF: `turk-savunma-sanayii-urun-katalogu.pdf`, 2026 baskısı, **1370 sayfa**, metin katmanlı. Yerelde metne çevrilip yalnız başlık/firma/sayfa indeksi çıkarıldı (`ssb_katalog_indeks.json`); metin kopyalanmadı, görsel yüklenmedi.
- Katalog **firma bazlı**: İçindekilerde 151 firma satırı; ürün başlığı çıkarılan 139 firma.
- Otomatik başlık taraması: **968 tekil aday başlık** (bölüm/firma başlıkları ve alt ürün kalemleri dahil, gürültülü). Envanter'deki ürün sayfalarıyla ad eşleşmesi: **313**. Gerçek tekil ürün sayısı elle temizlik sonrası netleşir; şimdilik kesin sayı değildir.
- Katalogda ayrıca doğrulanan örnekler: Bayraktar AKINCI, KALKAN DİHA, KIZILELMA, Mini İHA, TB2, TB3; TUSAŞ: AKSUNGUR, ANKA-III, GÖKTÜRK-1R/-3, HÜRJET, KAAN, SÜPER ŞİMŞEK, T129 ATAK, T929 ATAK-II. **Envanter'de eksik görünen katalog ürünleri (yeni içerik adayı):** TB3, Mini İHA, KALKAN DİHA, Süper Şimşek, Göktürk-1R/-3 (kontrol edilecek).
- Katalog güncel durum bilgisi vermez ("olacak" gibi ifadeler içerir); durum sütunu hâlâ üretici/SSB duyurusuyla ayrıca doğrulanmalı.
