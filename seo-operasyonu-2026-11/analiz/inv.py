import json,re,html,unicodedata
def pl(u):
    m=re.match(r'https://envantermedya\.com/(en|es|ar|ru|zh)/',u); return m.group(1) if m else 'tr'
def norm(s):
    s=html.unescape(s).lower()
    s=s.replace('ı','i')
    s=''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c))
    return re.findall(r'[\w\-]+',s)
STOP=set("the a an of and in to for on with is what how de la el los las del y en para con por que un una le les des et du ve ile bir bu ne mi icin nedir в и на с по для что как من في على و ما هو هي ال".split())
def toks(s): return set(t for t in norm(s) if t not in STOP and len(t)>1)
def load():
    a=json.load(open('data/posts_all.json'))['all']; d=json.load(open('data/posts.json'))
    assigned={p['id']:l for l in d for p in d[l]}
    out=[]
    for p in a:
        m=p.get('meta') or {}
        t=html.unescape(p['title']['rendered'])
        out.append(dict(id=p['id'],url=p['link'],lang=pl(p['link']),pll=assigned.get(p['id']),date=p['date'],mod=p['modified'],slug=p['slug'],title=t,
            rm_title=m.get('rank_math_title',''),rm_desc=m.get('rank_math_description',''),focus=m.get('rank_math_focus_keyword',''),
            cats=p.get('categories',[]),tok=toks(t+' '+re.sub(r'[-_]',' ',p['slug']))))
    return out
