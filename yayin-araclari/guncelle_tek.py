#!/usr/bin/env python3
"""Envanter'de tek bir (çevirisiz) yazının içeriğini JSON'daki tr bloğuyla doldurur; başlık/slug korunur. Kullanım: guncelle_tek.py haber.json"""
import json, os, sys, requests
EV = "https://envantermedya.com/wp-json"
d = json.load(open(sys.argv[1])); L = d["langs"]["tr"]
u, p = os.environ["EV_AUTH"].split(":", 1)
r = requests.post(f"{EV}/wp/v2/posts/{d['post_id']}", auth=(u, p), timeout=120, json={
    "content": L["html"], "excerpt": L["excerpt"],
    "meta": {"rank_math_title": L["seo_title"], "rank_math_description": L["meta_description"], "rank_math_focus_keyword": L["focus_keyword"]}})
r.raise_for_status(); j = r.json()
print(j["id"], j["status"], j["slug"], len(j["content"]["rendered"]))
