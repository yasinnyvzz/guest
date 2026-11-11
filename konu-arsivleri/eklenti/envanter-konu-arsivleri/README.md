# Envanter Konu Arşivleri (WordPress eklentisi)

Şirket, ürün, ülke ve teknoloji arşivlerini (topic hub) **mevcut kategori ve etiket URL'leri üzerinde** kurar.
Yeni URL yapısı (`/konu/`, `/sirket/`) açmaz; mevcut URL'ler, hreflang grupları ve Rank Math ayarları korunur.

## Ne yapar

| Bileşen | Davranış |
|---|---|
| Hub arşiv sayfası | Hub işaretli terimde tema açıklamasının altına: özgün tanıtım (yalnız 1. sayfa), son güncelleme + haber sayısı, editörün seçtiği öne çıkan haberler, ilgili arşivler, "Son … Haberleri" başlığı. Haber listesi temanın kendi döngüsüdür (yeniden eskiye, sayfalı). |
| Haber altı kutusu | "İlgili Haber Arşivleri / Related News Topics / مواضيع إخبارية ذات صلة": yazının bağlı olduğu ve indekslenebilir hub arşivlerine 2–7 gerçek `<a href>` bağlantı. JS yok. Arapçada `dir="rtl"` taşır (EV temasının `body.rtl{direction:ltr}` kuralından etkilenmez). |
| Editör öneri kutusu | Başlık + özet + gövde analiz edilir; öneriler güven düzeyiyle listelenir. Editör onaylamadan hiçbir terim eklenmez. Gutenberg ve klasik editör. |
| Kalite kapısı | Hub yalnız şu koşullarla `index`: ≥5 yazı, ≥40 kelime özgün tanıtım, sözlükte varlık eşlemesi, son 12 ayda yazı. Aksi hâlde `noindex, follow`. Hub olmayan terimlerde sitenin mevcut ayarı geçerli. Editör `index`/`noindex` ile ezebilir. |
| Site haritası | `INDEX` kararı alan hub **etiketleri** `/eka-konu-sitemap.xml`'e girer ve Rank Math dizinine eklenir (kategoriler zaten Rank Math kategori haritasında). |
| Yapılandırılmış veri | Rank Math'in `CollectionPage` düğümüne `about` (Organization/Country/Thing + alternateName) ve `dateModified` eklenir. Rank Math yoksa `CollectionPage` + `BreadcrumbList` basılır. Rich result vaadi yoktur. |
| Toplu sınıflandırma | WP-CLI; varsayılan **kuru**. `--uygula` ile 200'lük partiler, term sayımı ertelenir, her ekleme `wp_eka_log` tablosuna yazılır, Rank Math birincil kategorisi korunur, Polylang eşitlemesiyle çevirilere geçen terimler de günlüğe düşer. `geri-al` yalnız o partinin eklediklerini kaldırır. |

Sayfa yüklenmesinde analiz yapılmaz: öneriler yazı kaydında `_eka_oneriler` meta'sına önbelleklenir; arşivin son güncelleme zamanı terim meta'sında tutulur.

## Kurulum (önce test/staging)

```bash
# 1) Eklentiyi yükle ve etkinleştir (hiçbir arşivin robots'u değişmez)
wp plugin activate envanter-konu-arsivleri

# 2) Hub eşlemesini yükle (motor/hub_esle.py çıktısı; site: ev | dm | da)
wp eka hub-ice-aktar hublar.json --site=ev            # kuru: özet
wp eka hub-ice-aktar hublar.json --site=ev --uygula

# 3) İlk arşivleri hub yap (Rank Math başlık/açıklaması doluysa EZİLMEZ)
wp eka hub-kur seo_metinleri.json --dil=tr --varlik=kaan,tusas            # kuru
wp eka hub-kur seo_metinleri.json --dil=tr --varlik=kaan,tusas --uygula

# 4) Kalite/indeks denetimi
wp eka denetle

# 5) Eski haberleri sınıflandır — önce rapor
wp eka siniflandir --dil=tr --varlik=kaan --rapor=kaan.csv
wp eka siniflandir --dil=tr --varlik=kaan --guven=yuksek --uygula
wp eka partiler
wp eka geri-al <parti> --uygula                        # gerekirse
```

`seo_metinleri.json` anahtarları `site:dil:varlik` biçimindedir (ör. `ev:tr:kaan`); `--dil` değeri dil kısmıyla eşleşir.

## Ayarlar (seçenekler)

- `eka_otomatik_kutu` = `0` → haber altı kutusu otomatik eklenmez; şablonda `eka_ilgili_arsivler()` kullanılır.
- `eka_otomatik_hub` = `0` → hub modülleri açıklamaya eklenmez; arşiv şablonunda `eka_hub_modulleri()` kullanılır.
- `eka_sozluk_json` → sözlüğü dosya yerine seçenekten okur (yeni varlık eklemek için).
- Filtre `eka_varsayilan_indeks` → hub olmayan etiketlerin bağlantı verilebilirliği (varsayılan: yalnız kategoriler).

## Sözlük kuralları (özet)

`data/varliklar.json`: her varlık TEK arşive karşılık gelir; eşanlamlılar ayrı arşiv açmaz.
`cs` harf duyarlı (KAAN ≠ "Kaan Onuk"), `amb` bağlam ister (ör. "Altay" yalnız tank/BMC bağlamında),
`neg` yakın çevrede dışlar ("anti-tank", "Eurofighter Typhoon", "الحصار"). Başlıkta geçmeyen ve gövdede yalnız anılan
varlık önerilmez. Python referans motoru (`motor/eslestir.py`) ile PHP motoru `tests/parite_testi.py` ile birebir karşılaştırılır.

## Test edilenler (yerel WordPress 6.x + Rank Math + Polylang, Twenty Twenty-Five)

- 499 gerçek EV yazısı (TR 259 / EN 120 / AR 120), 231 hub eşlemesi
- Kuru sınıflandırma 500 yazı ≈ 3,7 sn; uygulama 1.557 ekleme; geri alma sonrası fazladan terimli yazı 0
- Hub sayfası: Rank Math title/description/robots/canonical, 2. sayfada tanıtım yok + self-canonical, `about` şeması
- 4 yazılı hub → `noindex, follow`; INDEX hub etiketleri site haritasında
- Haber altı kutusu TR/EN/AR; Arapça kutu tema LTR zorlamasında da RTL
- Editör kutusu (Gutenberg): öneri → seçilenleri ekle → editör terim durumuna yazıldı
- REST `/eka/v1/oner`: yetkili 200, anonim 401
