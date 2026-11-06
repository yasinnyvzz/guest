# Envanter Medya — taslak yazım şartnamesi (writers)

Site: https://envantermedya.com (WordPress + Polylang + Rank Math). Languages: tr (default, no prefix), en (/en/), es (/es/), ar (/ar/), ru (/ru/), zh (/zh/).
Today: 2026-11-06. Output is a WordPress DRAFT payload — nothing is published by you. Do NOT call any WordPress write endpoint.

## Output file (one per article)
`/tmp/claude-0/-home-user-guest/f56c3702-5f19-5f6a-9b53-9a9c954b7eff/scratchpad/out/drafts/<lang>-<slug>.json`

```json
{
  "lang": "es",
  "title": "H1/post title (natural search phrasing, no clickbait)",
  "slug": "<lang>-<short-ascii-slug>",            // tr: no prefix; others prefixed: en-, es-, ar-, ru-
  "excerpt": "1–2 sentences",
  "content_html": "<p>…</p><h2>…</h2>…",          // WordPress block-free HTML: p, h2, h3, ul/ol, table, blockquote, a
  "rank_math_title": "≤ 60 chars, contains the main query",
  "rank_math_description": "140–158 chars, answers the query, no clickbait",
  "rank_math_focus_keyword": "main query",
  "target_query": "exact GSC query this answers",
  "demand_evidence": "copy from brief",
  "category_hint": "e.g. Savunma Sözlüğü / Kara / Deniz / Hava / Firma Profili / Haber",
  "sources": [{"name": "...", "url": "...", "supports": "which facts"}],
  "internal_links": [{"url": "https://envantermedya.com/...", "anchor": "..."}],
  "hreflang_equivalents": {"tr": "url-or-null", "en": "...", ...},   // existing equivalent pages in other languages, if any
  "image": {"recommendation": "Envanter title card 1200x675 (lacivert zemin, altın şerit, 'ENVANTER MEDYA'), or a licence-safe official/press image with credit", "alt": "localized alt text"},
  "word_count": 0,
  "verification_notes": ["anything an editor must double-check before publishing"],
  "duplicate_check": "what you searched on the site and what you found"
}
```

## Content rules
1. Write ORIGINAL text natively in the target language. Not a word-for-word translation of the Turkish/English page. Think about what a reader in that market searches for (e.g. Spanish readers: España/Latinoamérica angle; Russian readers: terminology used in Russian military literature).
2. First 80–100 words must directly answer the query (definition / what it is / key numbers).
3. Structure: H2 sections + at least one comparison or spec table + an FAQ section (H2 "Preguntas frecuentes"/"FAQ"/"Часто задаваемые вопросы"/"Sık sorulan sorular") with 4–6 Q&A as H3 + short answers. 900–1,400 words.
4. Facts: every number (calibre, weight, range, quantity, revenue, ownership %, dates) must come from a source you opened (manufacturer, ministry, annual report, Janes/Naval News/Defense News/Reuters, etc.). If sources disagree, give a range and say so. If you cannot verify a figure, leave it out. Never present unverified inventory/order/delivery numbers as certain — use "según…", "according to…", "по данным…".
5. Do NOT cite Turkish aggregators (Defence Türk, SavunmaSanayiST, GDH) as sources. Wikipedia may be used only to find primary sources, not as the cited source.
6. No clickbait, no "son dakika", no hype words. Neutral, technical, news-agency tone.
7. Internal links: 3–6 links to EXISTING Envanter pages, preferably in the SAME language. Find them via the public REST API, e.g.
   `curl -s -A "Mozilla/5.0" "https://envantermedya.com/wp-json/wp/v2/posts?search=<kw>&lang=all&per_page=20&_fields=id,date,link,title"`
   (also `.../wp/v2/savunma_terimi?search=...` for the Turkish glossary). Only link URLs that return HTTP 200.
8. Duplicate check: before writing, search the site (lang=all) for the topic in the target language. If a dedicated page on the SAME intent already exists in that language, STOP and write a short JSON with `"status_decision": "SKIP – duplicate"` and the URL instead of an article.
9. hreflang_equivalents: list existing pages on the same topic in other languages (from the same REST search), so the editor can group translations.
10. Images: never copy photos without licence; never use AI-generated images as if they were real photos. Recommend the house title card or an official press image with credit.
11. Also save a quick human-readable copy: same path with `.html` (just the title as <h1> + content_html).
