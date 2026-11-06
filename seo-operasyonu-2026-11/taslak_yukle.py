#!/usr/bin/env python3
"""Envanter Medya: SEO taslaklarını WordPress'e YALNIZCA 'draft' olarak yükler.

Kimlik: EV_AUTH="kullanıcı:uygulama parolası" (envantermedya.com için; başka sitenin bilgisi kullanılmaz).
Kullanım:
  python3 taslak_yukle.py taslaklar/*.json            # kuru çalıştırma (varsayılan) — hiçbir şey yazmaz
  python3 taslak_yukle.py taslaklar/*.json --yaz      # taslak oluşturur, dil atar; YAYINLAMAZ
Kurallar: aynı slug (publish/draft/future/pending) varsa atlar; status her zaman 'draft';
kategori yalnız TR için verilir (Polylang eşitlemesi), diğer dillerde editör grupladıktan sonra eşitlenir.
"""
import json, os, sys, requests

EV = "https://envantermedya.com/wp-json"
TR_CATS = [53, 24795]


def sess():
    auth = os.environ.get("EV_AUTH")
    if not auth:
        sys.exit("EV_AUTH tanımlı değil (envantermedya.com kullanıcı:uygulama parolası).")
    s = requests.Session()
    s.auth = tuple(auth.split(":", 1))
    s.headers["User-Agent"] = "Mozilla/5.0 (EnvanterSEO)"
    me = s.get(f"{EV}/wp/v2/users/me", timeout=60)
    if me.status_code != 200:
        sys.exit(f"Kimlik doğrulanamadı: {me.status_code}")
    return s


def exists(s, slug):
    r = s.get(f"{EV}/wp/v2/posts", params={"slug": slug, "status": "publish,draft,future,pending", "lang": "all",
                                           "_fields": "id,status,link"}, timeout=60)
    return r.json() if r.status_code == 200 else []


def main(paths, write):
    s = sess() if write else None
    out = []
    for p in paths:
        d = json.load(open(p))
        if d.get("status_decision", "").startswith("SKIP"):
            print("ATLA (mükerrer):", p); continue
        payload = {"title": d["title"], "slug": d["slug"], "content": d["content_html"], "excerpt": d["excerpt"],
                   "status": "draft", "meta": {"rank_math_title": d["rank_math_title"],
                   "rank_math_description": d["rank_math_description"], "rank_math_focus_keyword": d["rank_math_focus_keyword"]}}
        if d["lang"] == "tr":
            payload["categories"] = TR_CATS
        if not write:
            print(f"[kuru] {d['lang']} {d['slug']} | {len(d['content_html'])} karakter | kaynak: {len(d.get('sources', []))}")
            continue
        ex = exists(s, d["slug"])
        if ex:
            print("ZATEN VAR, atlandı:", d["slug"], ex[0]["id"], ex[0]["status"]); continue
        r = s.post(f"{EV}/wp/v2/posts", json=payload, timeout=120); r.raise_for_status()
        pid = r.json()["id"]
        s.post(f"{EV}/ev/v1/set-post-lang", json={"post_id": pid, "lang": d["lang"]}, timeout=60).raise_for_status()
        chk = s.get(f"{EV}/wp/v2/posts/{pid}", params={"context": "edit", "_fields": "id,status,link"}, timeout=60).json()
        assert chk["status"] == "draft", chk
        out.append({"file": p, "lang": d["lang"], "post_id": pid, "status": chk["status"], "link": chk["link"]})
        print("TASLAK:", d["lang"], pid, chk["link"])
    if out:
        json.dump(out, open("yukleme_kaydi.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args, "--yaz" in sys.argv)
