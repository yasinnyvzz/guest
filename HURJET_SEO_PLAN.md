# HÜRJET SEO Pre-Positioning + Hızlı Yayın Rutini — Yapı Planı

Bu dosya, resmî açıklama öncesi/sonrası HÜRJET içerik ağı için URL yapısını,
gece yayın takvimini, iç link haritasını ve SSS/başlık şablonlarını tanımlar.
WordPress'e otomatik yayın için bir REST API entegrasyonu henüz bağlı değil —
bu doküman, o entegrasyon (veya editörlerin manuel girişi) için kaynak plandır.

## 1) Sayfa/URL Envanteri (tek intent = tek URL, mevcutsa güncelle)

| # | Sayfa (intent) | Önerilen slug | Rol |
|---|---|---|---|
| 0 | HÜRJET nedir? (HUB) | `/hurjet-nedir` | Merkez sayfa, tüm alt sayfalara link verir/alır |
| 1 | HÜRJET ne zaman envantere girecek? (teslimat) | `/hurjet-envantere-ne-zaman-girecek` | Teslimat takvimi, resmî açıklamalarla güncellenir |
| 2 | HÜRJET ilk uçuş | `/hurjet-ilk-ucus` | Prototip ilk uçuşu vs. teslimat konfigürasyonu ayrımı |
| 3 | HÜRJET kaç adet üretilecek | `/hurjet-kac-adet-uretilecek` | Üretim adedi, ihracat |
| 4 | HÜRJET fiyatı | `/hurjet-fiyati-ne-kadar` | Liste/paket/birim fiyat ayrımı |
| 5 | HÜRJET motoru | `/hurjet-motoru` | Motor, üretici, itki |
| 6 | HÜRJET hızı / Mach | `/hurjet-hizi-kac-mach` | Maks hız, süpersonik kabiliyet |
| 7 | HÜRJET görevleri | `/hurjet-gorevleri` | Eğitim, hafif taarruz vb. |
| 8 | HÜRJET vs M-346 | `/hurjet-vs-m-346` | Karşılaştırma |
| 9 | HÜRJET vs T-50 | `/hurjet-vs-t-50` | Karşılaştırma |
| 10 | HÜRJET neden önemli | `/hurjet-neden-onemli` | Evergreen analiz |
| 11 | HÜRJET seri üretim süreci | `/hurjet-seri-uretim-sureci` | Kronoloji: prototip→test→montaj→teslimat |

**Kural:** Yayından önce WordPress'te bu 12 intent için mevcut sayfa arattırılır
(başlık + slug + içerik taraması). Var olan güçlü sayfa **silinmez**, üzerine
güncelleme yapılır (kaynak, tablo, SSS, iç link, görsel, SEO title).

## 2) Gece Yayın Takvimi (00:00 sonrası, yalnız kamuya açık/evergreen)

| Saat | Sayfa | Not |
|---|---|---|
| 00:05 | Hub (#0) güncelle | Teknik tablo + tüm alt sayfalara link |
| 00:45 | Teslimat (#1) | Yalnız kamuya açık takvim, kesin tarih iddiası yok |
| 01:30 | Hız/Mach (#6) | İlk 100 kelimede doğrudan cevap |
| 02:15 | Motor (#5) | Üretici, itki, entegrasyon |
| 03:00 | Üretim adedi (#3) | Kesin olmayan adetleri kesin gibi yazma |
| 04:00 | Fiyat (#4) | Katalog fiyatı yoksa açıkça belirt |
| 05:00 | vs M-346 (#8) | Üretici kaynaklı veri |
| 06:00 | vs T-50 (#9) | Üretici kaynaklı veri |

Aynı gece aynı intent için ikinci URL açılmaz; mevcut sayfa güncellenir.

## 3) Resmî Açıklama Sonrası Hızlı Yayın Sırası (hedef: 5 dk içinde ana haber)

1. Ana haber (tek, güçlü — 4 farklı "ilk uçtu" haberi açılmaz)
2. Hub (#0) → "Son durum" kutusu + ana habere link
3. Teslimat (#1) güncelle — eski beklenti / yeni gelişme ayrımı
4. İlk uçuş (#2) güncelle — prototip vs. teslimat konfigürasyonu karışmasın
5. Ana haberden tüm ilgili evergreen sayfalara iç link
6. Evergreen sayfalardan ana habere geri link
7. Diğer diller (EN, AR, RU, ES, aktif 6. dil) — kısa aralıklarla
8. Sitemap / internal link / Search Console kontrolü

## 4) İç Link Zinciri (topic authority)

```
HÜRJET nedir? (hub)
  → HÜRJET motoru
  → HÜRJET hızı / Mach
  → HÜRJET teslimat
  → HÜRJET üretim adedi
  → HÜRJET fiyatı
  → HÜRJET vs M-346 / vs T-50
  → güncel HÜRJET haberleri (ana haber dahil)
```
Her alt sayfa hub'a geri link verir; hub tüm alt sayfalara link verir.

## 5) Başlık Şablonları

- Evergreen, iddialı-olmayan başlıklar kullan (ör. "HÜRJET nedir? Özellikleri,
  motoru, hızı ve kullanım amacı").
- **Kullanma:** "HÜRJET için kritik saatler", "teslimat öncesi son dakika",
  "tarihi gün yaklaşıyor" gibi henüz açıklanmamış olayı ima eden başlıklar.
- Resmî açıklama sonrası ana haber başlığı, resmî ifadeye sadık kalınarak
  yazılır (örnek yapı, kelimesi kelimesine kopyalanmaz).

## 6) Standart SSS Bloğu (her ana sayfanın sonuna)

1. HÜRJET nedir?
2. HÜRJET ne zaman uçtu?
3. HÜRJET ne zaman envantere girecek?
4. HÜRJET hangi motoru kullanıyor?
5. HÜRJET'in hızı ne kadar? Kaç Mach?
6. HÜRJET kaç adet üretilecek?
7. HÜRJET'in fiyatı ne kadar?
8. HÜRJET silahlı mı?
9. HÜRJET hangi ülkelere satılacak?
10. HÜRJET TUSAŞ tarafından mı üretiliyor?
11. HÜRJET'in rakipleri hangi uçaklar?

Cevaplar 2–4 cümle, featured-snippet uzunluğunda, yalnız kamuya açık bilgiyle.

## 7) Editoryal Kırmızı Çizgiler (resmî açıklama öncesi)

Kullanılmayacak ifadeler: "ilk teslim HÜRJET bugün uçacak", "yarın teslim
edilecek", "Hava Kuvvetleri'ne gidecek ilk uçak hazır", açıklanmamış uçuş
süresi/adet/tarih/konfigürasyon.

## 8) Yayın Öncesi Kontrol Listesi (gece)

- [ ] Bilgi kamuya açık mı?
- [ ] Güncel/resmî kaynak var mı?
- [ ] Gelecekteki açıklamayı ima ediyor mu?
- [ ] Aynı intent için mevcut sayfa var mı? (varsa yeni URL açma)
- [ ] En az 2 gerçek/izinli görsel var mı?
- [ ] Özgün teknik tablo var mı?
- [ ] İç link (hub'a ve hub'dan) var mı?
- [ ] SEO title doğal mı (keyword doldurma yok)?

## 9) Yayın Sonrası Kontrol Listesi (resmî açıklama)

- [ ] Resmî açıklamanın tam ifadesi doğrulandı mı?
- [ ] Hangi konfigürasyon/uçak anlatılıyor, netleşti mi?
- [ ] "İlk uçuş" ifadesi prototiple mi teslimat uçağıyla mı karıştı?
- [ ] Uçuş süresi / adet resmî mi, yoksa tahmini mi?
- [ ] Teslimat ile ilk uçuş birbirine karışmadı mı?

## 10) Sonraki Adım — WordPress Entegrasyonu

Otomatik yayın/güncelleme için gerekli:
- Site URL (`https://envantermedya.com`)
- WP REST API kullanıcı adı + Application Password (Admin > Kullanıcılar >
  Uygulama Şifreleri) — okuma+yazma
- Mevcut HÜRJET sayfalarının post ID/slug listesi (arşiv taraması için)

Bu bilgiler sağlandığında yukarıdaki 12 sayfa için create-or-update script'i
yazılabilir (mevcut sayfa var mı kontrolü + güncelleme, yoksa oluşturma).
