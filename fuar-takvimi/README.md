# Fuar Takvimi — sıralama ve 2027 tarih kontrolü (10 Kasım 2026)

Takvim, Code Snippets #332 "Fuar Takvimi v2" ile çiziliyor (`[fuar_takvimi]` kısa kodu + `/wp-json/em/v1/fuarlar`).

## Canlıya alınan değişiklik (snippet #332)
- Bitiş tarihi bugünden önce olan fuarlar listeden çıkarıldı (sunucu + tarayıcı tarafında).
- Liste yakın tarihten uzak tarihe sıralanıyor (başlangıç, eşitse bitiş).
- `?gecmis=1` ile REST ucu geçmiş fuarları yine verebiliyor (yönetim/rapor amaçlı).
- `snippet-332-onceki.php`: değişiklikten önceki hâl; `snippet-332.php`: canlıdaki hâl.

## SSB 2027 listesiyle karşılaştırma
| SSB listesi | SSB tarihi | Sitede | Durum |
|---|---|---|---|
| IDEX NAVDEX 2027 (Abu Dabi) | 25-29 Ocak 2027 | 21-25 Ocak (metinde 21-25 Şubat) | Düzeltilecek |
| LAAD 2027 (Rio) | 13-16 Nisan | 13-16 Nisan | Doğru |
| IQDEX (Bağdat) | 17-20 Nisan | yok | Eksik |
| LIMA (Langkawi) | 20-24 Nisan | 20-24 Nisan (metinde 25-29 Mayıs) | Metin düzeltilecek |
| ASDA 2027 (Zagreb) | 27-29 Nisan | yok | Eksik |
| IDEF 2027 (İstanbul) | 3-9 Mayıs | 3-9 Mayıs (metinde 27-30 Temmuz) | Metin düzeltilecek |
| Indo Defence (Jakarta, 2026'dan ertelendi) | 12-15 Mayıs 2027 | "Indo Defence 2026", 18-21 Kasım 2026 | Düzeltilecek (başlık + tarih) |
| FEINDEF 2027 (Madrid) | 18-20 Mayıs | 18-20 Mayıs | Doğru |
| IDET (Brno) | 26-28 Mayıs | yok | Eksik |
| DSEI 2027 (Londra) | 7-10 Eylül | 7-10 Eylül (metinde 14-17 Eylül) | Metin düzeltilecek |
| MSPO 2027 (Kielce) | 31 Ağustos-3 Eylül | 31 Ağu-3 Eyl (metinde 1-4 Eylül) | Metin düzeltilecek |
| TEKNOFEST İstanbul 2027 | Eylül-Ekim 2027 | yok | Kesin tarih yok |
| SIDIF 2027 (Şam) | 6-9 Kasım | yok | Eksik |
| EDEX 2027 (Kahire) | 6-9 Aralık | 6-9 Aralık (metin EDEX 2026, 1-4 Aralık 2026) | Metin düzeltilecek |
| DSEI Germany (Hannover) | 9-12 Mart | yok | Eksik |
| DSEI Japan (Chiba) | 28-30 Nisan | yok | Eksik |
| Seoul ADEX 2027 | 19-24 Ekim | 19-24 Ekim | Doğru |
