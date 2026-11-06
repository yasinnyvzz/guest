import json,glob,re,requests,html,sys
H={"User-Agent":"Mozilla/5.0"}
BAN=re.compile(r'defenceturk|savunmasanayist|gdh\.|wikipedia',re.I)
for f in sorted(glob.glob('out/drafts/*.json')):
    d=json.load(open(f))
    if d.get('status_decision','').startswith('SKIP'): print('SKIP',f,d.get('status_decision')); continue
    c=d['content_html']; txt=re.sub(r'<[^>]+>',' ',c); wc=len(html.unescape(txt).split())
    links=re.findall(r'href="(https://envantermedya\.com[^"]+)"',c)
    bad=[]
    for u in set(links):
        try:
            r=requests.head(u,headers=H,timeout=30,allow_redirects=True)
            if r.status_code!=200: bad.append((u,r.status_code))
        except Exception as e: bad.append((u,'err'))
    srcban=[s['url'] for s in d.get('sources',[]) if BAN.search(s.get('url',''))]
    inban=BAN.findall(c)
    print(f"{d['lang']} {d['slug'][:45]:45} wc={wc} T={len(d['rank_math_title'])} D={len(d['rank_math_description'])} src={len(d.get('sources',[]))} int={len(set(links))} bad={bad} ban={srcban or inban} h1={'<h1' in c} faq={bool(re.search(r'FAQ|Preguntas|Часто|Sık sorulan|الأسئلة',c))} verify={len(d.get('verification_notes',[]))}")
