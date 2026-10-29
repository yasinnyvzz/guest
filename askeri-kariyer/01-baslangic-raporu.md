# Envanter Medya — Askerî Kariyer Dikeyi: Başlangıç Raporu

Tarih: 29.10.2026 · Durum: TASLAK, editör onayı bekliyor · Canlıya hiçbir şey alınmadı.

## 0) Önce bilinmesi gerekenler

1. **Resmî kılavuza erişemedim.** `personeltemin.msb.gov.tr` ve `msb.gov.tr` bu ortamdan 403 veriyor. Aşağıdaki doğrulama, kılavuz içeriğini aktaran ikincil haber kaynaklarına dayanıyor. Haber yayımlanmadan önce aşağıdaki "Editör kontrol listesi" kılavuz PDF'i açılarak işaretlenmeli.
2. **Görseldeki iddialar iki ayrı alımı karıştırıyor olabilir.** Bkz. bölüm 2.
3. **Boy şartı (168/162 cm) hiçbir kaynakta doğrulanamadı.** Doğrulanana kadar yayımlanmaz.
4. **Zaman baskısı:** Genel muvazzaf subay alımının son başvurusu **2 Kasım 2026 17.30** (4 gün). Haber bu hafta çıkmazsa değerini kaybeder.
5. **Veri araçları kapalı:** Semrush API birimi yok, Frase deneme süresi bitmiş, Search Console verisine erişim yok. Bu yüzden **hiçbir arama hacmi verilmedi**; öncelik sırası arama niyeti, haber takvimi ve içerik boşluğu mantığına dayanıyor. Search Console bağlanınca sıralama güncellenecek.

## 1) Mevcut site envanteri (envantermedya.com, herkese açık REST API ile tarandı)

- **Askerî kariyer / personel alımı / mülakat içeriği: yok.** "Kariyer" kategorisi (id 31179, ~190 yazı) tamamen **savunma sanayii** kariyeridir (ASELSAN, TUSAŞ, Baykar, FNSS, MKE staj, mülakat, maaş). MSB, MSÜ, subay, astsubay, uzman erbaş, sözleşmeli er, rütbe, KPSS ile TSK alımı için yazı bulunmadı.
- Yakın içerik (iç link kaynağı olarak kullanılabilir):
  - `/subay-astsubay-beylik-tabancasi-hakki/`
  - `/uzman-erbas-silah-tasima-hakki/`
  - `/polis-askeri-personel-silah-tasima-hakki/`
  - `/beylik-tabancasi-nedir/`
  - `/jandarma-hangi-silahlari-kullaniyor/`
  - `/aselsan-is-basvurusu-mulakat-sureci/` (sanayi mülakatı, TSK değil; karışmaması için ayrı tutulacak)
- Depoda (`/home/user/guest`) askerî kariyer dosyası yok. Mevcut rutinler: HÜRJET SEO planı, Bedail al-Gharb (haftalık), Threat and Shield, DİKAB Dershanesi (28.10–05.11 zamanlanmış), Canik/KAAN/FNSS kart ve haber paketleri.
- Not: REST araması Türkçe karakterli ve boş sonuçlu sorgularda hata verdi; `MSÜ`, `sözleşmeli er`, `rütbe`, `maaş subay`, `jandarma alım` aramaları sonuç döndürmedi. Yayından önce WP yönetim panelinde başlık+slug taraması (HÜRJET planındaki "var olan sayfayı güncelle" kuralı) tekrarlanmalı.

### Çakışma analizi
| Konu | Risk | Çözüm |
|---|---|---|
| "Kariyer" kategorisi savunma sanayii | Karışım, yanlış iç link, mülakat sorgularında kendi sayfalarımızla kanibalizasyon | Yeni, ayrı kategori **Askerî Kariyer**; sanayi mülakat yazıları ayrı kalır, karşılıklı "TSK mu sanayi mi" kutusu |
| Haber kategorisi 53/24795 | Güncel alım haberi Savunma Haberleri akışında boğulur | Haber: 53 + Askerî Kariyer; rehberler yalnız Askerî Kariyer |
| Yayın rutinleri | Gece/hafta içi yayın slotları dolu | Slot çakışması yok; ilk haber dışındaki yayınlar günde ≤2 |
| Çok dilli (Polylang) | Her yazıya 5 dil açma refleksi | Bu dikey **yalnız TR** başlar; dil kararı Search Console verisine bağlı |
| Tekrar içerik kuralı | Aynı bilgi birden çok sayfada | Şart tabloları tek canonical sayfada, diğerleri link verir |

## 2) 2026 MSB subay alımı — resmî kaynak doğrulama raporu

Ortada **üç ayrı alım** var; görseldeki bilgiler bunları birleştiriyor görünüyor.

| Alım | Kontenjan | Başvuru | Puan türü |
|---|---|---|---|
| **Muvazzaf Subay Adayı Temini (genel kılavuz)** | 1.289 (Kara 837, Hava 308, Deniz 144) | 12 Ekim – **2 Kasım 2026 17.30** | KPSS Lisans **P3** (2025 veya 2026; yüksek olan) |
| **Deniz Kuvvetleri deniz sınıfı (ayrı kılavuz)** | 50 (35 güverte, 15 makine) | 12 Ekim – 2 Kasım 2026 | KPSS yok; genel kültür sınavı en az 50 |
| **MSÜ öğretmen/mühendis + tabip/diş tabibi/özel nitelikli BEÖ** | 346 (163+56 = 219 öğretmen-mühendis; 85+6+36 = 127 diğer) | 5 – **20 Ekim 2026** (**kapandı**) | ALES en az 70 (öğretmen, mühendis); genel kültür 50 (diğerleri) |

Toplam 1.339 = 1.289 + 50. Jandarma 135 subay ayrı alımdır (kapanış 26 Ekim, JSGA sistemi).

### Görsel iddiaları vs bulgular
| İddia | Sonuç | Not |
|---|---|---|
| Lisans 27 yaş | **Doğrulandı (ikincil)** | 1 Ocak 2026 esas; 1 Ocak 1999 ve sonrası doğumlu |
| Lisansüstü 32 yaş | **Doğrulandı (ikincil)** | 1 Ocak 1994 ve sonrası; programın **tamamlanmış** olması gerekir, öğrencilik yetmez. Veteriner/eczacı ve tıp/diş için 32 yaş ayrıca anılıyor; kaynaklar çelişiyor → kılavuzdan |
| 2 Kasım'a kadar başvuru | **Kısmen doğru** | Yalnız genel kılavuz ve deniz sınıfı için. 346'lık alım 20 Ekim'de kapandı |
| 2025 ve 2026 KPSS P3 | **Doğrulandı, kapsam dar** | Genel kılavuzda geçerli; 2024 ve öncesi kabul edilmiyor. Piyade (Komando) en az 60, diğerleri 70. Deniz sınıfı ve tabip/BEÖ'de KPSS yok |
| Erkek 168 / kadın 162 cm | **DOĞRULANAMADI** | Hiçbir kaynakta yok. Resmî olmayan bir hukuk sitesi 165/160 yazıyor. Branş/sınıfa göre değişebilir. Yayımlama |
| Psikoloji, İngilizce öğretmenliği, beden eğitimi | **Yanlış alıma ait olabilir** | Bu branşlar 346'lık MSÜ öğretmen alımında geçiyor (kapandı, ALES). Genel KPSS alımındaki branş listesi kılavuzdan çekilmeli |
| Mühendislik | Her ikisinde de var | Genel kılavuzda mühendislik sınıfı ve 346'da MSÜ mühendis (bilgisayar 12, elektronik 8…) ayrı |

Seçim aşamaları (ikincil): evrak kontrolü, fiziki değerlendirme, kişilik testi, fiziki yeterlilik, mülakat, sağlık kurulu, güvenlik soruşturması. Seçimler Ankara Mamak MEBS Okulu ve Eğitim Merkezi Komutanlığı'nda. 346'lık alımda mülakattan geçmek için en az 70 puan; ağırlıklar ALES %60 / fiziki %15 / mülakat %25 (öğretmen-mühendis). Genel kılavuzun puan ağırlıkları **bulunamadı**. Başvuru ücreti 600 TL (VakıfBank), şehit-gazi yakınları muaf (kılavuz şartlarıyla).

### Editör kontrol listesi (kılavuz PDF'inden, yayın öncesi zorunlu)
- [ ] Alımın resmî adı ve kılavuz tarihi
- [ ] Başvuru bitiş saati ve ücret son ödeme saati
- [ ] Sınıf/branş tablosu ve kadın-erkek kontenjanı
- [ ] Boy ve kilo (VKİ) şartı — sınıf bazında
- [ ] Lisansüstü ve veteriner/eczacı/tıp yaş maddeleri
- [ ] Fiziki yeterlilik testi hareketleri ve puanlama
- [ ] Genel kılavuzdaki puan ağırlıkları ve mülakat geçme puanı
- [ ] Kara Havacılık pilot/İHA yaş istisnası

## 3) İçerik boşluğu ve arama niyeti (hacimsiz)

Google'ın otomatik tamamlama ve ilgili aramaları bu ortamdan çekilemedi; aşağıdaki gruplandırma görev tanımındaki sorgulara ve arama sonuçlarında görünen rakip yapıya dayanır, **hacim iddiası içermez**.

- Sonuçlarda görülen rakipler: eleman.net, memur365, memurlar.net, ekonomist, Milliyet, NTV, yerel haber siteleri ve hukuk büroları. Çoğu **tek seferlik haber**; güncelliği yönetilen, kılavuzları birbirinden ayıran kalıcı rehber az. Rakip haberlerde kontenjan (346 / 219 / 1.339) ve tarih (20 Ekim / 2 Kasım) çelişkisi var → **"hangi alım, hangi tarih" netliği** en güçlü fark.
- Boşluklar: (a) alım türlerini ayıran sayfa, (b) yaş hesabı, (c) KPSS P3 / ALES farkı, (d) mülakat hazırlığı, (e) etkileşimli test. Hepsi sitede sıfırdan.

## 4) İlk 10 yayın (öncelik sırası)

Tümü TR, "Askerî Kariyer" kategorisi. 1–3 zaman kritik, 4'ten sonrası kılavuz doğrulamasına bağlı.

| # | Tür | Başlık | Slug | Neden / bağımlılık |
|---|---|---|---|---|
| 1 | Haber | MSB 2026 Subay Alımı: Kimler Başvurabilir? Yaş, KPSS, Boy ve Branş Şartları | `/msb-2026-subay-alimi/` | Son gün 2 Kasım; taslak ayrı dosyada. Boy satırı doğrulanana dek "kılavuzda sınıfa göre belirtilir" |
| 2 | Rehber | Subaylık Yaş Sınırı Nasıl Hesaplanır? (1 Ocak 2026 esası) | `/askeri-kariyer/subaylik-yas-siniri/` | Kılavuz doğrulaması yeterli; haberin ilk iç linki |
| 3 | Rehber | MSB 346 mi, 1.339 mu? 2026 Subay Alımlarının Farkı | `/askeri-kariyer/2026-subay-alimlari-farki/` | Rakiplerdeki karışıklığı çözer; kapanmış 346 alımını "kapandı" etiketiyle anlatır |
| 4 | Rehber (pillar) | Subay Nasıl Olunur? Güncel Başvuru ve Eğitim Yolları | `/askeri-kariyer/subay-nasil-olunur/` | Hub; MSÜ, muvazzaf alım, yedek subaylık ayrımı |
| 5 | Rehber | Subaylık KPSS P3 ve ALES Şartı | `/askeri-kariyer/subaylik-kpss-p3/` | Haber 1'den doğan soru |
| 6 | Rehber | Subaylık Mülakatında Neler Sorulur? | `/askeri-kariyer/subaylik-mulakat-sorulari/` | Mülakat kümesinin çekirdeği; kurul kriterleri uydurulmaz, yalnız kılavuzdaki puanlama |
| 7 | Rehber | Subaylık Fiziki Yeterlilik Testi | `/askeri-kariyer/subaylik-fiziki-yeterlilik/` | Hareket ve puanlar yalnız kılavuzdan |
| 8 | Rehber | Subaylık Boy ve Kilo Şartları | `/askeri-kariyer/subaylik-boy-kilo-sartlari/` | Sınıf bazlı tablo; 168/162 meselesi netleşir |
| 9 | Rehber | Muvazzaf ve Sözleşmeli Subay Arasındaki Fark | `/askeri-kariyer/muvazzaf-sozlesmeli-subay-farki/` | Mevzuat kaynaklı, kılavuz bağımsız |
| 10 | Soru bankası | Subaylık Mülakatı: 50 Örnek Hazırlık Sorusu | `/askeri-kariyer/mulakat-hazirlik/subaylik-ornek-sorular/` | "Örnek hazırlık sorusu" etiketi zorunlu; simülatörün veri tabanı |

Hub `/askeri-kariyer/` 4. yazıyla birlikte açılır. Astsubay, uzman erbaş, MSÜ ve maaş rehberleri ikinci dalga (11–20).

## 5) Onay gereken kararlar
1. Yeni kategori **Askerî Kariyer** (mevcut "Kariyer" kategorisi dokunulmadan) ve `/askeri-kariyer/` URL öneki uygun mu? WP'de mevcut kalıcı bağlantı yapısı doğrulanmadı.
2. Resmî kılavuz PDF'ini bana iletebilir misiniz? Yüklenirse tablo ve boy/kilo maddelerini satır satır doğrulayıp haberi kesinleştiririm.
3. Haberi yalnız TR mi, 5 dilde mi açalım? Öneri: TR.
4. Search Console erişimi ve Semrush kotası olmadan bu plan hacimsizdir; erişim sağlanırsa sıralamayı güncellerim.

## 6) Sonraki teslimatlar (bu turda yapılmadı)
İlk 100 konu adayı, en önemli 30, 30 günlük takvim, ilk 5 rehberin tam metni, 50 örnek soru, simülatör tasarımı, günlük rutin ve Search Console ölçüm planı. Haber taslağı `02-haber-taslagi-msb-2026-subay-alimi.md` dosyasında.
