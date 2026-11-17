#!/usr/bin/env python3
"""Defence Arabia'ya Markdown seri makalesini (ör. bedail-al-gharb/*.md) zamanlanmış yayınlar.
Kimlik: DA_AUTH ortam değişkeni ("kullanıcı:uygulama parolası"). Zaman UTC.
Kullanım: yayinla_md_da.py makale.md "2026-11-18T06:00" "296,336,352" [--dry]
         yayinla_md_da.py makale.md --update      (var olan yazının içeriğini/SEO alanlarını günceller; tarih ve durum değişmez)
- YAML ön bilgi: slug, seo_title, meta_description, primary_keyword kullanılır.
- H1 başlık olur; editör bölümleri (المقترحات البصرية، ربط داخلي وخارجي) yayınlanmaz.
- Aynı slug sitede varsa (yayında/taslak/zamanlanmış) durur."""
import os, re, sys, tempfile
import markdown, requests
sys.path.insert(0, os.path.dirname(__file__))
from kapak import make

DA = "https://www.defencearabia.com/wp-json"
EDITOR_SECTIONS = ("المقترحات البصرية", "ربط داخلي وخارجي")
SERIES_LABEL = "بدائل الغرب"


def parse(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    fm, body = {}, txt
    if m:
        for line in m.group(1).splitlines():
            k = re.match(r"^([a-z_]+):\s*(.*)$", line)
            if k and k.group(2):
                fm[k.group(1)] = k.group(2).strip().strip('"')
        body = txt[m.end():]
    h1 = re.search(r"^# (.+)$", body, re.M)
    title = h1.group(1).strip()
    body = body[h1.end():]
    # editör bölümlerini çıkar (bir sonraki ## başlığına kadar)
    parts = re.split(r"(?m)^(?=## )", body)
    body = "".join(p for p in parts if not any(p.startswith("## " + s) for s in EDITOR_SECTIONS))
    body = re.sub(r"(?m)^---\s*$\n?(?=\s*(?:---\s*$|\Z))", "", body)
    # satır içi editör notlarını çıkar: *(رابط Envanter ...)*
    body = re.sub(r"\s*\*\((?:رابط )?Envanter[^*]*\)\*", "", body)
    # çıplak URL'leri bağlantıya çevir
    body = re.sub(r"(?<![(<\"])(https?://[^\s)<>]+)", r"<\1>", body)
    html = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists"])
    return fm, title, html


def update(path):
    fm, title, html = parse(path)
    s = requests.Session()
    u, p = os.environ["DA_AUTH"].split(":", 1)
    s.auth, s.headers["User-Agent"] = (u, p), "Mozilla/5.0 (DAYayin)"
    r = s.get(f"{DA}/wp/v2/posts", params={"slug": fm["slug"], "status": "publish,draft,future,pending,private"}, timeout=60)
    r.raise_for_status()
    if not r.json():
        sys.exit(f"YOK: {fm['slug']}")
    pid = r.json()[0]["id"]
    s.post(f"{DA}/wp/v2/posts/{pid}", json={"title": title, "content": html, "excerpt": fm.get("meta_description", "")},
           timeout=120).raise_for_status()
    s.post(f"{DA}/rankmath/v1/updateMeta", timeout=60, json={"objectType": "post", "objectID": pid, "meta": {
        "rank_math_title": fm.get("seo_title", title), "rank_math_description": fm.get("meta_description", ""),
        "rank_math_focus_keyword": fm.get("primary_keyword", "")}}).raise_for_status()
    print("GÜNCELLENDİ", pid, fm["slug"])


def main():
    if "--update" in sys.argv:
        return update(sys.argv[1])
    path, when, cats = sys.argv[1], sys.argv[2], [int(c) for c in sys.argv[3].split(",")]
    dry = "--dry" in sys.argv
    fm, title, html = parse(path)
    slug = fm["slug"]
    if dry:
        out = os.path.join(tempfile.mkdtemp(), slug + ".html")
        open(out, "w", encoding="utf-8").write(f"<h1>{title}</h1>\n{html}")
        print("DRY", slug, title, len(html), out)
        return
    s = requests.Session()
    u, p = os.environ["DA_AUTH"].split(":", 1)
    s.auth, s.headers["User-Agent"] = (u, p), "Mozilla/5.0 (DAYayin)"
    r = s.get(f"{DA}/wp/v2/posts", params={"slug": slug, "status": "publish,draft,future,pending,private"}, timeout=60)
    r.raise_for_status()
    if r.json():
        sys.exit(f"ZATEN VAR: {slug} -> {r.json()[0]['id']}")
    png = os.path.join(tempfile.mkdtemp(), "c.png")
    make(png, SERIES_LABEL, title, "DEFENCE ARABIA", True)
    m = s.post(f"{DA}/wp/v2/media", data=open(png, "rb").read(), timeout=120,
               headers={"Content-Disposition": f'attachment; filename="{slug}-cover.png"', "Content-Type": "image/png"})
    m.raise_for_status()
    mid = m.json()["id"]
    s.post(f"{DA}/wp/v2/media/{mid}", json={"alt_text": title, "title": title}, timeout=60).raise_for_status()
    r = s.post(f"{DA}/wp/v2/posts", timeout=120, json={
        "title": title, "slug": slug, "content": html, "excerpt": fm.get("meta_description", ""),
        "status": "future", "date": when, "date_gmt": when, "featured_media": mid, "categories": cats,
        "meta": {"rank_math_title": fm.get("seo_title", title), "rank_math_description": fm.get("meta_description", ""),
                 "rank_math_focus_keyword": fm.get("primary_keyword", "")}})
    r.raise_for_status()
    j = r.json()
    # RankMath alanları REST "meta" ile kaydolmuyor; kendi uç noktası kullanılır
    s.post(f"{DA}/rankmath/v1/updateMeta", timeout=60, json={"objectType": "post", "objectID": j["id"], "meta": {
        "rank_math_title": fm.get("seo_title", title), "rank_math_description": fm.get("meta_description", ""),
        "rank_math_focus_keyword": fm.get("primary_keyword", "")}}).raise_for_status()
    print(j["id"], j["status"], j["date_gmt"], j["link"])


if __name__ == "__main__":
    main()
