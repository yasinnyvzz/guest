import json,time,sys,urllib.request
B='https://envantermedya.com/wp-json/wp/v2/'
F='id,date,modified,slug,status,link,title,type'
res=[]
for t in ['pages','savunma_sistemi','savunma_terim','savunma_firma','savunma_terimi','fuar','firma']:
    p=1;n=0
    while True:
        try: d=json.load(urllib.request.urlopen(urllib.request.Request(f'{B}{t}?per_page=100&page={p}&_fields={F}',headers={'User-Agent':'envanter-seo-audit'}),timeout=60))
        except Exception as e: break
        if not d: break
        for x in d: x['type']=t; res.append(x)
        n+=len(d); p+=1
        if len(d)<100: break
        time.sleep(0.2)
    print(t,n,flush=True)
json.dump(res,open(sys.argv[1],'w'),ensure_ascii=False)
