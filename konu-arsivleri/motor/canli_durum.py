#!/usr/bin/env python3
"""Salt okuma: ilk 40 arşivin canlı <title>, meta açıklama, robots, canonical, H1 ve sayfa sayısını çeker."""
import json, re, sys, html, requests, concurrent.futures as cf
D = sys.argv[1]
H = json.load(open(f"{D}/hublar.json"))
keys = json.load(open(sys.argv[2]))
def one(k):
    h = H.get(k)
    if not h:
        return k, None
    r = requests.get(h["link"], headers={"User-Agent": "Mozilla/5.0 (EnvanterArsivDenetimi)"}, timeout=60)
    t = r.text
    g = lambda rx: (lambda m: html.unescape(m.group(1)).strip() if m else "")(re.search(rx, t, re.S | re.I))
    return k, dict(url=h["link"], tax=h["tax"], id=h["id"], count=h["count"], kopya=len(h["kopya"]), http=r.status_code,
                   title=g(r"<title>(.*?)</title>"), desc=g(r'<meta name="description" content="([^"]*)"'),
                   robots=g(r'<meta name="robots" content="([^"]*)"'), canonical=g(r'<link rel="canonical" href="([^"]*)"'),
                   h1=re.sub(r"<[^>]+>", "", g(r"<h1[^>]*>(.*?)</h1>")).strip(),
                   hreflang=len(re.findall(r'hreflang="', t)), pages=g(r"Sayfa \d+ / (\d+)|page \d+ of (\d+)"))
with cf.ThreadPoolExecutor(8) as ex:
    out = dict(ex.map(one, keys))
json.dump(out, open(f"{D}/canli40.json", "w"), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(k, "|", v and v["count"], "|", v and v["robots"], "|", v and v["title"][:70], "|", v and v["h1"][:40], "|", v and len(v["desc"]))
