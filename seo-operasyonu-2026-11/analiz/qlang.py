import re
ES=set("de del la las los el y para con por que qué cuál cuantos cuántos cuántas tiene armada ejército ejercito fuerza fuerzas aérea aerea submarino submarinos avión aviones avion buque buques fragata fragatas españa española español méxico mexico argentina chile colombia perú peru venezuela militar militares guerra tanque tanques misil misiles caza cazas helicóptero helicoptero marina defensa nuevo nueva compra turquía turquia turco turca dron drones mundo mejor mejores más países pais país año sistema infantería portaaviones naval".split())
TR=set("iyi hafif silah tabanca modelleri kimin nerede romanya afrika iha siha ve ile nedir ne zaman kaç nasıl hangi alımı alımi başvuru basvuru şartları maaş maaşları maaslari savunma sanayi sanayii türk türkiye uçak uçağı tank füze hava kuvvetleri deniz kara jandarma polis askeri asker ilanı haberleri son dakika ilk özellikleri fiyatı hızı yerli milli için mı mi kadar sınav sonuçları tercih alım envanteri helikopteri gemisi denizaltı".split())
def qlang(q):
    if re.search(r'[Ѐ-ӿ]',q): return 'ru'
    if re.search(r'[؀-ۿ]',q): return 'ar'
    if re.search(r'[一-鿿]',q): return 'zh'
    if re.search(r'[ğışöüçĞİŞÖÜÇ]',q): return 'tr'
    w=re.findall(r'\w+',q.lower())
    if re.search(r'[ñáéíóú¿¡]',q): return 'es'
    t=sum(x in TR for x in w); e=sum(x in ES for x in w)
    if t>e and t>0: return 'tr'
    if e>t and e>0: return 'es'
    return 'en'
