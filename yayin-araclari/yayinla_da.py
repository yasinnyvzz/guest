#!/usr/bin/env python3
"""Yalnız Defence Arabia'ya zamanlanmış yayın. Kullanım: yayinla_da.py haber.json "2026-10-30T04:25" (Arabia UTC)"""
import json, os, sys, tempfile
import requests
sys.path.insert(0, os.path.dirname(__file__))
from kapak import make
from yayinla import DA, DA_CATS, sess, upload, meta
d = json.load(open(sys.argv[1])); L = d["langs"]["ar_defencearabia"]
da = sess(os.environ["DA_AUTH"])
if da.get(f"{DA}/wp/v2/posts", params={"slug": L["slug"], "status": "publish,draft,future"}, timeout=60).json():
    sys.exit("ZATEN VAR")
png = tempfile.mkdtemp() + "/c.png"
make(png, L["cover"]["line1"], L["cover"]["line2"], "DEFENCE ARABIA", True)
m = upload(da, DA, png, f"{L['slug']}-cover.png", L["title"])
r = da.post(f"{DA}/wp/v2/posts", json={"title": L["title"], "slug": L["slug"], "content": L["html"], "excerpt": L["excerpt"],
    "status": "future", "date": sys.argv[2], "date_gmt": sys.argv[2], "featured_media": m,
    "categories": DA_CATS.get(d.get("category_hint"), DA_CATS["default"]), "meta": meta(L)}, timeout=120)
r.raise_for_status(); print(r.json()["id"], r.json()["status"], r.json()["date"])
