#!/usr/bin/env python3
"""Tek dilli (EN) taslak yükleme; kimlik gerekmez (proxy yetkili)."""
import json, urllib.request, urllib.error
from pathlib import Path
BASE="https://envantermedya.com/wp-json"; R=Path(__file__).parent/"en"
def call(m,p,data=None,raw=None,h=None):
    hd={"User-Agent":"envanter-pub"}; body=None
    if raw is not None: body=raw; hd.update(h or {})
    elif data is not None: body=json.dumps(data).encode(); hd["Content-Type"]="application/json"
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE+p,data=body,method=m,headers=hd),timeout=120) as r: return json.load(r)
    except urllib.error.HTTPError as e: raise SystemExit(f"{m} {p} -> {e.code} {e.read()[:300]}")
j=json.loads((R/"haber.json").read_text())
ex=call("GET",f"/wp/v2/posts?slug={j['slug']}&status=publish,draft,future,pending&context=edit&_fields=id,status")
if ex: raise SystemExit(f"zaten var: {ex}")
print(call("GET","/wp/v2/users/me?_fields=name"))
m=call("POST","/wp/v2/media",raw=(R/"kapak.png").read_bytes(),h={"Content-Type":"image/png","Content-Disposition":f'attachment; filename="{j["slug"]}-kapak.png"'})
alt="Envanter Medya title card: the most expensive missile in the world"
call("POST",f"/wp/v2/media/{m['id']}",{"alt_text":alt,"title":j["title"]})
call("POST","/ev/v1/set-post-lang",{"post_id":m["id"],"lang":"en"})
p=call("POST","/wp/v2/posts",{"title":j["title"],"slug":j["slug"],"status":"draft","content":(R/j["content_file"]).read_text(),
 "excerpt":j["excerpt"],"categories":j["categories"],"featured_media":m["id"],
 "meta":{k:j[k] for k in ("rank_math_title","rank_math_description","rank_math_focus_keyword")}})
call("POST","/ev/v1/set-post-lang",{"post_id":p["id"],"lang":"en"})
print("media",m["id"],"post",p["id"],p["status"],p.get("link"))
