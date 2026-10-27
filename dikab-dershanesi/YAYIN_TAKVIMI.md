# DİKAB Dershanesi — Kavram İçerikleri SEO Planı ve 24 Saatlik Yayın Takvimi

Kaynak: Search Console sorguları (tıklama 0, gösterim 1–3). Bu sorgular gösterim
alıyor ama tıklama getirmiyor; yani sitede bu niyete tam cevap veren bir sayfa yok.
Plan, her niyet için **tek URL** açar ve aynı niyetteki sorguları birleştirir.

## 1) Sorgu → sayfa eşleşmesi (tek niyet = tek URL)

| Sorgu (gösterim) | Birleştirilen sayfa | Slug |
|---|---|---|
| sebut tival ne demek (3), sebut tıval nedir (1) | Seb'u't-tıvâl nedir? | `/sebut-tival-nedir` |
| beda ne demek kelam (2), beda nedir (2) | Bedâ nedir? | `/beda-nedir` |
| vakfı kafi nedir (2) | Vakf-ı kâfî nedir? | `/vakf-i-kafi-nedir` |
| li aynihi vacip (2) | Vâcib li-aynihî nedir? | `/vacib-li-aynihi-nedir` |
| kan yada evlilik yoluyla birbirine bağlı olan insanlara ne denir (2) | Akraba / hısımlık | `/kan-ya-da-evlilik-yoluyla-birbirine-bagli-insanlara-ne-denir` |
| baas ne demek (1) | Ba's ne demek? | `/bas-nedir` |
| ehlivukuf ne demek (1) | Ehl-i vukuf ne demek? | `/ehl-i-vukuf-ne-demek` |
| dikab (1) | DİKAB kavram sözlüğü (hub) | `/dikab-kavram-sozlugu` |

10 sorgu → 8 sayfa. "beda" ve "sebut tıval" sorguları için ikinci URL açılmaz.

## 2) Yayın takvimi (24 saat arayla, 09:00 TSİ)

Sıra gösterim sayısına göre; hub en sona konuldu ki yayımlandığı gün tüm alt
sayfalar canlı olsun ve hiçbir iç link boşa çıkmasın.

| Gün | Tarih / saat | Dosya | Durum |
|---|---|---|---|
| 1 | 28.10.2026 Çar 09:00 | `makaleler/01-sebut-tival-nedir.md` | READY TO PUBLISH |
| 2 | 29.10.2026 Per 09:00 | `makaleler/02-beda-nedir-kelam.md` | READY TO PUBLISH |
| 3 | 30.10.2026 Cum 09:00 | `makaleler/03-vakf-i-kafi-nedir.md` | READY TO PUBLISH |
| 4 | 31.10.2026 Cmt 09:00 | `makaleler/04-vacib-li-aynihi-nedir.md` | READY TO PUBLISH |
| 5 | 01.11.2026 Paz 09:00 | `makaleler/05-kan-ya-da-evlilik-yoluyla-bagli-insanlar-akraba.md` | READY TO PUBLISH |
| 6 | 02.11.2026 Pzt 09:00 | `makaleler/06-bas-ne-demek.md` | READY TO PUBLISH |
| 7 | 03.11.2026 Sal 09:00 | `makaleler/07-ehl-i-vukuf-ne-demek.md` | READY TO PUBLISH |
| 8 | 04.11.2026 Çar 09:00 | `makaleler/08-dikab-kavram-sozlugu-hub.md` | READY TO PUBLISH |

WordPress'te her yazı "Zamanla" (Schedule) ile yukarıdaki saate kurulabilir; böylece
8 yazı bir kerede girilip sırayla kendiliğinden yayımlanır.

## 3) İç link haritası

```
DİKAB kavram sözlüğü (hub, gün 8)
  → seb'u't-tıvâl → vakf-ı kâfî            (Kur'an ilimleri / tecvid)
  → bedâ ↔ vâcib li-aynihî ↔ ba's          (kelam)
  → akraba/hısımlık ↔ ehl-i vukuf          (fıkıh / toplum)
```
Her yazının sonunda hub'a ve aynı kümedeki 1–2 yazıya link var. Henüz
yayımlanmamış bir yazıya giden link, o yazı yayımlanana kadar 404 verir:
link ya yayın günü eklenmeli ya da yazılar takvimdeki sırayla girilmeli
(hub en son olduğu için hub'daki linklerin hepsi canlı olur).

## 4) Yazı şablonu (her makalede uygulandı)

- İlk paragrafta **kalın "Kısa cevap"** — featured snippet için 40–60 kelime.
- Haber tarzı giriş: kavramın hangi sınav/ünitede sorulduğu.
- Sözlük / terim anlamı + tablo.
- Sınavda karıştırılan kavramlarla fark tablosu.
- SSS bloğu (4–5 soru; arama sorgularının birebir hâli soru olarak).
- Kaynaklar (TDV İslâm Ansiklopedisi, Kur'an âyet numaraları, mevzuat).
- Front matter: slug, SEO title, meta description, birincil/ikincil anahtar kelime.

## 5) Yayın öncesi kontrol listesi

- [ ] Sitede aynı niyetle eski bir yazı var mı? Varsa yeni URL açma, eskisini güncelle.
- [ ] Slug, front matter'daki ile aynı mı?
- [ ] SEO title ve meta description Yoast/RankMath alanına girildi mi?
- [ ] SSS bloğu FAQ schema olarak işaretlendi mi?
- [ ] Arapça terimler (سبع طوال، بعث vb.) doğru göründü mü?
- [ ] Hub'daki tüm linkler canlı mı? (gün 8'de kontrol)

## 6) Yayın sonrası takip (2–4 hafta)

- Search Console'da her sayfanın sorguları: gösterim ↑, ortalama pozisyon, CTR.
- `li aynihi vacip` sayfası kelam mı usul mü niyetiyle tıklanıyor, ona göre bölme kararı.
- Tıklama gelmeyen sayfalarda title/description A/B değişikliği.
- Yeni gösterim alan kavram sorguları bu tabloya eklenip aynı ritimle (24 saatte bir) sıraya alınır.
