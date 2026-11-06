import json,collections,sys,re
sys.path.insert(0,'scripts')
from qlang import qlang
from inv import toks
P=json.load(open('data/inv.json'))
for p in P: p['t']=set(p['tok'])
G=json.load(open('data/gsc.json'))
bylang=collections.defaultdict(list)
for p in P: bylang[p['lang']].append(p)
df={l:collections.Counter(t for p in ps for t in p['t']) for l,ps in bylang.items()}
def best(q,l,k=3):
    qt=toks(q)
    if not qt: return []
    n=len(bylang[l]); sc=[]
    for p in bylang[l]:
        common=qt&p['t']
        if not common: continue
        s=sum(1/(1+df[l][t]/n*50) for t in common)/sum(1/(1+df[l].get(t,0)/n*50) for t in qt)
        sc.append((round(s,2),p))
    sc.sort(key=lambda x:(-x[0],-len(x[1]['date'])))
    return [(s,p['url'][24:],p['date'][:10]) for s,p in sc[:k]]
out=[]
for q,c,i,ctr,pos in G['queries']:
    l=qlang(q)
    m=best(q,l)
    out.append(dict(q=q,lang=l,clicks=c,impr=i,ctr=ctr,pos=pos,match=m))
json.dump(out,open('data/qmatch.json','w'),ensure_ascii=False)
for o in sorted(out,key=lambda o:-o['impr']):
    if o['impr']<int(sys.argv[1]): continue
    m=o['match'][0] if o['match'] else (0,'-','')
    flag='GAP?' if m[0]<0.75 else ''
    print(f"{o['lang']}|{o['q'][:60]}|{o['clicks']:.0f}/{o['impr']:.0f}@{o['pos']}|{m[0]}|{m[1][:85]}|{flag}")
