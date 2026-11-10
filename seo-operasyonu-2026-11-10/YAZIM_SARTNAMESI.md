# Envanter Medya — writer spec (SEO pilot, 10 Nov 2026)

Site: https://envantermedya.com (WordPress + Polylang + Rank Math). Languages: tr (default), en (/en/), es (/es/), ar (/ar/), ru (/ru/).
Today: 2026-11-10. You produce a DRAFT payload file. NEVER call any WordPress write endpoint (no POST/PUT/DELETE to envantermedya.com). Read-only GETs to the public site/REST are fine but keep them few (cached inventory is already provided to you in the brief).

## Output (one file per article)
`taslaklar/<slug>.json` plus `<slug>.html` (title as <h1> + content_html) for human reading.

```json
{
  "decision": "NEW | NEW ANGLE | UPDATE",
  "update_post_id": null,                     // only for UPDATE: the existing post id
  "content_type": "news | analysis | explainer | profile | guide",   // do not label evergreen guides as breaking news
  "lang": "en",
  "title": "post title / H1 — natural search phrasing, strong but no clickbait",
  "slug": "en-short-ascii-slug",               // tr: no prefix; others prefixed en-/es-/ar-/ru-; ASCII transliteration for ru/ar
  "excerpt": "1–2 sentences",
  "content_html": "<p>…</p><h2>…</h2>…",      // p, h2, h3, ul/ol, table (with thead), blockquote, a. No H1 inside content. No images inside content.
  "rank_math_title": "≤ 60 chars, contains the main query near the start",
  "rank_math_description": "140–158 chars, answers the query, no clickbait",
  "rank_math_focus_keyword": "main query",
  "target_query": "exact GSC query",
  "secondary_queries": ["long-tail variants this page should also satisfy"],
  "demand_evidence": "copy from brief",
  "category_hint": "Haber / Analiz / Savunma Sözlüğü / Kara / Hava / Deniz / Firma / Profil",
  "sources": [{"name": "...", "url": "...", "date": "YYYY-MM-DD or n/a", "supports": "which facts"}],
  "internal_links": [{"url": "https://envantermedya.com/...", "anchor": "..."}],
  "hreflang_equivalents": {"tr": "url-or-null", "en": null, "es": null, "ar": null, "ru": null},
  "image": {
     "type": "official_photo | public_domain_photo | cc_photo | title_card",
     "source_page_url": "page where the image and its licence are shown (DVIDS/marines.mil/af.mil/Wikimedia Commons file page/manufacturer media page)",
     "direct_image_url": "direct jpg/png url if available",
     "licence": "e.g. Public domain (US DoD work) / CC BY-SA 4.0 / manufacturer press image, editorial use",
     "credit": "photographer / organisation as required",
     "alt": "localized, descriptive alt text (what is actually visible)"
  },
  "last_updated_note": "localized 'Last updated: 10 November 2026' line is already included at the end of content_html",
  "word_count": 0,
  "verification_notes": ["anything an editor must double-check"],
  "duplicate_check": "what existing Envanter pages cover nearby intents and why this page is different"
}
```

## Content rules
1. Write ORIGINAL text natively in the target language (not a translation of an Envanter page in another language). Vary the opening — do NOT start with "In the world of…", "When it comes to…", "X is a…" boilerplate, rhetorical questions, or the same sentence pattern other Envanter pages use. Natural journalistic language. No hype words, no "son dakika/breaking".
2. The first paragraph (≤ 90 words) directly answers the main query with concrete facts (what it is / key numbers / what happened, with date).
3. H2/H3 structure; at least one comparison or spec table; an FAQ section (H2 FAQ / Preguntas frecuentes / Часто задаваемые вопросы / Sık sorulan sorular) with 4–6 H3 questions + short answers. Explainers/profiles 1,000–1,500 words; news/analysis 700–1,100 words.
4. Facts: every number (calibre, weight, range, quantity, money, dates, percentages) must come from a source you actually opened. Prefer primary sources: manufacturer, ministry/armed forces, official contract announcements (defense.gov), company IR / SEC filings, parliamentary documents; then established outlets (Reuters, AP, Janes, Defense News, Breaking Defense, Naval News, The War Zone, Military Times, Infodefensa, TASS/RIA only for attributed Russian statements). If sources disagree give a range and say so. If you cannot verify a figure, leave it out. Inventory/order numbers: attribute ("according to IISS Military Balance 2026", "по данным…", "según…"). Development goals must be written as goals, not as achieved capabilities.
5. Do NOT cite Turkish aggregator sites (Defence Türk, SavunmaSanayiST, GDH, Savunma Sanayi Dergilik, haber.aero) or Wikipedia as sources (Wikipedia only to find primary sources).
6. Put a short "Sources" list (H2 Sources / Fuentes / Источники / Kaynaklar) at the end with linked source names, then the localized "Last updated: 10 November 2026" line (Son güncelleme: 10 Kasım 2026 / Última actualización: 10 de noviembre de 2026 / Обновлено: 10 ноября 2026 г.).
7. Internal links: 3–6 links to EXISTING published Envanter pages, preferably in the same language, inline in the body with natural anchors. Use the candidate list in your brief (all published). Do not link drafts or scheduled posts.
8. Finance topics: report facts and company/analyst statements; no investment advice, no price targets of your own; include the date/time context of any share-price figure.
9. Images: never use images without a clear licence; never AI-generated images presented as real photos. Best: US government public-domain photos (DVIDS, marines.mil, af.mil, army.mil, navy.mil) or Wikimedia Commons files with an explicit free licence shown on the file page (record licence + author). Otherwise set type "title_card" (the house 1200×675 card will be generated).
10. Keep the article distinct from the existing Envanter pages listed in your brief (different search intent). If you discover during research that an existing PUBLISHED Envanter page already covers the same intent in the same language, stop and write {"decision":"SKIP – duplicate", "url": "..."} instead.
