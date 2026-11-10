#!/usr/bin/env python3
"""Editoryal ONAYDAN SONRA taslakları WordPress'te zamanlar (status=future). Kuyruk WordPress'te kalıcıdır;
tarayıcı/bilgisayar kapansa da WP-Cron yayımlar.

Kullanım:
  python3 zamanla.py takvim.json            # kuru çalıştırma: kontrolleri yapar, hiçbir şey yazmaz
  python3 zamanla.py takvim.json --yaz      # onaylı satırları zamanlar

takvim.json: [{"post_id": 123, "slot": "2026-11-10T16:30", "onay": true}, ...]   (saat: site saati, Europe/Istanbul)
Kurallar:
- Yalnız "onay": true satırlar işlenir; yazı 'draft' değilse dokunulmaz (iki kez zamanlama yok).
- Ardışık slotlar arasında 10–20 dakika olmalı; geçmiş saat reddedilir.
- Aynı dakikada sitenin kendi zamanlanmış kuyruğunda yazı varsa uyarır (çakışma).
- Hata olursa durur; kontrolsüz tekrar yok.
"""
import json, os, sys
from datetime import datetime, timedelta
import requests

EV = "https://envantermedya.com/wp-json"


def main(path, write):
    rows = json.load(open(path))
    s = requests.Session(); s.headers["User-Agent"] = "envanter-seo-pilot"
    if os.environ.get("EV_AUTH"):
        s.auth = tuple(os.environ["EV_AUTH"].split(":", 1))
    rows = [r for r in rows if r.get("onay") is True and r.get("tur") != "update"]  # UPDATE'ler guncelle.py ile
    rows.sort(key=lambda r: r["slot"])
    now = datetime.now()
    prev = None
    for r in rows:
        t = datetime.fromisoformat(r["slot"])
        if prev and not timedelta(minutes=10) <= t - prev <= timedelta(minutes=20):
            sys.exit(f"Aralık 10–20 dk değil: {prev} → {t}")
        prev = t
    future = s.get(f"{EV}/wp/v2/posts", params={"status": "future", "per_page": 100, "context": "edit",
                                                 "orderby": "date", "order": "asc", "_fields": "id,date"}, timeout=60).json()
    busy = {f["date"][:16] for f in future}
    for r in rows:
        p = s.get(f"{EV}/wp/v2/posts/{r['post_id']}", params={"context": "edit", "_fields": "id,status,title,meta"}, timeout=60).json()
        if p.get("status") != "draft":
            print("ATLA (draft değil):", r["post_id"], p.get("status")); continue
        if not p["meta"].get("rank_math_title") or not p["meta"].get("rank_math_description"):
            sys.exit(f"SEO alanları eksik: {r['post_id']}")
        if r["slot"][:16] in busy:
            print("UYARI: aynı dakikada sitede başka zamanlanmış yazı var:", r["slot"])
        print(("ZAMANLA" if write else "[kuru]"), r["post_id"], r["slot"], p["title"]["raw"][:70])
        if write:
            u = s.post(f"{EV}/wp/v2/posts/{r['post_id']}", json={"status": "future", "date": r["slot"] + ":00"}, timeout=60)
            u.raise_for_status()
            assert u.json()["status"] == "future", u.json()["status"]


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a:
        sys.exit(__doc__)
    main(a[0], "--yaz" in sys.argv)
