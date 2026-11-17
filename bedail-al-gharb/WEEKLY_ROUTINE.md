# بدائل الغرب — Weekly Routine (AMBARGO DELENLER)

The standing instructions for every weekly run. **ONE article maximum per run.**

## Steps (every 7 days)

1. Read `QUEUE.md` and all published articles in this folder.
2. Search for new export restrictions, denials, approvals (DSCA notifications), sanctions actions and supplier shifts affecting Arab buyers since the last run.
3. Update stale facts in the queue and in published articles. Refresh the `facts_checked` date and add a short changelog line at the bottom of each updated article.
4. Select ONE topic: the strongest evidence + news hook. New stories may displace queued items.
5. Research outside WordPress. Use primary sources first (DSCA, ministries, company releases, UN panels, SIPRI), then Janes, Breaking Defense, Defense News and similar.
6. **Verify causation.** If the evidence cannot show why the supplier changed, do not invent it. SKIP or reframe as "diversification / unknown motive".
7. Write in Arabic, using the 16-section case-study structure (see article #1).
8. Prepare SEO in the front matter: slug, SEO title, meta description, primary + secondary keywords.
9. Propose visuals: timeline, map, package table, and an "original → alternative" graphic that marks proven vs interpretive arrows.
10. Prepare the sources list, grouped: official / policy / contracts / performance / unconfirmed.
11. Add at most one natural Envanter Media link for Turkish systems, never as the sole source.
12. Set `status: READY TO PUBLISH`, update `QUEUE.md`, commit.

## Non-negotiable rules

- Status vocabulary: RUMOURED · REPORTED · EVALUATED · REQUESTED · APPROVED · SELECTED · CONTRACTED · DELIVERED · OPERATIONAL.
- Never turn interest into an order, an approval into a contract, an MoU into a procurement, or a show display into an operator.
- Separate: official restriction / formal denial / delayed approval / reported political condition / analyst interpretation / buyer diversification / unconfirmed motive.
- Never compare package values as if they were unit prices.
- No supplier "always wins". Türkiye, China, Russia and South Korea are each tested on evidence.
- Do not let the series become "Türkiye vs West" every week.

## Publishing

Target: **www.defencearabia.com**. Publisher: `yayin-araclari/yayinla_md_da.py` (reads credentials only from the `DA_AUTH` environment variable, format `user:application-password`).

- **New article:** `python3 yayin-araclari/yayinla_md_da.py bedail-al-gharb/NN-....md "YYYY-MM-DDT06:00:00" "<category IDs>"` — schedules a WordPress `future` post (UTC), uploads a cover, sets RankMath fields. Then write `status: SCHEDULED (WordPress)`, `planned_publish` and `wp_post_id` into the front matter and the QUEUE table. Next free slot: the Wednesday after the last scheduled article.
- **Fact refresh of an already scheduled/published article:** edit the Markdown, then `python3 yayin-araclari/yayinla_md_da.py <file> --update` (date and status unchanged).
- Arabic category IDs used so far: 254 land, 260 artillery, 266 fighters, 270 trainers, 276 UAVs, 286 frigates/corvettes, 296 air defence, 322 defence companies, 334 exports & cooperation, 336 export deals, 338 international partnerships, 340 technology transfer, 342 localisation, 344 defence policy, 346 Gulf security, 348 geopolitics, 350 procurement, 352 Arab armed forces.
- Never write credentials into files, prompts or commits. If `DA_AUTH` is not set, stop at READY TO PUBLISH and report it.
