#!/usr/bin/env python3
"""Salt okuma: üç sitenin terimlerini ve yazılarını REST ile indirir (yazma yok).
Kullanım: cek.py <cikti_klasoru> [terms|posts|all]
Kimlik: envantermedya.com için oturum vekili kimliği ekler; diğerleri herkese açık uç noktalar."""
import json, os, sys, concurrent.futures as cf, requests, time

SITES = {"ev": "https://envantermedya.com/wp-json", "dm": "https://defencemena.com/wp-json",
         "da": "https://defencearabia.com/wp-json"}
UA = {"User-Agent": "Mozilla/5.0 (EnvanterArsivDenetimi)"}


def get(url, params, tries=4):
    for i in range(tries):
        try:
            r = requests.get(url, params=params, headers=UA, timeout=120)
            if r.status_code == 400:
                return None  # sayfa sonu
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 ** (i + 1))


def paged(base, ep, fields, extra=None, workers=8, maxpages=2000):
    out, page, done = [], 1, False
    with cf.ThreadPoolExecutor(workers) as ex:
        while not done and page <= maxpages:
            batch = list(range(page, page + workers))
            res = ex.map(lambda p: get(f"{base}/wp/v2/{ep}",
                                       dict(per_page=100, page=p, _fields=fields, **(extra or {}))), batch)
            for r in res:
                if not r:
                    done = True
                    continue
                out.extend(r)
                if len(r) < 100:
                    done = True
            page += workers
            print(ep, len(out), file=sys.stderr)
    return out


def main(OUT, WHAT):
  for key, base in SITES.items():
      if WHAT in ("terms", "all"):
          for ep in ("categories", "tags"):
              d = paged(base, ep, "id,name,slug,count,link,description,parent")
              json.dump(d, open(f"{OUT}/{key}_{ep}.json", "w"), ensure_ascii=False)
      if WHAT in ("posts", "all"):
          d = paged(base, "posts", "id,date,modified,link,slug,title,excerpt,content,categories,tags,author",
                    {"orderby": "id", "order": "desc"})
          json.dump(d, open(f"{OUT}/{key}_posts.json", "w"), ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "all")
