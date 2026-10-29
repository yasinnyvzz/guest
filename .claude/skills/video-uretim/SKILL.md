---
name: video-uretim
description: Claude Code + HyperFrames ile Envanter Medya (ve diğer işler) için animasyonlu video üretir. Açıklayıcı Reel (anlatım sesli, kelime kelime beliren başlık) ve tek planlı marka reklamı iş akışlarını, ElevenLabs ile Türkçe seslendirmeyi ve Envanter marka kurallarını içerir. "video yap", "Reel hazırla", "reklam filmi", "seslendirme", "HyperFrames" gibi isteklerde kullan.
---

# Video üretimi (HyperFrames + Claude Code)

Kaynak: @aygramm.ai'nin iki rehberi. Fikir: Claude her sahneyi web sayfası olarak tasarlar, HyperFrames (ücretsiz, açık kaynak) bunu kare kare MP4'e çevirir. Kullanıcı kod yazmaz, onay verir.

Akış her zaman: **Fikir → Senaryo → Prompt → Önizleme (still) → onay → Render → MP4**

## Kurulum (bir kez)
- Node.js 22+ ve ffmpeg gerekir; eksikse kur. Her komutu önce basit sözlerle açıkla.
- HyperFrames skill'leri: `npx skills add heygen-com/hyperframes` (hyperframes, hyperframes-animation, hyperframes-keyframes, product-launch-video, media-use, hyperframes-audio, isteğe bağlı no-ai-slop). Eklendikten sonra yeni oturum gerekebilir.
- Bulut oturumunda render yavaş/kısıtlı olabilir; ağır render için kullanıcının bilgisayarındaki Claude Code (Code sekmesi, Local klasör) önerilir. Bu ortamda senaryo, prompt ve sahne planı her zaman hazırlanabilir.

## İş akışı A: Açıklayıcı Reel (Level Zero)
Format: ~45 sn, 1080x1920, 30fps. Haber özeti, veri/infografik, "X gelişme" videoları için.

1. **Senaryo (~130 kelime, 45–55 sn):** sayılı kanca → sürpriz/dönüş → maddeler (ad + tek kısa cümle) → çağrı ("KELİME yaz, sana gönderelim"). Her cümlede tek fikir. Kanca için 3 seçenek sun. Yüksek sesle okununca doğal olmalı; kısaltmaları okunacağı gibi yaz.
2. **Prompt şablonu:** "En iyi motion ve ses tasarımcısısın. HyperFrames skill'lerini kullan. [45] sn dikey Reel (1080x1920, 30fps) yap. SENARYO (kelimesi kelimesine): […]. GÖRÜNÜM: [marka renkleri/zemin]. Başlık üstte, söylenen cümle; her kelime söylendiği anda yumuşak fade-up ile belirir. Cümle başına bir anahtar kelime vurgulu. Altında her cümle için tek animasyonlu kart (uygulama penceresi, liste, telefon maketi, sayaç). Metin ortadaki %80'in içinde. SES: seslendirme üstte, her pop/tik/whoosh için küçük efekt, müzik çok kısık. SÜREÇ: önce plan ve birkaç önizleme karesi göster, `hyperframes check` çalıştır, ben 'render' diyene kadar MP4 üretme."
3. Önizlemeyi tarayıcıda göster, düzeltmeleri normal cümleyle uygula, onayda render + en iyi kareden kapak.

## İş akışı B: Tek planlı marka reklamı
Format: 30 sn, 9:16, 1080x1920, **60fps** master, motion blur. Tanıtım filmi, ürün/uygulama videosu için.

- Dosyalar: resmî logo (SVG/PNG, **asla yeniden çizme**) ve gerçek uygulama/site ekran kaydı (30–60 sn). Kişisel isim/bakiye gizlenir.
- Prompt omurgası: marka, tek bir vaat (açı), tema ve renk kodları, açılış (logo → morph), hero sahne, "TEK KESİNTİSİZ ÇEKİM, her sahne öncekinden dönüşerek çıkar, slayt kesmesi yok", hero öncesi başlık, sonda logo + slogan, ses (müzik+efekt veya seslendirme+müzik), son 3 sn imza.
- Çalışma sırası: (1) kısa seçenekli sorular, (2) saniye saniye beat sheet, onay bekle, (3) ~20 karelik kontak sayfası, onay bekle, (4) ses tasarımı, 60fps render, ses **-14 LUFS**, MP4.
- Render ~25 dk/30 sn sürer. İndirme yapmadan veya onaylanmış bir şeyi değiştirmeden önce sor.

## Ses
- **Seçenek 1 (ücretsiz):** HyperFrames yerleşik sesi. Önce 2–3 sesi dinlet. Türkçe kalitesini denemeden varsayma.
- **Seçenek 2 (ElevenLabs, kullanıcının hesabı var):** Türkçe için `eleven_multilingual_v2` veya güncel çok dilli model; hazır (kütüphane) sesler. Gerçek kişileri taklit eden klon kullanma.
  - API anahtarı yalnızca ortam değişkeninde (`ELEVENLABS_API_KEY`). Sohbete yapıştırtma, dosyaya/commit'e yazma, çıktıda gösterme. Yoksa ortam gizli değişkenlerinden eklemesini söyle.
  - Ağ erişimi `api.elevenlabs.io` için açık olmalı; engelliyse söyle.
  - **Sesi cümle cümle üret, klipleri birleştir.** Uzun tek kaydı kırpmak kelime uçlarını keser. Yalnızca gerçek sessizlikleri kısalt.
  - Başlamadan önce toplam karakter sayısını ve kotadan düşeceğini söyle; önce 1 cümlelik deneme klibi dinlet; her senaryo için onay al.
  - Her cümleyi ayrı dosya yap, süreleri sahne zamanlamasına bağla (kelime/cümle zamanlaması ses süresinden gelir).

## Müzik ve efekt
- Pixabay (müzik, efekt) ve Openverse (gerçek kayıtlar). CC0 tercih et, "NonCommercial" olanlardan kaçın. Pixabay'de **"Content ID registered"** parçaları kullanma. 3 seçenek sun, kullanıcı seçsin.
- Miks: ses en yüksek, efektler sonra, müzik en kısık; müzik konuşmanın altında kısılır ("voiceover carve"). Her ses ekranda görülen bir şeye karşılık gelsin, rastgele whoosh olmasın. Hero anında müzik "drop" yapabilir.

## Sık hatalar
Müzik yüksek · söylenmemiş kelimeyi önceden göstermek · tek uzun ses kaydını kırpmak · metni kenara yakın koymak (Instagram butonları kapatır; orta %80) · erken render (önce still) · başkasının stilini/maskotunu birebir kopyalamak.

## Düzeltme usulü
Düzeltmeleri **zaman damgasıyla ve tek mesajda** iste ("9.0 sn'de harita çok koyu"). Claude hepsini topluca uygular, değişen anların still'lerini gösterir, sonra yeniden render eder. Kullanıcı "pause" derse render durur. Bitince "öğrendiklerimizi kaydet" ile ses, renk ve miks tercihleri bu dosyaya eklenir.

## Envanter Medya uyarlaması
- **Marka:** lacivert zemin, altın şerit, "ENVANTER MEDYA" kimliği (kapak kartlarıyla aynı); logolar `kartlar/marka/` altında (`envanter-logo-white.png`, `-red.png`, `-black.png`). Logoyu olduğu gibi kullan. Renk kodlarını mevcut kartlardan örnekle.
- **Dil:** Türkçe anlatım/altyazı; gerekirse EN/AR/ES/RU sürümleri. Caption ve Reels senaryosu için `envanter-sosyal-icerik` skill'ini kullan.
- **Doğruluk ve kaynak:** Rakamları ve olguları yayından önce kontrol ettir. Defence Türk, GDH gibi Türk savunma siteleri kaynak olarak gösterilmez; yalnız konu ipucudur, asıl kaynak (resmî duyuru, bülten, ajans, yabancı özel yayın) bulunur. Bulunamayan olgu videodan çıkarılır. Bkz. `ENVANTER_YAYIN_REHBERI.md`.
- **Telif:** Üçüncü kişilerin fotoğraf/logosu için izin ve kaynak notu; müzikte Content ID kontrolü.
- **Özgünlük:** Başka yayınların metnini kopyalama; senaryo özgün yazılır.
- **Diğer işler:** Aynı yöntem eğitim anlatımı, sunum özeti, ürün/hizmet ve etkinlik duyurusu için de kullanılır; marka bölümünü ilgili işe göre değiştir.
