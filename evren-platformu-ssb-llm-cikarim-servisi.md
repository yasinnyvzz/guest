# SSB'nin EVREN Platformu yayında: yerli H200 altyapısıyla 11 yapay zekâ modeline tek API'den erişim

**Özet:** Cumhurbaşkanlığı Savunma Sanayii Başkanlığı (SSB) bünyesinde, Savunma Sanayii Yapay Zekâ (SSYZ) girişimi kapsamında geliştirilen **EVREN Platformu**'nun LLM Çıkarım Servisi kullanıma açıldı. Türkiye'de konumlandırılan **64 adet NVIDIA H200 GPU**'dan oluşan yerli altyapı üzerinde çalışan sistem, açık ağırlıklı büyük dil modellerine OpenAI uyumlu tek bir API üzerinden erişim sağlıyor. Platform, SAHA EXPO 2026'da da tanıtıldı ve yabancı bulut servislerine ile ihracat kısıtlamalarına (ITAR/EAR) bağımlılığı azaltmayı hedefliyor.

## EVREN nedir?

EVREN, SSB'nin SSYZ (Savunma Sanayii Yapay Zekâ) girişimi kapsamında hayata geçirdiği, veri hazırlama, veri etiketleme, model eğitimi, test süreçleri, model yayınlama ve operasyonel kullanım aşamalarını tek bir merkezi yapı altında birleştiren uçtan uca bir **MLOps (Makine Öğrenmesi Operasyonları) platformu**. Platform, yerli ve millî yapay zekâ ekosistemini güçlendirmek ve nitelikli insan kaynağı kapasitesini artırmak amacıyla geliştirildi; kendi bare-metal HPC altyapısı üzerinde çalışarak yabancı bulut sağlayıcılarına ve ihracat kısıtlamalarına (ITAR/EAR) tabi platformlara bağımlılığı azaltmayı hedefliyor.

Platform, `evren.ssyz.org.tr` adresinden **e-Devlet kimlik doğrulaması** ile erişime açılıyor. Kullanıcılar, veri seti yükleme ve etiketleme gibi katkılar karşılığında kredi kazanıyor ve bu kredileri yüksek kapasiteli GPU kaynaklarına erişim için kullanabiliyor. Yeni kullanıcılara başlangıçta 1.000 CR kredi tanınıyor.

## LLM Çıkarım Servisi devreye alındı

EVREN'in LLM Çıkarım (LLM Inference) modülü, açık ağırlıklı büyük dil modellerine hem tarayıcı üzerinden sohbet arayüzüyle hem de OpenAI uyumlu API üzerinden erişim sunuyor. Servis; yerli H200 altyapısı, akıllı model yönlendirme (Auto Router) ve canlı telemetri gibi özelliklerle öne çıkıyor. Sosyal medyada paylaşılan tanıtım içeriklerine göre platform, tek bir API üzerinden 11 farklı yapay zekâ modeline erişim sağlıyor.

*Not: LLM model çağrılarının kredi kesintisinden muaf tutulduğu süreye ilişkin platformun kendi duyurusu **1 Kasım 2026** tarihini işaret ederken, konuyla ilgili bazı sosyal medya paylaşımlarında bu süre "ilk 1 ay ücretsiz kullanım" şeklinde aktarılmıştır. Kesin ve güncel koşullar için platformun resmî sayfası esas alınmalıdır.*

## Gelişmiş akıl yürütme ve yazılım geliştirme

Platform bünyesinde yer alan **GLM-5.3, DeepSeek-V4-Flash, Qwen3.8-Flash-Next** ve **Gemma-4-31B** modelleri, 1 milyon token'a (1M bağlam penceresi) varan kapasiteleriyle dikkat çekiyor. Bu modeller sayesinde karmaşık yazılım geliştirme süreçleri, geniş kod tabanı analizi, derin akıl yürütme ve çok adımlı otonom ajan iş akışlarının desteklendiği belirtiliyor.

## Görsel, ses ve belge analizi

Çok modlu (multimodal) işleme kapasitesi sunan **Qwen3-VL-30B, Qwen3-ASR, dots-ocr** ve **DeepSeek-OCR-2** modelleri; 260 saniyeye kadar video analizi, 30 dilde yüksek doğruluklu ses tanıma, karmaşık arşiv dijitalleştirme ve bilimsel şemaların SVG formatına dönüştürülmesi gibi işlevleri destekliyor.

## Kurumsal RAG ve içerik güvenliği

Anlamsal arama ve veri doğruluğunu artırmak amacıyla entegre edilen **Qwen3-Embedding-8B, Qwen3-Reranker-8B** ve **Qwen3-Guard-4B** modelleri; esnek vektör boyutlarıyla kurumsal RAG (Retrieval-Augmented Generation) sistemlerinde yüksek hassasiyet sağlarken, kapsamlı içerik güvenliği ve risk tespiti de sunuyor.

## Yerli altyapı ve kolay entegrasyon

Platform, OpenAI uyumlu API, Python SDK ve anlık yüke göre model seçen Auto Router mimarisiyle geliştiricilere kolay entegrasyon imkânı tanıyor. Eğitim tarafında 64 NVIDIA H200 GPU, görüntü çıkarımı tarafında ise 8 NVIDIA A6000 GPU'dan oluşan yerli altyapı sayesinde tüm veri ve model trafiğinin Türkiye sınırları içinde kalması sağlanarak üst düzey veri güvenliği hedefleniyor.

## Üniversitelerde ve SAHA EXPO'da tanıtım

Platform; Ankara Üniversitesi, Hacettepe Üniversitesi, Selçuk Üniversitesi, Sakarya Üniversitesi ve Bursa Uludağ Üniversitesi gibi çok sayıda akademik kurumun resmî web sitelerinde duyurularla paylaşılarak öğrencilerin ve araştırmacıların bilimsel çalışmalarında kullanımına yönlendirildi. Ayrıca EVREN, savunma sanayiinin önde gelen fuarlarından **SAHA EXPO 2026**'da da sergilenerek yapay zekâ projelerinin uçtan uca yönetilmesini sağlayan yerli ve millî bir MLOps platformu olarak tanıtıldı.

## Sonuç

SSB'nin SSYZ girişimi kapsamında hayata geçirdiği EVREN Platformu ve onun LLM Çıkarım Servisi, savunma sanayiinde ve daha geniş kamu/akademi ekosisteminde yerli ve millî yapay zekâ altyapısı hedefi doğrultusunda önemli bir adım olarak öne çıkıyor. Yerli H200 GPU altyapısı, OpenAI uyumlu tek API üzerinden çoklu model erişimi ve kredi tabanlı kullanım modeli, platformu geliştiriciler, akademisyenler ve kurumlar için dikkat çekici kılıyor.

---

*Kaynaklar:*
- *[Evren Yapay Zeka Platformu – Ankara Üniversitesi Yapay Zeka Enstitüsü](https://yze.ankara.edu.tr/2026/06/19/evren-yapay-zeka-platformu/)*
- *[EVREN Yapay Zekâ MLOps Platformu Kullanıma Açıldı – Selçuk Üniversitesi](https://selcuk.edu.tr/birim/icerik/5337/evren-yapay-zek-mlops-platformu-kullanima-acildi-80270)*
- *[EVREN Yapay Zekâ Geliştirme Platformu (MLOps) – Hacettepe Üniversitesi](https://isletme.hacettepe.edu.tr/tr/evren_yapay_zek%C3%A2_gelistirme_p-1362)*
- *[LLM Çıkarımı – EVREN resmî sayfası](https://evren.ssyz.org.tr/llm-inference/)*
- *[Keşfet – EVREN Yapay Zeka Platformu](https://evren.ssyz.org.tr/explore/)*
- *[EVREN Nedir? Yapay Zekâ Platformu, Giriş ve API Rehberi – Yapay Zeka Okulum](https://www.yapayzekaokulum.com/blog/evren-yapay-zeka-platformu-nedir)*
- *[SAHA EXPO 2026'da EVREN tanıtımı – Siber Diplomasi & İstihbarat Araştırmaları Merkezi (X)](https://x.com/sdiam_tr/status/2062541790347989472)*
- *[WeeklyOne.co Instagram gönderisi – "SSB Bünyesinde Geliştirilen EVREN Platformu"](https://www.instagram.com/weeklyone.co/) (model listesi ve yetenek özetleri için)*

*Bu haber, yukarıdaki kaynaklardan derlenen kamuya açık bilgilere dayanmaktadır (erişim: Eylül 2026). SSB'nin ek resmî açıklamaları yayımlandıkça güncellenecektir.*
