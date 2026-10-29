#!/usr/bin/env python3
"""Defence Arabia'daki mevcut (zamanlanmış) kaydın metnini JSON'daki ar_defencearabia ile günceller. Kullanım: guncelle_da.py haber.json post_id"""
import json, os, sys, requests
DA = "https://www.defencearabia.com/wp-json"
d = json.load(open(sys.argv[1]))["langs"]["ar_defencearabia"]
u, p = os.environ["DA_AUTH"].split(":", 1)
r = requests.post(f"{DA}/wp/v2/posts/{sys.argv[2]}", auth=(u, p), timeout=120, json={
    "title": d["title"], "slug": d["slug"], "content": d["html"], "excerpt": d["excerpt"],
    "meta": {"rank_math_title": d["seo_title"], "rank_math_description": d["meta_description"], "rank_math_focus_keyword": d["focus_keyword"]}})
r.raise_for_status()
print(sys.argv[2], r.json()["status"], r.json()["date"], r.json()["slug"])
