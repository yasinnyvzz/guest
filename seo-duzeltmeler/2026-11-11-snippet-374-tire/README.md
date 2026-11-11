# Snippet #374 ("EV Haber Hub v1") — başlık soneki tire eşleşmesi

## Sorun

Snippet'teki filtre, başlığın sonundaki ` - Envanter Medya - Savunma Sanayii Haberleri` sonekini ` | Envanter Medya` ile değiştirmek için yazılmış. Ancak `str_replace` yalnız **kısa tireli** (`-`) yazımı arıyor. Canlıda Rank Math ayırıcısı **uzun tire** (`–`, bazen `&ndash;` olarak), bu yüzden filtre hiç eşleşmiyor:

```
canlı:   HÜRJET – Envanter Medya – Savunma Sanayii Haberleri
amaç:    HÜRJET | Envanter Medya
```

## Değişiklik (yalnız filtre bloğu; snippet'in geri kalanı aynı, CRLF satır sonları korundu)

`degisiklik.diff`:

```diff
-  return str_replace(array(' - Envanter Medya - Savunma Sanayii Haberleri',' – Envantermedya'), ' | Envanter Medya', $t);
+  $sep = '\s*(?:-|–|—|&ndash;|&mdash;|&#8211;|&#8212;|&#x2013;|&#x2014;)\s*';
+  return preg_replace(array(
+    '/' . $sep . 'Envanter Medya' . $sep . 'Savunma Sanayii Haberleri\s*$/u',
+    '/' . $sep . 'Envantermedya\s*$/u',
+  ), ' | Envanter Medya', $t);
```

- Kapsam özgün amaçla aynı. Yalnız iki sonek kısalır: "Envanter Medya + slogan" ve "Envantermedya".
- Eşleşme yalnız başlığın **sonunda** aranır. Ortada geçen "Envanter Medya - Savunma Sanayii Haberleri" ifadesine dokunulmaz.
- Ana sayfa istisnası (`is_front_page() || is_home()`) aynen korunur.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `snippet-374-onceki.php` | Canlıdaki kod (11.11.2026'da REST'ten salt okuma; snippet son değişiklik tarihi 2026-09-18) |
| `snippet-374-yeni.php` | Düzeltilmiş tam kod |
| `eski-blok.php` / `yeni-blok.php` | Yalnız değişen filtre bloğu (elle yapıştırmak için) |
| `degisiklik.diff` | Fark |
| `kalip_testi.php` | Kalıp testi (`php kalip_testi.php`) |

## Testler

**Kalıp testi (13 durum, 0 hata).** Canlıda görülen biçim (uzun tire), sayfanın yalnız birinde uzun tire olan karışık biçim, `&ndash;` ve `&#8211;` varlıkları, em tire ve sayfalı başlık yeni kodla kısaldı; eski kod bu 6 durumun hiçbirini yakalayamıyor. Dokunulmaması gereken başlıklar olduğu gibi kaldı: yazı şablonu `… - Envanter Medya`, özel Rank Math başlıkları, Polylang düzeltmesi sonrası `… – Envanter Medya` ve ortada geçen ifade.

**Yerel WordPress** (Rank Math 1.0.282 + Polylang 3.9.2; canlıdaki şablonlar: ayırıcı `–`, kategori `%term% %sep% %sitename%`, ana sayfa `%sitename% %sep% %sitedesc%`). Snippet'in tamamı önce eski, sonra yeni hâliyle yüklendi:

| Sayfa | Eski snippet | Yeni snippet |
|---|---|---|
| `/category/kaan/` | KAAN – Envanter Medya - Savunma Sanayii Haberleri | KAAN \| Envanter Medya |
| `/category/kaan/page/2/` | aynı | KAAN \| Envanter Medya |
| `/en/category/kaan-en/` | KAAN Fighter Jet – Envanter Medya - Savunma Sanayii Haberleri | KAAN Fighter Jet \| Envanter Medya |
| `/ar/category/kaan-ar/` | مقاتلة KAAN – Envanter Medya - Savunma Sanayii Haberleri | مقاتلة KAAN \| Envanter Medya |
| `/`, `/en/` (ana sayfalar) | değişmez | değişmez (istisna) |
| yazı (şablon `%title% - Envanter Medya`) | değişmez | değişmez |

Site adı hem kısa tireli hem uzun tireli yazıldığında sonuç aynı çıktı. PHP hata günlüğünde kayıt yok.

## Polylang site adı düzeltmesiyle (`../2026-11-11-baslik-slogan/`) birlikte

| Sayfa | Yalnız bu snippet | İkisi birlikte |
|---|---|---|
| `/category/…` (tr) | KAAN \| Envanter Medya | KAAN \| Envanter Medya |
| `/en/category/…` | KAAN Fighter Jet \| Envanter Medya | KAAN Fighter Jet – Envanter Medya |
| `/en/` | Türkçe site adı + slogan (değişmez) | Envanter Medya – Defence Industry News and Analysis from Türkiye |

- Bu snippet tek başına arşivlerdeki Türkçe sloganı her dilde kaldırır, ama TR dışı ana sayfaları düzeltmez; o iş Polylang düzeltmesinin.
- İkisi birlikte uygulanırsa TR arşivlerde ayırıcı `|`, EN/AR arşivlerde `–` olur. Bu yalnız görsel bir tutarsızlıktır.
- Her dilde `|` istenirse kalıba ` – Envanter Medya$` eklenebilir. Ancak yazı şablonu `… - Envanter Medya` ile karışmaması için yalnız uzun tireli biçim seçilmeli. Bu ayrı bir karardır.

## Uygulama (Code Snippets panelinden)

1. Snippets › "EV Haber Hub v1" (#374) açın. Son değişiklik tarihi 2026-09-18 değilse önce farkı kontrol edin.
2. `eski-blok.php` içeriğini bulup yerine `yeni-blok.php` içeriğini yapıştırın › Kaydet. Code Snippets sözdizimi hatasında kaydetmez.
3. LiteSpeed › Tümünü temizle.
4. Kontrol: `/category/envanter/tusas/hurjet/` başlığı `HÜRJET | Envanter Medya` olmalı; ana sayfa ve yazı başlıkları değişmemeli.

Geri alma: `yeni-blok.php` yerine `eski-blok.php` içeriğini geri yapıştırın, önbelleği temizleyin.
