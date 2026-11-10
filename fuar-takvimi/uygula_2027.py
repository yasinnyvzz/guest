#!/usr/bin/env python3
"""SSB 2027 fuar listesine göre Envanter Medya fuar kayıtlarını düzeltir ve eksik fuarları ekler.

Kimlik bilgisi gerekmez (proxy ekler). Adımlar:
  duzelt  : mevcut fuarların tarih/başlık/metin/kapak düzeltmeleri
  ekle    : eksik 2027 fuarlarını 6 dilde ekler
Kullanım: python3 uygula_2027.py duzelt|ekle KAPAK_KLASORU
"""
import json
import subprocess
import sys
import time

API = "https://envantermedya.com/wp-json"
KAYIT = {}


def req(method, path, body=None, data_file=None, headers=()):
    cmd = ["curl", "-sS", "-X", method, API + path]
    for h in headers:
        cmd += ["-H", h]
    if body is not None:
        cmd += ["-H", "Content-Type: application/json", "--data-binary", json.dumps(body, ensure_ascii=False)]
    if data_file:
        cmd += ["--data-binary", "@" + data_file]
    out = subprocess.check_output(cmd)
    try:
        return json.loads(out)
    except ValueError:
        raise SystemExit(f"{method} {path}: JSON değil: {out[:300]!r}")


def get_post(i):
    return req("GET", f"/wp/v2/fuar/{i}?context=edit&_fields=id,title,content,excerpt,slug,featured_media,status")


def update_post(i, **f):
    r = req("POST", f"/wp/v2/fuar/{i}", f)
    if "id" not in r:
        raise SystemExit(f"güncelleme hatası {i}: {r}")
    return r


def meta(i, **m):
    r = req("POST", "/em/v1/fuar-guncelle", dict(id=i, **m))
    if not r.get("ok"):
        raise SystemExit(f"meta hatası {i}: {r}")
    return r["guncellenen"]


def upload(png, slug, alt):
    from PIL import Image
    webp = png.rsplit(".", 1)[0] + ".webp"
    Image.open(png).convert("RGB").save(webp, "WEBP", quality=86)
    r = req("POST", "/wp/v2/media", data_file=webp,
            headers=["Content-Type: image/webp", f'Content-Disposition: attachment; filename="{slug}.webp"'])
    if "id" not in r:
        raise SystemExit(f"medya hatası: {r}")
    req("POST", f"/wp/v2/media/{r['id']}", {"alt_text": alt, "title": alt})
    return r["id"]


def grup(tr):
    return req("GET", f"/em/v1/fuar-ceviriler/{tr}")


def degistir(metin, ciftler, kimlik):
    for eski, yeni in ciftler:
        n = metin.count(eski)
        if n != 1:
            raise SystemExit(f"{kimlik}: '{eski[:60]}' {n} kez geçiyor (1 bekleniyordu)")
        metin = metin.replace(eski, yeni)
    return metin


# ---------------------------------------------------------------- düzeltmeler
TR_METIN = {
    18834: [("21-25 Şubat 2027 tarihlerinde", "25-29 Ocak 2027 tarihlerinde")],
    18829: [
        ("<strong>Indo Defence 2026</strong>, 11-14 Kasım 2026 tarihlerinde Cakarta JIExpo Kemayoran'da düzenlenecek olan,",
         "<strong>Indo Defence 2027</strong>, Kasım 2026'dan ertelenerek 12-15 Mayıs 2027 tarihlerinde Cakarta yakınındaki Tangerang'da, NICE PIK 2 fuar merkezinde düzenlenecek olan,"),
        ("2026 için <strong>900+", "2027 için <strong>900+"),
        ("2026 için beklenen Türk katılım", "2027 için beklenen Türk katılım"),
    ],
    18839: [("25-29 Mayıs 2027 tarihlerinde", "20-24 Nisan 2027 tarihlerinde")],
    18842: [
        ("16. kez 27-30 Temmuz 2027 tarihlerinde", "16. kez 3-9 Mayıs 2027 tarihlerinde"),
        ("Fuar 27 Temmuz 2027 Salı sabah 09:30'da Cumhurbaşkanı açılışı ile başlayacak; 30 Temmuz Cuma akşam 18:00'de kapanacak.",
         "Fuar 3 Mayıs 2027 Pazartesi günü açılacak, 9 Mayıs 2027 Pazar günü sona erecek."),
        (" ve son tarih 30 Mayıs 2027'dir.", "; son başvuru tarihi fuar öncesinde resmi sitede duyurulacak."),
        ("Akreditasyon kapanışı 30 Mayıs 2027", "Son başvuru tarihi resmi sitede duyurulacak"),
    ],
    18843: [("1-4 Eylül 2027 tarihlerinde", "31 Ağustos-3 Eylül 2027 tarihlerinde")],
    18844: [("14-17 Eylül 2027 tarihlerinde", "7-10 Eylül 2027 tarihlerinde")],
    18831: [
        ("<strong>EDEX 2026 (Egypt Defence Expo)</strong>, 1-4 Aralık 2026 tarihlerinde",
         "<strong>EDEX 2027 (Egypt Defence Expo)</strong>, 6-9 Aralık 2027 tarihlerinde"),
        ("2026 edisyonunda", "2027 edisyonunda"),
        ("İki yılda bir düzenleniyor; 2018, 2021, 2023, 2026 edisyonları gerçekleşti.",
         "İki yılda bir düzenleniyor; önceki edisyonların verileri aşağıdaki tabloda yer alıyor."),
        ("2026 için <strong>30+", "2027 için <strong>30+"),
        ("EDEX 2026'da beklenen", "EDEX 2027'de beklenen"),
        ("<li>Ekim 2026'da kapanıyor</li>", "<li>Son başvuru tarihi resmi sitede duyurulacak</li>"),
    ],
}
TARIH = {18834: ("2027-01-25", "2027-01-29"), 18829: ("2027-05-12", "2027-05-15")}
BASLIK = {18829: ("Indo Defence 2026", "Indo Defence 2027"), 18831: ("EDEX 2026", "EDEX 2027")}
KAPAK = {  # tr_id: (dosya, slug, alt)
    18834: ("18834.png", "fuar-idex-navdex-2027-kapak-ocak", "IDEX & NAVDEX 2027 - Abu Dabi, BAE, 25-29 Ocak 2027"),
    18829: ("18829.png", "fuar-indo-defence-2027-kapak", "Indo Defence 2027 - Cakarta, Endonezya, 12-15 Mayıs 2027"),
    18839: ("18839.png", "fuar-lima-2027-kapak-nisan", "LIMA 2027 - Langkawi, Malezya, 20-24 Nisan 2027"),
    18842: ("18842.png", "fuar-idef-2027-kapak-mayis", "IDEF 2027 - İstanbul, Türkiye, 3-9 Mayıs 2027"),
    18831: ("18831.png", "fuar-edex-2027-kapak", "EDEX 2027 - Kahire, Mısır, 6-9 Aralık 2027"),
}


def duzelt(kapak_dir):
    for tr, ciftler in TR_METIN.items():
        g = grup(tr)
        p = get_post(tr)
        yeni = degistir(p["content"]["raw"], ciftler, tr)
        f = {"content": yeni}
        if tr in BASLIK:
            f["title"] = p["title"]["raw"].replace(*BASLIK[tr])
        update_post(tr, **f)
        KAYIT.setdefault("duzelt", {})[tr] = {"metin": len(ciftler)}
        # çeviriler: başlık / kısa metin / özet
        if tr in BASLIK:
            eski, yeni_b = BASLIK[tr]
            for l, i in g.items():
                if l == "tr":
                    continue
                q = get_post(i)
                upd = {}
                for k in ("title", "content", "excerpt"):
                    if eski in q[k]["raw"]:
                        upd[k] = q[k]["raw"].replace(eski, yeni_b)
                if upd:
                    update_post(i, **upd)
                    KAYIT["duzelt"].setdefault(f"{tr}-ceviri", []).append(i)
        if tr in TARIH:
            for l, i in g.items():
                meta(i, fuar_baslangic=TARIH[tr][0], fuar_bitis=TARIH[tr][1])
            KAYIT["duzelt"][tr]["tarih"] = TARIH[tr]
        if tr in KAPAK:
            dosya, slug, alt = KAPAK[tr]
            mid = upload(f"{kapak_dir}/{dosya}", slug, alt)
            for l, i in g.items():
                update_post(i, featured_media=mid)
            KAYIT["duzelt"][tr]["kapak"] = mid
        print("düzeltildi", tr)


# ---------------------------------------------------------------- yeni fuarlar
AY = {
    "en": ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "ar": ["", "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"],
    "es": ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    "ru": ["", "января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"],
    "tr": ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"],
}


def tarih_metni(lang, b, e):
    y, m, d1 = (int(x) for x in b.split("-"))
    d2 = int(e.split("-")[2])
    if lang == "zh":
        return f"{y}年{m}月{d1}日至{d2}日"
    if lang == "es":
        return f"del {d1} al {d2} de {AY['es'][m]} de {y}"
    if lang == "ru":
        return f"{d1}-{d2} {AY['ru'][m]} {y} года"
    return f"{d1}-{d2} {AY[lang][m]} {y}"


YENI = [
    dict(
        slug="iqdex-2027", baslik="IQDEX 2027", kapak="iqdex.png",
        b="2027-04-17", e="2027-04-20", sehir="Bağdat", ulke="Irak", lat="33.3075", lng="44.3610", web="https://iqdex.iq/",
        yer={"en": ("Baghdad", "Iraq"), "ar": ("بغداد", "العراق"), "es": ("Bagdad", "Irak"), "ru": ("Багдад", "Ирак"), "zh": ("巴格达", "伊拉克")},
        ozet="Irak'ın uluslararası savunma ve güvenlik fuarı; 17-20 Nisan 2027, Bağdat.",
        en_ac="the International Defense Exhibition in Iraq, brings together land, air, naval and homeland security systems for Iraq's armed forces and security agencies.",
        tr=(
            "<p><strong>IQDEX 2027 (Iraq International Defense Exhibition)</strong>, 17-20 Nisan 2027 tarihlerinde Irak'ın başkenti "
            "Bağdat'ta, Bağdat Uluslararası Fuar Alanı'nda düzenlenecek savunma ve güvenlik fuarıdır. Kara, hava ve deniz sistemleriyle "
            "iç güvenlik teknolojilerini bir araya getiren fuar, Irak silahlı kuvvetleri ve güvenlik birimlerinin tedarik ihtiyaçlarına "
            "yönelik görüşmelerin yapıldığı başlıca platformlardan biridir.</p>\n\n"
            "<p>Organizatör, 2027 edisyonunun salon planlarını resmi sitesinde yayımladı. Katılımcı listesi ve konferans programı "
            "açıklandıkça bu sayfa güncellenecek.</p>"
        ),
    ),
    dict(
        slug="asda-2027", baslik="ASDA 2027", kapak="asda.png",
        b="2027-04-27", e="2027-04-29", sehir="Zagreb", ulke="Hırvatistan", lat="45.7713", lng="15.9356", web="",
        yer={"en": ("Zagreb", "Croatia"), "ar": ("زغرب", "كرواتيا"), "es": ("Zagreb", "Croacia"), "ru": ("Загреб", "Хорватия"), "zh": ("萨格勒布", "克罗地亚")},
        ozet="Adriyatik'in savunma, havacılık ve güvenlik fuarı; 27-29 Nisan 2027, Zagreb.",
        en_ac="Adriatic Sea Defense & Aerospace, is a biennial tri-service defence, aerospace and security exhibition.",
        tr=(
            "<p><strong>ASDA 2027 (Adriatic Sea Defense &amp; Aerospace)</strong>, 27-29 Nisan 2027 tarihlerinde Hırvatistan'ın başkenti "
            "Zagreb'de, Arena Zagreb'de düzenlenecek savunma, havacılık ve güvenlik fuarıdır. İki yılda bir yapılan ASDA, kara, hava ve "
            "deniz kuvvetlerine yönelik sistemleri tek çatı altında toplayan bir fuar olarak Adriyatik ve Güneydoğu Avrupa pazarına "
            "odaklanıyor. Fuarın 2025 edisyonu da Zagreb'de yapılmıştı.</p>\n\n"
            "<p>Fuar, savunma, iç güvenlik ve havacılık alanlarındaki kamu ve sanayi temsilcilerine yönelik profesyonel bir etkinlik "
            "olarak düzenleniyor. Katılımcı listesi ve program açıklandıkça bu sayfa güncellenecek.</p>"
        ),
    ),
    dict(
        slug="idet-2027", baslik="IDET 2027", kapak="idet.png",
        b="2027-05-26", e="2027-05-28", sehir="Brno", ulke="Cekya", lat="49.1866", lng="16.5817", web="https://www.bvv.cz/en/idet",
        yer={"en": ("Brno", "Czechia"), "ar": ("برنو", "التشيك"), "es": ("Brno", "Chequia"), "ru": ("Брно", "Чехия"), "zh": ("布尔诺", "捷克")},
        ozet="Orta Avrupa'nın savunma ve güvenlik teknolojileri fuarı; 26-28 Mayıs 2027, Brno.",
        en_ac="the International Fair of Defence and Security Technologies, is a biennial show at the Brno Exhibition Centre, held alongside ISET and PYROS.",
        tr=(
            "<p><strong>IDET 2027 (International Defence and Security Technologies Fair)</strong>, 26-28 Mayıs 2027 tarihlerinde "
            "Çekya'nın Brno kentindeki Brno Fuar Merkezi'nde düzenlenecek savunma ve güvenlik teknolojileri fuarıdır. BVV Trade Fairs "
            "Brno organizasyonunda iki yılda bir yapılan IDET, Orta Avrupa'nın başlıca savunma fuarlarından biridir.</p>\n\n"
            "<p>Fuarla eş zamanlı olarak güvenlik teknolojileri fuarı ISET ve yangınla mücadele fuarı PYROS da düzenleniyor. "
            "Organizatörün 2027 tanıtım broşürüne göre IDET 650'yi aşkın katılımcı ve 35.000'i aşkın ziyaretçiyi bir araya getiriyor; "
            "ürün lansmanları, canlı gösterimler ve resmî heyet görüşmeleri üç güne sığdırılıyor.</p>"
        ),
    ),
    dict(
        slug="sidif-2027", baslik="SIDIF 2027", kapak="sidif.png",
        b="2027-11-06", e="2027-11-09", sehir="Şam", ulke="Suriye", lat="33.5138", lng="36.2765", web="",
        yer={"en": ("Damascus", "Syria"), "ar": ("دمشق", "سوريا"), "es": ("Damasco", "Siria"), "ru": ("Дамаск", "Сирия"), "zh": ("大马士革", "叙利亚")},
        ozet="Suriye'nin uluslararası savunma sanayii fuarı; 6-9 Kasım 2027, Şam.",
        en_ac="the Syria International Defense Industry Fair, is an international defence industry exhibition in Damascus.",
        tr=(
            "<p><strong>SIDIF 2027 (Syria International Defense Industry Fair)</strong>, 6-9 Kasım 2027 tarihlerinde Suriye'nin "
            "başkenti Şam'da düzenlenmesi planlanan uluslararası savunma sanayii fuarıdır.</p>\n\n"
            "<p>Fuarın düzenleneceği mekân, katılımcı listesi ve program ayrıntıları organizatör tarafından açıklandıkça bu sayfa "
            "güncellenecek. Envanter Medya, fuar yaklaştıkça öne çıkan gelişmeleri ve Türk savunma sanayii katılımını burada "
            "derleyecek.</p>"
        ),
    ),
    dict(
        slug="dsei-germany-2027", baslik="DSEI Germany 2027", kapak="dsei-germany.png",
        b="2027-03-09", e="2027-03-12", sehir="Hannover", ulke="Almanya", lat="52.3226", lng="9.8037", web="https://www.dsei-germany.com/",
        yer={"en": ("Hanover", "Germany"), "ar": ("هانوفر", "ألمانيا"), "es": ("Hannover", "Alemania"), "ru": ("Ганновер", "Германия"), "zh": ("汉诺威", "德国")},
        ozet="DSEI'nin Almanya edisyonu ilk kez Hannover'de; 9-12 Mart 2027.",
        en_ac="the German edition of DSEI, debuts at the Hanover Exhibition Grounds, organised by Clarion Events with Deutsche Messe AG.",
        tr=(
            "<p><strong>DSEI Germany 2027</strong>, 9-12 Mart 2027 tarihlerinde Almanya'nın Hannover kentindeki Hannover Fuar "
            "Alanı'nda (Messegelände Hannover) ilk kez düzenlenecek savunma ve güvenlik fuarıdır. Londra'daki DSEI'nin organizatörü "
            "Clarion Events, fuarı Deutsche Messe AG ile birlikte düzenliyor.</p>\n\n"
            "<p>Organizatörler, yoğun talep nedeniyle fuara dördüncü bir salon eklediklerini ve kapalı sergi alanının 100.000 "
            "metrekareye ulaşacağını açıkladı. Fuarın genel müdürlüğünü 1 Ekim 2025'ten bu yana emekli Albay Bernd Kögel yürütüyor. "
            "DSEI Germany, 1-3 Mart 2027'de Nürnberg'de yapılacak Enforce Tac'ın hemen ardından gerçekleşecek.</p>"
        ),
    ),
    dict(
        slug="dsei-japan-2027", baslik="DSEI Japan 2027", kapak="dsei-japan.png",
        b="2027-04-28", e="2027-04-30", sehir="Chiba", ulke="Japonya", lat="35.6481", lng="140.0346", web="https://www.dsei-japan.com/",
        yer={"en": ("Chiba", "Japan"), "ar": ("تشيبا", "اليابان"), "es": ("Chiba", "Japón"), "ru": ("Тиба", "Япония"), "zh": ("千叶", "日本")},
        ozet="Japonya'nın savunma ve güvenlik fuarı; 28-30 Nisan 2027, Makuhari Messe.",
        en_ac="Japan's integrated defence and security exhibition, is held at Makuhari Messe and organised by Clarion Defence & Security.",
        tr=(
            "<p><strong>DSEI Japan 2027</strong>, 28-30 Nisan 2027 tarihlerinde Japonya'nın Chiba kentindeki Makuhari Messe'de "
            "düzenlenecek savunma ve güvenlik fuarıdır. Clarion Defence &amp; Security organizasyonunda yapılan fuar, kara, hava ve "
            "deniz alanlarını tek etkinlikte buluşturuyor ve Japon savunma sanayii ile uluslararası firmalar arasında iş birliği "
            "görüşmelerine sahne oluyor.</p>\n\n"
            "<p>Katılımcı listesi ve konferans programı açıklandıkça bu sayfa güncellenecek.</p>"
        ),
    ),
]


def tr_icerik(f):
    tarih = tarih_metni("tr", f["b"], f["e"])
    satirlar = [f"<li><strong>Tarih:</strong> {tarih}</li>", f"<li><strong>Yer:</strong> {f['sehir']}, {'Çekya' if f['ulke'] == 'Cekya' else f['ulke']}</li>"]
    if f["web"]:
        satirlar.append(f'<li><strong>Resmi site:</strong> <a href="{f["web"]}" target="_blank" rel="noopener">{f["web"].split("//")[1].rstrip("/")}</a></li>')
    return (f["tr"] + "\n\n<h2>Fuar Bilgileri</h2>\n<ul>\n" + "\n".join(satirlar) + "\n</ul>\n\n"
            f"<p>{f['baslik']} için takvim kaydı, harita ve diğer savunma fuarları <a href=\"https://envantermedya.com/fuar-takvimi/\">"
            "Envanter Medya Fuar Takvimi</a> sayfasında.</p>")


def ceviri_icerik(f, lang):
    t = f["baslik"]
    city, country = f["yer"][lang]
    d = tarih_metni(lang, f["b"], f["e"])
    if lang == "en":
        return f"{t}, {f['en_ac']} It takes place on {d} in {city}, {country}."
    if lang == "ar":
        return f"{t} - معرض دولي للصناعات الدفاعية يقام في {city}، {country} خلال الفترة {d}."
    if lang == "es":
        return f"{t} - Exposición internacional de la industria de defensa, {d} en {city} ({country})."
    if lang == "ru":
        return f"{t} - Международная выставка оборонной промышленности: {d}, {city} ({country})."
    return f"{t} - 国际防务工业展览会，{d}在{country}{city}举行。"


def ekle(kapak_dir):
    for f in YENI:
        metas = dict(fuar_baslangic=f["b"], fuar_bitis=f["e"], fuar_sehir=f["sehir"], fuar_ulke=f["ulke"],
                     fuar_lat=f["lat"], fuar_lng=f["lng"], fuar_web=f["web"])
        var = req("GET", f"/wp/v2/fuar?slug={f['slug']}&status=publish,draft,future&_fields=id,status,featured_media")
        if var and var[0]["status"] == "publish":
            print("zaten yayında, atlandı:", f["slug"], var)
            continue
        if var:  # yarım kalmış kayıt: taslaktan devam
            tr, mid = var[0]["id"], var[0]["featured_media"]
        else:
            mid = upload(f"{kapak_dir}/{f['kapak']}", f"fuar-{f['slug']}-kapak",
                         f"{f['baslik']} - {f['sehir']}, {'Çekya' if f['ulke'] == 'Cekya' else f['ulke']} savunma fuarı kapak görseli")
            p = req("POST", "/wp/v2/fuar", {"title": f["baslik"], "slug": f["slug"], "status": "draft",
                                             "content": tr_icerik(f), "excerpt": f["ozet"], "featured_media": mid})
            tr = p["id"]
        meta(tr, **metas)
        kayit = {"tr": tr, "kapak": mid}
        g = grup(tr)
        for lang in ("en", "ar", "es", "ru", "zh"):
            metin = ceviri_icerik(f, lang)
            alanlar = dict(title=f["baslik"], slug=f"{f['slug']}-{lang}", content=f"<p>{metin}</p>",
                           excerpt=metin, featured_media=mid)
            if lang in g:
                i = g[lang]
            else:
                r = req("POST", "/em/v1/fuar-cevir", {"kaynak_id": tr, "dil": lang})
                if r.get("ok"):
                    i = r["id"]
                elif r.get("error") == "Gecersiz dil":
                    # fuar-cevir bu dili desteklemiyor: elle oluştur, dil ata, gruba bağla
                    i = req("POST", "/wp/v2/fuar", dict(alanlar, status="draft"))["id"]
                    req("POST", "/ev/v1/set-post-lang", {"post_id": i, "lang": lang})
                    meta(i, **metas)
                else:
                    raise SystemExit(f"çeviri hatası {f['slug']} {lang}: {r}")
                g[lang] = i
                req("POST", "/ev/v1/link-post-translations", {"groups": [g]})
            update_post(i, status="publish", **alanlar)
            kayit[lang] = i
        update_post(tr, status="publish")
        kontrol = grup(tr)
        if sorted(kontrol) != sorted(["tr", "en", "ar", "es", "ru", "zh"]):
            raise SystemExit(f"çeviri grubu eksik {f['slug']}: {kontrol}")
        KAYIT.setdefault("ekle", {})[f["slug"]] = kayit
        print("eklendi", f["slug"], kayit)
        time.sleep(1)


if __name__ == "__main__":
    adim, kapak_dir = sys.argv[1], sys.argv[2]
    try:
        {"duzelt": duzelt, "ekle": ekle}[adim](kapak_dir)
    finally:
        with open(f"uygulama_kaydi_{adim}.json", "w", encoding="utf8") as fh:
            json.dump(KAYIT, fh, ensure_ascii=False, indent=1)
