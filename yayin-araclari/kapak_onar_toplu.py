#!/usr/bin/env python3
"""Aynı fiziksel kapak dosyasını paylaşan (farklı başlıklı) yazılara kendi başlık kartlarını verir.

Girdi: sinif JSON'u ({"kart": [{"url":…, "posts":[{"id","type","title","media",…}]}]}),
       tarama betiğinin ürettiği dosya. Yalnız "kart" grupları işlenir; aynı başlıklı kopya
       yazılar ("kopya") ve fotoğraflar ("foto") bu betiğe dahil değildir.

Her yazı için:
  1. Dili Polylang grubundan okunur (yoksa dosya adındaki -ar-/-en-… ekinden).
  2. kapak.py ile başlık kartı üretilir (ar: sağdan sola, zh: CJK yazı tipi).
  3. "<post_id>-<dil>-kapak.png" adıyla yüklenir; sunucunun aynı adı koruduğu doğrulanır.
  4. Medya dili atanır, eski medyanın çeviri grubunda yerine konur.
  5. Yeni medya, çevirilerin kapaklarıyla aynı medya çeviri grubuna bağlanır (Polylang kapak
     eşitlemesi diğer dillere yanlış kapak kopyalamasın), sonra featured_media güncellenir.
  6. Kayıttan sonra çeviri grubu yeniden okunur (eklenti kayıtta otomatik bağlayabiliyor);
     kapağı değişen kardeş yazı önceki değerine (ya da KAPAK_TABAN taramasındaki değere) döndürülür.
İlerleme kapak_onar_toplu.log dosyasına yazılır; yeniden çalıştırınca bitenler atlanır.

Kullanım: kapak_onar_toplu.py <sinif.json> [--uygula] [--sinir N]
"""
import json, os, re, sys, tempfile, time, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kapak import make

B = os.environ.get("ENVANTER_WP_URL", "https://envantermedya.com").rstrip("/") + "/wp-json"
REST = {"posts": "posts", "pages": "pages"}  # diğer tipler aynı adla
args = [a for a in sys.argv[1:] if not a.startswith("--")]
UYGULA = "--uygula" in sys.argv
SINIR = int(sys.argv[sys.argv.index("--sinir") + 1]) if "--sinir" in sys.argv else None
LOG = Path(os.environ.get("KAPAK_LOG", Path(args[0]).with_suffix(".log")))
OUT = Path(tempfile.mkdtemp(prefix="kapak_toplu_"))


def call(method, path, data=None, raw=None, headers=None):
    h = {"User-Agent": "envanter-pub"}
    body = None
    if raw is not None:
        body = raw; h.update(headers or {})
    elif data is not None:
        body = json.dumps(data).encode(); h["Content-Type"] = "application/json"
    for i in range(5):
        req = urllib.request.Request(B + path, data=body, method=method, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code < 500 and e.code != 429:
                raise RuntimeError(f"{method} {path} -> {e.code}: {e.read()[:300].decode(errors='replace')}")
        except Exception:
            pass
        time.sleep(2 ** (i + 1))
    raise RuntimeError(f"{method} {path}: yanıt alınamadı")


def grup(pid):
    try:
        return {l: v["id"] for l, v in call("GET", f"/ev/v1/post-translations?id={pid}").items()}
    except RuntimeError:
        return {}


def dil_bul(pid, url):
    for l, i in grup(pid).items():
        if i == pid:
            return l
    m = re.search(r"-(en|ar|es|ru|zh|tr)-kapak", url) or re.search(r"/cover-(en|ar|es|ru|zh)\.", url)
    return m.group(1) if m else "tr"


def fm(tip, pid):
    return call("GET", f"/wp/v2/{tip}/{pid}?context=edit&_fields=featured_media")["featured_media"]


BASE = {}      # bu sabahki taramadan post_id -> featured_media (beklenen eski değer)
YENI = {}      # bu betiğin verdiği kapaklar: post_id -> yeni medya
OLUSAN = set() # bu betiğin oluşturduğu medya kimlikleri


def bagla(grup_):
    if len(grup_) > 1:
        call("POST", "/ev/v1/link-post-translations", {"groups": [grup_]})


def isle(p, url, etkilenen):
    pid, tip = p["id"], REST.get(p["type"], p["type"])
    cur = call("GET", f"/wp/v2/{tip}/{pid}?context=edit&_fields=id,title,featured_media")
    if cur["featured_media"] != p["media"] and cur["featured_media"] not in OLUSAN:
        return f"atlandı (kapak zaten değişmiş: {cur['featured_media']})"
    title = cur["title"]["raw"].strip()
    g0 = grup(pid)
    lang = next((l for l, i in g0.items() if i == pid), None) or dil_bul(pid, url)
    png = OUT / f"{pid}-{lang}-kapak.png"
    make(str(png), "", title, "ENVANTER MEDYA", lang == "ar")
    if not UYGULA:
        return f"kuru: {lang} | {title[:70]}"
    kardes = {i: l for l, i in g0.items() if i != pid}
    once = {i: fm(tip, i) for i in kardes}
    m = call("POST", "/wp/v2/media", raw=png.read_bytes(), headers={
        "Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{png.name}"'})
    if Path(m["source_url"]).stem != png.stem:
        raise RuntimeError(f"yükleme beklenen adla kaydedilmedi: {m['source_url']}")
    n = m["id"]; OLUSAN.add(n)
    call("POST", f"/wp/v2/media/{n}", {"alt_text": title, "title": title})
    call("POST", "/ev/v1/set-post-lang", {"post_id": n, "lang": lang})
    # Medya çeviri grubu: Polylang kapak eşitlemesi her dilde doğru medyaya çevirsin
    mg = {lang: n}
    for i, l in kardes.items():
        if i in YENI:
            mg[l] = YENI[i]
        elif i in etkilenen:
            continue  # sırası gelince kendi kartını alacak
        elif once[i]:
            mg[l] = once[i]
    bagla(mg)
    call("POST", f"/wp/v2/{tip}/{pid}", {"featured_media": n})
    YENI[pid] = n
    notlar = []
    # Kayıt sırasında grup değişmiş olabilir (eklenti otomatik bağlıyor); kardeşleri denetle
    for l, i in grup(pid).items():
        if i == pid:
            continue
        bek = YENI.get(i, once.get(i, BASE.get(i)))
        simdi = fm(tip, i)
        if bek is None or simdi == bek:
            continue
        if i in etkilenen and i not in YENI:
            notlar.append(f"{i} sırada bekliyor")
            continue
        mg[l] = bek; bagla(mg)
        call("POST", f"/wp/v2/{tip}/{i}", {"featured_media": bek})
        notlar.append(f"{i} geri yazıldı {simdi}->{bek}")
    if fm(tip, pid) != n:
        call("POST", f"/wp/v2/{tip}/{pid}", {"featured_media": n})
        if fm(tip, pid) != n:
            raise RuntimeError("featured_media tutmuyor (Polylang eşitlemesi)")
    return f"tamam {lang} medya {n}" + (f" ({'; '.join(notlar)})" if notlar else "")


def main():
    s = json.load(open(args[0]))
    if os.environ.get("KAPAK_TABAN"):
        BASE.update({int(k): v for k, v in json.load(open(os.environ["KAPAK_TABAN"])).items()})
    etkilenen = {p["id"] for g in s["kart"] for p in g["posts"]}
    bitti = set()
    if LOG.exists():
        for ln in LOG.read_text().splitlines():
            pid, r = ln.split("\t", 1)
            if r.startswith("tamam"):
                bitti.add(int(pid))
                n = int(r.split("medya ")[1].split()[0])
                YENI[int(pid)] = n; OLUSAN.add(n)
            elif r.startswith("atlandı"):
                bitti.add(int(pid))
    n = 0
    with LOG.open("a") as log:
        for g in s["kart"]:
            for p in g["posts"]:
                if p["id"] in bitti:
                    continue
                if SINIR is not None and n >= SINIR:
                    return
                n += 1
                try:
                    r = isle(p, g["url"], etkilenen)
                except Exception as e:
                    r = f"HATA {e}"
                ln = f"{p['id']}\t{r}"
                print(ln, flush=True)
                if UYGULA:
                    log.write(ln + "\n"); log.flush()


if __name__ == "__main__":
    main()
