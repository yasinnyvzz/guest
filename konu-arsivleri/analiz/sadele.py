#!/usr/bin/env python3
"""Ham REST yazılarını eşleştirme için sade metne çevirir: id, site, dil, tarih, başlık, özet, gövde metni, terimler."""
import json, re, html, sys
D = sys.argv[1]
PFX = {"ev": r"https://envantermedya\.com/(en|es|ar|ru|zh)/", "dm": r"https://defencemena\.com/(fr|pt)/",
       "da": r"https://defencearabia\.com/(en)/"}
BASE = {"ev": "tr", "dm": "en", "da": "ar"}


def txt(h):
    h = re.sub(r"<(script|style|figure|figcaption)[^>]*>.*?</\1>", " ", h or "", flags=re.S | re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(h)).strip()


for k in ("ev", "dm", "da"):
    out = []
    for p in json.load(open(f"{D}/{k}_posts.json")):
        m = re.match(PFX[k], p["link"])
        out.append(dict(id=p["id"], site=k, lang=m.group(1) if m else BASE[k], date=p["date"], link=p["link"],
                        title=txt(p["title"]["rendered"]), excerpt=txt(p["excerpt"]["rendered"]),
                        body=txt(p["content"]["rendered"]), cats=p.get("categories", []), tags=p.get("tags", []),
                        author=p.get("author")))
    json.dump(out, open(f"{D}/{k}_lite.json", "w"), ensure_ascii=False)
    print(k, len(out))
