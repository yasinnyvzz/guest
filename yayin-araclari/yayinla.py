#!/usr/bin/env python3
"""Haber JSON'unu Envanter Medya (5 dil, Polylang) ve Defence Arabia'ya zamanlanmış yayınlar.
Kimlik bilgileri ortam değişkeninden: EV_AUTH, DA_AUTH ("kullanıcı:uygulama parolası").
Kullanım: yayinla.py haber.json "2026-10-29T18:00" [--dry]   (zaman: Envanter yerel saati; Arabia UTC'ye çevrilir)"""
import json, os, sys, tempfile, datetime as dt
import requests
sys.path.insert(0, os.path.dirname(__file__))
from kapak import make

EV = "https://envantermedya.com/wp-json"
DA = "https://www.defencearabia.com/wp-json"
EV_TZ = 3  # Envanter yerel saat = UTC+3 (ilk yayında doğrulanır)
EV_LANGS = ["tr", "en", "ar", "es", "ru"]
EV_CATS = [53, 24795]
DA_CATS = {"air-defense": [296, 332], "aircraft": [266, 264, 332], "helicopter": [268, 264, 332],
           "missile": [294, 332], "land": [254, 332], "industry": [322, 332], "budget": [348, 350],
           "default": [350, 332]}
BRAND = {"tr": "ENVANTER MEDYA", "en": "ENVANTER MEDYA", "ar": "ENVANTER MEDYA", "es": "ENVANTER MEDYA", "ru": "ENVANTER MEDYA"}


def sess(auth):
    s = requests.Session()
    u, p = auth.split(":", 1)
    s.auth = (u, p)
    s.headers["User-Agent"] = "Mozilla/5.0 (EnvanterYayin)"
    return s


def upload(s, base, png, name, alt):
    r = s.post(f"{base}/wp/v2/media", data=open(png, "rb").read(),
               headers={"Content-Disposition": f'attachment; filename="{name}"', "Content-Type": "image/png"}, timeout=120)
    r.raise_for_status()
    mid = r.json()["id"]
    s.post(f"{base}/wp/v2/media/{mid}", json={"alt_text": alt, "title": alt}, timeout=60).raise_for_status()
    return mid


def body(L):
    return L["html"]


def meta(L):
    return {"rank_math_title": L["seo_title"], "rank_math_description": L["meta_description"],
            "rank_math_focus_keyword": L["focus_keyword"]}


def publish(path, start, dry=False):
    d = json.load(open(path))
    if not d.get("publishable"):
        print("publishable=false, atlandı:", d.get("notes"))
        return
    nid = d["id"]
    t0 = dt.datetime.fromisoformat(start)
    tmp = tempfile.mkdtemp()
    ev, da = sess(os.environ["EV_AUTH"]), sess(os.environ["DA_AUTH"])
    out = {"id": nid}

    # --- Envanter ---
    for lang in EV_LANGS:
        slug = d["langs"][lang]["slug"]
        r = ev.get(f"{EV}/wp/v2/posts", params={"slug": slug, "status": "publish,draft,future,pending", "lang": lang}, timeout=60).json()
        if r:
            print("ZATEN VAR:", lang, slug, r[0]["id"]); return
    media, posts = {}, {}
    for i, lang in enumerate(EV_LANGS):
        L = d["langs"][lang]
        png = f"{tmp}/{nid}-{lang}.png"
        make(png, L["cover"]["line1"], L["cover"]["line2"], "ENVANTER MEDYA", lang == "ar")
        if dry:
            print("kapak", png); continue
        media[lang] = upload(ev, EV, png, f"{L['slug']}-kapak.png", L["title"])
        when = (t0 + dt.timedelta(minutes=5 * i)).strftime("%Y-%m-%dT%H:%M:%S")
        payload = {"title": L["title"], "slug": L["slug"], "content": body(L), "excerpt": L["excerpt"],
                   "status": "draft", "date": when, "featured_media": media[lang], "meta": meta(L)}
        if lang == "tr":
            payload["categories"] = EV_CATS
        r = ev.post(f"{EV}/wp/v2/posts", json=payload, timeout=120)
        r.raise_for_status()
        posts[lang] = r.json()["id"]
        for kind, ident in (("post", posts[lang]), ("media", media[lang])):
            pass
        ev.post(f"{EV}/ev/v1/set-post-lang", json={"post_id": posts[lang], "lang": lang}, timeout=60).raise_for_status()
        ev.post(f"{EV}/ev/v1/set-post-lang", json={"post_id": media[lang], "lang": lang}, timeout=60)
    if dry:
        return
    ev.post(f"{EV}/ev/v1/link-post-translations", json={"groups": [media]}, timeout=60)
    ev.post(f"{EV}/ev/v1/link-post-translations", json={"groups": [posts]}, timeout=60).raise_for_status()
    for i, lang in enumerate(EV_LANGS):
        when = (t0 + dt.timedelta(minutes=5 * i)).strftime("%Y-%m-%dT%H:%M:%S")
        r = ev.post(f"{EV}/wp/v2/posts/{posts[lang]}", json={"status": "future", "date": when, "featured_media": media[lang]}, timeout=120)
        r.raise_for_status()
    ev.post(f"{EV}/wp/v2/posts/{posts['tr']}", json={"categories": EV_CATS}, timeout=120)
    out["envanter"] = posts

    # --- Defence Arabia (Arapça, UTC) ---
    L = d["langs"]["ar_defencearabia"]
    png = f"{tmp}/{nid}-da.png"
    make(png, L["cover"]["line1"], L["cover"]["line2"], "DEFENCE ARABIA", True)
    m = upload(da, DA, png, f"{L['slug']}-cover.png", L["title"])
    when = (t0 + dt.timedelta(minutes=25) - dt.timedelta(hours=EV_TZ)).strftime("%Y-%m-%dT%H:%M:%S")
    cats = DA_CATS.get(d.get("category_hint"), DA_CATS["default"])
    r = da.post(f"{DA}/wp/v2/posts", json={"title": L["title"], "slug": L["slug"], "content": body(L), "excerpt": L["excerpt"],
        "status": "future", "date": when, "date_gmt": when, "featured_media": m, "categories": cats, "meta": meta(L)}, timeout=120)
    r.raise_for_status()
    out["defencearabia"] = r.json()["id"]
    print(json.dumps(out))


if __name__ == "__main__":
    publish(sys.argv[1], sys.argv[2], "--dry" in sys.argv)
