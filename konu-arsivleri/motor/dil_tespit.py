"""Metnin yazı dilini kaba olarak tespit eder (Polylang dili atanmamış yazıları yakalamak için)."""
import re
SW = {
    "tr": set("ve bir bu ile için olarak da de olan ise daha en çok gibi ancak sonra kadar ayrıca yeni tarafından".split()),
    "en": set("the and of to in is for that with on as by was from are its this which has be".split()),
    "es": set("el la de que y en los las del por con para una es su al se como más".split()),
}


def tespit(metin):
    s = metin[:3000]
    if not s.strip():
        return None
    n = len(s)
    if len(re.findall(r"[؀-ۿ]", s)) / n > 0.25:
        return "ar"
    if len(re.findall(r"[Ѐ-ӿ]", s)) / n > 0.25:
        return "ru"
    if len(re.findall(r"[一-鿿]", s)) / n > 0.15:
        return "zh"
    w = re.findall(r"[a-zçğıöşüñáéíóú]+", s.lower())
    sc = {k: sum(1 for x in w if x in v) for k, v in SW.items()}
    sc["tr"] += 3 * len(re.findall(r"[ğış]", s.lower()))
    return max(sc, key=sc.get)
