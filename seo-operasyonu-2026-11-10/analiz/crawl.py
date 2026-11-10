import json,time,sys,urllib.request,urllib.error,os
OUT=sys.argv[1]
B='https://envantermedya.com/wp-json/wp/v2/'
F='id,date,modified,slug,status,link,title,categories,featured_media,meta.rank_math_title,meta.rank_math_description,meta.rank_math_focus_keyword,meta.rank_math_canonical_url'
def get(url,tries=3):
    for i in range(tries):
        try:
            r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'envanter-seo-audit'}),timeout=60)
            return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code==400: return None   # past last page
            time.sleep(3*(i+1))
        except Exception as e:
            time.sleep(3*(i+1))
    raise SystemExit('fail '+url)
res={}
for typ in ['posts']:
  for st in ['publish','draft','future','pending','private']:
    p=1; n=0
    while True:
        d=get(f'{B}{typ}?per_page=100&page={p}&status={st}&context=edit&_fields={F}&orderby=id&order=desc')
        if not d: break
        for x in d: res[x['id']]=x
        n+=len(d); p+=1
        if len(d)<100: break
        time.sleep(0.25)
    print(typ,st,n,flush=True)
json.dump(list(res.values()),open(OUT,'w'),ensure_ascii=False)
print('total',len(res))
