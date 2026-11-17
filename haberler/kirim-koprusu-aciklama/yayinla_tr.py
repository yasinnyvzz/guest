import json, sys, urllib.request, os
B="https://envantermedya.com/wp-json"
H={"Authorization":"Basic ZHVtbXk6ZHVtbXk=","User-Agent":"envanter-pub"}
def call(m,p,data=None,raw=None,hd=None):
    h=dict(H); body=None
    if raw is not None: body=raw; h.update(hd)
    elif data is not None: body=json.dumps(data).encode(); h["Content-Type"]="application/json"
    r=urllib.request.Request(B+p,data=body,method=m,headers=h)
    try: return json.load(urllib.request.urlopen(r,timeout=120))
    except urllib.error.HTTPError as e: sys.exit(f"{p} {e.code} {e.read()[:300]}")
h=json.load(open("haber.json",encoding="utf-8"))
ex=call("GET",f"/wp/v2/posts?slug={h['slug']}&status=publish,draft,future,pending&context=edit&_fields=id")
if ex: sys.exit(f"exists {ex}")
m=call("POST","/wp/v2/media",raw=open("kapak.png","rb").read(),hd={"Content-Type":"image/png","Content-Disposition":f'attachment; filename="{h["slug"]}-kapak.png"'})
call("POST",f"/wp/v2/media/{m['id']}",{"alt_text":h["title"],"title":h["title"]})
call("POST","/ev/v1/set-post-lang",{"post_id":m["id"],"lang":"tr"})
p=call("POST","/wp/v2/posts",{"title":h["title"],"slug":h["slug"],"status":"draft","content":open("icerik.html",encoding="utf-8").read(),"excerpt":h["excerpt"],"categories":h["categories"],"featured_media":m["id"],"meta":{k:h[k] for k in ("rank_math_title","rank_math_description","rank_math_focus_keyword")}})
call("POST","/ev/v1/set-post-lang",{"post_id":p["id"],"lang":"tr"})
print(p["id"],m["id"],p["status"],p.get("link"))
