import openpyxl,re,json,sys,warnings,collections
warnings.filterwarnings('ignore')
wb=openpyxl.load_workbook(sys.argv[1],read_only=True)
S={ws.title:list(ws.iter_rows(values_only=True))[1:] for ws in wb.worksheets}
def qlang(q):
    if re.search(r'[؀-ۿ]',q): return 'ar'
    if re.search(r'[Ѐ-ӿ]',q): return 'ru'
    if re.search(r'[一-鿿]',q): return 'zh'
    if re.search(r'[çğıöşü]',q): return 'tr'
    if re.search(r'[ñáéíóú¿]',q): return 'es'
    w=set(q.split())
    if w & {'nedir','ne','nasıl','nasil','kaç','kac','maaşı','maasi','alımı','alimi','ve','ile','hangi','en','iyi','türk','turk','yerli','milli','ozellikleri','özellikleri','fiyatı','fiyati','ucak','uçak','tank','nerede','kimdir','ordusu','gucu'} - {'en'}: return 'tr'
    if w & {'de','del','la','el','los','las','que','qué','cuantos','cuántos','ejercito','ejército','armada','fuerza','egipto','misil','submarino','fuerzas','armadas','avion','buque','cuanto'}: return 'es'
    if w & {'do','da','dos','exército','exercito','marinha','força','forca'}: return 'pt'
    return 'en/?'
def plang(u):
    m=re.match(r'https://envantermedya\.com/(en|es|ar|ru|zh|pt|fr|de)/',u); return m.group(1) if m else 'tr'
Q=[dict(q=r[0],c=r[1],i=r[2],ctr=r[3],pos=r[4],lang=qlang(r[0])) for r in S['Sorgular']]
P=[dict(u=r[0],c=r[1],i=r[2],ctr=r[3],pos=r[4],lang=plang(r[0])) for r in S['Sayfa sayısı']]
json.dump(dict(Q=Q,P=P,C=S['Ülkeler'],D=S['Cihazlar'],G=S['Grafik'],A=S['Arama görünümü'],F=S['Filtreler']),open(sys.argv[2],'w'),ensure_ascii=False,default=str)
tc=sum(r[1] for r in S['Grafik']); ti=sum(r[2] for r in S['Grafik'])
print('Grafik toplam',tc,ti,round(tc/ti*100,2),'saat',len(S['Grafik']),S['Grafik'][0][0],S['Grafik'][-1][0])
print('Cihaz',S['Cihazlar']); print('Görünüm',S['Arama görünümü']); print('Filtre',S['Filtreler'])
qc=sum(x['c'] for x in Q); qi=sum(x['i'] for x in Q); print('Sorgular sekmesi',len(Q),qc,qi, f'{qi/ti:.0%} of impressions')
pc=sum(x['c'] for x in P); pi=sum(x['i'] for x in P); print('Sayfalar sekmesi',len(P),pc,pi)
for name,arr in [('SORGU DİLİ',Q),('SAYFA DİLİ',P)]:
    a=collections.defaultdict(lambda:[0,0,0,0.0])
    for x in arr: s=a[x['lang']]; s[0]+=1;s[1]+=x['c'];s[2]+=x['i'];s[3]+=x['pos']*x['i']
    print(name); [print(' ',k,v[0],int(v[1]),int(v[2]),f"ctr {v[1]/v[2]*100:.2f}%",f"pos {v[3]/v[2]:.1f}") for k,v in sorted(a.items(),key=lambda kv:-kv[1][2])]
print('Hourly:'); [print(' ',r[0][5:16],int(r[1]),int(r[2]),r[4]) for r in S['Grafik']]
print('Ülkeler top25'); [print(' ',r[0],int(r[1]),int(r[2]),round(r[3]*100,2),r[4]) for r in S['Ülkeler'][:25]]
