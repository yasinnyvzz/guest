# D–M — Uygulama durumu, QA, performans, SEO, yayın planı

## Ne yapıldı / ne yapılmadı (dürüst durum)
**Yapıldı (çalışan kod, gerçek WordPress 6.x + Polylang üzerinde yerel test, gerçek canlı içerikle):**
`theme/gegensports-editorial-pro` — bağımsız tema. 7 şablon + yardımcılar:
1. Ana sayfa `front-page.php` · 2. Haber detay `single.php` · 3. Scout merkezi `page-templates/scout-center.php` (+ `/dossier/` dizini) · 4. Gegen Dossier `page-templates/dossier.php` (rota `/dossier/{rapor-slug}`) · 5. Gegen Rankings `template-parts/single-ranking.php` · 6. Takım/lig/kategori arşivi `archive.php` · 7. İngilizce ana sayfa (aynı `front-page.php`, `/en/`). Ek: arama, 404, `/haberler/` arşivi, sayfa, mobil çekmece + alt navigasyon.
Ekran görüntüleri: `audit/after/{1440,1280,768,390,360}-*.png` (10 sayfa × 5 genişlik = 50). Otomatik kontrol (`audit/after/metrics.json`): 50/50 sayfada yatay taşma yok, tek H1, "()"/"undefined"/"Özet bulunamadı" sızıntısı yok.

**Yapılmadı / sınırlar:**
- **Canlı siteye hiçbir şey uygulanmadı.** Bu oturumda gegensports.com için yazma yetkisi/yedek/staging yok; ayrıca Olivin ve GPScout kaynak kodu depoda yok.
- `/scout` GPScout eklentisinin kendi koyu uygulaması (giriş, harita, mesajlaşma). Eklenti şablonu görmeden yeniden tasarlanmadı; yeni editoryal merkez ayrı sayfa olarak (`Gegen Scout` şablonu, öneri slug `gegen-scout`) geliyor. `/scout` olduğu gibi kalır.
- **Maçlar sekmesi, lig tablosu, form grafiği, Gegen DNA, Gegen Fit** yapılmadı: güncel maç/puan veri kaynağı veya normalize edilmiş DNA/Fit verisi API'de yok; sahte ekran üretilmedi. Maç şeridi için `gsx_match_data` filtresi hazır.
- Oyuncu "benzer futbolcular", "kariyer geçmişi" panelleri veri yokluğundan yok; `playerProfile` alanı kenar panelde gösteriliyor.
- Gegen Rankings veri modeli: yazı meta `gsx_ranking` (JSON). **Yönetim arayüzü (metabox) yok**; şu an elle/REST ile giriliyor. Testteki sıralama bir şablon fixture'ıdır, yayın içeriği değil.
- Dossier fotoğrafı bazı raporlarda kare portre değil geniş kapak görseli (veri kaynağı); kırpma görünür.
- Çeviri ilişkili hreflang tema tarafından **üretilmiyor** (Polylang/Rank Math/GSX üretmeye devam eder; tema başlık/canonical'a dokunmaz).
- Title/meta/schema/breadcrumb JSON-LD, sitemap tema dışı eklentilerde kalır; tema yalnızca görünür breadcrumb basar. Yeni `/dossier/*` ve `/haberler/` rotaları için başlık eklendi, **meta description/canonical/schema yok** → yayında `noindex` veya SEO eklentisi eşlemesi gerekir.
- Erişilebilirlik: klavye odağı, skip-link, `aria-*`, 44 px hedef, kontrast token'larla AA hedeflendi; **resmî WCAG denetimi (axe/Lighthouse) yapılmadı.**
- GP Scout/Report/Radar/Watch/Signal kategorileri "Scouting" menüsü altında toplandı; kullanıcı dostu açıklamalar için editoryal onay gerekir.
- Footer'da Kaynak politikası ve Gizlilik sayfaları canlı sitede **404**; sayfalar oluşturulana kadar bağlantı gizli kalır.

## Performans (K) — `audit/perf.json`, mobil 390, Playwright
| | LCP | CLS | İstek | JS dosyası | DOM | Aktarım (bildirilen) |
|---|---|---|---|---|---|---|
| Canlı ana sayfa (Olivin) | 2,78 s | 0,048 | 107 | 23 | 1.274 | ~2,9 MB |
| Canlı makale | 1,43 s | 0,049 | 80 | 17 | 1.357 | ~3,4 MB |
| Yeni ana sayfa (yerel) | 0,17 s | 0 | 13 | 1 | 383 | ~125 KB |
| Yeni makale (yerel) | 0,15 s | 0 | 6 | 1 | 422 | ~82 KB |
**Uyarı:** yeni değerler localhost'tur (ağ/CDN yok, GA/reklam/GPScout/video widget'ları ve LiteSpeed yok). Karşılaştırılabilir **değildir**; yapısal azalma (istek, JS, DOM, harici font yok) gerçektir. Gerçek hedefler (LCP ≤2,5 s, CLS ≤0,1, INP ≤200 ms) staging'de CrUX/Lighthouse ile ölçülmelidir.

## SEO güvenlik listesi (L)
- [ ] Mevcut URL'ler değişmedi (yeni rotalar yalnız ekleme: `/haberler/`, `/dossier/…`).
- [ ] Staging'de eski/yeni için H1, `<title>`, meta description, canonical, hreflang, JSON-LD, breadcrumb schema karşılaştırması (50 URL örneklemi).
- [ ] Rank Math/GSX çıktısının `wp_head`'de korunduğunu doğrula (tema `title-tag` desteği açık, kendi meta basmıyor).
- [ ] Olivin'in kendi schema/breadcrumb/OG çıktısı varsa yeni temada karşılığı var mı kontrol et (**bilinmiyor** — Olivin kaynağı görülmedi).
- [ ] Sayfalama (`/page/N`) ve kategori arşivi canonical'ları; görsel alt metinleri (tema `alt` = başlık verir, öne çıkan görsel alt'ı varsa onu tercih etmeli — **iyileştirme gerekli**).
- [ ] Sitemap yolu (`/sitemap_index.xml` 404) ve Search Console'da kapsam izleme (yayın sonrası 14 gün).
- [ ] `/dossier/*` indekslenecek mi kararı (GPScout rapor içeriği ile yinelenme riski → canonical stratejisi).

## Yayın planı (M) — onay gerektirir
1. Tam yedek (DB + `wp-content`), Olivin ayarları (Customizer/tema seçenekleri, menüler, widget) dışa aktar.
2. Canlının kopyası staging'e; `gegensports-editorial-pro` yükle, **etkinleştirmeden** önce ekran karşılaştırması.
3. Staging'de: Olivin'e özgü shortcode/blok/widget kullanan içerikleri tara (`grep` ile `[olivin` vb.), GPScout/GP-Hub shortcode'larının sayfalarda çalıştığını doğrula, LiteSpeed önbelleği temizle, Polylang menü/dil anahtarı kontrolü.
4. Yeni sayfalar: `Gegen Scout` (şablon seç), Gizlilik, Kaynak politikası, (isteğe bağlı) Gegen Rankings.
5. QA: 5 genişlik, Lighthouse/axe, SEO listesi.
6. **Onayınızla** canlıda etkinleştir; geri dönüş = Görünüm'den Olivin'i tekrar etkinleştirmek. İlk 48 saat Search Console + 404 logu izle.

## Yerel yeniden üretim
`dev/` : harness mu-plugin (canlı GPScout API'sine salt-okunur proxy), seed betiği, ekran görüntüsü/performans betikleri. WordPress + SQLite + Polylang ile çalıştırılır.
