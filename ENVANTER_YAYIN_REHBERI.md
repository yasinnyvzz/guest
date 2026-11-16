# Envanter Medya — REST ile yayın rehberi

Kimlik bilgileri dosyaya, commit'e yazılmaz. Oturumda ortam değişkeni olarak verilir
(WordPress kullanıcı adı + Uygulama Parolası, Basic Auth).

## Site düzeni
- Polylang: `tr` (varsayılan), `en`, `ar`, `es`, `ru`, `zh`. Haberler genelde TR + EN + AR + ES + RU açılır.
- Slug: TR sade; diğer diller `en-…`, `ar-…`, `es-…`, `ru-…` önekli.
- SEO: Rank Math meta alanları `rank_math_title`, `rank_math_description`, `rank_math_focus_keyword`.
- Haber kategorileri: TR `53` HABERLER + `24795` Savunma Haberleri (+ şirket kategorisi, ör. `385` Canik).
- Kapak: 1200×675 başlık kartı (lacivert zemin, altın şerit, "ENVANTER MEDYA"), her dile ayrı.

## Polylang eşitlemesi (önemli)
`taxonomies`, `post_meta` ve `_thumbnail_id` çeviriler arasında eşitleniyor:
- Kapaklar dile atanıp **medya çeviri grubu** yapılmazsa, kayıt sırasında tüm dillere aynı kapak kopyalanır.
- Kategoriler TR'den çevrilerek dağıtılır; diğer dillerde elle farklı kategori seçmek kalıcı olmaz.

## Sıra
1. Aynı slug/haber var mı kontrol et (`/wp/v2/posts?slug=…&status=publish,draft,future`).
2. Her dil için kapağı yükle (`/wp/v2/media`), alt metin ver.
3. Postları taslak oluştur (başlık, slug, içerik, özet, kategori, kapak, Rank Math meta).
4. Dil ata: `POST /ev/v1/set-post-lang {"post_id":…, "lang":"en"}` — postlar ve kapaklar için.
5. Grupla: `POST /ev/v1/link-post-translations {"groups":[{"tr":…,"en":…,…}]}` — önce kapaklar, sonra postlar.
6. Yayına al (`status: publish`), ardından TR postu bir kez kaydet ve her dilin kapak/kategorisini doğrula.
7. Kontrol: `GET /ev/v1/post-translations?id=<tr_id>`; grubu çözmek gerekirse `POST /ev/v1/pll-detach {"ids":[…]}`.

## Kalıcı kural: tekrar içerik
Defence Arabia metni, Envanter AR metninin kopyası/çevirisi olmaz. Başlık, giriş, bölüm sırası ve cümleler özgün yazılır; 5-gram örtüşme %25'in altında kalmalı. Yeni haberlerde `yayinla.py` öncesi örtüşme ölçülür.

## Kalıcı kural: kaynak
Defence Türk, GDH gibi Türk savunma siteleri kaynak olarak gösterilmez; yalnız konu ipucudur. Asıl kaynak (resmî duyuru, şirket/bakanlık bülteni, ajans veya yabancı özel yayın) bulunup o gösterilir. Bulunamayan olgu metinden çıkarılır.

## Kalıcı kural: aynı haber varsa yapma
Aynı olay Envanter'de yazılmışsa yeni URL açılmaz ve mevcut yazı da güncellenmez; haber atlanır. Yalnızca olay farklıysa (ör. yeni sipariş dilimi) yazılır.

# DefenceMENA (defencemena.com) — REST ile yayın

Kimlik bilgisi dosyaya, commit'e, sohbete yazılmaz. Ortamın ağ sırlarında `defencemena.com` için
Basic Auth (kullanıcı + Uygulama Parolası) kayıtlı; proxy Authorization başlığını kendisi ekler,
betiklerde sahte değer (`proxy-injected:x`) yeterli. Kayıtlı sır reddedilirse proxy kendi başlığını
yine bastırır; o durumda kullanıcıdan sırrı ortam ayarlarında güncellemesi istenir.

## Site düzeni
- Polylang: `en` (varsayılan), `fr`, `pt`, `ar`. Haberler EN + FR + PT açılır; slug'larda dil öneki yok.
- Metin Envanter metninin çevirisi olmaz; Afrika/MENA okuruna göre özgün kurgulanır (5-gram örtüşme %25 altı).
- Rank Math: `rank_math_title`, `rank_math_description`, `rank_math_focus_keyword`.
- Kapak: gerçek fotoğraf; üç dilde aynı medya kimliği kullanılabilir.
- Görsel kalıbı: `<figure style="margin:28px 0"><img … style="width:100%;height:auto;border-radius:6px" loading="lazy" /><figcaption style="font-size:13px;color:#6b7280;padding-top:6px">… Photo: …</figcaption></figure>`

## Sık kategori/etiket kimlikleri
| Konu | EN | FR | PT |
|---|---|---|---|
| Drones | 244 | 622 | 624 |
| Electronic warfare | 252 | 626 | 628 |
| Defence industry | 245 | 540 | 543 |
| Air defence & missiles | 243 | 618 | 620 |
| Turkish defence in Africa | 250 | 570 | 573 |
| Etiket ASELSAN | 1187 | 1194 | 1201 |
| Etiket counter-drone | 2674 | 4620 | 4628 |
| Etiket Steel Dome | 2672 | 4596 | 4600 |
| Etiket Türkiye | 198 | 2074 | 2351 |

## Dil atama ve bağlama
`POST /wp-json/dm/v1/pll-link {"translations":{"en":ID,"fr":ID,"pt":ID}}` — dilleri atar ve grubu bağlar.
(`?lang=` sorgu parametresi taslaklarda dil atamaz.) Yalnız kendi yeni taslaklarımızda kullanılır.

## Sıra
1. Aynı haber var mı: `/wp/v2/posts?search=…` ve slug kontrolü.
2. Fotoğrafları `/wp/v2/media` ile yükle, alt metin + altyazı ver.
3. Üç dili taslak aç (kategori, etiket, kapak, Rank Math).
4. `dm/v1/pll-link` ile bağla, sonra `status: publish`; canlı sayfaları kontrol et.
Örnek: `haberler/aselsan-ejderha-51-dron-rekor/defencemena/`.
