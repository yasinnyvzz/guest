import json,html,requests
B="https://envantermedya.com/envanter/"
HUB="https://envantermedya.com/turk-savunma-sanayii-urunleri/"
def a(t,s): return f'<a href="{B}{s}/">{t}</a>'
# ---- KPSS
Q=[
("KAAN hangi kurum tarafından geliştirilmektedir?",["Baykar","TUSAŞ","ASELSAN","Roketsan"],1,"KAAN, TUSAŞ'ın geliştirdiği 5. nesil millî savaş uçağı projesidir."),
("Bayraktar TB2'nin üreticisi hangisidir?",["Baykar","TUSAŞ","MKE","STM"],0,"Bayraktar TB2 silahlı insansız hava aracını Baykar üretir."),
("Aşağıdakilerden hangisi bir ana muharebe tankı projesidir?",["PARS","ALTAY","KİRPİ","VURAN"],1,"ALTAY ana muharebe tankıdır; diğerleri zırhlı/taktik araçlardır."),
("HÜRJET hangi amaçla geliştirilmiştir?",["Gemisavar füzesi","İleri jet eğitim ve hafif taarruz","Hava savunma","Elektronik harp"],1,"HÜRJET, TUSAŞ'ın ileri jet eğitim ve hafif taarruz uçağıdır."),
("HÜRKUŞ'un görevi aşağıdakilerden hangisidir?",["Temel eğitim ve hafif taarruz","Ağır nakliye","Denizaltı savunma","Uydu fırlatma"],0,"HÜRKUŞ turboprop temel eğitim uçağıdır; hafif taarruz görevine uygundur."),
("GÖKBEY nedir?",["Savaş gemisi","Genel maksatlı helikopter","Tüfek","Gemisavar füzesi"],1,"GÖKBEY, TUSAŞ'ın genel maksatlı helikopteridir."),
("ATMACA hangi tür silahtır?",["Gemisavar füzesi","Piyade tüfeği","Zırhlı araç","İnsansız deniz aracı"],0,"ATMACA, Roketsan'ın gemisavar füzesidir."),
("ATMACA'nın geliştiricisi hangi şirkettir?",["ASELSAN","Roketsan","Otokar","HAVELSAN"],1,"ATMACA'yı Roketsan geliştirmiştir."),
("Alçak ve orta irtifa hava savunma için geliştirilen sistem ailesi hangisidir?",["HİSAR","TAYFUN","ALTAY","MPT-76"],0,"HİSAR alçak ve orta irtifa hava savunma ailesidir."),
("SİPER hangi amaçla geliştirilmiştir?",["Uzun menzilli hava ve füze savunma","Piyade desteği","Denizaltı tespiti","Siber savunma"],0,"SİPER, uzun menzilli hava ve füze savunma sistemidir."),
("MİLGEM projesi hangi alanla ilgilidir?",["Millî gemi inşası","Millî tüfek","Millî uçak","Millî uydu"],0,"MİLGEM, Millî Gemi projesidir."),
("MPT-76'yı hangi kurum üretir?",["MKE","ASELSAN","BMC","TEI"],0,"MPT-76 millî piyade tüfeğini MKE üretir."),
("Aşağıdakilerden hangisi bir balistik füzedir?",["TAYFUN","ATMACA","KORKUT","GÖKDENİZ"],0,"TAYFUN, Roketsan'ın balistik füzesidir."),
("KORKUT'u hangi şirket geliştirmiştir?",["ASELSAN","TUSAŞ","Baykar","FNSS"],0,"KORKUT, ASELSAN'ın alçak irtifa hava savunma sistemidir."),
("GÖKDENİZ ne tür bir sistemdir?",["Gemi yakın hava savunma sistemi","Tank","Helikopter","Tabanca"],0,"GÖKDENİZ, gemilerde kullanılan yakın hava savunma sistemidir."),
("Aşağıdakilerden hangisi elektronik ve radar alanında öne çıkan şirkettir?",["ASELSAN","MKE","Sarsılmaz","Otokar"],0,"ASELSAN radar, elektronik harp ve haberleşme alanlarında öne çıkar."),
("TCG Anadolu hangi tür gemidir?",["Amfibi hücum gemisi (LHD)","Denizaltı","Fırkateyn","Karakol botu"],0,"TCG Anadolu amfibi hücum gemisidir."),
("Savunma sanayiinin koordinasyonundan sorumlu kurum hangisidir?",["Savunma Sanayii Başkanlığı","Milli Eğitim Bakanlığı","TÜBİTAK","Sayıştay"],0,"Savunma sanayii projelerini SSB koordine eder."),
("Bayraktar AKINCI hangi tür araçtır?",["Taarruz insansız hava aracı","Tank","Fırkateyn","Uydu"],0,"AKINCI, Baykar'ın taarruz İHA'sıdır."),
("Aşağıdakilerden hangisi TUSAŞ ürünü değildir?",["ANKA","AKSUNGUR","HÜRJET","ATMACA"],3,"ATMACA Roketsan ürünüdür; diğerleri TUSAŞ ürünleridir."),
]
L="ABCD"
def kpss():
    h=[f'<p>Savunma sanayii ürünleri genel kültür sorularında ürün adı, üretici ve görev eşleştirmesi olarak karşımıza çıkar. Bu rehber, <strong>yerli ve millî savunma sanayii ürünlerini</strong> kısa cevaplarla toplar: hangi ürünü hangi kurum geliştirir, ne işe yarar. Aşağıdaki sorular Envanter Medya tarafından hazırlanmış örneklerdir; resmî KPSS sorusu değildir ve belirli bir ürünün sınavda çıkacağı anlamına gelmez. Daha geniş liste için <a href="{HUB}">Türk savunma sanayii ürünleri</a> sayfasına bakın.</p>',
"<h2>Kısa cevaplarla önemli ürünler</h2>",
f"<h3>KAAN hangi kurum tarafından geliştiriliyor?</h3><p>KAAN, TUSAŞ'ın geliştirdiği 5. nesil millî savaş uçağıdır. {a('KAAN dosyası','kaan')}</p>",
f"<h3>Bayraktar TB2'nin üreticisi kim?</h3><p>Baykar. {a('Bayraktar TB2','bayraktar-tb2-siha')}</p>",
f"<h3>ALTAY nedir?</h3><p>Millî ana muharebe tankı projesidir. {a('ALTAY','altay-amt-ana-muharebe-tanki')}</p>",
f"<h3>HÜRJET hangi amaçla geliştirildi?</h3><p>İleri jet eğitimi ve hafif taarruz için. {a('HÜRJET','hurjet')}</p>",
f"<h3>HÜRKUŞ nedir?</h3><p>TUSAŞ'ın temel eğitim ve hafif taarruz görevine uygun turboprop uçağıdır. {a('HÜRKUŞ','tusas-hurkus')}</p>",
f"<h3>GÖKBEY nedir?</h3><p>TUSAŞ'ın genel maksatlı helikopteridir. {a('GÖKBEY','gokbey')}</p>",
f"<h3>ATMACA nedir?</h3><p>Roketsan'ın gemisavar füzesidir. {a('ATMACA','atmaca-gemisavar-fuzesi')}</p>",
f"<h3>HİSAR ve SİPER arasındaki fark nedir?</h3><p>HİSAR alçak ve orta irtifa, SİPER ise uzun menzilli hava ve füze savunma içindir. {a('HİSAR','hisar')} · {a('SİPER','roketsan-siper')}</p>",
f"<h3>MİLGEM nedir?</h3><p>Millî Gemi projesidir; Ada sınıfı korvetler ve İstif sınıfı fırkateynler bu çatıdadır. {a('MİLGEM','milgem-ada-sinifi')}</p>",
f"<h3>Yerli piyade tüfekleri hangileri?</h3><p>MKE'nin MPT-76 ve MPT-55 tüfekleri başlıca örneklerdir. {a('MPT-76','piyade-tufegi-mpt-76')}</p>",
"<h2>Hızlı tekrar tablosu</h2><table><thead><tr><th>Ürün</th><th>Üretici</th><th>Ne olduğu</th></tr></thead><tbody>"
"<tr><td>KAAN</td><td>TUSAŞ</td><td>5. nesil savaş uçağı</td></tr><tr><td>HÜRJET</td><td>TUSAŞ</td><td>İleri jet eğitim/hafif taarruz</td></tr><tr><td>HÜRKUŞ</td><td>TUSAŞ</td><td>Temel eğitim uçağı</td></tr><tr><td>GÖKBEY</td><td>TUSAŞ</td><td>Genel maksatlı helikopter</td></tr>"
"<tr><td>Bayraktar TB2 / AKINCI</td><td>Baykar</td><td>Silahlı/taarruz İHA</td></tr><tr><td>ALTAY</td><td>Otokar / BMC</td><td>Ana muharebe tankı</td></tr><tr><td>ATMACA</td><td>Roketsan</td><td>Gemisavar füzesi</td></tr><tr><td>TAYFUN</td><td>Roketsan</td><td>Balistik füze</td></tr>"
"<tr><td>HİSAR</td><td>ASELSAN, Roketsan</td><td>Alçak/orta irtifa hava savunma</td></tr><tr><td>SİPER</td><td>Roketsan, ASELSAN</td><td>Uzun menzilli hava savunma</td></tr><tr><td>KORKUT</td><td>ASELSAN</td><td>Alçak irtifa hava savunma</td></tr><tr><td>MPT-76</td><td>MKE</td><td>Millî piyade tüfeği</td></tr></tbody></table>",
"<h2>Şirketler ve uzmanlık alanları</h2><p>ASELSAN: radar, elektronik harp, haberleşme. TUSAŞ: uçak, helikopter, İHA. Roketsan: füze ve roketler. Baykar: insansız hava araçları. MKE: silah ve mühimmat. STM: deniz platformları ve sistem entegrasyonu. HAVELSAN: yazılım ve komuta kontrol sistemleri.</p>",
"<h2>20 örnek çoktan seçmeli soru</h2><p>Sorular bu sitenin hazırladığı çalışma örnekleridir.</p><ol>"]
    for q,o,c,e in Q:
        h.append(f"<li><p>{html.escape(q)}</p><p>"+" ".join(f"{L[i]}) {html.escape(x)}" for i,x in enumerate(o))+"</p></li>")
    h.append("</ol><h2>Cevap anahtarı ve kısa açıklamalar</h2><ol>")
    for q,o,c,e in Q: h.append(f"<li><strong>{L[c]}</strong> — {html.escape(e)}</li>")
    h.append("</ol><p><em>Son güncelleme: 8 Kasım 2026. Kaynak: SSB 2026 Ürün Kataloğu ve ilgili şirketlerin resmî sayfaları. Güncel durum bilgisi için üretici duyurularına bakın.</em></p>")
    return "".join(h)
def sirket():
    return ('<p><strong>Türkiye\'nin savunma sanayii şirketleri</strong>; uçaktan füzeye, zırhlı araçtan yazılıma geniş bir ürün yelpazesi geliştirir. SSB 2026 Ürün Kataloğu, yüzü aşkın firmanın ürününü ayrı ayrı sunar. Aşağıdaki tablo başlıca şirketleri uzmanlık alanı ve öne çıkan ürünleriyle özetler; tüm ürünler için '
f'<a href="{HUB}">Türk savunma sanayii ürünleri</a> sayfasına bakın.</p>'
"<h2>Başlıca şirketler</h2><table><thead><tr><th>Şirket</th><th>Uzmanlık alanı</th><th>Önemli ürünler</th><th>Ürün kategorileri</th></tr></thead><tbody>"
f"<tr><td>ASELSAN</td><td>Elektronik, radar, haberleşme</td><td>{a('KORKUT','aselsan-korkut')}, {a('GÖKDENİZ','gokdeniz-yakin-hava-savunma-sistemi')}, {a('MURAD','aselsan-murad-100-a')}, {a('KORAL','aselsan-koral-ad')}</td><td>Radar, elektronik harp, hava savunma</td></tr>"
f"<tr><td>TUSAŞ</td><td>Havacılık ve uzay</td><td>{a('KAAN','kaan')}, {a('HÜRJET','hurjet')}, {a('HÜRKUŞ','tusas-hurkus')}, {a('GÖKBEY','gokbey')}, {a('ANKA','tusas-anka')}, {a('AKSUNGUR','tusas-aksungur')}</td><td>Savaş uçağı, helikopter, İHA</td></tr>"
f"<tr><td>Roketsan</td><td>Füze ve roket</td><td>{a('ATMACA','atmaca-gemisavar-fuzesi')}, {a('TAYFUN','roketsan-tayfun')}, {a('SİPER','roketsan-siper')}</td><td>Füze, hava savunma</td></tr>"
f"<tr><td>Baykar</td><td>İnsansız hava araçları</td><td>{a('Bayraktar TB2','bayraktar-tb2-siha')}, {a('AKINCI','bayraktar-akinci')}, {a('KIZILELMA','baykar-kizilelma')}</td><td>İHA, insansız muharip uçak</td></tr>"
"<tr><td>STM</td><td>Deniz platformları, sistem entegrasyonu</td><td>MİLGEM projeleri</td><td>Savaş gemisi, yazılım</td></tr>"
"<tr><td>HAVELSAN</td><td>Yazılım, komuta kontrol, simülasyon</td><td>Komuta kontrol ve simülatör sistemleri</td><td>Savunma yazılımı</td></tr>"
f"<tr><td>MKE</td><td>Silah ve mühimmat</td><td>{a('MPT-76','piyade-tufegi-mpt-76')}</td><td>Piyade silahı, mühimmat</td></tr>"
f"<tr><td>BMC</td><td>Askerî araç</td><td>{a('KİRPİ II','bmc-kirpi-ii')}, {a('VURAN','bmc-vuran')}</td><td>Zırhlı araç</td></tr>"
f"<tr><td>FNSS</td><td>Zırhlı muharebe araçları</td><td>{a('PARS','fnss-pars-alpha-8x8')}, {a('KAPLAN MT','kaplan-mt')}</td><td>Zırhlı araç, tank</td></tr>"
f"<tr><td>Otokar</td><td>Askerî araç, tank</td><td>{a('COBRA II','cobra-ii-mrap')}, {a('ALTAY','altay-amt-ana-muharebe-tanki')}</td><td>Zırhlı araç, tank</td></tr>"
"<tr><td>TEI</td><td>Havacılık motorları</td><td>Hava aracı motorları</td><td>Motor</td></tr><tr><td>Kale Jet Motorları</td><td>Jet motoru</td><td>Küçük jet motorları</td><td>Motor</td></tr></tbody></table>"
"<h2>Sık sorulan sorular</h2><h3>Savunma sanayii projelerini kim koordine eder?</h3><p>Cumhurbaşkanlığı Savunma Sanayii Başkanlığı (SSB).</p>"
"<h3>Katalogda kaç firma var?</h3><p>SSB 2026 Ürün Kataloğu'nun içindekiler bölümünde yüz elliden fazla firma satırı yer alır.</p>"
"<p><em>Son güncelleme: 8 Kasım 2026. Kaynaklar: SSB 2026 Ürün Kataloğu ve şirketlerin resmî sayfaları.</em></p>")
P=[("kpss-yerli-ve-milli-savunma-sanayii-urunleri","KPSS İçin Yerli ve Millî Savunma Sanayii Ürünleri: İsimler, Üreticiler ve Özellikleri","yerli savunma sanayi ürünleri kpss","KPSS için yerli savunma sanayii ürünleri: kısa cevaplar, hızlı tekrar tablosu, 20 örnek soru ve cevap anahtarı.","KPSS İçin Yerli Savunma Sanayii Ürünleri",kpss()),
("turkiye-savunma-sanayii-sirketleri","Türkiye'nin Savunma Sanayii Şirketleri ve Ürettikleri Ürünler","türk savunma sanayii şirketleri","Türkiye'nin savunma sanayii şirketleri, uzmanlık alanları ve ürettikleri ürünler: ASELSAN, TUSAŞ, Roketsan, Baykar ve daha fazlası.","Türk Savunma Sanayii Şirketleri ve Ürünleri",sirket())]
H={"User-Agent":"Mozilla/5.0 (EnvanterSEO)"};EV="https://envantermedya.com/wp-json"
for slug,t,fk,desc,rt,body in P:
    json.dump({"lang":"tr","title":t,"slug":slug,"content_html":body,"rank_math_focus_keyword":fk,"rank_math_description":desc,"rank_math_title":rt},open(f"../taslaklar/tr-{slug}.json","w"),ensure_ascii=False,indent=1)
    if requests.get(f"{EV}/wp/v2/posts",params={"slug":slug,"status":"publish,draft,future,pending","lang":"all","_fields":"id"},headers=H,timeout=60).json():
        print("VAR",slug);continue
    r=requests.post(f"{EV}/wp/v2/posts",json={"title":t,"slug":slug,"content":body,"excerpt":desc,"status":"draft","meta":{"rank_math_title":rt,"rank_math_description":desc,"rank_math_focus_keyword":fk}},headers=H,timeout=90)
    i=r.json().get("id");print(r.status_code,i,r.json().get("status"))
    if i: requests.post(f"{EV}/ev/v1/set-post-lang",json={"post_id":i,"lang":"tr"},headers=H,timeout=60)
