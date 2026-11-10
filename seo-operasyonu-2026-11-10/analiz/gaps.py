import json,sys,re
sys.path.insert(0,'.')
from inv import load,norm
items=[x for x in load() if x['status'] in ('publish','draft','future')]
d=json.load(open('../work/gsc1110.json'))
STOP=set('the a an of and in to for on with is what how de la el los las del y en para con por que un una ve ile bir bu ne mi icin nedir demek в и на с по для что как من في على ما هو 2026 2027 vs'.split())
idx=[(x,norm(x['title']+' '+x['slug'].replace('-',' ')+' '+x['rmt'])) for x in items]
rows=[]
for q in d['Q']:
    if q['i']<20: continue
    toks=[t for t in re.findall(r'[\w\-\.]+',norm(q['q'])) if t not in STOP and len(t)>1]
    if not toks: continue
    hits=[x for x,h in idx if all(t in h for t in toks)]
    langs={}
    for x in hits: langs[x['lang']]=langs.get(x['lang'],0)+1
    rows.append((q['q'],q['lang'],int(q['i']),int(q['c']),q['pos'],len(hits),langs))
for r in sorted(rows,key=lambda r:(r[5]>0, -r[2])):
    if r[5]<=1: print(f"{r[0][:42]:42} {r[1]:5} i{r[2]:4} c{r[3]:2} p{r[4]:5.1f} hits={r[5]} {r[6]}")
