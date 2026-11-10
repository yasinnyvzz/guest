#!/usr/bin/env python3
"""Ortak "kapak.webp" dosyasına bağlanmış TR haberlerine kendi kapaklarını geri verir.

Sorun: yayinla_tr.py her TR kapağını "kapak.png" adıyla yüklüyordu. Sitedeki WebP dönüştürücü
bunu her seferinde aynı wp-content/uploads/2026/11/kapak.webp dosyasının üzerine yazdığı için
bütün TR haberleri en son yüklenen kartı (SUNGUR) gösteriyordu.

Her haber için: başlık kartı üretilir -> "<slug>-kapak.png" adıyla yüklenir -> dil TR atanır ->
medya çeviri grubunda eski TR kapağın yerine konur -> postun featured_media'sı değiştirilir.

Kullanım: python3 kapak_onar.py [--uygula]   (varsayılan: kuru çalıştırma, yalnız kartları üretir)
"""
import json, os, sys, tempfile, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kapak import make

B = os.environ.get("ENVANTER_WP_URL", "https://envantermedya.com").rstrip("/") + "/wp-json"
UYGULA = "--uygula" in sys.argv
OUT = Path(tempfile.mkdtemp(prefix="kapak_onar_"))

# post_id: (etiket, manşet)
ISLER = {
    85681: ("LOCKHEED", "Lockheed Martin füze üretimine 8 milyar dolar yatıracak"),
    85666: ("FA'AZ", "Pakistan, Fa'az füzesini JF-17'den test etti"),
    85651: ("SKYRANGER", "Belçika 20 Skyranger 30 sipariş etti"),
    85451: ("FDI", "Fransa, FDI'ların Aster kapasitesini 32'ye çıkarıyor"),
    85386: ("TAURUS", "İsveç, Gripen için Taurus füzelerini teslim aldı"),
    85383: ("RTX", "RTX, füze üretimini 70 milyar dolarlık sözleşmelerle 2-4 kat artırıyor"),
    85043: ("SUNGUR", "SUNGUR, BURÇ'tan ilk atışta hedefi vurdu"),
    85040: ("SİPER", "SİPER'in üst katmanı için hipersonik radar"),
}


def call(method, path, data=None, raw=None, headers=None):
    h = {"User-Agent": "envanter-pub"}
    auth = os.environ.get("EV_AUTH")
    if auth:
        import base64
        h["Authorization"] = "Basic " + base64.b64encode(auth.encode()).decode()
    body = None
    if raw is not None:
        body = raw; h.update(headers or {})
    elif data is not None:
        body = json.dumps(data).encode(); h["Content-Type"] = "application/json"
    req = urllib.request.Request(B + path, data=body, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path} -> {e.code}: {e.read()[:400].decode(errors='replace')}")


def main():
    for pid, (etiket, manset) in ISLER.items():
        p = call("GET", f"/wp/v2/posts/{pid}?context=edit&_fields=id,slug,title,featured_media")
        eski = p["featured_media"]
        png = OUT / f"{p['slug']}-kapak.png"
        make(str(png), etiket, manset)
        print(f"[{pid}] {p['slug']}  eski kapak {eski}  -> {png}")
        if not UYGULA:
            continue
        m = call("POST", "/wp/v2/media", raw=png.read_bytes(), headers={
            "Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{png.name}"'})
        if Path(m["source_url"]).stem != png.stem:
            sys.exit(f"  yükleme yine ortak dosyaya gitti: {m['source_url']}")
        title = p["title"]["raw"]
        call("POST", f"/wp/v2/media/{m['id']}", {"alt_text": title, "title": title})
        call("POST", "/ev/v1/set-post-lang", {"post_id": m["id"], "lang": "tr"})
        grup = {l: v["id"] for l, v in call("GET", f"/ev/v1/post-translations?id={eski}").items()} if eski else {}
        grup["tr"] = m["id"]
        if eski:
            call("POST", "/ev/v1/pll-detach", {"ids": [eski]})
        call("POST", "/ev/v1/link-post-translations", {"groups": [grup]})
        call("POST", f"/wp/v2/posts/{pid}", {"featured_media": m["id"]})
        print(f"  yeni kapak {m['id']}: {m['source_url']}  grup {grup}")


if __name__ == "__main__":
    main()
