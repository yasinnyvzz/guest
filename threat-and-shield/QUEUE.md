# THREAT-AND-SHIELD QUEUE

The weekly routine reads this file first and updates it at the end of every run.
Full topic cards are in `SERIES_PLAN.md`. Articles go in `articles/NN-<slug>.md`.

## Published / ready

| # | Slug | File | Status | Data as of |
|---|---|---|---|---|
| 1 | `/gulf-missile-defense/` | `articles/01-gulf-missile-defense.md` | READY TO PUBLISH | 2026-09-29 |

## Queue (next run takes the top item unless a stronger new topic appears)

| Order | Card | Arabic title | Slug | Priority | Hook to re-check before writing |
|---|---|---|---|---|---|
| 1 | #2 | مخزون الصواريخ الاعتراضية: كيف تعيد دول الخليج بناء درعها بعد 2026؟ | `/gulf-interceptor-stockpile/` | P1 | New DSCA/Federal Register Patriot/THAAD notices; PAC-3 MSE production-rate news; GCC strategic reserve |
| 2 | #3 | كيف تواجه دول الخليج المسيّرات الرخيصة؟ معادلة الكلفة | `/counter-drone-arab-states/` | P1 | New C-UAS contracts (Coyote, APKWS, KORKUT, Ukrainian interceptors) |
| 3 | #4 | كيف تحمي منشآت النفط والغاز الخليجية نفسها من المسيّرات والصواريخ؟ | `/gulf-energy-infrastructure-protection/` | P1 | Ras Laffan/Habshan repair status; new strikes |
| 4 | #5 | إذا تعطلت الملاحة في مضيق هرمز، ما القدرات البحرية الخليجية لحماية التجارة؟ | `/hormuz-gulf-naval-capabilities/` | P1 | Blockade status, Aspides/UK–France mine mission, talks in Doha |
| 5 | #6 | كيف تبني السعودية دفاعاً متعدد الطبقات ضد الصواريخ والمسيّرات؟ | `/saudi-layered-air-defense/` | P2 | THAAD battery activations; M-SAM II schedule |
| 6 | #7 | كيف تواجه مصر التهديدات الجوية والبحرية في البحر الأحمر؟ | `/egypt-red-sea-air-naval-defense/` | P2 | Houthi activity; Suez revenue; Egyptian navy deployment statements |
| 7 | #8 | محطات التحلية والكهرباء: كيف تحمي دول الخليج مياهها من الهجمات؟ | `/gulf-desalination-protection/` | P2 | New attacks on utilities; GCC water-security decisions |
| 8 | #9 | التشويش والحرب الإلكترونية والهجمات السيبرانية: الدرع غير المرئي | `/gulf-electronic-warfare-cyber/` | P2 | GNSS interference data; cyber council statements |
| 9 | #10 | كورية أم تركية أم صينية أم غربية؟ كيف تنوّع الجيوش العربية موردي الدفاع الجوي | `/air-defense-suppliers-arab-states/` | P3 | Confirmation of any Turkish/Chinese contract with an Arab state |

## Reserve (promote only if demand exceeds a queued topic)

- الألغام البحرية وقدرات الإجراءات المضادة للألغام في الخليج — `/gulf-mine-countermeasures/`
- حماية مسارات تصدير النفط البديلة (ينبع، الفجيرة) — `/hormuz-bypass-routes-protection/`
- الدفاع الجوي الأردني بعد 2026 — `/jordan-air-defense/`
- العراق وتنويع الدفاع الجوي (KM-SAM والمنظومات التركية) — `/iraq-air-defense/`

## Weekly routine (every 7 days, ONE article maximum)

1. Read this queue.
2. Check whether a new regional threat has materially changed Arabic search demand. Look at news volume in Al Jazeera, Al Arabiya, Asharq, Annahar and Sky News Arabia, and at Semrush if API units are available.
3. Add a new topic only if it is stronger than the queued ones. Record the reason under the change log.
4. Select ONE topic.
5. Research it, preferring primary sources: MoDs, DSCA, the Federal Register, companies, GCC-SG and SIPRI.
6. Verify every figure. Label each claim confirmed, contracted, approved, reported or unverified.
7. Write it in Arabic using the fixed structure: H1, direct answer, sections 1–12, FAQ and sources.
8. Build the data table (an indicator matrix, not a ranking).
9. Build the gallery and map concept (broad regional maps only).
10. Prepare the SEO package: title, H1, evergreen slug, meta description, primary and secondary queries, PAA questions, FAQ, JSON-LD, internal links, country hubs, system pages and supplier pages.
11. Add at most one Envanter Media link, and only when a Turkish system is genuinely relevant.
12. Run the safety checklist: no positions, blind spots, routes, depletion or saturation math, defeat methods, EW bypass or target selection.
13. Mark the article READY TO PUBLISH, move it to "Published / ready", commit and push.

## Change log

- 2026-09-29: Series created and the original 10-topic pool validated.
  - Merged: original #3 (THAAD/Patriot) went into the stockpile article, and #5 (loitering munitions) went into the cheap-drones article.
  - Dropped: #9 (ballistic preparation), absorbed by #1 and #2.
  - Added three topics: interceptor stockpile, desalination and power, EW and cyber.
  - Semrush had no API units, so demand was judged from media coverage.
  - Article #1 written.
