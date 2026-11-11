#!/usr/bin/env python3
"""DRY-RUN: mevcut bütün yazıları varlık sözlüğüyle eşleştirir ve hangi yazıya hangi arşivin EKLENECEĞİNİ raporlar.
Hiçbir siteye yazmaz. Çıktı: eslestirme_<site>.csv.gz (+ ozet.json).

Durum değerleri:
  zaten_bagli  — yazı bu arşive (ya da aynı varlığın kopya terimine) zaten bağlı
  eklenecek    — yüksek güven, arşiv mevcut → onaydan sonra toplu eklenebilir
  editor_onayi — orta güven → editör kuyruğu
  hub_yok      — bu site/dilde varlığın arşivi yok (Tablo B: yeni arşiv adayı)
  kopya_terime_bagli — yazı aynı varlığın kopya terimine bağlı (birleştirme kararı bekler)
  dil_uyumsuz  — URL dili ile metin dili farklı; eşleştirme yapılmadı (önce dil düzeltilmeli)
Kullanım: kuru_calistir.py <veri_klasoru> <cikti_klasoru>"""
import csv, gzip, json, os, sys, collections
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from eslestir import Motor
from dil_tespit import tespit

KOK = os.path.join(os.path.dirname(__file__), "..")
D, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
HUB = json.load(open(f"{D}/hublar.json"))
M = None


def init():
    global M
    M = Motor(f"{KOK}/sozluk/varliklar.json")


def isle(p):
    td = tespit(p["title"] + " " + p["body"])
    if td and td != p["lang"] and not (p["site"] == "dm" and p["lang"] in ("fr", "pt")):
        return [[p["site"], p["lang"], p["id"], p["date"][:10], p["title"][:160], p["link"], "", "", "", "metin_dili:" + td,
                 0, 0, 0, "dil_uyumsuz"]]
    guclu, _ = M.oner(p["title"], p["excerpt"], p["body"])
    mevcut = {("category", c) for c in p["cats"]} | {("post_tag", t) for t in p["tags"]}
    satirlar = []
    for o in guclu:
        h = HUB.get(f"{p['site']}:{p['lang']}:{o['id']}")
        if not h:
            durum, terim = "hub_yok", ""
        else:
            ids = {(h["tax"], h["id"])} | {(k["tax"], k["id"]) for k in h["kopya"]}
            terim = f"{h['tax']}:{h['id']}"
            if (h["tax"], h["id"]) in mevcut:
                durum = "zaten_bagli"
            elif ids & mevcut:
                durum = "kopya_terime_bagli"
            else:
                durum = "eklenecek" if o["guven"] == "yuksek" else "editor_onayi"
        satirlar.append([p["site"], p["lang"], p["id"], p["date"][:10], p["title"][:160], p["link"], o["id"], terim,
                         o["guven"], o["kaynak"], o["T"], o["L"], o["B"], durum])
    return satirlar


if __name__ == "__main__":
    ozet = {}
    for site in ("ev", "dm", "da"):
        posts = json.load(open(f"{D}/{site}_lite.json"))
        with Pool(os.cpu_count(), initializer=init) as pool:
            res = pool.map(isle, posts, chunksize=50)
        sayac = collections.Counter()
        varlik = collections.Counter()
        yazi_basi = []
        with gzip.open(f"{OUT}/eslestirme_{site}.csv.gz", "wt", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["site", "dil", "yazi_id", "tarih", "baslik", "url", "varlik", "arsiv_terimi", "guven", "kaynak",
                        "baslikta", "giriste", "govdede", "durum"])
            for rows in res:
                yazi_basi.append(len([r for r in rows if r[-1] != "dil_uyumsuz"]))
                for r in rows:
                    w.writerow(r)
                    sayac[r[-1]] += 1
                    varlik[(r[1], r[6], r[-1])] += 1
        ozet[site] = dict(yazi=len(posts), oneri=sum(sayac.values()), durum=dict(sayac),
                          ort_oneri=round(sum(yazi_basi) / max(1, len(yazi_basi)), 2),
                          onerisiz_yazi=sum(1 for n in yazi_basi if n == 0),
                          varlik={f"{a}|{b}|{c}": n for (a, b, c), n in varlik.items()})
        print(site, ozet[site]["yazi"], ozet[site]["durum"], "ort", ozet[site]["ort_oneri"], flush=True)
    json.dump(ozet, open(f"{OUT}/ozet.json", "w"), ensure_ascii=False, indent=1)
