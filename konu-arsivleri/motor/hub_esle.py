#!/usr/bin/env python3
"""Her varlık için her site/dilde mevcut TEKİL arşivi bulur (yeni terim açmaz).

Öncelik: elle belirlenmiş eşleme (sozluk/hub_elle.json) > indekslenen kategori (en çok yazılı) > etiket (en çok yazılı).
Aynı varlığa denk gelen diğer terimler 'kopya' olarak raporlanır (birleştirme adayı, otomatik işlem yok).
Kullanım: hub_esle.py <veri_klasoru> <cikti.json>"""
import json, re, sys, html, os, urllib.parse as up
sys.path.insert(0, os.path.dirname(__file__))
from eslestir import fold

KOK = os.path.join(os.path.dirname(__file__), "..")
SOZ = json.load(open(f"{KOK}/sozluk/varliklar.json", encoding="utf-8"))
ELLE = json.load(open(f"{KOK}/sozluk/hub_elle.json", encoding="utf-8"))
D = sys.argv[1]
DIL = {"ev": (r"https://envantermedya\.com/(en|es|ar|ru|zh)/", "tr"), "dm": (r"https://defencemena\.com/(fr|pt)/", "en"),
       "da": (r"https://defencearabia\.com/(en)/", "ar")}
# terim adı/slug'ındaki dil ve yıl artıkları
SUFFIX = re.compile(r"[\s\-](en|es|ar|ru|zh|fr|pt|tr|\d{1,4})$")
# sitenin indeksleme politikası (canlı HTML'den doğrulandı, 11.11.2026)
TAG_INDEX = {"ev": "noindex (tüm etiketler)", "dm": "index (yazı sayısı eşiğiyle)", "da": "index (yazı sayısı eşiğiyle)"}


def norm(s):
    s = fold(html.unescape(up.unquote(s)))
    s = re.sub(r"[()\[\]–—&;:,.'\"/]", " ", s).replace("-", " ")
    s = re.sub(r"\s+", " ", s).strip()
    for _ in range(2):
        s = SUFFIX.sub("", s).strip()
    return s


def dil(site, link):
    rx, base = DIL[site]
    m = re.match(rx, link)
    return m.group(1) if m else base


def anahtarlar(v):
    ks = {norm(a["t"]) for a in v["alias"] if not a.get("amb")}
    ks |= {norm(x) for x in v["ad"].values()}
    return {k for k in ks if len(k) >= 2}


out = {}
for site in ("ev", "dm", "da"):
    terms = []
    for tax, f in (("category", "categories"), ("post_tag", "tags")):
        seen = set()
        for t in json.load(open(f"{D}/{site}_{f}.json")):
            if t["id"] in seen:
                continue
            seen.add(t["id"])
            terms.append(dict(tax=tax, id=t["id"], name=html.unescape(t["name"]), link=up.unquote(t["link"]),
                              count=t["count"], lang=dil(site, t["link"]), desc=bool(t["description"].strip()),
                              k={norm(t["name"]), norm(t["slug"])}))
    for v in SOZ["varliklar"]:
        ks = anahtarlar(v)
        cands = [t for t in terms if t["k"] & ks]
        for lang in sorted({t["lang"] for t in terms}):
            c = [t for t in cands if t["lang"] == lang]
            key = f"{site}:{lang}:{v['id']}"
            elle = ELLE.get(key)
            if elle == "yok":
                continue
            sec = None
            if elle:
                tax, tid = elle.split(":")
                sec = next((t for t in terms if t["tax"] == tax and t["id"] == int(tid)), None)
            if not sec and c:
                sec = sorted(c, key=lambda t: (t["tax"] != "category", -t["count"]))[0]
            if not sec:
                continue
            kopya = [dict(tax=t["tax"], id=t["id"], name=t["name"], link=t["link"], count=t["count"])
                     for t in c if t is not sec and t["count"] > 0]
            out[key] = dict(site=site, lang=lang, varlik=v["id"], tax=sec["tax"], id=sec["id"], name=sec["name"],
                            link=sec["link"], count=sec["count"], desc=sec["desc"], elle=bool(elle),
                            robots=("index" if sec["tax"] == "category" else TAG_INDEX[site]), kopya=kopya)
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print(len(out), "eşleme")
