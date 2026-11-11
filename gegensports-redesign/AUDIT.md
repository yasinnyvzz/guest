# A — GegenSports mevcut tasarım denetimi (11 Kasım 2026)

Yöntem: canlı site yalnızca **okundu** (herkese açık sayfalar + herkese açık REST); Playwright ile masaüstü 1440 ve mobil 390 ekran görüntüleri `audit/before/` altında. Canlı siteye hiçbir yazma yapılmadı.

## Teknik tespit (doğrulanmış)
- Tema: **Olivin** (`/wp-content/themes/olivin`), 24 kaynak referansı. Kaynak kodu bu depoda **yok**; ticari tema.
- Eklentiler (REST ad alanlarından): Polylang (`pll/v1`), LiteSpeed Cache, GPScout (`gpscout/v1`, `gp-hub`, `gp/v1`), GSX (`gsx/v1`, SEO/şema), GNL (`gnl/v1`, bülten), Code Snippets, license.
- Diller: TR / EN / ES (hreflang var). Sitemap `/sitemap_index.xml` 404 döndü (başka bir yolda olabilir — doğrulanmalı).
- Sayfa başına: ana sayfa 107 istek, ~3 MB, 23 JS dosyası, 7 CSS, 1.274 DOM düğümü; makale 80 istek, ~3,5 MB, 17 JS.
- 34–50 farklı arka plan rengi, 5 font ailesi (Noto Sans, Bebas Neue, Inter, Font Awesome Pro, Google Sans Text), 20–35 farklı yazı boyutu / sayfa.

## İstenen 15 kontrol maddesi
| # | Madde | Sonuç |
|---|---|---|
| 1 | Çok menü/alt menü | **Doğrulandı.** Ana sayfada ~47–53 gezinme bağlantısı; ayrı üst bar + ana menü + yan yüzen araç çubuğu + GPScout'un kendi 12 öğeli menüsü. |
| 2 | Aynı görünümlü kartlar | Doğrulandı (ana sayfa/arşivlerde aynı kart). |
| 3 | Etiket/kategori kalabalığı | **Doğrulandı.** Makalede 4 yeşil rozet; kenar çubuğunda "Uncategorized (112)" ve ilgisiz "Basketbol Türkiye" gibi kategoriler görünüyor. |
| 4 | Boş scout kartları | Bu örneklemde görülmedi. |
| 5 | "Özet Bulunamadı" | **Görülmedi** (taranan 20 sayfada yok). |
| 6 | Hatalı/eksik profil istatistikleri | **Kısmen.** GPScout API'sinde ilk 40 rapor özetinin **23'ü boş "()" şablon kalıntısı** içeriyor ("…FC Gagra formasıyla oynuyor ()"). |
| 7 | TR/EN/ES karışıklığı | **Doğrulandı.** REST listesi dil filtresi uygulamıyor (TR liste EN yazıları döndürdü); kategori listesinde "Español", "English" gibi dil kategorileri normal kategoriler arasında. Makale sayfasında kendi dilinde olmayan kategori adları var. |
| 8 | Kayan bantlar | Ana sayfada ticker görülmedi. Yüzen "Gegen Pres — Son Video" oynatıcısı içerik üstünü kapatıyor ve **"Video unavailable"** gösteriyor (masaüstü + mobil). |
| 9 | Güncel olmayan puan durumu | Taranan sayfalarda puan durumu yok; kontrol edilemedi. |
| 10 | İlgisiz modüller | Kenar çubuğunda "Basketbol Türkiye"; kripto/finans ticker'ı görülmedi. |
| 11 | Hazır tema isimleri / demo | **Doğrulandı:** tema `olivin`; kategori "Uncategorized" (112 yazı) görünür; sayfa `<title>` kalıntıları yok. "Olivin – Blog ve Haber Teması" başlığı sayfada **görünmüyor**. |
| 12 | Mobil boşluklar | **Doğrulandı:** logo ile yüzen tema düğmesi/araç çubuğu çakışıyor, hero görselin üstüne biniyor (`audit/before/mobile-home.png`). `/genc-yetenek-hub/` mobilde **143.648 px** yükseklik, 558 görsel. |
| 13 | Tutarsız font/boyut | Doğrulandı (5 aile, 20–35 boyut). |
| 14 | Çok renkli rozet | Doğrulandı (yeşil, turuncu, mavi rozetler aynı ekranda). |
| 15 | Çok vurgu rengi | Doğrulandı (turuncu, altın, yeşil, mavi, lacivert + GPScout'ta ayrı koyu tema). |

## Diğer bulgular
- `/scout` **ayrı bir koyu uygulama** (GPScout, `scrollWidth` 1722 > 1440 → **yatay taşma**; 839 görsel; mobilde "0.0"-benzeri sayılar). Kendi 12 öğeli menüsü var; site temasından tamamen farklı kimlik.
- `/genc-yetenek-hub/` masaüstünde 64.553 px, 570 görsel.
- "FM27'nin Yeni Yüzleri: 22 Genç Yetenek, 100 Üzerinden Puan" yazısı ve GPScout `ratings`/`hiddenAttrs` alanları: kaynaksız puan ve **FM oyun verisi** ile gerçek performans aynı yerde. Yeni Dossier bunları ayırır.
- GPScout rapor alanlarında örnekler arası **birebir aynı** değerler var (ör. "Çoklu maç / Orta-yüksek / Bölge üstü potansiyel / Hücumcu bek", aynı "Bölge radarında tutulmalı…" önerisi). Bu şablon üretimi izlenimi verir; **editoryal denetim önerilir** (tema bunu düzeltemez; veri katmanı sorunu).
- Mobil makale 14.093 px; ilk ekranda yüzen çubuk + video penceresi.

Ekran görüntüleri: `audit/before/*.png`, metrikler `audit/before/metrics.json`.
