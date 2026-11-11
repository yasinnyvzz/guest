#!/usr/bin/env python3
"""Envanter Medya varlık eşleştirme motoru (Python referans uygulaması).

WordPress eklentisindeki PHP motoru (eklenti/envanter-konu-arsivleri/includes/class-matcher.php)
aynı kuralları uygular; tests/parite_testi.py ikisinin aynı sonucu verdiğini doğrular.

Kurallar (özet):
  * Başlıkta geçen varlık güçlüdür; gövdede tek geçen varlık "anılma" sayılır ve önerilmez.
  * cs=true takma adlar özgün metinde harf duyarlı aranır (KAAN ≠ Kaan Onuk).
  * amb=true takma adlar yalnız yazıda bağlam deseni (ctx) varsa sayılır.
  * neg desenleri eşleşmenin ±60 karakter çevresinde varsa o eşleşme düşer.
  * Ürün → üretici şirket ve ürün → üst konu ilişkileri çıkarımla eklenir (bir kademe düşük güvenle).
  * En fazla 7 öneri; liste tipi yazılarda (çok sayıda şirket) yalnız başlıkta geçen şirketler kalır.
"""
import json
import re
import unicodedata

LATIN = str.maketrans({
    "İ": "i", "I": "i", "ı": "i", "Ş": "s", "ş": "s", "Ğ": "g", "ğ": "g", "Ü": "u", "ü": "u", "Ö": "o", "ö": "o",
    "Ç": "c", "ç": "c", "Â": "a", "â": "a", "Î": "i", "î": "i", "Û": "u", "û": "u", "É": "e", "é": "e", "È": "e",
    "è": "e", "Ê": "e", "ê": "e", "Á": "a", "á": "a", "À": "a", "à": "a", "Ó": "o", "ó": "o", "Í": "i", "í": "i",
    "Ñ": "n", "ñ": "n", "Ã": "a", "ã": "a", "Õ": "o", "õ": "o", "Ô": "o", "ô": "o", "Ë": "e", "ë": "e", "Ï": "i",
    "ï": "i", "’": "'", "‘": "'", "`": "'",
    "أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ة": "ه", "ؤ": "و", "ئ": "ي",
})
AR_STRIP = re.compile("[\u064B-\u065F\u0670\u0640]")  # harekeler + tatvil
WORD = "a-z0-9\u0621-\u064a"
LATIN_ORJ = "A-Za-z0-9ÇĞİÖŞÜÂÎÛçğıöşüâîû"
AR_PROCLITIC = "(?:وال|بال|فال|كال|لل|ال|و|ف|ب|ل|ك)?"
WINDOW = 60
WS = re.compile("[ \t\n\r\f\v\u00a0\u2000-\u200b\u202f\u3000]+")
MAX_ONERI = 7


def fold(s):
    s = AR_STRIP.sub("", s or "")
    s = s.translate(LATIN).lower()
    return s


def ws(s):
    return WS.sub(" ", s or "")


def is_arabic(s):
    return any("؀" <= c <= "ۿ" for c in s)


class Varlik:
    def __init__(self, d):
        self.d = d
        self.id = d["id"]
        self.tip = d["tip"]
        self.ctx = [re.compile(p) for p in d.get("ctx", [])]
        self.neg = [re.compile(p) for p in d.get("neg", [])]
        self.desenler = []  # (regex, cs, amb)
        for a in d["alias"]:
            t, cs, amb, suf = a["t"], a.get("cs", False), a.get("amb", False), a.get("suf", False)
            if cs:
                core = re.escape(t).replace(r"\ ", r"[\s\-]+")
                rx = re.compile(r"(?<![" + LATIN_ORJ + r"])" + core + (r"" if suf else r"(?![" + LATIN_ORJ + r"])"))
            else:
                ft = fold(t)
                core = re.escape(ft).replace(r"\ ", r"[\s\-]+")
                if is_arabic(ft):
                    rx = re.compile(r"(?<![" + WORD + r"])" + AR_PROCLITIC + core + (r"" if suf else r"(?![" + WORD + r"])"))
                else:
                    rx = re.compile(r"(?<![a-z0-9])" + core + (r"" if suf else r"(?![a-z0-9])"))
            self.desenler.append((rx, cs, amb))

    def say(self, orj, kat, ctx_var):
        """orj: özgün metin, kat: katlanmış metin. Geçerli eşleşme sayısını döndürür."""
        n = 0
        for rx, cs, amb in self.desenler:
            if amb and not ctx_var:
                continue
            hedef = orj if cs else kat
            for m in rx.finditer(hedef):
                if self.neg:
                    pencere = (fold(orj[max(0, m.start() - WINDOW): m.end() + WINDOW]) if cs
                               else kat[max(0, m.start() - WINDOW): m.end() + WINDOW])
                    if any(ng.search(pencere) for ng in self.neg):
                        continue
                n += 1
        return n


class Motor:
    def __init__(self, sozluk_yolu):
        d = json.load(open(sozluk_yolu, encoding="utf-8"))
        self.tipler = d["tipler"]
        self.v = {x["id"]: Varlik(x) for x in d["varliklar"]}

    def puanla(self, baslik, ozet, govde):
        baslik, ozet, govde = ws(baslik), ws(ozet), ws(govde)
        lead_orj = (ozet + " " + govde[:400]).strip(" ")
        doc_orj = baslik + " " + govde
        k_b, k_l, k_d = fold(baslik), fold(lead_orj), fold(doc_orj)
        sonuc = {}
        for v in self.v.values():
            ctx_var = (not v.ctx) or any(c.search(k_d) for c in v.ctx)
            t = v.say(baslik, k_b, ctx_var)
            gov = v.say(govde, fold(govde), ctx_var)
            if t == 0 and gov == 0:
                continue
            l = v.say(lead_orj, k_l, ctx_var)
            sonuc[v.id] = dict(T=t, L=l, B=gov)
        return sonuc

    @staticmethod
    def guven(h, tip, baskin=False, govde_bos=False):
        """yuksek: başlıkta geçer (ya da şirket/ürün olarak giriş + gövdede baskın);
        orta: editör onayı; dusuk: önerilmez; None: tek anılma."""
        T, L, B = h["T"], h["L"], h["B"]
        if T >= 1 and (B >= 1 or govde_bos):
            return "yuksek"
        if tip == "sirket" and baskin and L >= 1 and B >= 4:
            return "yuksek"
        if T >= 1:
            return "orta"
        if tip == "ulke":
            return "orta" if (L >= 1 and B >= 6 and baskin) else ("dusuk" if B >= 2 else None)
        if (L >= 1 and B >= 2) or B >= 5:
            return "orta"
        if B >= 2:
            return "dusuk"
        return None  # tek anılma: önerilmez

    def oner(self, baslik, ozet, govde, haric=()):
        hits = self.puanla(baslik, ozet, govde)
        g = {}
        enust = {}
        for vid, h in hits.items():
            t = self.v[vid].tip
            if h["B"] > enust.get(t, (0, None))[0]:
                enust[t] = (h["B"], vid)
        for vid, h in hits.items():
            t = self.v[vid].tip
            c = self.guven(h, t, baskin=(enust.get(t, (0, None))[1] == vid), govde_bos=not ws(govde).strip(" "))
            if c:
                g[vid] = dict(guven=c, kaynak="dogrudan", **h)
        # liste tipi yazı: çok sayıda şirket orta+ ise yalnız başlıktakiler ve en güçlü ikisi kalır
        sirketler = [k for k, x in g.items() if self.v[k].tip == "sirket" and x["guven"] != "dusuk"]
        if len(sirketler) > 4:
            sirali = sorted(sirketler, key=lambda k: (-g[k]["T"], -g[k]["B"]))
            koru = set(sirali[:2]) | {k for k in sirketler if g[k]["T"] >= 1}
            for k in sirketler:
                if k not in koru:
                    g[k]["guven"] = "dusuk"
                    g[k]["not"] = "liste_yazisi"
        # çıkarım: ürün → üretici, her şey → üst konu
        sira = {"yuksek": 3, "orta": 2, "dusuk": 1}
        ters = {3: "yuksek", 2: "orta", 1: "dusuk"}

        def ekle(hid, seviye, neden):
            if hid not in self.v or seviye < 1:
                return
            mevcut = g.get(hid)
            if mevcut and sira[mevcut["guven"]] >= seviye:
                return
            g[hid] = dict(guven=ters[seviye], kaynak="cikarim:" + neden, T=0, L=0, B=0) if not mevcut else \
                {**mevcut, "guven": ters[seviye], "kaynak": mevcut["kaynak"] + "+cikarim:" + neden}

        # üretici yükseltmesi: yüksek güvenli ürünün üreticisi yazıda doğrudan anılıyorsa yüksek olur
        for k, x in list(g.items()):
            if x["guven"] == "yuksek" and x["kaynak"] == "dogrudan":
                for y in self.v[k].d.get("yapan", []):
                    hy = hits.get(y)
                    if hy and (hy["T"] + hy["B"]) >= 1 and y in self.v:
                        onceki = g.get(y)
                        if not onceki or onceki["guven"] != "yuksek":
                            g[y] = dict(guven="yuksek", kaynak="dogrudan+uretici:" + k, **hy)
        for _ in range(3):  # üç kademe (ürün → tür → ana konu)
            for k, x in list(g.items()):
                s = sira[x["guven"]]
                if s < 2:
                    continue
                d = self.v[k].d
                for y in d.get("yapan", []):
                    ekle(y, s - 1 if s == 3 else 1, k)
                # başlıkta geçmeyen doğrudan varlıktan yapılan çıkarım en fazla "orta" olur
                tavan = 2 if (x["kaynak"].startswith("dogrudan") and x["T"] == 0) else 3
                for u in d.get("ust", []):
                    ekle(u, min(tavan, s if self.v[k].tip in ("teknoloji", "kategori") else s - (0 if s == 3 else 1)), k)
        oneriler = [dict(id=k, **x) for k, x in g.items() if k not in haric]
        oncelik = {t: self.tipler[t]["oncelik"] for t in self.tipler}
        oneriler.sort(key=lambda o: (-sira[o["guven"]], oncelik[self.v[o["id"]].tip], -o["T"], -o["B"]))
        guclu = [o for o in oneriler if o["guven"] != "dusuk"][:MAX_ONERI]
        zayif = [o for o in oneriler if o["guven"] == "dusuk"]
        return guclu, zayif


if __name__ == "__main__":
    import sys
    m = Motor(sys.argv[1])
    g, z = m.oner(sys.argv[2], "", sys.argv[3] if len(sys.argv) > 3 else "")
    for o in g:
        print(o)
    print("zayıf:", [o["id"] for o in z])
