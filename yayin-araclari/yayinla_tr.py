#!/usr/bin/env python3
"""Tek dilli (TR) haberi zamanlanmış yayınlar. Kimlik: WP_URL, WP_USER, WP_APP_PASSWORD.
Kullanım: yayinla_tr.py haber.json "2026-10-30T09:00" [--dry]  (zaman Envanter yerel saati)"""
import json, os, sys, tempfile
import requests
sys.path.insert(0, os.path.dirname(__file__))
from kapak import make

base = os.environ["WP_URL"].rstrip("/") + "/wp-json"
s = requests.Session()
s.auth = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
s.headers["User-Agent"] = "Mozilla/5.0 (EnvanterYayin)"
d = json.load(open(sys.argv[1]))
when = sys.argv[2]
ex = s.get(f"{base}/wp/v2/posts", params={"slug": d["slug"], "status": "publish,draft,future,pending"}, timeout=60).json()
if ex:
    sys.exit(f"ZATEN VAR: {ex[0]['id']}")
png = tempfile.mkdtemp() + "/kapak.png"
make(png, d["cover"][0], d["cover"][1])
if "--dry" in sys.argv:
    sys.exit(f"dry: {png}")
r = s.post(f"{base}/wp/v2/media", data=open(png, "rb").read(), timeout=120,
           headers={"Content-Disposition": f'attachment; filename="{d["slug"]}-kapak.png"', "Content-Type": "image/png"})
r.raise_for_status()
mid = r.json()["id"]
s.post(f"{base}/wp/v2/media/{mid}", json={"alt_text": d["title"], "title": d["title"]}, timeout=60)
r = s.post(f"{base}/wp/v2/posts", timeout=120, json={
    "title": d["title"], "slug": d["slug"], "content": d["html"], "excerpt": d["excerpt"],
    "status": "future", "date": when, "featured_media": mid, "categories": d["categories"],
    "meta": {"rank_math_title": d["seo_title"], "rank_math_description": d["meta_description"],
             "rank_math_focus_keyword": d["focus_keyword"]}})
r.raise_for_status()
p = r.json()
print(p["id"], p["status"], p["date"], p["link"])
