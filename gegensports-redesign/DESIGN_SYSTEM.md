# B/C — GegenSports Editorial Pro: tasarım sistemi

Tüm değerler tek dosyada: `theme/gegensports-editorial-pro/assets/css/tokens.css`.

**Renk (v0.2, logo ile uyumlu):** primary `#0B1F3A` (logo laciverti), background `#F6F4EF` (sıcak kâğıt), surface `#FFFFFF`, text `#14202B`, muted `#5F6B76`, border `#E4E0D6`, accent `#F2A900` (logo kehribarı; yalnızca çizgi/dolgu), accent-text `#8F5E00` (metin, AA), success `#0F7B5F`, danger `#B83A3F`, neutral `#EFECE4`. İlk brief'teki mercan `#E85D3F` paleti, "yapay zekâ gibi duruyor" geri bildirimi üzerine bırakıldı.
**Boşluk:** 4/8/12/16/24/32/48/64. **Köşe:** 6/10/14. Gölge yok; ince border.
**Tipografi:** başlıklar **Archivo Variable** (temada barındırılır, 2 dosya ≈ 67 KB, OFL lisans, tam Türkçe karakter); gövde sistem fontu/Inter. `clamp()` ölçeği: H1 28→40/42, bölüm 21→28, kart 17→19, gövde 15,5→17, ikincil 12–13. Okuma sütunu 70 karakter.
**Ayrıntı:** başlık üstünde büyük harfli etiket yok — kategori tarih satırında; bölüm başlıkları üstte kalın çizgiyle açılır; seçim rengi, imleç ve kaydırma çubuğu paletten; görseli olmayan haberde boş kutu basılmaz.
**Kurallar:** açık tema; koyu panel yalnızca scouting bağlamında (Gegen Scout bölümü, Dossier üst paneli, arşiv başlığı). Gradient, glow, animasyon yok.

## Bileşen → dosya
| Bileşen | Yer |
|---|---|
| SiteHeader / PrimaryNavigation / MobileNavigation | `template-parts/site-header.php`, `mobile-nav.php`, `assets/js/ui.js` (~1 KB, framework yok) |
| SectionHeader, LeadStory, StandardNewsCard, CompactNewsRow, PlayerCard, EmptyState, Pagination, Sidebar | `inc/components.php` |
| Breadcrumbs, SourceDisclosure | `inc/helpers.php`, `single.php` |
| GegenVerdict, PlayerProfileHeader, FM27 paneli | `page-templates/dossier.php` |
| RankingCard, ComparisonTable | `front-page.php`, `template-parts/single-ranking.php` |
| SiteFooter | `template-parts/site-footer.php` |
| GegenDNAChart, GegenFitPanel, LeagueTable, ClubHeader | **Yapılmadı** — gerekçe: kaynak veri yok (aşağıya bakın). Takım/lig başlığı `archive.php` içinde. |

## Veri kuralları (kod ile uygulanır)
- Boş alan → bileşen gizlenir (`—` ya da hiç render edilmez); "0.0" ve "Özet Bulunamadı" basılmaz.
- Boş şablon kalıntısı "()" metinden temizlenir (`gsx_clean_text`).
- Maç şeridi yalnızca `gsx_match_data` filtresi gerçek veri döndürürse görünür; **varsayılan boş** → sahte maç yok.
- Rozet: kart başına tek kategori; "Uncategorized/Genel/dil" kategorileri gizlenir.
- Haber ≠ scouting: ana sayfa haber havuzu scout kategorilerini dışlar; scout kartları ayrı tür.
- FM27 oyun verisi ayrı panelde ve açık uyarıyla.
