#!/usr/bin/env python3
"""Salt okuma: Envanter'in varlık sayfası CPT'lerini (sistem, firma, savunma_firma) başlık+bağlantı olarak indirir."""
import json, sys
from cek import paged
OUT = sys.argv[1]
for ep in ("savunma_sistemi", "firma", "savunma_firma"):
    d = paged("https://envantermedya.com/wp-json", ep, "id,slug,link,title,date")
    json.dump(d, open(f"{OUT}/ev_cpt_{ep}.json", "w"), ensure_ascii=False)
