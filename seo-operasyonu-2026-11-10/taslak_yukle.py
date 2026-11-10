#!/usr/bin/env python3
"""Envanter Medya — SEO pilot taslaklarını WordPress'e YALNIZCA 'draft' olarak yükler (10 Kasım 2026).

Kimlik: EV_AUTH="kullanıcı:uygulama parolası" ya da oturum vekilinin eklediği yetki (EV_AUTH yoksa
Authorization başlığı gönderilmez; /users/me ile yetki doğrulanır). Bilgi dosyaya yazılmaz.

Kullanım:
  python3 taslak_yukle.py taslaklar/*.json          # kuru çalıştırma — hiçbir şey yazmaz
  python3 taslak_yukle.py taslaklar/*.json --yaz    # taslak + öne çıkan görsel + dil; YAYINLAMAZ, ZAMANLAMAZ

Kurallar:
- decision UPDATE/SKIP olan dosyalar yeni yazı açmaz (UPDATE'ler onaydan sonra guncelle.py ile uygulanır).
- Aynı slug herhangi bir durumda (publish/draft/future/pending/private) varsa atlanır; yukleme_kaydi.json'da
  kayıtlı dosya tekrar gönderilmez (aynı makale iki kez gönderilmez).
- Görsel: lisanslı fotoğraf (kamu malı / açık lisans) indirilir, 1200 px genişliğe ölçeklenip WebP'ye çevrilir,
  altyazıya kredi + lisans yazılır. Lisanssız ya da indirilemeyen görselde ev başlık kartı (WebP) kullanılır.
- Hata durumunda kontrolsüz tekrar yok: GET'ler en fazla 3 deneme, POST'lar tek deneme.
"""
import io, json, os, re, sys, time
from pathlib import Path
import requests
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "yayin-araclari"))
from kapak import make  # noqa: E402

EV = "https://envantermedya.com/wp-json"
LOG = HERE / "taslaklar" / "yukleme_kaydi.json"
# Dil ve içerik türüne göre kategori (TR'de Polylang eşitlemesi kategorileri TR'den dağıtır).
CATS = {
    ("tr", "*"): [53, 24795],
    ("en", "explainer"): [11221], ("en", "guide"): [11221], ("en", "analysis"): [8174, 8198],
    ("en", "profile"): [8290], ("en", "news"): [8174, 30246],
    ("es", "explainer"): [29685], ("es", "guide"): [28950], ("es", "news"): [20556, 46535],
    ("ru", "explainer"): [29561], ("ru", "guide"): [31840], ("ru", "news"): [8180, 31132],
}
LABEL = {"en": "EXPLAINER", "es": "GUÍA", "ru": "СПРАВКА", "tr": "REHBER", "ar": "دليل"}
LABEL_BY_TYPE = {"analysis": {"en": "ANALYSIS"}, "profile": {"en": "PROFILE"}, "news": {"en": "NEWS", "es": "NOTICIA", "ru": "НОВОСТИ"}}


def session():
    s = requests.Session()
    s.headers["User-Agent"] = "envanter-seo-pilot"
    if os.environ.get("EV_AUTH"):
        s.auth = tuple(os.environ["EV_AUTH"].split(":", 1))
    me = s.get(f"{EV}/wp/v2/users/me", params={"context": "edit", "_fields": "id,name,capabilities"}, timeout=60)
    if me.status_code != 200 or not me.json().get("capabilities", {}).get("edit_posts"):
        sys.exit(f"Yetki doğrulanamadı: {me.status_code}")
    print("Oturum:", me.json()["name"])
    return s


def get(s, url, **kw):
    for i in range(3):
        try:
            r = s.get(url, timeout=60, **kw)
            if r.status_code < 500:
                return r
        except requests.RequestException:
            pass
        time.sleep(4 * (i + 1))
    sys.exit(f"GET başarısız: {url}")


def slug_exists(s, slug):
    r = get(s, f"{EV}/wp/v2/posts", params={"slug": slug, "status": "publish,draft,future,pending,private",
                                           "context": "edit", "_fields": "id,status,link"})
    return r.json() if r.status_code == 200 else []


def webp_bytes(img: Image.Image) -> bytes:
    img = img.convert("RGB")
    if img.width > 1200:
        img = img.resize((1200, round(img.height * 1200 / img.width)), Image.LANCZOS)
    buf = io.BytesIO(); img.save(buf, "WEBP", quality=82, method=6)
    return buf.getvalue()


def cover(d):
    """(bytes, kaynak notu) — lisanslı fotoğraf ya da ev başlık kartı."""
    im = d.get("image") or {}
    url = im.get("direct_image_url")
    if im.get("type") in ("public_domain_photo", "cc_photo", "official_photo") and url and im.get("licence"):
        try:
            r = requests.get(url, timeout=60, headers={"User-Agent": "envanter-seo-pilot (editorial image fetch)"})
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("image/"):
                img = Image.open(io.BytesIO(r.content))
                if img.width >= 800:
                    return webp_bytes(img), f"{im.get('credit', '')} — {im['licence']} ({im.get('source_page_url', url)})"
        except Exception as e:  # görsel alınamazsa başlık kartına düş
            print("  görsel alınamadı, başlık kartı kullanılacak:", e)
    tmp = HERE / "taslaklar" / f"{d['slug']}-kapak.png"
    lab = LABEL_BY_TYPE.get(d.get("content_type"), {}).get(d["lang"]) or LABEL.get(d["lang"], "ENVANTER")
    make(str(tmp), lab, d["title"], "ENVANTER MEDYA", d["lang"] == "ar")
    data = webp_bytes(Image.open(tmp)); tmp.unlink()
    return data, "Envanter Medya başlık kartı (fotoğraf değildir)"


def main(paths, write):
    log = json.loads(LOG.read_text()) if LOG.exists() else []
    done = {x["file"] for x in log}
    s = session() if write else None
    for p in map(Path, paths):
        d = json.loads(p.read_text(encoding="utf-8"))
        dec = d.get("decision", "")
        if dec.startswith("SKIP") or dec.startswith("UPDATE"):
            print(f"ATLA ({dec}):", p.name); continue
        if p.name in done:
            print("ZATEN YÜKLENDİ (kayıtta var):", p.name); continue
        cats = CATS.get((d["lang"], "*")) or CATS.get((d["lang"], d.get("content_type", "explainer")), [])
        payload = {"title": d["title"], "slug": d["slug"], "content": d["content_html"], "excerpt": d["excerpt"],
                   "status": "draft", "categories": cats,
                   "meta": {"rank_math_title": d["rank_math_title"], "rank_math_description": d["rank_math_description"],
                            "rank_math_focus_keyword": d["rank_math_focus_keyword"]}}
        if not write:
            print(f"[kuru] {d['lang']} {d['slug']} | {len(d['content_html'])} krk | kaynak {len(d.get('sources', []))} | "
                  f"görsel {d.get('image', {}).get('type')} | kategori {cats}"); continue
        ex = slug_exists(s, d["slug"])
        if ex:
            print("AYNI SLUG VAR, atlandı:", d["slug"], ex[0]["id"], ex[0]["status"]); continue
        data, note = cover(d)
        m = s.post(f"{EV}/wp/v2/media", data=data, timeout=120,
                   headers={"Content-Disposition": f'attachment; filename="{d["slug"]}.webp"', "Content-Type": "image/webp"})
        m.raise_for_status(); mid = m.json()["id"]
        alt = (d.get("image") or {}).get("alt") or d["title"]
        s.post(f"{EV}/wp/v2/media/{mid}", json={"alt_text": alt, "title": d["title"], "caption": note}, timeout=60).raise_for_status()
        s.post(f"{EV}/ev/v1/set-post-lang", json={"post_id": mid, "lang": d["lang"]}, timeout=60)
        payload["featured_media"] = mid
        r = s.post(f"{EV}/wp/v2/posts", json=payload, timeout=120); r.raise_for_status()
        pid = r.json()["id"]
        s.post(f"{EV}/ev/v1/set-post-lang", json={"post_id": pid, "lang": d["lang"]}, timeout=60).raise_for_status()
        chk = get(s, f"{EV}/wp/v2/posts/{pid}", params={"context": "edit", "_fields": "id,status,link,meta"}).json()
        assert chk["status"] == "draft", chk
        assert chk["meta"].get("rank_math_title") == d["rank_math_title"], "Rank Math başlığı kaydedilmedi"
        log.append({"file": p.name, "lang": d["lang"], "post_id": pid, "media_id": mid, "status": "draft",
                    "preview": f"https://envantermedya.com/?p={pid}&preview=true", "title": d["title"], "slug": d["slug"],
                    "target_query": d.get("target_query", ""), "decision": dec, "content_type": d.get("content_type"),
                    "image_note": note, "sources": len(d.get("sources", []))})
        LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1))
        print("TASLAK:", d["lang"], pid, d["slug"], "|", note[:60])
        time.sleep(1)


if __name__ == "__main__":
    main([a for a in sys.argv[1:] if not a.startswith("--")], "--yaz" in sys.argv)
