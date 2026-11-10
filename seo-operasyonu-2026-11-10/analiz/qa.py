import json,re,sys,html,urllib.request,glob
BAD=['defenceturk','defenceturkey','savunmasanayist','gdh.digital','haber.aero','wikipedia.org','savunmasanayidergilik']
def st(u):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,method='HEAD',headers={'User-Agent':'Mozilla/5.0'}),timeout=30); return r.status
    except urllib.error.HTTPError as e: return e.code
    except Exception as e: return str(e)[:30]
for f in sys.argv[1:]:
    d=json.load(open(f)); c=d.get('content_html','')
    txt=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',c)))
    p1=re.search(r'<p>(.*?)</p>',c,re.S); p1w=len(re.sub('<[^>]+>','',p1.group(1)).split()) if p1 else 0
    links=re.findall(r'href="([^"]+)"',c)
    internal=[u for u in links if 'envantermedya.com' in u]
    probs=[]
    if len(d.get('rank_math_title',''))>60: probs.append('rmt>60')
    if not 135<=len(d.get('rank_math_description',''))<=160: probs.append(f"rmd={len(d.get('rank_math_description',''))}")
    if '<table' not in c: probs.append('no table')
    if not re.search(r'<h2[^>]*>[^<]*(FAQ|Preguntas|Часто|Sık sorulan|Frequently)',c,re.I): probs.append('no FAQ h2')
    if '<h1' in c: probs.append('h1 in content')
    for u in links:
        if any(b in u for b in BAD): probs.append('bad source '+u)
    bad_int=[(u,st(u)) for u in internal]; bad_int=[x for x in bad_int if x[1]!=200]
    if bad_int: probs.append(f'internal non-200: {bad_int}')
    print(f"## {f.split('/')[-1]} | {d.get('decision')} {d.get('lang')} | words {len(txt.split())} | p1 {p1w}w | int {len(internal)} | ext {len(links)-len(internal)} | src {len(d.get('sources',[]))} | img {d.get('image',{}).get('type')} | {d.get('title')}")
    print('   RMT:',d.get('rank_math_title'),'| RMD:',d.get('rank_math_description'))
    print('   PROBLEMS:',probs or 'none')
