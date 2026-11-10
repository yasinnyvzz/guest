import json,re,html,unicodedata,sys,os
W=os.path.join(os.path.dirname(__file__),'..','work')
def lang_of(p):
    m=re.match(r'https://envantermedya\.com/(en|es|ar|ru|zh)/',p.get('link',''))
    if m: return m.group(1)
    s=p.get('slug','')
    m=re.match(r'(en|es|ar|ru|zh)-',s)
    if m: return m.group(1)
    m=re.search(r'-(en|es|ar|ru|zh)$',s)
    if m: return m.group(1)
    return 'tr'
def norm(s):
    s=html.unescape(s or '').lower().replace('ı','i')
    s=''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c))
    return s
def load():
    P=json.load(open(os.path.join(W,'posts_all.json')))
    C=json.load(open(os.path.join(W,'cpt_all.json')))
    out=[]
    for p in P:
        t=p['title']['raw'] if isinstance(p['title'],dict) and 'raw' in p['title'] else p['title'].get('rendered','')
        m=p.get('meta') or {}
        out.append(dict(id=p['id'],type='post',status=p['status'],date=p['date'],mod=p['modified'],slug=p['slug'],link=p['link'],title=html.unescape(t),lang=lang_of(p),
            rmt=m.get('rank_math_title',''),rmd=m.get('rank_math_description',''),fk=m.get('rank_math_focus_keyword','')))
    for p in C:
        out.append(dict(id=p['id'],type=p['type'],status=p['status'],date=p['date'],mod=p['modified'],slug=p['slug'],link=p['link'],title=html.unescape(p['title']['rendered']),lang=lang_of(p),rmt='',rmd='',fk=''))
    return out
def search(items,terms,lang=None,status=None):
    terms=[norm(t) for t in terms]
    r=[]
    for x in items:
        if lang and x['lang']!=lang: continue
        if status and x['status'] not in status: continue
        hay=norm(x['title']+' '+x['slug'].replace('-',' ')+' '+x['rmt']+' '+x['fk'])
        if all(t in hay for t in terms): r.append(x)
    return r
if __name__=='__main__':
    items=load()
    lang=None; args=sys.argv[1:]
    if args and args[0].startswith('lang='): lang=args[0][5:]; args=args[1:]
    for x in sorted(search(items,args,lang),key=lambda x:x['date'],reverse=True)[:60]:
        print(f"{x['id']:6} {x['status'][:4]} {x['lang']} {x['date'][:10]} {x['type'][:6]:6} {x['title'][:85]} | {x['link'][24:90]}")
