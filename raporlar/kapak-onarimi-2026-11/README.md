# Ortak kapak dosyası onarımı (10 Kasım 2026)

Sitedeki WebP dönüştürücü, aynı adla yüklenen görselin `.webp` dosyasının üzerine yazıyor.
Aynı adla yüklenen kapaklar (ör. `kapak.png`, `haber-ar-kapak.png`, `cover-en.png`) bu yüzden
tek bir fiziksel dosyayı paylaştı ve yazılar başka haberin kartını gösterdi.

## Düzeltilen (374 yazı)
- 8 TR haber (`yayin-araclari/kapak_onar.py`): Lockheed, Pakistan Fa'az, Belçika Skyranger,
  Fransa FDI, İsveç Taurus, RTX, SUNGUR, SİPER.
- 366 yazı (`yayin-araclari/kapak_onar_toplu.py`, liste: `duzeltilen_kapaklar.csv`):
  çoğu AR (`haber-ar-kapak.webp` 323 yazı), ayrıca RU, EN, ES, ZH kartları ve CTech/MSPO
  yazısı (fotoğrafı Tanzanya fotoğrafıyla ezilmişti, özgün fotoğraf kurtarılamadı; başlık kartı verildi).
- Her yazıya `<post_id>-<dil>-kapak.webp` adlı kendi kartı verildi; Polylang medya grupları kuruldu.

## Düzeltilmeyen, karar bekleyen: kopya yazılar (`kopya_yazilar.csv`)
32 grupta 1.726 yayında EN/ES yazı aynı haberin kopyası (ör. "The U.S. Army purchases 82 P550…"
345 kez). Kapakları doğru, sorun yazıların kendisi. Hiçbir şey silinmedi.
`öneri` sütunu her grupta kalması önerilen tek yazıyı gösterir (çeviri grubuna bağlı olan ya da en eskisi).
