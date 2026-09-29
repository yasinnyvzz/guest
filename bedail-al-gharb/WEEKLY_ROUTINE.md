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

WordPress is for final publishing only. Credentials live exclusively in environment secrets:
`WP_URL`, `WP_USERNAME`, `WP_APP_PASSWORD`. Never write them into files, prompts or commits.
If these variables are not present, stop at READY TO PUBLISH and leave publishing to an editor.
