#!/usr/bin/env python3
"""Bir haber klasörünü üç siteye yavaşça ve kaldığı yerden devam edecek şekilde yükler.

Klasör düzeni: <klasör>/haber.json + icerik.html + kapak.png (TR), alt klasörler en/ ar/ es/ ru/
(Envanter), defencearabia/ (AR), defencemena/ (EN). Olmayan alt klasör atlanır.

Kimlik: oturum vekili ekliyorsa gerekmez; yoksa EV_AUTH / DA_AUTH / MENA_AUTH ("kullanıcı:uygulama parolası").

Kullanım:
  python3 yayinla_toplu.py <klasör> [--site=ev,da,mena] [--taslak] [--mena-kat=1,2] [--bekle=8]
Yeniden çalıştırmak güvenlidir: var olan taslak yeniden kullanılır, yayındaki slug atlanır.
"""
import base64, json, os, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--")]
opt = dict(a[2:].split("=", 1) if "=" in a else (a[2:], "1") for a in sys.argv[1:] if a.startswith("--"))
if not args:
    sys.exit(__doc__)
ROOT = Path(args[0]).resolve()
SITES = opt.get("site", "ev,da,mena").split(",")
TASLAK = "taslak" in opt
BEKLE = float(opt.get("bekle", 8))
BASE = {"ev": "https://envantermedya.com/wp-json", "da": "https://www.defencearabia.com/wp-json", "mena": "https://defencemena.com/wp-json"}
ENV = {"ev": "EV_AUTH", "da": "DA_AUTH", "mena": "MENA_AUTH"}
EV_LANGS = ["tr", "en", "ar", "es", "ru"]


def call(site, method, path, data=None, raw=None, headers=None):
    h = {"User-Agent": "Mozilla/5.0 (envanter-pub)"}
    if os.environ.get(ENV[site]):
        h["Authorization"] = "Basic " + base64.b64encode(os.environ[ENV[site]].encode()).decode()
    body = None
    if raw is not None:
        body = raw; h.update(headers or {})
    elif data is not None:
        body = json.dumps(data).encode(); h["Content-Type"] = "application/json"
    for deneme in range(4):
        req = urllib.request.Request(BASE[site] + path, data=body, method=method, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                out = json.load(r)
            time.sleep(BEKLE if method != "GET" else 1)
            return out
        except urllib.error.HTTPError as e:
            msg = f"{site} {method} {path} -> {e.code}: {e.read()[:300].decode(errors='replace')}"
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            msg = f"{site} {method} {path} -> ağ hatası: {e}"
        # Yalnız GET yeniden denenir; yazma isteği yarım kalmış olabilir, betik yeniden çalıştırılır.
        if method == "GET" and deneme < 3:
            time.sleep(10 * (deneme + 1)); continue
        raise RuntimeError(msg)


def load(sub):
    d = ROOT / sub if sub else ROOT
    if not (d / "haber.json").exists():
        return None
    h = json.loads((d / "haber.json").read_text(encoding="utf-8"))
    h["_html"] = (d / h["content_file"]).read_text(encoding="utf-8")
    h["_cover"] = d / h["cover"]["file"]
    return h


def find(site, slug):
    q = urllib.parse.urlencode({"slug": slug, "status": "publish,draft,future,pending", "context": "edit",
                                "_fields": "id,status,featured_media,link"})
    r = call(site, "GET", f"/wp/v2/posts?{q}")
    return r[0] if r else None


def cover(site, h):
    m = call(site, "POST", "/wp/v2/media", raw=h["_cover"].read_bytes(), headers={
        "Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{h["slug"]}-kapak.png"'})
    call(site, "POST", f"/wp/v2/media/{m['id']}", {"alt_text": h["title"], "title": h["title"]})
    return m["id"]


def payload(h, cats, cov):
    p = {"title": h["title"], "slug": h["slug"], "status": "draft", "content": h["_html"], "excerpt": h["excerpt"],
         "featured_media": cov, "meta": {k: h[k] for k in ("rank_math_title", "rank_math_description", "rank_math_focus_keyword")}}
    if cats:
        p["categories"] = cats
    return p


def envanter():
    items = {l: load("" if l == "tr" else l) for l in EV_LANGS}
    items = {l: h for l, h in items.items() if h}
    posts, covers, yeni = {}, {}, []
    for l, h in items.items():
        var = find("ev", h["slug"])
        if var and var["status"] != "draft":
            print(f"  ev[{l}] zaten {var['status']}: {var['link']}"); posts[l] = var["id"]; covers[l] = var["featured_media"]; continue
        if var and var.get("featured_media"):
            covers[l] = var["featured_media"]
        else:
            covers[l] = cover("ev", h)
            call("ev", "POST", "/ev/v1/set-post-lang", {"post_id": covers[l], "lang": l})
        if var:
            posts[l] = var["id"]
            call("ev", "POST", f"/wp/v2/posts/{var['id']}", {"featured_media": covers[l]})
        else:
            posts[l] = call("ev", "POST", "/wp/v2/posts", payload(h, h["categories"], covers[l]))["id"]
        call("ev", "POST", "/ev/v1/set-post-lang", {"post_id": posts[l], "lang": l})
        yeni.append(l); print(f"  ev[{l}] taslak {posts[l]} kapak {covers[l]}")
    if not yeni:
        return
    if len(posts) > 1:
        call("ev", "POST", "/ev/v1/link-post-translations", {"groups": [covers]})
        call("ev", "POST", "/ev/v1/link-post-translations", {"groups": [posts]})
    if TASLAK:
        return
    for l in yeni:
        call("ev", "POST", f"/wp/v2/posts/{posts[l]}", {"status": "publish"})
    call("ev", "POST", f"/wp/v2/posts/{posts['tr']}", {"categories": items["tr"]["categories"], "featured_media": covers["tr"]})
    for l in items:  # Polylang eşitlemesi kapağı ezdiyse düzelt
        p = call("ev", "GET", f"/wp/v2/posts/{posts[l]}?context=edit&_fields=id,status,link,featured_media")
        if p["featured_media"] != covers[l]:
            call("ev", "POST", f"/wp/v2/posts/{posts[l]}", {"featured_media": covers[l]})
            print(f"  ev[{l}] kapak düzeltildi")
        print(f"  ev[{l}] {p['status']} {p['link']}")


def tek(site, sub, cats):
    h = load(sub)
    if not h:
        return
    var = find(site, h["slug"])
    if var and var["status"] != "draft":
        print(f"  {site} zaten {var['status']}: {var['link']}"); return
    cov = var["featured_media"] if var and var.get("featured_media") else cover(site, h)
    pid = var["id"] if var else call(site, "POST", "/wp/v2/posts", payload(h, cats or h.get("categories"), cov))["id"]
    if not TASLAK:
        call(site, "POST", f"/wp/v2/posts/{pid}", {"status": "publish", "featured_media": cov})
    p = call(site, "GET", f"/wp/v2/posts/{pid}?context=edit&_fields=id,status,link")
    print(f"  {site} {p['status']} {p['link']}")


if __name__ == "__main__":
    print(ROOT.name)
    try:
        if "ev" in SITES: envanter()
        if "da" in SITES: tek("da", "defencearabia", None)
        if "mena" in SITES: tek("mena", "defencemena", [int(x) for x in opt["mena-kat"].split(",")] if opt.get("mena-kat") else None)
    except RuntimeError as e:
        sys.exit(f"DURDU: {e}")
