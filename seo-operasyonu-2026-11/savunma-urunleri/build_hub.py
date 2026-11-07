import json,html,collections
from urunler import URUNLER,B
def link(ad,slug):
    if not slug: return html.escape(ad)
    u = "https://envantermedya.com/"+slug[1:]+"/" if slug.startswith("@") else B+slug+"/"
    return f'<a href="{u}">{html.escape(ad)}</a>'
cats=collections.OrderedDict()
for k,*r in URUNLER: cats.setdefault(k,[]).append(r)
intro={
"Savaş uçakları":"Türkiye'nin yerli savaş uçağı ve eğitim uçağı projeleri TUSAŞ çatısında toplanıyor.",
"İnsansız hava araçları":"Baykar ve TUSAŞ, silahlı ve muharip insansız hava araçlarında öne çıkan iki üreticidir.",
"Helikopterler":"Yerli helikopter programları taarruz ve genel maksatlı sınıfları kapsar.",
"Tanklar":"Yerli tank projeleri Otokar, BMC ve FNSS çevresinde şekilleniyor.",
"Zırhlı araçlar":"Tekerlekli ve mayına karşı korumalı zırhlı araçlar hem envanterde hem ihracatta yer alıyor.",
"Piyade silahları":"Piyade tüfekleri ağırlıklı olarak MKE'nin milli tüfek programlarından çıkıyor.",
"Füzeler":"Gemisavar, seyir ve balistik füzeler Roketsan ve TÜBİTAK SAGE tarafından geliştiriliyor.",
"Hava savunma":"Katmanlı hava savunma, ASELSAN ve Roketsan'ın ortak çalıştığı ürün ailelerinden oluşuyor.",
"Radar ve elektronik harp":"Radar ve elektronik harp sistemlerinin başlıca geliştiricisi ASELSAN'dır.",
"Savaş gemileri":"MİLGEM programı ve büyük deniz platformları yerli tasarım gemi üretiminin omurgasıdır.",
}
h=["<p><strong>Türk savunma sanayii ürünleri</strong>; savaş uçaklarından insansız hava araçlarına, tanklardan füzelere, hava savunma sistemlerinden savaş gemilerine kadar yerli ve millî olarak geliştirilen platformlardan oluşur. Bu sayfa, başlıca ürünlerin adını, üreticisini, temel görevini ve genel durumunu kategoriler hâlinde tek tabloda toplar; her ürünün ayrıntılı dosyasına bağlantı verir. Durum bilgisi genel evreyi gösterir ve düzenli olarak güncellenir.</p>",
"<h2>Türk savunma sanayii nedir?</h2><p>Türk savunma sanayii, Savunma Sanayii Başkanlığı'nın (SSB) koordinasyonunda; kamu ve özel şirketlerin silah, araç, platform ve sistem geliştirdiği sanayi alanıdır. Başlıca şirketler arasında ASELSAN, TUSAŞ, Roketsan, Baykar, STM, HAVELSAN, MKE, BMC, FNSS ve Otokar bulunur. <em>Savunma sanayi</em> ve <em>savunma sanayii</em> yazımlarının ikisi de kullanılır; bu sitede “savunma sanayii” tercih edilir.</p>",
"<h2>Kategorilere göre yerli savunma ürünleri</h2><p>Aşağıdaki tablolar her kategoride öne çıkan ürünleri listeler. Ürün adları, varsa Envanter Medya'daki ayrıntılı dosyaya bağlanır.</p>"]
n=3
for k,rows in cats.items():
    h.append(f"<h3>{k}</h3><p>{intro[k]}</p><table><thead><tr><th>Ürün adı</th><th>Üretici</th><th>Temel görev</th><th>Genel durum</th></tr></thead><tbody>")
    for ad,ur,gor,dur,slug in rows:
        h.append(f"<tr><td>{link(ad,slug)}</td><td>{html.escape(ur)}</td><td>{html.escape(gor)}</td><td>{html.escape(dur)}</td></tr>")
    h.append("</tbody></table>")
h.append("<h2>Türk savunma sanayii şirketleri</h2><table><thead><tr><th>Şirket</th><th>Uzmanlık alanı</th><th>Önemli ürünler</th></tr></thead><tbody>"
"<tr><td>ASELSAN</td><td>Radar, elektronik harp, haberleşme, hava savunma</td><td>KORKUT, GÖKDENİZ, MURAD, KORAL</td></tr>"
"<tr><td>TUSAŞ</td><td>Uçak, helikopter, İHA</td><td>KAAN, HÜRJET, HÜRKUŞ, GÖKBEY, ANKA, AKSUNGUR</td></tr>"
"<tr><td>Roketsan</td><td>Füze ve roket sistemleri</td><td>ATMACA, TAYFUN, BORA, SİPER</td></tr>"
"<tr><td>Baykar</td><td>İnsansız hava ve muharip hava araçları</td><td>Bayraktar TB2, AKINCI, KIZILELMA</td></tr>"
"<tr><td>MKE</td><td>Silah ve mühimmat</td><td>MPT-76, MPT-55</td></tr>"
"<tr><td>BMC, FNSS, Otokar</td><td>Zırhlı ve tekerlekli askerî araçlar, tank</td><td>KİRPİ II, VURAN, PARS, KAPLAN MT, COBRA II, ALTAY</td></tr>"
"<tr><td>STM</td><td>Deniz platformları ve sistem entegrasyonu</td><td>MİLGEM projeleri</td></tr></tbody></table>")
h.append("<h2>Sık sorulan sorular</h2>"
"<h3>Türkiye'nin yerli savaş uçağı hangisi?</h3><p>KAAN, TUSAŞ tarafından geliştirilen 5. nesil millî savaş uçağı projesidir. HÜRJET ve HÜRKUŞ ise eğitim ve hafif taarruz uçaklarıdır.</p>"
"<h3>Bayraktar TB2'yi kim üretiyor?</h3><p>Bayraktar TB2, Baykar tarafından üretilen silahlı insansız hava aracıdır.</p>"
"<h3>HİSAR ile SİPER arasındaki fark nedir?</h3><p>HİSAR alçak ve orta irtifa, SİPER ise daha uzun menzilli hava ve füze savunma için geliştirilen sistem ailesidir.</p>"
"<h3>Bu liste tam mı?</h3><p>Hayır. Liste başlıca ürünleri kapsar ve Savunma Sanayii Başkanlığı kataloğu ile üretici kaynakları doğrultusunda genişletilir.</p>"
"<p><em>Son güncelleme: 7 Kasım 2026. Kaynaklar: SSB, ASELSAN, TUSAŞ, Roketsan, Baykar ve ilgili şirketlerin resmî sayfaları.</em></p>")
body="\n".join(h)
d={"lang":"tr","title":"Türk Savunma Sanayii Ürünleri: Yerli ve Millî Silah, Araç ve Sistemlerin İsimleri","slug":"turk-savunma-sanayii-urunleri",
"excerpt":"Türk savunma sanayii ürünlerinin isimleri, üreticileri, görevleri ve genel durumları kategoriler hâlinde tek sayfada.",
"content_html":body,"rank_math_title":"Türk Savunma Sanayii Ürünleri: İsimler ve Üreticiler","rank_math_description":"Türk savunma sanayii ürünlerinin isimleri, üreticileri, görevleri ve genel durumları: KAAN, TB2, ALTAY, ATMACA, HİSAR, SİPER ve daha fazlası.",
"rank_math_focus_keyword":"türk savunma sanayii ürünleri","category_hint":"Savunma Sanayii Rehberi","status_decision":"NEW",
"verification_notes":["Durum sütunu genel evredir; SSB kataloğuna erişilemediği için yayın öncesi üretici/SSB ile doğrulanmalı","İstif sınıfı, ALTAY, GÖKBEY, HÜRJET durumları öncelikli doğrulama","Görsel yok: lisanslı/resmî basın görseli eklenmeli"],
"sources":[],"internal_links":[]}
json.dump(d,open("../taslaklar/tr-turk-savunma-sanayii-urunleri.json","w"),ensure_ascii=False,indent=1)
open("../taslaklar/tr-turk-savunma-sanayii-urunleri.html","w").write("<h1>"+d["title"]+"</h1>"+body)
print(len(body))
