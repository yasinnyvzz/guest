import json,collections,math,sys
P=json.load(open('data/inv.json'))
G=json.load(open('data/gsc.json'))
gp={}
for u,c,i,ctr,pos in G['pages']:
    b=u.split('#')[0].rstrip('/'); a=gp.setdefault(b,[0,0,[]]); a[0]+=c;a[1]+=i;a[2].append((i,pos))
def wpos(l): 
    s=sum(i for i,_ in l); return round(sum(i*p for i,p in l)/s,1) if s else None
bylang=collections.defaultdict(list)
for p in P: bylang[p['lang']].append(p)
df={l:collections.Counter(t for p in ps for t in set(p['tok'])) for l,ps in bylang.items()}
GEN=set("2026 2025 military strength inventory how many tanks aircraft ships fighter jets missiles army ranking full".split())
def rare(p):
    l=p['lang'];n=len(bylang[l])
    return set(t for t in p['tok'] if df[l][t]/n<0.01 and t not in GEN)
for p in P: p['r']=rare(p); p['t']=set(p['tok'])
idx=collections.defaultdict(lambda: collections.defaultdict(set))
for p in P:
    for t in p['r']: idx[p['lang']][t].add(p['id'])
byid={p['id']:p for p in P}
byurl={p['url'].rstrip('/'):p for p in P}
pairs=[];seen=set()
for u,(c,i,pl) in gp.items():
    p=byurl.get(u)
    if not p or i<20: continue
    cand=collections.Counter()
    for t in p['r']:
        if len(idx[p['lang']][t])<60:
            for q in idx[p['lang']][t]: cand[q]+=1
    for qid,k in cand.items():
        if qid==p['id'] or k<2: continue
        q=byid[qid]
        jr=len(p['r']&q['r'])/max(1,len(p['r']|q['r'])); ja=len(p['t']&q['t'])/max(1,len(p['t']|q['t']))
        if jr>=0.4 and ja>=0.35:
            key=tuple(sorted((p['id'],q['id'])))
            if key in seen: continue
            seen.add(key); qg=gp.get(q['url'].rstrip('/'),[0,0,[]])
            pairs.append(dict(lang=p['lang'],u1=p['url'],u2=q['url'],id1=p['id'],id2=q['id'],jr=round(jr,2),ja=round(ja,2),c1=c,i1=i,pos1=wpos(pl),c2=qg[0],i2=qg[1],pos2=wpos(qg[2]),t1=p['title'],t2=q['title'],d1=p['date'][:10],d2=q['date'][:10],pll1=p['pll'] is not None,pll2=q['pll'] is not None))
pairs.sort(key=lambda x:-(x['i1']+x['i2']))
json.dump(pairs,open('data/dup_pairs.json','w'),ensure_ascii=False)
print(len(pairs))
for x in pairs[:int(sys.argv[1])]:
    print(f"{x['lang']}|r{x['jr']} a{x['ja']}|{x['i1']:.0f}/{x['c1']:.0f}@{x['pos1']} vs {x['i2']:.0f}/{x['c2']:.0f}@{x['pos2']}|{x['d1']} {x['d2']}|pll {x['pll1']}/{x['pll2']}\n   {x['t1'][:95]}\n   {x['t2'][:95]}\n   {x['u1'][24:]} || {x['u2'][24:]}")
