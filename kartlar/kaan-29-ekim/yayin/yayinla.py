#!/usr/bin/env python3
"""KAAN 29 Ekim galeri haberini envantermedya.com'a (TR) yükler.

Kimlik bilgisi ortam değişkenlerinden okunur, dosyaya veya commit'e yazılmaz:
  ENVANTER_WP_USER          WordPress kullanıcı adı
  ENVANTER_WP_APP_PASSWORD  Uygulama Parolası
  (ENVANTER_WP_URL isteğe bağlı, varsayılan https://envantermedya.com)

Kullanım:
  python3 yayinla.py            # yükler ve yayına alır
  python3 yayinla.py --taslak   # yükler, taslak olarak bırakır
"""
import base64, json, mimetypes, os, sys, urllib.error, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = os.environ.get("ENVANTER_WP_URL", "https://envantermedya.com").rstrip("/") + "/wp-json"
USER = os.environ.get("ENVANTER_WP_USER")
PWD = os.environ.get("ENVANTER_WP_APP_PASSWORD")
if not (USER and PWD):
    sys.exit("ENVANTER_WP_USER ve ENVANTER_WP_APP_PASSWORD tanımlı değil")
AUTH = "Basic " + base64.b64encode(f"{USER}:{PWD}".encode()).decode()
TASLAK = "--taslak" in sys.argv


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
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path} -> {e.code}: {e.read()[:400].decode(errors='replace')}")


def upload(item):
    f = HERE / item["file"]
    media = call("POST", "/wp/v2/media", raw=f.read_bytes(), headers={
        "Content-Type": mimetypes.guess_type(f.name)[0] or "image/jpeg",
        "Content-Disposition": f'attachment; filename="{f.name}"',
    })
    call("POST", f"/wp/v2/media/{media['id']}", {
        "alt_text": item["alt"], "title": item.get("caption", item["alt"]), "caption": item.get("caption", ""),
    })
    call("POST", "/ev/v1/set-post-lang", {"post_id": media["id"], "lang": "tr"})
    print(f"  medya {media['id']}: {f.name}")
    return media


def gallery_block(images):
    inner = []
    for m, it in images:
        url = m["source_url"]
        cap = f'<figcaption class="wp-element-caption">{it["caption"]}</figcaption>' if it.get("caption") else ""
        inner.append(
            f'<!-- wp:image {{"id":{m["id"]},"sizeSlug":"full","linkDestination":"media"}} -->\n'
            f'<figure class="wp-block-image size-full"><a href="{url}"><img src="{url}" alt="{it["alt"]}" class="wp-image-{m["id"]}"/></a>{cap}</figure>\n'
            f'<!-- /wp:image -->'
        )
    return (
        '<!-- wp:gallery {"columns":1,"imageCrop":false,"linkTo":"media","sizeSlug":"full"} -->\n'
        '<figure class="wp-block-gallery has-nested-images columns-1">\n'
        + "\n".join(inner) + "\n</figure>\n<!-- /wp:gallery -->"
    )


def main():
    h = json.loads((HERE / "haber.json").read_text(encoding="utf-8"))
    me = call("GET", "/wp/v2/users/me")
    print(f"Oturum: {me.get('name')}")
    var = call("GET", f"/wp/v2/posts?slug={h['slug']}&status=publish,draft,future,pending&context=edit")
    if var:
        sys.exit(f"Bu slug zaten var: post {var[0]['id']} ({var[0]['status']}). Önce onu kontrol edin.")

    print("Görseller yükleniyor")
    cover = upload(h["cover"])
    imgs = [(upload(it), it) for it in h["gallery"]]

    content = "\n\n".join(h["body_before_gallery"] + [gallery_block(imgs)] + h["body_after_gallery"])
    post = call("POST", "/wp/v2/posts", {
        "title": h["title"], "slug": h["slug"], "status": "draft", "content": content,
        "excerpt": h["excerpt"], "categories": h["categories"], "featured_media": cover["id"],
        "meta": {k: h[k] for k in ("rank_math_title", "rank_math_description", "rank_math_focus_keyword")},
    })
    call("POST", "/ev/v1/set-post-lang", {"post_id": post["id"], "lang": "tr"})
    print(f"Taslak: post {post['id']}")

    if not TASLAK:
        post = call("POST", f"/wp/v2/posts/{post['id']}", {"status": "publish"})
        post = call("POST", f"/wp/v2/posts/{post['id']}", {"featured_media": cover["id"], "categories": h["categories"]})
    print(f"Durum: {post['status']}  Kapak: {post['featured_media']}  Kategoriler: {post['categories']}")
    print(f"Adres: {post['link']}")


if __name__ == "__main__":
    main()
