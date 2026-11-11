# B/C — GegenSports Editorial Pro: tasarım sistemi

Tüm değerler tek dosyada: `theme/gegensports-editorial-pro/assets/css/tokens.css`.

**Renk:** primary `#101820`, background `#F4F6F8`, surface `#FFFFFF`, text `#17212B`, muted `#64748B`, border `#E2E7EC`, accent `#E85D3F`, success `#168569`, danger `#C74B50`, neutral `#EDF1F5`. Not: beyaz üzerinde metin olarak accent yerine `--color-accent-text #B8431F` (AA 5.3:1) kullanılır; `#E85D3F` yalnızca çizgi/arka plan vurgusudur.
**Boşluk:** 4/8/12/16/24/32/48/64. **Köşe:** 6/10/14. Gölge yok; ince border.
**Tipografi:** sistem fontu + Inter (harici font isteği yok), `clamp()` ile H1 28→40/42, bölüm 21→28, kart 17→19, gövde 15,5→17, ikincil 12–13.
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
