#!/usr/bin/env python3
"""Dosyayı envantermedya.com'a (TR) yükler: kapak + satır içi infografikler + post.

Kimlik: EV_AUTH (kullanıcı:uygulama parolası) ya da proxy kimlik enjeksiyonu (EV_AUTH yoksa sahte değer gönderilir).
Kullanım: python3 yayinla.py [--yayinla]   (varsayılan: taslak)
"""
import base64, json, mimetypes, os, sys, urllib.error, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = os.environ.get("ENVANTER_WP_URL", "https://envantermedya.com").rstrip("/") + "/wp-json"
AUTH = "Basic " + base64.b64encode(os.environ.get("EV_AUTH", "x:x").encode()).decode()
YAYINLA = "--yayinla" in sys.argv


def call(method, path, data=None, raw=None, headers=None):
    h = {"Authorization": AUTH, "User-Agent": "envanter-pub"}
    body = None
    if raw is not None:
        body = raw
        h.update(headers or {})
    elif data is not None:
        body = json.dumps(data).encode()
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=body, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path} -> {e.code}: {e.read()[:400].decode(errors='replace')}")


def upload(item):
    f = HERE / item["file"]
    m = call("POST", "/wp/v2/media", raw=f.read_bytes(), headers={
        "Content-Type": mimetypes.guess_type(f.name)[0] or "image/png",
        "Content-Disposition": f'attachment; filename="ss41-{f.name}"'})
    call("POST", f"/wp/v2/media/{m['id']}", {"alt_text": item["alt"], "title": item["alt"], "caption": item.get("caption", "")})
    call("POST", "/ev/v1/set-post-lang", {"post_id": m["id"], "lang": "tr"})
    print(f"  medya {m['id']}: {m['source_url']}")
    return m


def main():
    h = json.loads((HERE / "haber.json").read_text(encoding="utf-8"))
    print("Oturum:", call("GET", "/wp/v2/users/me").get("name"))
    if call("GET", f"/wp/v2/posts?slug={h['slug']}&status=publish,draft,future,pending&context=edit"):
        sys.exit("Bu slug zaten var.")
    content = (HERE / h["content_file"]).read_text(encoding="utf-8")
    for key, it in h["inline"].items():
        content = content.replace("{{%s}}" % key, upload(it)["source_url"])
    assert "{{" not in content
    cover = upload(h["cover"])
    post = call("POST", "/wp/v2/posts", {
        "title": h["title"], "slug": h["slug"], "status": "draft", "content": content,
        "excerpt": h["excerpt"], "categories": h["categories"], "featured_media": cover["id"],
        "meta": {k: h[k] for k in ("rank_math_title", "rank_math_description", "rank_math_focus_keyword")}})
    call("POST", "/ev/v1/set-post-lang", {"post_id": post["id"], "lang": "tr"})
    if YAYINLA:
        post = call("POST", f"/wp/v2/posts/{post['id']}", {"status": "publish"})
        post = call("POST", f"/wp/v2/posts/{post['id']}", {"featured_media": cover["id"], "categories": h["categories"]})
    print(f"Post {post['id']} durum={post['status']} kapak={post['featured_media']} kat={post['categories']}")
    print("Adres:", post["link"])
    (HERE / "yukleme.json").write_text(json.dumps({"post_id": post["id"], "status": post["status"], "link": post["link"], "cover": cover["id"]}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
