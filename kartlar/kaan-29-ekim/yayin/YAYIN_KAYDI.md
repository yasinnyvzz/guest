# KAAN 29 Ekim galeri haberi — yayın kaydı

Durum: **yayına hazır, henüz yayımlanmadı.** Bu oturumda envantermedya.com'a yazma yetkisi olan kimlik bilgisi yoktu (ortamdaki `WP_*` değişkenleri thedailyenergy.com'a ait).

Paket:
- `haber.json`: başlık, slug, özet, kategoriler, Rank Math alanları, metin ve galeri sırası
- `kaan-29-ekim-kapak.jpg`: 1200×675 öne çıkan görsel (lacivert zemin, altın şerit)
- `kaan-29-ekim-kart-1…5.jpg`: galeri kartları (1080×1350)
- `yayinla.py`: yükleme ve yayın betiği

Hedef: TR, slug `29-ekimde-gozler-kaandaydi`, kategoriler KAAN – MMU (333), TUSAŞ (332), HABERLER (53), Savunma Haberleri (24795). Galeri tek sütun, görseller tam boy ve tıklanınca büyüyor.

Yayın:
```
export ENVANTER_WP_USER=...            # ortam ayarından
export ENVANTER_WP_APP_PASSWORD=...    # ortam ayarından
python3 kartlar/kaan-29-ekim/yayin/yayinla.py            # yayına alır
python3 kartlar/kaan-29-ekim/yayin/yayinla.py --taslak   # taslak bırakır
```
