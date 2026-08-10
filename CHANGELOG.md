# Changelog

What changed, when, and why. Review entries are logged even when nothing changed — "reviewed, no changes" is information.

## 2026-08-10 — One numbered spine

**Fixed** — three independent numbering schemes were running at once and two of them collided. Stations counted 1–5, the loop in `docs/00-intro.md` counted 1–6, and Station 1's own sections counted 1–5. The two 1–5 sequences meant different things and did not correspond: Station 1's "3. The worked example" was loop step 2, its "5. Try it yourself" was loop step 3, and its "4. Don't believe it — check it" was not a loop step at all, while loop step 4 ("Check") was the unnumbered "How you'll know it's good" further down. A reader using the numbers to locate themselves was actively misled.

**The rule now: the station is the only number in the course. Everything else is named.** This follows the section skeleton `applied-ai-operations` already uses on its pages.

- `docs/00-intro.md` — the six-step numbered loop became a named skeleton, listing the headings that recur in every station. States the one-number rule explicitly.
- `docs/01-the-interview.md` — dropped `1.`–`5.` from the section headings. The two order-independent numbered lists (the five ways to provoke an error, the five checkpoints) became bullets, removing two further competing 1–5 sequences. Only "Pass 1–4" survives, and it is a local sequence with a distinct noun.
- `docs/01-the-interview.md` — "Don't believe it — check it" became "Don't believe it — **interrogate** it". Two adjacent sections were both called some form of *check*: interrogating Claude's output, and checking your own guide. Renaming one separates them.
- `docs/01-the-interview.md` — the cross-reference "that is exactly why section 4 …" pointed at a number that no longer exists; it now names the section.
- `build-site.py` — the sidebar gained a nested outline of each station's `##` headings. Only the station you are currently inside is expanded; all six at once is a wall of links. Position is now something you see rather than something you count.
- `build-site.py` — the scroll-spy rule changed from "first target intersecting the top band" to "last target whose top has passed the reading line". The old rule could not highlight a heading at all, because a station's `<section>` spans the whole station and always won over the headings inside it. It also now syncs on `hashchange` and `load`, so a shared deep link highlights on arrival, and it scrolls only the sidebar rather than calling `scrollIntoView`, which was free to fight the reader's own scrolling.
- `build-site.py` — the *About the course* group lost its "What this course is not" link. That heading now appears in the introduction's own outline, and having it in both places put a duplicate id in the scroll-spy's lookup map.

## 2026-08-10 — Initial scaffold

**Added**
- `README.md` — thesis, the five-station table, the page index, the review routine, license and contribution position.
- `docs/00-intro.md` — the introduction: what the course is about, what it deliberately is not, who it is for, the six-step loop each station follows, what you need in front of you, and the four AI Fluency competencies.
- `docs/01-the-interview.md` — Station 1, written as the format exemplar. The three-column sort (Mechanical / Groundwork / Decision), the four prompt components that carry ordinary office work, the four-pass worked example, the five ways to provoke an error, and the review instruction participants hand to Claude.
- `build-site.py` — site generator, adapted from `applied-ai-operations`. Standard library only.
- `site/index.html` — generated. Committed, opens by double-clicking.
- `LICENSE` — CC BY 4.0.
- `.github/workflows/pages.yml` — deploys `site/` as the Pages root.

**Structure decisions**
- **Fixed order, not a reference.** The `COURSE` list in `build-site.py` is the single source of the course order and the navigation order. Nothing sorts alphabetically anywhere. This is the substantive difference from `applied-ai-operations`, which is explicitly a reference with no reading order.
- **Stations 2–5 appear before they are written.** They sit in `COURSE` with a `pending` line taken from the station table in `README.md`, and render as dimmed navigation entries and placeholder sections. A course whose arc is invisible until it is finished reads as three disconnected pages.
- **`Verb:` became `Competencies:`.** The four verbs of the reference repo (Design / Build / Evaluate / Ship) have no meaning here. Each station declares which of the four AI Fluency competencies it trains, and a station can declare several — Station 1 declares three. The four badge colour tokens were renamed accordingly, and `build-site.py` rejects a competency name outside the known four.
- **The Process Filter was dropped,** along with its CSS and JavaScript. It is a diagnostic tied to the other repo's thesis. `docs/00-intro.md` promises a self-check at the end of the course; that is the natural replacement, and it is not written yet.
- **The `Positions` navigation group became `About the course`.** It holds *What this course is not*, *Freshness*, and *Author & license*. The first is an anchor into the introduction page rather than a duplicate of it — `docs/` stays canonical and nothing is maintained twice.

**Source:** German working drafts (`Intro.md`, `Station1.md`, 2026-08-10), translated in full. The drafts stay out of the repo via `.gitignore`; the repo is English. The invented worked example — Hartmann Verpackungstechnik and Nordfrucht, euros, German trade detail — was kept rather than localised, because the specificity is what makes the four passes legible.
