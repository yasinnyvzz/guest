# Envanter staging kurulum listesi — envanter-konu-arsivleri 0.1.0

Paket: `envanter-konu-arsivleri-0.1.0.zip`
SHA-256: `ee1f271ec0fe596914cda47c76170da65ca5a0ebf82f3f00ac66eeb0dc5471ec`

## Ön koşullar

- Staging, canlının **güncel bir kopyası** olmalı: aynı veritabanı (terim kimlikleri `veri/hublar.json` ile eşleşsin diye), Polylang, Rank Math + Rank Math Pro ve olivin/olivin-child teması.
- Staging arama motorlarına kapalı olmalı: Ayarlar › Okuma › "Arama motorlarını engelle" ya da HTTP parolası.
- LiteSpeed önbelleği staging'de kapalı olmalı ya da her adımdan sonra temizlenmeli.
- Toplu sınıflandırma ve hub kurulumu WP-CLI ile yapılır. SSH yoksa 1–3. adımlar yine yapılabilir; 4–6. adımlar için SSH gerekir.

## Adımlar

1. **Yükle:** Eklentiler › Yeni Ekle › Eklenti Yükle › zip › Etkinleştir.
   - Beklenen: sitede görünür bir değişiklik olmaz. Hub eşlemesi yokken haber altı kutusu ve arşiv modülleri basılmaz, robots ayarları değişmez.
   - Tek görünür değişiklik: yazı düzenleme ekranında "Akıllı Arşiv Önerileri" kutusu çıkar.
   - Veritabanına `wp_eka_log` tablosu eklenir.
2. **Editör kutusu:** Herhangi bir KAAN haberini açın › "Önerileri getir". Liste gelmeli; "Bu dilde arşivi yok" uyarısı normaldir, eşleme henüz yüklenmedi. Yazıyı kaydetmeyin.
3. **Hata günlüğü:** `wp-content/debug.log` ya da sunucu hata günlüğünde `envanter-konu-arsivleri` kaynaklı uyarı olmamalı.
4. **Eşleme:**
   ```
   wp eka hub-ice-aktar hublar.json --site=ev           # kuru: "N eşleme bulundu, 0 terim bu sitede yok" beklenir
   wp eka hub-ice-aktar hublar.json --site=ev --uygula
   ```
5. **İki pilot hub:**
   ```
   wp eka hub-kur seo_metinleri.json --dil=tr --varlik=kaan,aselsan            # kuru
   wp eka hub-kur seo_metinleri.json --dil=tr --varlik=kaan,aselsan --uygula
   wp eka denetle
   ```
   `/category/envanter/tusas/mmu/` ve `/category/envanter/aselsan/` sayfalarını **olivin temasında**, masaüstü ve mobilde kontrol edin: H1, tanıtım, son güncelleme, ilgili arşivler, `<title>`, meta açıklama, robots, canonical ve 2. sayfa.
6. **Pilot sınıflandırma ve geri alma provası:**
   ```
   wp eka siniflandir --dil=tr --varlik=kaan --rapor=kaan.csv                   # kuru; kaan.csv'den 20 satırı editör kontrol eder
   wp eka siniflandir --dil=tr --varlik=kaan --guven=yuksek --uygula
   wp eka partiler
   wp eka geri-al <parti> --uygula                                              # geri almanın çalıştığını doğrulayın
   ```
   Uygulama sonrasında kontrol edin:
   - Bir KAAN haberinin altında "İlgili Haber Arşivleri" kutusu var mı?
   - Haber kartlarındaki kategori etiketi ve breadcrumb değişmedi mi? Rank Math birincil kategorisi korunmalı.
   - EN/AR çevirilerine Polylang eşitlemesiyle terim geçtiyse `wp eka partiler` çıktısında `add_sync` görünmeli.
   - Arapça haberde kutu sağdan sola akıyor mu?

## Geri dönüş

- Önce `wp eka geri-al <parti> --uygula` ile eklenen terimleri kaldırın, sonra eklentiyi devre dışı bırakın.
- Hub meta'ları (`eka_*`) ve Rank Math terim başlık/açıklamaları kalır; eklenti kapalıyken hiçbir etkileri olmaz. Rank Math alanları hub kurulumundan önce boştu; gerekirse elle temizlenir.
