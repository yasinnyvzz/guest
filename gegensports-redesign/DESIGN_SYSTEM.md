# B/C — GegenSports Editorial Pro: tasarım sistemi

Tüm değerler tek dosyada: `theme/gegensports-editorial-pro/assets/css/tokens.css`.

**Renk (v0.3 — sakin editoryal):** zemin ve kartlar beyaz `#FFFFFF`, mürekkep `#111111`, metin `#1A1A1A`, ikincil `#666B70`, ince çizgi `#E4E4E1`, sakin bant `#F5F5F2`. Tek renkli vurgu koyu saha yeşili `#0B6B50` (yalnız kategori adı, odak halkası, olumlu veri); olumsuz veri `#B3261E`. Lacivert, sarı ve koyu bölümler geri bildirim üzerine kaldırıldı; renk fotoğraflardan gelir.
**Boşluk:** 4/8/12/16/24/32/48/64. **Köşe:** 3/4/6 (daha keskin, gazete hissi). Gölge yok; kutu yerine ince çizgi.
**Tipografi:** başlıklar **Host Grotesk Variable** (referans sitedeki font; temada barındırılır, 2 dosya ≈ 32 KB, OFL, tam Türkçe karakter); gövde sistem fontu/Inter. `clamp()` ölçeği: H1 28→40/42, bölüm 21→28, kart 17→19, gövde 15,5→17. Okuma sütunu 70 karakter.
**Ayrıntı:** kategori tarih satırında; son haberler kutusuz, ince çizgili liste; scouting bölümleri açık gri bant; alt bilgi beyaz, üstte tek siyah çizgi.
**Kurallar:** tamamen açık tema; scouting bağlamı (Gegen Scout bölümü, Dossier üst paneli, arşiv başlığı) açık gri bantla ayrılır. Gradient, glow, animasyon yok.

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
