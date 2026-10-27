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
