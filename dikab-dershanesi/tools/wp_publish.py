#!/usr/bin/env python3
"""DİKAB Dershanesi: Markdown makaleleri sitenin Sözlük şablonuna çevirip
WordPress'e zamanlanmış (future) yazı olarak gönderir.

Kimlik bilgisi dosyadan okunur (DIKAB_WP_AUTH_FILE, içerik: "kullanici:uygulama sifresi").
Bu dosya depoya asla eklenmez.

Kullanım:
  wp_publish.py render            # HTML'leri out/ klasörüne yazar (deneme)
  wp_publish.py publish           # yoksa oluşturur, varsa (aynı slug) günceller
  wp_publish.py publish --relink  # tüm iç linkleri tarih kontrolü olmadan açar
"""
import base64
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

import markdown

SITE = "https://dikabdershanesi.com"
API = SITE + "/wp-json/wp/v2"
HERE = os.path.dirname(os.path.abspath(__file__))
ARTICLES = os.path.join(HERE, "..", "makaleler")

SOZLUK_CAT = 12
REHBER_CAT_SLUG = "diyanet-rehberi"
REHBER_CAT_NAME = "Diyanet Rehberi"

# (dosya, slug, başlık, tür, yayın tarihi TSİ)
SCHEDULE = [
    ("01-sebut-tival-nedir.md", "sebut-tival-nedir", "Seb'u't-Tıvâl (Sebut Tıval) Nedir?", "sozluk", "2026-10-28T09:00:00"),
    ("03-vakf-i-kafi-nedir.md", "vakf-i-kafi-nedir", "Vakf-ı Kâfî Nedir?", "sozluk", "2026-10-29T09:00:00"),
    ("04-vacib-li-aynihi-nedir.md", "li-aynihi-vacip-nedir", "Li-aynihi Vâcip Nedir?", "sozluk", "2026-10-30T09:00:00"),
    ("09-diyanet-becayis-nasil-yapilir.md", "diyanet-becayis-nasil-yapilir", None, "rehber", "2026-10-31T09:00:00"),
    ("10-diyanet-munhal-kadro-nedir.md", "diyanet-munhal-kadro-nedir", None, "rehber", "2026-11-01T09:00:00"),
    ("11-facebook-becayis-gruplari.md", "facebook-becayis-gruplari", None, "rehber", "2026-11-02T09:00:00"),
    ("12-imam-vakitte-camide-yoksa-cezasi.md", "imam-namaz-vaktinde-camide-yoksa-cezasi-nedir", None, "rehber", "2026-11-03T09:00:00"),
    ("13-imam-murakip-denetimi.md", "imam-murakip-denetimi", None, "rehber", "2026-11-04T09:00:00"),
    ("14-imam-sevgili-yaparsa-gorevden-atilir-mi.md", "imam-sevgili-yaparsa-gorevden-atilir-mi", None, "rehber", "2026-11-05T09:00:00"),
]

# Sitede zaten yayında olan sayfalar (tarih kontrolü gerekmez)
EXISTING = {
    "beda-nedir": "/beda-nedir/",
    "akraba-nedir": "/akraba-nedir/",
    "baas-nedir": "/baas-nedir/",
    "ehlivukuf-nedir": "/ehlivukuf-nedir/",
    "dikab-kavramlar-sozlugu": "/dikab-kavramlar-sozlugu/",
}
# Taslaklardaki eski göreli linkler -> sitedeki slug
ALIASES = {
    "bas-nedir": "baas-nedir",
    "ehl-i-vukuf-ne-demek": "ehlivukuf-nedir",
    "kan-ya-da-evlilik-yoluyla-birbirine-bagli-insanlara-ne-denir": "akraba-nedir",
    "dikab-kavram-sozlugu": "dikab-kavramlar-sozlugu",
    "vacib-li-aynihi-nedir": "li-aynihi-vacip-nedir",
}
GMT_OFFSET_H = 3  # Europe/Istanbul


def auth_header():
    path = os.environ.get("DIKAB_WP_AUTH_FILE")
    if not path:
        sys.exit("DIKAB_WP_AUTH_FILE tanımlı değil")
    with open(path) as f:
        token = base64.b64encode(f.read().strip().encode()).decode()
    return {"Authorization": "Basic " + token}


def api(method, path, body=None):
    req = urllib.request.Request(API + path, method=method, headers={**auth_header(), "Content-Type": "application/json"})
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, data, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            sys.exit(f"{method} {path} -> {e.code}: {e.read()[:500]!r}")
        except urllib.error.URLError:
            # POST yalnız bağlantı kurulamadıysa tekrar denenir; ikinci POST kopya yaratabilir
            if attempt == 4 or method != "GET":
                raise
            time.sleep(2 ** (attempt + 1))


def parse(path):
    text = open(path, encoding="utf-8").read()
    _, fm, body = text.split("---\n", 2)
    meta = {}
    for line in fm.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    # editör notlarını ve H1'i at
    body = re.sub(r"(?m)^> \*\*Editör notu:\*\*.*(?:\n>.*)*\n?", "", body)
    body = re.sub(r"(?m)^# .*\n", "", body, count=1)
    return meta, body.strip()


def link_rewriter(pub_date, relink):
    dates = {slug: date for _, slug, _, _, date in SCHEDULE}

    def repl(m):
        label, target = m.group(1), m.group(2)
        if not target.startswith("/"):
            return m.group(0)
        slug = ALIASES.get(target.strip("/"), target.strip("/"))
        if slug in EXISTING:
            return f"[{label}]({SITE}{EXISTING[slug]})"
        if slug in dates and (relink or dates[slug] <= pub_date):
            return f"[{label}]({SITE}/{slug}/)"
        return label  # henüz yayımlanmamış yazı: düz metin

    return repl


def md(s):
    return markdown.markdown(s, extensions=["tables"])


def build(meta, body, kind, pub_date, relink):
    body = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_rewriter(pub_date, relink), body)

    lead_m = re.match(r"\*\*Kısa cevap:\*\*\s*(.+?)\n\n", body, re.S)
    lead = lead_m.group(1).strip()
    body = body[lead_m.end():]

    parts = re.split(r"(?m)^## (.+)$", body)
    intro, sections = parts[0].strip(), list(zip(parts[1::2], parts[2::2]))

    faq, tail_html = [], ""
    out_sections = []
    for title, content in sections:
        content = content.strip()
        # son bölümdeki --- sonrası (ilgili + kaynaklar) ayrılır
        if "\n---\n" in content:
            content, tail = content.split("\n---\n", 1)
            tail_html = tail.strip()
        if title.strip().lower().startswith("sıkça sorulan"):
            for q, a in re.findall(r"\*\*(.+?)\*\*\n(.+?)(?:\n\n|$)", content.strip() + "\n\n", re.S):
                faq.append((q.strip(), a.strip()))
            continue
        out_sections.append((title.strip(), md(content.strip())))

    h = []
    if kind == "sozluk":
        h.append(f'<p class="dks-meta"><span class="dks-tur">Kavram</span> · <a href="{SITE}/sozluk/">DİKAB Sözlük</a></p>')
    else:
        h.append(f'<p class="dks-meta"><span class="dks-tur">Rehber</span> · <a href="{SITE}/category/{REHBER_CAT_SLUG}/">{REHBER_CAT_NAME}</a></p>')
    h.append(f'<p class="dks-lead">{md(lead)[3:-4]}</p>')
    if intro:
        h.append(md(intro))

    if kind == "sozluk":
        for i, (title, content) in enumerate(out_sections):
            h.append(f'<details class="dks-acc"{" open" if i == 0 else ""}><summary>{html.escape(title)}</summary><div class="dks-in">{content}</div></details>')
    else:
        for title, content in out_sections:
            h.append(f"<h2>{html.escape(title)}</h2>{content}")

    if faq:
        qa = "".join(f'<h3 class="dks-q">{md(q)[3:-4]}</h3><p class="dks-a">{md(a)[3:-4]}</p>' for q, a in faq)
        if kind == "sozluk":
            h.append(f'<details class="dks-acc"><summary>Sık Sorulan Sorular</summary><div class="dks-in">{qa}</div></details>')
        else:
            h.append(f"<h2>Sık Sorulan Sorular</h2>{qa}")

    for para in [p for p in tail_html.split("\n\n") if p.strip()]:
        inner = md(para.strip())[3:-4]
        cls = "dks-ilgili" if para.startswith("**İlgili") else "dks-kaynak"
        h.append(f'<p class="{cls}">{inner}</p>')

    h.append(f'<p class="dks-cta">Bu konuyu sınav formatında pekiştirmek için <a href="{SITE}/coz/">soru çöz</a> veya <a href="{SITE}/notlar/">özet ders notlarına</a> göz at.</p>')

    if faq:
        strip = lambda s: re.sub(r"<[^>]+>", "", md(s)).strip()
        ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]}
        h.append('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>")
    return "".join(h)


def gmt(local):
    d, t = local.split("T")
    y, mo, da = map(int, d.split("-"))
    hh = int(t[:2]) - GMT_OFFSET_H
    if hh < 0:  # 09:00 için gerekmez, ama güvenli olsun
        raise SystemExit("gün kayması desteklenmiyor")
    return f"{d}T{hh:02d}{t[2:]}"


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "render"
    relink = "--relink" in sys.argv
    out = os.path.join(HERE, "..", "out")
    os.makedirs(out, exist_ok=True)

    rehber_cat = None
    if mode == "publish":
        cats = api("GET", f"/categories?slug={REHBER_CAT_SLUG}")
        rehber_cat = cats[0]["id"] if cats else api("POST", "/categories", {"name": REHBER_CAT_NAME, "slug": REHBER_CAT_SLUG})["id"]

    for fname, slug, title, kind, date in SCHEDULE:
        meta, body = parse(os.path.join(ARTICLES, fname))
        content = build(meta, body, kind, date, relink)
        title = title or meta["seo_title"]
        if mode == "render":
            with open(os.path.join(out, slug + ".html"), "w", encoding="utf-8") as f:
                f.write(f"<h1>{html.escape(title)}</h1>\n" + content)
            print("render", slug, len(content))
            continue
        existing = api("GET", f"/posts?slug={slug}&status=publish,future,draft,pending,private&context=edit")
        payload = {"content": content, "excerpt": meta["meta_description"]}
        if existing:
            p = api("POST", f"/posts/{existing[0]['id']}", payload)
            print("update", p["id"], p["status"], p["date"], p["link"])
        else:
            payload.update({"title": title, "slug": slug, "status": "future", "date": date, "date_gmt": gmt(date),
                            "categories": [SOZLUK_CAT if kind == "sozluk" else rehber_cat]})
            p = api("POST", "/posts", payload)
            print("create", p["id"], p["status"], p["date"], p["slug"], p["link"])


if __name__ == "__main__":
    main()
