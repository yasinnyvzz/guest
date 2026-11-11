# Türkçe dışı sayfalarda Türkçe site adı ve slogan (Envanter Medya)

## Sorun (canlıdan, 11.11.2026)

| Sayfa | Canlı `<title>` |
|---|---|
| `/en/` | Envanter Medya – Savunma Sanayii Haberleri – Türkiye'nin Savunma Sanayii Haber ve Analiz Platformu |
| `/ar/` | aynı (Türkçe) |
| `/en/category/inventory-en/aselsan-en/` | ASELSAN – Envanter Medya – Savunma Sanayii Haberleri |
| `/es/category/turk-savunma-sanayi-es/` | TÜRK SAVUNMA SANAYİ – Envanter Medya – Savunma Sanayii Haberleri |

Kendi Rank Math başlığı girilmiş yazı ve terimler etkilenmiyor. Etkilenenler: ana sayfalar ile özel başlığı olmayan kategori ve etiket arşivleri. Bu arşivler Rank Math şablonu `%term% %sep% %sitename%` / `%sitename% %sep% %sitedesc%` ile başlık alıyor.

## Kök neden

WordPress site başlığı `Envanter Medya - Savunma Sanayii Haberleri`, slogan ise `Türkiye'nin Savunma Sanayii Haber ve Analiz Platformu`. Polylang'de bu iki dize ("Site Title", "Tagline") TR dışındaki diller için çevrilmemiş; bu yüzden `%sitename%` ve `%sitedesc%` her dilde Türkçe basılıyor.

## Düzeltme

Rank Math şablonu ve Türkçe başlıklar değişmez. Yalnız Polylang dize çevirileri yazılır:

| Dil | Site Title | Tagline |
|---|---|---|
| en | Envanter Medya | Defence Industry News and Analysis from Türkiye |
| ar | Envanter Medya | أخبار وتحليلات الصناعات الدفاعية من تركيا |
| es | Envanter Medya | Noticias y análisis de la industria de defensa desde Türkiye |
| ru | Envanter Medya | Новости и аналитика оборонной промышленности Турции |
| zh | Envanter Medya | 来自土耳其的国防工业新闻与分析 |

**Yol A — panelden, kod yok:** Diller › Dizeler Çevirisi (Translations) › grup "WordPress" › "Site Title" ve "Tagline" satırlarına yukarıdaki değerleri girip kaydedin. Ardından LiteSpeed › Tümünü temizle.

**Yol B — betikle:**
- `uygula.php` dosyasını Code Snippets'e "yalnız bir kez çalıştır" (single-use) olarak ekleyip çalıştırın; ya da `wp eval-file uygula.php` ile çalıştırın.
- Önce mevcut çevirileri `eka_backup_pll_site_20261111` seçeneğine yedekler.
- Zaten çevrilmiş bir dile dokunmaz.
- Sonucu `eka_baslik_slogan_rapor_20261111` seçeneğine yazar ve LiteSpeed önbelleğini temizler.
- Geri alma: `geri-al.php`.

## Beklenen sonuç (yerel test sitesinde doğrulandı: WordPress + Rank Math 1.0.282 + Polylang 3.9.2, aynı şablonlar)

| Sayfa | Önce | Sonra |
|---|---|---|
| `/` (tr) | Envanter Medya - Savunma Sanayii Haberleri – Türkiye'nin … | değişmez |
| `/en/` | Envanter Medya - Savunma Sanayii Haberleri – Türkiye'nin … | Envanter Medya – Defence Industry News and Analysis from Türkiye |
| `/ar/` | aynı (Türkçe) | Envanter Medya – أخبار وتحليلات الصناعات الدفاعية من تركيا |
| `/category/…` (tr) | KAAN – Envanter Medya - Savunma Sanayii Haberleri | değişmez |
| `/en/category/…` | KAAN Fighter Jet – Envanter Medya - Savunma Sanayii Haberleri | KAAN Fighter Jet – Envanter Medya |
| `/ar/category/…` | مقاتلة KAAN – Envanter Medya - Savunma Sanayii Haberleri | مقاتلة KAAN – Envanter Medya |
| Rank Math başlığı olan yazılar | — | değişmez |

İkinci çalıştırmada hiçbir şey değişmedi; `geri-al.php` bütün başlıkları önceki hâline döndürdü.

Site adı aynı zamanda `og:site_name` ve şemadaki yayıncı adını besler. TR dışı dillerde bunlar da "Envanter Medya" olur.

## Kapsam dışı, ayrıca bakılmalı

- **Aktif snippet #374 ("EV Haber Hub v1"):** Başlıktaki ` - Envanter Medya - Savunma Sanayii Haberleri` sonekini ` | Envanter Medya` ile değiştirmeye çalışıyor ama hiç eşleşmiyor. Canlıda ayırıcı `–` (uzun tire). Bu düzeltmeden sonra soneki yalnız Türkçe sayfalarda kalır. Onu da kısaltmak isteniyorsa iki tire biçimini de kapsayacak şekilde düzeltilmeli; bu Türkçe başlıkları değiştirir, ayrı karar ister.
- **Kategori sayfalarında `og:title`:** Terim adı yerine site adını gösteriyor (`Envanter Medya - Savunma Sanayii Haberleri`).
