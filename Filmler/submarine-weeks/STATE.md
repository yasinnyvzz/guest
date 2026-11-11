# State: How can a submarine stay underwater for weeks? (Defence MENA)

Read this first in every new session, after loading the cinecode skill (Claude Code: the Skill tool, never a plain read of SKILL.md), then `python3 KIT/scripts/init_film.py . --update-tools` silently; update "Now" before ending every turn. Keep it short.
Kit: /root/.claude/skills/cinecode
Method: this chat coordinates and builds what it holds the context for; a fresh helper takes only an independent part beside it (sound, narration takes, research, the independent viewer) or a long film's chapter, briefed from files (`/root/.claude/skills/cinecode/references/context-protocol.md`).

## Resume here
<!-- Updated at every gate and before every handoff. A new chat starts with "STATE.md'den devam et" / "Continue from STATE.md". -->
- **Phase:** 6a draft v2 delivered, waiting for the user's notes or final
- **Pace:** through (user: "Film modu, taslağa kadar")
- **Approved gates:** none
- **Open notes:** none (notes/round-N.md)
- **Next action:** notes -> notes/round-1.md and targeted edits in engine/film.html; final -> full size 1080x1920 render (about 60-80 min on this CPU) with the swiftshader flags
- **Budget so far:** <~estimate> of the <Balanced> ceiling (<n>%)

## Now
- **Step:** 6 draft
- **Gate:** <waiting for user: what / passed>
- **Next step:** <one concrete line>
- **Waiting for:** <user / background job / nothing>
- **Profile:** balanced
- **Purpose:** ad & product (explainer for a media brand) (`/root/.claude/skills/cinecode/references/purpose-<cinematic|ad>.md`)
- **Format:** 76 s, 9:16, 1080x1920, 30 fps, silent (no VO, no music; Turkish VO added later by editor)
- **Medium:** 3D realistic engineering animation (user brief)
- **Look:** custom deep-engineering (ROADMAP.md §3)
- **Finishing:** none <!-- off by default; chosen at the style frame -->
- **Music:** none (user)
- **Sound:** silent by choice (user brief: no VO, no music; editor adds Turkish narration later)
- **Type:** Saira 700/400 (OFL), caps, end card only; echoes the Defence MENA wordmark
- **Subtitles:** off
- **Last output:** renders/Denizalti-Haftalarca-draft.mp4 (= draft-v2, checks passed)
- **Disk free at last check:** <GB, date>

## Running jobs
| Job | Command (short) | PID | Status file | Log | Started |
|---|---|---|---|---|---|
| draft v2 picture 540x960 | capture.mjs engine/film.html --video renders/draft-v2-picture.mp4 | see logs/draft-v2.log | renders/draft-v2.status.json | logs/draft-v2.log | 2026-11-11 16:02 |

## Gates
| Step | Gate | Result | Date | Note |
|---|---|---|---|---|
| 1 | interview answered / defaults accepted | | | |
| 2 | roadmap approved | | | |
| 3 | script and text approved | | | |
| 4 | style frame approved, finishing chosen | | | |
| 4b | type pairing picked | | | |
| 5 | animatic approved | | | |
| 6a | draft cut approved | | | |
| 6 | final delivered | | | |

## Decisions
| Date | Decision | Why | Who |
|---|---|---|---|
| 2026-11-11 | Idea and 10-scene brief as given | complete brief | user |
| 2026-11-11 | On-screen text English only: REIS CLASS / CAN IT STAY SUBMERGED FOR WEEKS? | Defence MENA is English | user |
| 2026-11-11 | Logo: D icon in corner throughout + wordmark on end card | | user |
| 2026-11-11 | Film mode, straight to draft | | user |

## Notes rounds
Verbatim notes and the per-shot split live in `notes/round-N.md`.

| Round | File | Shots touched | Unchanged | Status |
|---|---|---|---|---|

## Agent tasks
| Task | Calls | Brief (files read) | Output file | Result |
|---|---|---|---|---|

## Budget meter
Ceiling: <Economy / Balanced / Quality> (internal caps: `references/context-protocol.md` §6). Stop and ask at 80%.

| Phase | Share of ceiling | Estimate so far | % of share | Note |
|---|---|---|---|---|
| 1-2 Interview + roadmap | 10% | | | |
| 3 Script | 10% | | | |
| 4 Style frame | 20% | | | |
| 5 Animatic | 15% | | | |
| 6 Render, sound, final | 35% | | | |
| Notes rounds | 10% | | | |
| **Total** | 100% | | | |

## Versions
| Version | File | What changed | Snapshot |
|---|---|---|---|
