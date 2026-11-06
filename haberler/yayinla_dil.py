#!/usr/bin/env python3
"""Bir haberin EN/AR/ES/RU sürümlerini yükler, TR yazıyla Polylang grubunda bağlar.

Kimlik bilgisi dosyaya yazılmaz: EV_AUTH="kullanıcı:uygulama parolası" ortam değişkeni
(ya da ENVANTER_WP_USER / ENVANTER_WP_APP_PASSWORD).

Kullanım:
  python3 yayinla_dil.py <haber_klasoru> <tr_post_id> <tr_kapak_id> [--taslak]
Örnek (yayınlanmış TR yazılar):
  python3 yayinla_dil.py siper-hipersonik-radar 85040 85039
  python3 yayinla_dil.py sungur-burc-ilk-atis   85043 85042
"""
import base64, json, mimetypes, os, sys, urllib.error, urllib.request
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) != 3:
    sys.exit(__doc__)
ROOT = Path(args[0]).resolve(); TR_POST = int(args[1]); TR_COVER = int(args[2])
TASLAK = "--taslak" in sys.argv
LANGS = ["en", "ar", "es", "ru"]
BASE = os.environ.get("ENVANTER_WP_URL", "https://envantermedya.com").rstrip("/") + "/wp-json"
USER = os.environ.get("ENVANTER_WP_USER"); PWD = os.environ.get("ENVANTER_WP_APP_PASSWORD")
if not (USER and PWD) and os.environ.get("EV_AUTH"):
    USER, PWD = os.environ["EV_AUTH"].split(":", 1)
if not (USER and PWD):
    sys.exit("EV_AUTH veya ENVANTER_WP_USER/ENVANTER_WP_APP_PASSWORD tanımlı değil")
AUTH = "Basic " + base64.b64encode(f"{USER}:{PWD}".encode()).decode()


def call(method, path, data=None, raw=None, headers=None):
    h = {"Authorization": AUTH, "User-Agent": "envanter-pub"}
    body = None
    if raw is not None:
        body = raw; h.update(headers or {})
    elif data is not None:
        body = json.dumps(data).encode(); h["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=body, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path} -> {e.code}: {e.read()[:400].decode(errors='replace')}")


def main():
    print("Oturum:", call("GET", "/wp/v2/users/me").get("name"))
    items = {l: json.loads((ROOT / l / "haber.json").read_text(encoding="utf-8")) for l in LANGS}
    for l, h in items.items():
        if call("GET", f"/wp/v2/posts?slug={h['slug']}&status=publish,draft,future,pending&context=edit"):
            sys.exit(f"[{l}] slug zaten var: {h['slug']}")
    covers, posts = {"tr": TR_COVER}, {"tr": TR_POST}
    for l, h in items.items():
        f = ROOT / l / h["cover"]["file"]
        m = call("POST", "/wp/v2/media", raw=f.read_bytes(), headers={
            "Content-Type": mimetypes.guess_type(f.name)[0] or "image/png",
            "Content-Disposition": f'attachment; filename="{h["slug"]}-kapak.png"'})
        call("POST", f"/wp/v2/media/{m['id']}", {"alt_text": h["title"], "title": h["title"]})
        call("POST", "/ev/v1/set-post-lang", {"post_id": m["id"], "lang": l})
        covers[l] = m["id"]; print(f"  [{l}] kapak {m['id']}")
    call("POST", "/ev/v1/link-post-translations", {"groups": [covers]})
    for l, h in items.items():
        content = (ROOT / l / h["content_file"]).read_text(encoding="utf-8")
        p = call("POST", "/wp/v2/posts", {
            "title": h["title"], "slug": h["slug"], "status": "draft", "content": content,
            "excerpt": h["excerpt"], "categories": h["categories"], "featured_media": covers[l],
            "meta": {k: h[k] for k in ("rank_math_title", "rank_math_description", "rank_math_focus_keyword")}})
        call("POST", "/ev/v1/set-post-lang", {"post_id": p["id"], "lang": l})
        posts[l] = p["id"]; print(f"  [{l}] taslak {p['id']}")
    call("POST", "/ev/v1/link-post-translations", {"groups": [posts]})
    if not TASLAK:
        for l in LANGS:
            call("POST", f"/wp/v2/posts/{posts[l]}", {"status": "publish"})
        call("POST", f"/wp/v2/posts/{TR_POST}", {"categories": items["en"]["categories"]})  # TR'yi bir kez kaydet
    tr = call("GET", f"/ev/v1/post-translations?id={TR_POST}")
    for l, v in tr.items():
        print(f"  {l}: {v['status']}  {v['link']}")


if __name__ == "__main__":
    main()
