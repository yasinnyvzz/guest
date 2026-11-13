# Envanter Medya — Video Üretim Kuralları (TÜM videolar için bağlayıcı)

Bu dosya her Reels / Shorts / TikTok / açıklayıcı video için geçerlidir. Video üretmeye başlamadan
önce okunur, teslimden önce aşağıdaki kontrol listesi tek tek uygulanır. Kural dışına çıkmak için
kullanıcıdan açık onay gerekir.

## 0. Kural çıkış noktası
"Radarların Görünmeyen Gücü" videosunun incelemesinden çıkan hatalar: statik kart şablonu,
aynı karenin 6-8 sn donması, her kartta tekrar eden uyarı, görüntüden bağımsız altyazı kutusu,
geçişsiz kesmeler, düşük çözünürlük (720×1280). Bunlar bir daha tekrarlanmaz.

## 1. Kurgu: akıcılık
- Tek sürekli görsel hikâye kur. Her cümleye yeni kart açma; aynı öğeyi hareket ettirerek
  (zoom, pan, parallax, morph, katman açma) bir sonraki bilgiye taşı.
- Hiçbir kare 2 sn'den uzun hareketsiz kalmaz. Her sahnede en az bir hareket olur
  (çizgi çizilmesi, sayı sayma, sinyal akışı, kamera hareketi).
- Geçiş: düz kesme yok. Kayma, mask/wipe, ölçek geçişi, morph. Tüm videoda tek hareket dili.
- Aynı şablonu (başlık + çizgi + 2 kutu) art arda 2'den fazla kullanma. Düzen sahneye göre değişir.
- Ritim: kanca soru → görsel cevap → sonraki soru. Sahne süresi çoğunlukla 2-4 sn.
- İlk 2 sn kanca (hareketli görüntü + tek satır). Son sahne 2 sn: tek cümle sonuç + logo.

## 2. Görsel
- Gerçek görüntü/fotoğraf varsa arka plana al, üstüne tek satırlık vurgu yaz. Metin de hareket etsin.
- Ekranda aynı anda en fazla 8-10 kelime.
- Kimlik: siyah, kırmızı (#C0392B), açık gri zemin; sahneye göre koyu zemin serbest. Logo sabit, küçük.
- Kaynak kartı (örn. "ASELSAN 2018 Faaliyet Raporu, s.108") tam ekran değil, 2-3 sn'lik ekran-içi öğe.

## 3. Altyazı
- Kelime kelime vurgulanan (karaoke), alt-orta güvenli alan, kutusuz veya yarı saydam şerit.
- Ses ile birebir senkron (kelime zaman damgası faster-whisper ile çıkarılır).
- Platform arayüzünün altında/sağında kalan bölgeye taşmaz (alt ~250 px ve sağ ~120 px boş).

## 4. Uyarı ve kredi metinleri
- "Temsili animasyon / ürün modeli değildir" uyarısı videoda yalnızca BİR kez, ~2 sn, küçük.
  Açıklama (caption) satırına da yazılır. Her kartta tekrar edilmez.
- Görsel kredisi yalnızca ilgili sahnede, kısa ve küçük.

## 5. İçerik doğruluğu
- Rakam, tarih, kurum adı ve alıntı kaynağıyla birebir kontrol edilir. Tarihsel beyan, güncel
  iddiaya çevrilmez ("bütün radarlar tamamen yerli" gibi genelleme yapılmaz).
- Kaynaksız iddia videoya girmez. Belirsizse "…beyan edilmiştir" kalıbı kullanılır.
- Türkçe metin `turkce-humanizer` ile yapay dil izlerinden arındırılır (uzun tire, kalıp cümleler).

## 6. Teknik çıktı
- 1080×1920 (9:16), 30 fps, H.264 + AAC, yüksek bit hızı. 720p teslim edilmez.
- Ses: -14 LUFS, TTS ise `chatterbox-tts`, gerekirse insan sesi.
- Üretim: Remotion veya Hyperframes (kodla). Gerekli araçlar `video-araclari/kurulum.sh` ile kurulur.
- Render sonrası `video-araclari/kontrol.sh` çalıştırılır.

## 7. Teslimden önce kontrol listesi (hepsi "evet" olmalı)
1. Çözünürlük 1080×1920 mi? (kontrol.sh)
2. Donmuş kare var mı? (kontrol.sh `freezedetect` 2 sn üstü raporlar → düzelt)
3. Sahne kesmeleri kontrol.sh'de ortalama 2-4 sn mi?
4. Altyazı kelime kelime, senkron, güvenli alanda mı?
5. Uyarı metni tek kez mi? Kaynak/kredi kısa mı?
6. Metin taşması, kırpılma, okunmaz küçük yazı var mı? (3-4 kareden ekran görüntüsü al, bak)
7. Rakam/kaynak doğrulandı mı?
8. Çıktı: MP4 + sahne listesi (saniye aralığı, görsel, metin, hareket türü).

## 8. İş akışı
1. Konu + kaynaklar → senaryo (kanca, 6-10 sahne, sonuç).
2. Sahne listesi (hareket türüyle) kullanıcıya gösterilir.
3. Ses/seslendirme → kelime zamanları → kurgu.
4. Render → kontrol.sh → kare kare gözden geçir → teslim.
Referans video verilirse önce `reverse-any-video` ile yapısı çözülür, hataları listelenir.
