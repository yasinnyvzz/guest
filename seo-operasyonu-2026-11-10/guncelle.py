#!/usr/bin/env python3
"""Editoryal ONAYDAN SONRA mevcut yayındaki sayfalara SEO revizyonu uygular.

İki mod:
  python3 guncelle.py meta ctr_revizyonlari.json [--yaz] [--id=85083,54957] [--kosul-tamam]
      "meta_kosulu" olan satırlar, koşul yerine getirildiği --kosul-tamam ile belirtilmedikçe atlanır.
      Yalnız Rank Math başlık/açıklamasını değiştirir ("to" değeri parantezle başlıyorsa atlanır).
  python3 guncelle.py icerik taslaklar/<UPDATE dosyası>.json [--yaz]
      decision=UPDATE olan tam metin revizyonunu update_post_id'ye yazar (slug ve URL korunur).
Varsayılan kuru çalıştırmadır. Yazmadan önce mevcut değerler yedek klasörüne kaydedilir (geri alınabilir).
"""
import json, os, sys, time
from pathlib import Path
import requests

EV = "https://envantermedya.com/wp-json"
HERE = Path(__file__).resolve().parent
BACKUP = HERE / "yedek"


def sess():
    s = requests.Session(); s.headers["User-Agent"] = "envanter-seo-pilot"
    if os.environ.get("EV_AUTH"):
        s.auth = tuple(os.environ["EV_AUTH"].split(":", 1))
    return s


def backup(s, typ, pid):
    BACKUP.mkdir(exist_ok=True)
    cur = s.get(f"{EV}/wp/v2/{typ}/{pid}", params={"context": "edit"}, timeout=60).json()
    (BACKUP / f"{typ}-{pid}-{int(time.time())}.json").write_text(json.dumps(cur, ensure_ascii=False))
    return cur


def meta(path, write, only):
    s = sess()
    for x in json.load(open(path)):
        if only and str(x["post_id"]) not in only:
            continue
        t, d = x["rank_math_title"]["to"], x["rank_math_description"]["to"]
        if t.startswith("(") or d.startswith("("):
            print("ATLA (yalnız birleştirme/inceleme):", x["post_id"]); continue
        if x.get("meta_kosulu") and "--kosul-tamam" not in sys.argv:
            print("ATLA (koşul):", x["post_id"], "-", x["meta_kosulu"]); continue
        assert len(t) <= 60 and 120 <= len(d) <= 160, (x["post_id"], len(t), len(d))
        print(("YAZ" if write else "[kuru]"), x["post_id"], "|", t)
        if write:
            backup(s, x["type"], x["post_id"])
            r = s.post(f"{EV}/wp/v2/{x['type']}/{x['post_id']}", json={"meta": {"rank_math_title": t, "rank_math_description": d}}, timeout=60)
            r.raise_for_status()
            time.sleep(1)


def icerik(path, write):
    d = json.load(open(path)); assert d["decision"].startswith("UPDATE") and d.get("update_post_id")
    s = sess(); pid = d["update_post_id"]
    print(("YAZ" if write else "[kuru]"), pid, d["title"], len(d["content_html"]), "krk")
    if write:
        cur = backup(s, "posts", pid)
        payload = {"title": d["title"], "content": d["content_html"], "excerpt": d["excerpt"],
                   "meta": {"rank_math_title": d["rank_math_title"], "rank_math_description": d["rank_math_description"],
                            "rank_math_focus_keyword": d["rank_math_focus_keyword"]}}
        r = s.post(f"{EV}/wp/v2/posts/{pid}", json=payload, timeout=120); r.raise_for_status()
        assert r.json()["slug"] == cur["slug"], "slug değişti!"


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    only = next((x[5:].split(",") for x in sys.argv if x.startswith("--id=")), None)
    if len(a) != 2:
        sys.exit(__doc__)
    (meta if a[0] == "meta" else icerik)(*( [a[1], "--yaz" in sys.argv, only] if a[0] == "meta" else [a[1], "--yaz" in sys.argv]))
