#!/usr/bin/env python3
"""Python referans motoru ile eklentideki PHP motorunun aynı sonucu verdiğini doğrular.
Kullanım: parite_testi.py <veri_klasoru> [ornek_sayisi]   (veri: cek.py + sadele.py çıktısı)"""
import json, os, random, subprocess, sys, tempfile
KOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, f"{KOK}/motor")
from eslestir import Motor

D = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
random.seed(42)
posts = []
for site in ("ev", "dm", "da"):
    P = json.load(open(f"{D}/{site}_lite.json"))
    posts += random.sample(P, min(len(P), N // 3))
# elle zor örnekler
posts += [dict(site="x", id=i, title=t, excerpt="", body=b) for i, (t, b) in enumerate([
    ("Kaan Onuk MKE'yi ziyaret etti", "Kaan Onuk, MKE tesislerinde. MKE yeni tüfek. MKE."),
    ("مقاتلة KAAN تحلق", "أعلنت توساش أن مقاتلة KAAN أكملت. وKAAN ستدخل. لـKAAN محرك."),
    ("Eurofighter Typhoon ve TAYFUN", "Eurofighter Typhoon, Tayfun değil. TAYFUN balistik füzesi ROKETSAN tarafından."),
    ("Boş gövde ASELSAN", ""),
    ("ALTAY tankı", "BMC ALTAY tankı üretimi. Altay Dağları değil. ALTAY tankı."),
])]
tmp = tempfile.mkdtemp()
json.dump(posts, open(f"{tmp}/in.json", "w"), ensure_ascii=False)
subprocess.run(["php", f"{KOK}/tests/parite_matcher.php", f"{KOK}/sozluk/varliklar.json", f"{tmp}/in.json", f"{tmp}/out.json"], check=True)
php = json.load(open(f"{tmp}/out.json"))
m = Motor(f"{KOK}/sozluk/varliklar.json")
fark = 0
for p in posts:
    g, z = m.oner(p["title"], p["excerpt"], p["body"])
    py = dict(g=[[o["id"], o["guven"], o["kaynak"], o["T"], o["L"], o["B"]] for o in g], z=[o["id"] for o in z])
    ph = php[f"{p['site']}:{p['id']}"]
    if py != ph:
        fark += 1
        if fark <= 5:
            print("FARK", p["site"], p["id"], p["title"][:80], "\n  py ", py, "\n  php", ph)
print(f"{len(posts)} yazı, {fark} fark")
sys.exit(1 if fark else 0)
