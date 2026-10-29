#!/usr/bin/env python3
"""Envanter'de mevcut bir haberi (5 dil) JSON içeriğiyle günceller; slug/URL/başlık korunur. Kullanım: guncelle_ev.py haber.json tr_post_id"""
import json, os, sys, requests
EV = "https://envantermedya.com/wp-json"
d = json.load(open(sys.argv[1]))["langs"]
u, p = os.environ["EV_AUTH"].split(":", 1)
s = requests.Session(); s.auth = (u, p)
tr = s.get(f"{EV}/ev/v1/post-translations", params={"id": sys.argv[2]}, timeout=60).json()
for lang, v in tr.items():
    L = d[lang]
    r = s.post(f"{EV}/wp/v2/posts/{v['id']}", timeout=120, json={"content": L["html"], "excerpt": L["excerpt"],
        "meta": {"rank_math_title": L["seo_title"], "rank_math_description": L["meta_description"], "rank_math_focus_keyword": L["focus_keyword"]}})
    r.raise_for_status(); print(lang, v["id"], r.json()["status"], r.json()["slug"])
