import json,re,collections,sys
sys.path.insert(0,'scripts')
from qlang import qlang
G=json.load(open('data/gsc.json')); P=json.load(open('data/inv.json'))
byurl={p['url'].rstrip('/'):p for p in P}
def pl(u):
    m=re.match(r'https://envantermedya\.com/(en|es|ar|ru|zh)/',u); return m.group(1) if m else 'tr'
base={}
for u,c,i,ctr,pos in G['pages']:
    b=u.split('#')[0].rstrip('/')
    a=base.setdefault(b,dict(url=b+'/',clicks=0,impr=0,posw=0,rows=0)); a['clicks']+=c;a['impr']+=i;a['posw']+=pos*i;a['rows']+=1
for a in base.values():
    a['pos']=round(a['posw']/a['impr'],2) if a['impr'] else None; a['ctr']=a['clicks']/a['impr'] if a['impr'] else 0
    a['lang']=pl(a['url']); p=byurl.get(a['url'].rstrip('/'),{})
    a.update(id=p.get('id'),type=p.get('type'),title=p.get('title'),date=(p.get('date') or '')[:10],pll=p.get('pll') is not None if p else None,rm_desc=bool(p.get('rm_desc')),rm_title=p.get('rm_title',''))
# Table 1
T1={}
for l in ['tr','en','es','ar','ru','zh']:
    rs=[a for a in base.values() if a['lang']==l]
    c=sum(a['clicks'] for a in rs); i=sum(a['impr'] for a in rs)
    T1[l]=dict(pages=len(rs),clicks=c,impr=i,ctr=round(c/i*100,2) if i else 0,pos=round(sum(a['posw'] for a in rs)/i,1) if i else None,
       top=[(a['title'] or a['url'][24:],a['clicks'],a['impr']) for a in sorted(rs,key=lambda a:(-a['clicks'],-a['impr']))[:5]])
# query-language view
QL=collections.defaultdict(lambda:[0,0,0,0])
for q,c,i,ctr,pos in G['queries']:
    x=QL[qlang(q)]; x[0]+=1;x[1]+=c;x[2]+=i;x[3]+=pos*i
T1q={l:dict(queries=v[0],clicks=v[1],impr=v[2],ctr=round(v[1]/v[2]*100,2),pos=round(v[3]/v[2],1)) for l,v in QL.items()}
# country groups
HISP={'İspanya','Meksika','Arjantin','Kolombiya','Şili','Peru','Venezuela','Ekvador','Bolivya','Uruguay','Paraguay','Guatemala','Kosta Rika','Panama','Dominik Cumhuriyeti','Honduras','El Salvador','Nikaragua','Küba','Porto Riko'}
ARAB={'Suudi Arabistan','Mısır','Fas','Cezayir','Irak','Ürdün','Tunus','Birleşik Arap Emirlikleri','Kuveyt','Katar','Umman','Bahreyn','Libya','Sudan','Lübnan','Suriye','Yemen','Filistin','Moritanya'}
RUS={'Rusya','Belarus','Kazakistan','Kırgızistan','Özbekistan','Ukrayna','Azerbaycan','Ermenistan','Gürcistan','Tacikistan','Moldova'}
cg=collections.defaultdict(lambda:[0,0])
for n,c,i,ctr,pos in G['countries']:
    g='Türkiye' if n=='Türkiye' else 'İspanyolca konuşulan' if n in HISP else 'Arap ülkeleri' if n in ARAB else 'BDT/Rusça' if n in RUS else 'Çin/Tayvan/HK' if n in {'Çin','Tayvan','Hong Kong','Singapur'} else 'Diğer'
    cg[g][0]+=c; cg[g][1]+=i
hisp=[(n,c,i,round(pos,1)) for n,c,i,ctr,pos in G['countries'] if n in HISP]
# opportunity score
bench={1:.30,2:.16,3:.10,4:.07,5:.055,6:.045,7:.035,8:.028,9:.023,10:.02}
def b(p): return bench.get(max(1,min(10,round(p))),0.015)
site_ctr=sum(a['clicks'] for a in base.values())/sum(a['impr'] for a in base.values())
cal=site_ctr/ b(6.4)
for a in base.values():
    if not a['impr'] or a['pos'] is None: a['score']=0; continue
    tgt=max(1,a['pos']-3) if a['pos']>3 else a['pos']
    a['pot_clicks']=round(a['impr']*b(tgt)*cal,1)
    a['score']=round(max(0,a['pot_clicks']-a['clicks']),1)
top=sorted([a for a in base.values() if a['type'] not in (None,'pages') and a['url']!='https://envantermedya.com/'],key=lambda a:-a['score'])[:100]
json.dump(dict(T1=T1,T1q=T1q,countries=dict(cg),hisp=hisp,top100=top,cal=cal),open('data/report_data.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(T1,ensure_ascii=False,indent=0)[:3000]); print(T1q); print(dict(cg)); print(hisp)
for a in top[:30]: print(a['lang'],a['score'],a['impr'],a['clicks'],a['pos'],a['url'][24:90])
