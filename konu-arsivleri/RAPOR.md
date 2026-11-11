# Envanter Medya Yayın Ağı — Konu Arşivleri (Topic Hub) ve Akıllı Eşleştirme Sistemi

İlk teslimat · 11 Kasım 2026 · Durum: **test ortamında çalışıyor, canlıya hiçbir şey yazılmadı**

Tablolar: [`RAPOR_TABLOLARI.md`](RAPOR_TABLOLARI.md) ve [`KONU_ARSIVLERI_2026-11-11.xlsx`](KONU_ARSIVLERI_2026-11-11.xlsx) (Tablo A–F, dry-run özeti, 40 arşivin önce/sonra SEO metinleri).
Eklenti: [`eklenti/envanter-konu-arsivleri/`](eklenti/envanter-konu-arsivleri/) · Ekran görüntüleri: [`ekran/`](ekran/)

---

## 1. Kısa özet

- **Yeni URL yapısı açılmadı.** Envanter'de şirket ve ürün arşivleri zaten indekslenen kategoriler olarak var (`/category/envanter/aselsan/` 651 haber, `/category/envanter/tusas/` 219 haber). Sorun arşiv eksikliği değil, **haberlerin bu arşivlere bağlanmaması**: başlığında KAAN geçen 85 Türkçe haberin yalnız 15'i KAAN kategorisinde.
- **Varlık sözlüğü** (79 varlık; TR/EN/AR ad ve eşanlamlılar, bağlam ve dışlama kuralları) ve **eşleştirme motoru** yazıldı. Motor başlık + giriş + gövdeyi okur; yalnız anılan şirketi arşive eklemez ("Kaan Onuk" ≠ KAAN, "anti-tank" ≠ Tank, "الحصار" ≠ HİSAR).
- **Bütün arşiv dry-run'dan geçti** (EV 18.517, DefenceMENA 981, Defence Arabia 1.052 yazı). Siteye yazılmadı. Envanter için 20.552 yüksek güvenli ekleme önerisi, 16.523 editör onayı bekleyen öneri çıktı.
- **WordPress eklentisi** (`envanter-konu-arsivleri`): hub arşiv sayfası modülleri, haber altında "İlgili Haber Arşivleri", editör öneri kutusu, kalite kapılı indeksleme, hub site haritası, `CollectionPage.about` şeması ve geri alınabilir WP-CLI toplu sınıflandırma. Yerel WordPress + Rank Math + Polylang ortamında 499 gerçek EV yazısıyla test edildi.
- **İlk 40 arşiv** seçildi ve her biri için özgün H1, SEO başlığı, meta açıklama ve tanıtım yazıldı (10 TR, 10 EN, 10 Defence Arabia, 10 DefenceMENA).
- **GSC verisine bu oturumda erişim yok.** Tablo E'de yalnız 6 Kasım'daki 24 saatlik GSC dışa aktarımından gelen iki gerçek veri noktası var; geri kalanı "veri yok". Rakam üretilmedi.

## 2. Yayın ağının gerçek yapısı (tespit)

| Yayın | Alan adı | Kurulum | Diller | Tema | SEO | Bu oturumdaki erişim |
|---|---|---|---|---|---|---|
| Envanter Medya (TR + EN + AR + ES + RU + ZH) | envantermedya.com | **Tek WordPress**, Polylang | tr (varsayılan), en, ar, es, ru, zh | olivin + olivin-child | Rank Math | Yönetici REST (okuma) |
| DefenceMENA | defencemena.com | Ayrı WordPress, Polylang | en, fr, pt | defencemena-grid | Rank Math | Yalnız herkese açık REST (yönetici isteği 401) |
| Defence Arabia | defencearabia.com | Ayrı WordPress, Polylang | ar (+ az sayıda en) | olivin + olivin-child | Rank Math | Yalnız herkese açık REST |

Notlar:
- "Envanter İngilizce" ayrı site değil; aynı kurulumun `/en/` dilidir. Arşiv kararları dil bazında ayrı verildi.
- **DefenceMENA içerik olarak Afrika odaklı** ("Africa Defence Industry, Procurement and Security News"). Brifteki MENA arşivleri (Egypt, Saudi, UAE, Qatar…) mevcut etiketlerle karşılandı; Orta Doğu derinliği sınırlı.
- Envanter'in etiket arşivleri **site genelinde `noindex`** ve site haritasında yok; kategoriler `index` ve hreflang gruplu. DefenceMENA ve Defence Arabia'da etiketler `index`, tek yazılı etiketler `noindex`.

## 3. Mimari karar

**Yeni taksonomi açılmadı; mevcut kategori ve etiketler "hub" olarak işaretleniyor.**

1. Şirket/ürün kategorileri zaten indeksli, hreflang'li ve trafiğe açık. `/konu/` veya `/sirket/` açmak, aynı niyet için ikinci URL ve yönlendirme yükü getirirdi.
2. Her varlık **tek arşive** eşlenir (`sozluk/hub_elle.json` + `motor/hub_esle.py`). Eşanlamlılar (KAAN = Millî Muharip Uçak = MMU = TF-X) ayrı arşiv açmaz.
3. Kategorisi olmayan varlıklarda mevcut etiket kullanılır; Envanter'de etiketler kalite kapısını geçene kadar `noindex` kalır.
4. Aynı varlığın kopya terimleri (ALTAY için 4 kategori, KAAN için 5 terim, iki "Lockheed Martin" etiketi) **raporlandı, dokunulmadı**. Birleştirme 301 gerektirir; onay bekliyor.

Varlık türleri: ana konu (kategori) · şirket · platform/ürün · teknoloji · ülke (+ DefenceMENA için Kuzey Afrika ve Orta Doğu bölge varlıkları).

## 4. Eşleştirme motoru

- **Güven:** *yüksek* = varlık başlıkta geçer ve gövdede doğrulanır (şirketlerde başlıkta geçmese de girişte geçip gövdenin baskın şirketi olması yeter). *orta* = editör kuyruğu. Gövdede tek geçen varlık önerilmez.
- **Çıkarım:** ürün → üretici (KAAN → TUSAŞ), ürün → tür → ana konu (KAAN → Savaş Uçağı → Askerî Havacılık → Türk Savunma Sanayii). Başlıkta olmayan bir varlıktan yapılan çıkarım en çok "orta" olur.
- **Liste yazıları:** 4'ten fazla şirket varsa yalnız başlıktakiler ve en güçlü ikisi kalır.
- **En fazla 7 öneri;** yazı başına ortalama 2,6 (EV).
- **Dil koruması:** URL dili ile metin dili farklı 108 EV ve 36 DA yazısı eşleştirmeden çıkarıldı.
- **İki motor, tek kural:** Python referans motoru (`motor/eslestir.py`, dry-run ve raporlar) ile eklentideki PHP motoru `tests/parite_testi.py` ile 1.505 gerçek yazıda **0 farkla** doğrulandı.

**Doğruluk (benim elle kontrolüm; editör doğrulaması değildir):** "Toplu eklenebilir" önerilerden rastgele 60'lık örneklem. İlk kural setinde 49/60 (%82). Hatalar (anti-denizaltı, karşı-İHA, "الحصار", başlıkta olmayan baskın ürün, zincirleme çıkarım) giderildikten sonra **yeni bağımsız örneklemde 55/60 (%92)**. Kalan hatalar çoğunlukla liste/rehber yazılarında ana konu çıkarımı. Bu nedenle toplu uygulama varlık varlık yapılmalı ve her partiden önce editör 20 satırı kontrol etmeli (`--varlik=kaan --rapor=…`).

## 5. Dry-run sonucu (hiçbir şey yazılmadı)

| Site | Yazı | Yüksek güven (toplu eklenebilir) | Editör kuyruğu | Zaten bağlı | Kopya terime bağlı | Arşivi yok | Dil uyumsuz |
|---|---|---|---|---|---|---|---|
| Envanter Medya | 18.517 | 20.552 | 16.523 | 5.584 | 1.977 | 3.064 | 108 |
| DefenceMENA | 981 | 192 | 780 | 960 | 21 | 656 | — |
| Defence Arabia | 1.052 | 1.116 | 1.300 | 836 | 66 | 629 | 36 |

Satır satır sonuç: `veri/eslestirme_{ev,dm,da}.csv.gz` (yazı, önerilen varlık, hedef terim, güven, kaynak, başlık/giriş/gövde sayıları, durum). DefenceMENA etiketleri zaten iyi uygulanmış; ekleme önerisi az.

Örnek etki (Tablo B): KAAN TR arşivi 17 → 63 haber, ALTAY 6 → 25, EN ASELSAN 92 → 279, EN Baykar 28 → 395.

## 6. Eklenti

Ayrıntı: [`eklenti/envanter-konu-arsivleri/README.md`](eklenti/envanter-konu-arsivleri/README.md).

| Gereksinim | Nasıl karşılandı | Test |
|---|---|---|
| Arşivde SEO title, H1, açıklama, tanıtım | Rank Math terim alanları (boşsa doldurulur, doluysa ezilmez) + `eka_h1`, `eka_intro` | ✔ |
| Son haberler, sayfalama, yeniden eskiye | Temanın kendi döngüsü korunur | ✔ |
| Öne çıkan haberler | Editör seçer (`eka_featured`) | ✔ |
| İlgili alt konular / diğer arşivler | Sözlükteki üretici/üst/ilgili ilişkilerinden ya da editör listesinden | ✔ |
| Son güncelleme | Terim meta'sında önbellekli; yeni yazı bağlanınca tazelenir | ✔ |
| Haber altı 3–7 bağlantı, gerçek `<a href>`, JS yok | `the_content` sonuna; yalnız indekslenebilir hub'lar | ✔ TR/EN/AR |
| Arapça RTL | Kutular `dir="rtl" lang="ar"` taşır. EV temasındaki `body.rtl{direction:ltr !important}` kuralı altında da RTL kaldığı doğrulandı | ✔ |
| Editör öneri sistemi | Yan kutu; Gutenberg ve klasik editör; onaysız ekleme yok | ✔ |
| Kalite kapılı indeksleme | ≥5 yazı, ≥40 kelime özgün tanıtım, varlık eşlemesi, son 12 ayda yazı | ✔ (4 yazılı hub → noindex) |
| Site haritası | INDEX hub etiketleri `/eka-konu-sitemap.xml` → Rank Math dizini | ✔ |
| Şema | Rank Math `CollectionPage` + `about` + `dateModified`; Rank Math yoksa CollectionPage + BreadcrumbList | ✔ |
| Toplu sınıflandırma, geri alma | WP-CLI, varsayılan kuru; parti günlüğü; birincil kategori korunur; Polylang eşitlemesi günlüğe düşer | ✔ 1.557 ekleme → geri alındı → fazladan terim 0 |
| Performans | Sayfa yüklenmesinde analiz yok; 200'lük partiler; term sayımı ertelenir | 500 yazı kuru ≈ 3,7 sn |

Test sırasında bulunup düzeltilen hatalar: REST uç noktası yalnız admin'de yükleniyordu (Gutenberg REST ile kaydettiği için öneri kutusu çalışmazdı); blok temalarda hub modülleri basılmıyordu; `<title>` H1 filtresinden etkileniyordu.

Test edilmeyenler: olivin temasının kendisi (ticari tema, test ortamında yok — kod `term_description` ve `the_content` kancalarını kullanıyor; olivin açıklamayı H1 altında basıyor, uyum beklenir ama canlı staging'de görülmeli), Polylang taksonomi eşitlemesinin gerçek çeviri gruplarıyla davranışı (test verisinde çeviri grubu yoktu), canlı önbellek (LiteSpeed) etkisi.

## 7. İndeksleme stratejisi

- **INDEX:** hub + ≥5 ilgili haber + özgün tanıtım + net arama niyeti (sözlük varlığı) + son 12 ayda haber.
- **NOINDEX/IMPROVE:** boş, tek haberli, kopya, niyeti belirsiz ya da tanıtımı olmayan arşivler. Envanter'in 25.413 etiketinin %80'i ≤1 yazılı; site geneli `noindex` doğru, korunmalı.
- Türkiye ülke arşivi Envanter TR'de kullanılmaz (her habere uyar, ayırt edici değil).
- Şablonla çoğaltılmış açıklama yok: 40 tanıtımın her biri ayrı yazıldı; kapı 40 kelimenin altını indekse almaz. Yeni arşiv açılırken metin taslağı bile editör onayıyla girer (scaled content / doorway riskine karşı).

## 8. Onay bekleyen kararlar (canlıda yapılmadı)

1. Eklentinin Envanter staging'e, sonra canlıya kurulması.
2. İlk 40 hub'ın açılması (`hub-kur`) — Envanter'de 14/20 arşivin meta açıklaması boş, 10/10 İngilizce arşivin başlığına Türkçe slogan ekleniyor; bu düzeltmeler de bu adıma dahil.
3. Toplu sınıflandırma: varlık bazlı partilerle, önce 40 hub varlığı (`--guven=yuksek`).
4. Kopya terim birleştirmeleri (ALTAY×4, KAAN×5 …) — 301 ve GSC kontrolü gerektirir.
5. Envanter EN KAAN arşivi şu an `noindex` etiket (`/en/tag/kaan-en/`); hub olunca kalite kapısıyla index'e geçer. Alternatif: EN KAAN kategorisi açmak (yeni URL) — önerilmez.
6. Rank Math başlık şablonunda EN/AR/ES/RU için yerelleştirilmiş ayırıcı/slogan.
7. DefenceMENA ve Defence Arabia için yönetici erişimi (bu oturumda yok).

## 9. Kademeli yayın ve ölçüm

| Dalga | İçerik | Ölçüt |
|---|---|---|
| 0 (staging) | Eklenti + hub eşlemesi + 40 hub metni; olivin temasında görsel kontrol | Görsel onay, Rich Results Test (şema geçerliliği) |
| 1 | 10 TR + 10 EN Envanter hub'ı; KAAN, ASELSAN, TUSAŞ, ROKETSAN, BAYKAR, BMC, ALTAY, HÜRJET toplu sınıflandırma | 30. gün: hub URL'lerinin hedef sorgularda gösterimi, sorgu→sayfa eşleşmesinin haberden arşive kayması |
| 2 | Defence Arabia 10 + DefenceMENA 10 | 60. gün: CTR ve ortalama konum; indeks kapsamı (GSC Sayfalar raporu) |
| 3 | Kalan varlıklar, editör kuyruğu, yeni arşiv adayları (Tablo B "YENİ") | 90. gün: arşivlerin toplam tıklaması, yeni haberlerin arşivleri beslemesi |

Ölçüm için gereken: her site için GSC **28 gün ve 3 ay "Sayfa × Sorgu"** dışa aktarımı (ya da GSC API yetkisi). Bu gelince Tablo E gerçek değerlerle doldurulur ve Tablo B öncelikleri yeniden sıralanır.

## 10. Klasör

```
konu-arsivleri/
  RAPOR.md, RAPOR_TABLOLARI.md, KONU_ARSIVLERI_2026-11-11.xlsx
  sozluk/varliklar.json      varlık sözlüğü (eşanlamlı, bağlam, dışlama, ilişkiler)
  sozluk/hub_elle.json       varlık → tekil arşiv elle kararları
  sozluk/seo_metinleri.json  ilk 40 arşivin H1/title/meta/tanıtım metinleri
  motor/                     eslestir.py (referans motor), hub_esle.py, kuru_calistir.py, dil_tespit.py, canli_durum.py, ilk40.json
  analiz/                    cek.py, cek_cpt.py, sadele.py (salt okuma veri çekme), rapor_uret.py
  veri/                      hublar.json, canli40.json, ozet.json, eslestirme_*.csv.gz (dry-run)
  eklenti/envanter-konu-arsivleri/   WordPress eklentisi
  tests/                     parite_testi.py, parite_matcher.php, tohum.php (yalnız yerel test sitesi)
  ekran/                     test ortamı ekran görüntüleri
```

Yeniden üretim: `analiz/cek.py <klasör>` → `analiz/sadele.py` → `motor/hub_esle.py` → `motor/kuru_calistir.py` → `motor/canli_durum.py` → `analiz/rapor_uret.py`. Hepsi salt okumadır.
