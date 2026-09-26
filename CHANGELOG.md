# Changelog

What changed, when, and why. Review entries are logged even when nothing changed — "reviewed, no changes" is information.

## 2026-09-26 — Station 0: deciding what to hand over comes before the interview

In the employment analogy, working out what you would hand over is deciding whom to hire, not interviewing. Station 1 mixed both. The exercise now lives in the introduction, which becomes Station 0 — Who Are We Hiring?; Station 1 is only about asking well. Same split as in the Tbilisi workshop.

- `docs/00-intro.md` — title **Station 0 — Who Are We Hiring?**, competency Delegation. Gains the exercise *What are you actually handing over?* from Station 1, unchanged, plus its opening line ("about your work first") and the New hire box "Nobody runs an interview without knowing what they are hiring for." New in the exercise: a paragraph that it doesn't have to be management work, with everyday examples. *How you work with it* and *What you need* adjusted (Station 0 is the exception to the skeleton; paper and pen).
- `docs/01-the-interview.md` — competencies Description · Discernment. Starts with "Ask badly…" and "They simply interviewed badly." *Before you start*, *Try it yourself* and *What you keep* point to the list from Station 0. The anchor `#01-the-interview-what-are-you-actually-handing-over` becomes `#00-intro-what-are-you-actually-handing-over`.
- `docs/00-intro.md` — "splits the line instead of assigning the whole of it" replaced by a concrete example (the complaint: Claude gathers the delivery history, the decision stays with you). The phrase was too abstract to act on.
- `build-site.py` — Station 0 is numbered too (0.1, 0.2 …), so its exercise shows a number; spine starts "Who we're hiring".
- `README.md` — course pages table and the "start here" line.
- `Last reviewed` unchanged: this is an edit, not a full review.

## 2026-09-26 — Timesheets example removed

- `docs/01-the-interview.md` — removed the row "Typed up the timesheets | The whole row" from the three-column table. The course is aimed at managing directors and the self-employed, who rarely have a purely mechanical task like this; the paragraph after the table already says a nearly empty left column is normal. Same decision as in the Tbilisi workshop.
- `Last reviewed` unchanged: this is an edit, not a full review.

## 2026-09-25 — The analogy gets its own box; "briefing" instead of "interview guide"; Hartmann has 80 employees

The employment analogy helps a reader keep their place in the course, but it was mixed into the method: the table of prompt parts had a column "In the interview", and several sentences only made sense through the hiring picture. A reader learning what goes into a prompt should not be thinking about job-interview questions. Same change as in the Tbilisi workshop pages, so both use one convention.

- `build-site.py` — new convention: a blockquote whose first line starts with `**New hire:**` renders as a separate box in its own colour (sage, light and dark), labelled "New hire". On GitHub it still reads as a quote.
- `docs/01-the-interview.md` — analogy sentences moved into New hire boxes, wording unchanged: "Nobody runs an interview…", "They simply interviewed badly.", the "look friendly" comparison, and "The candidate has not got better. The question has got better." The table of the four prompt parts lost its "In the interview" column; the column's content is now one New hire box under the table.
- `docs/01-the-interview.md` — Hartmann Verpackungstechnik GmbH now has **80** employees instead of 40, in the example description and in the pass 2 prompt. Matches the workshop material.
- `docs/00-intro.md` — *How you work with it* explains the New hire box.
- **"Interview guide" is now "briefing"** everywhere (heading 1.5, *Try it yourself*, *Getting feedback*, *On your own material*, *What you keep*, the Station 2 hand-over, the introduction). The thing a participant writes is a prompt, and naming it after an interview invited exactly the confusion this change removes. The review instruction already called it a briefing. Section anchor `#…the-interview-guide` changes accordingly.
- `docs/01-the-interview.md` — the sentence the station turns on now ends "…a verdict on the **tool**", not "on the candidate".
- `build-site.py` — the Diligence badge is a muted red instead of green; green was too close to the New hire box.
- **Hartmann Packaging GmbH** instead of Hartmann Verpackungstechnik GmbH, in the example description and the pass 2 prompt. English course, English company name; matches the workshop.
- Station names now match the workshop: **Station 3 — The First Real Workday**, **Station 5 — The Promotion** (`README.md`, `COURSE` in `build-site.py`; pending slug `03-first-day` → `03-first-workday`).
- Removed "Anthropic reports up to 30 % better answer quality" from *Two moves that have nothing to do with wording*. The recommendation stays; the figure goes, because unverifiable quality percentages undercut the rest of the course in a sceptical room.
- `Last reviewed` unchanged: this is an edit, not a full review.

## 2026-08-10 — Two-part section numbers, and exercises marked

Sections are numbered again, but hierarchically: **`<station>.<section>`**. `1.4` is the fourth section of Station 1. This composes instead of colliding — the earlier bare `4.` could be read as Station 4 or as loop step 4, whereas a two-part number cannot be mistaken for a station number. The wall of unnumbered headings was also simply hard to scan.

- `build-site.py` — section numbers are **generated**, not typed into the markdown. The station number is parsed from the filename (`01-the-interview` → `1`), so inserting or moving a section renumbers the rest for free and no cross-reference can go stale. The introduction is station `00` and stays unnumbered; it is not a station.
- `build-site.py` — new `Exercise` marker convention: a line holding nothing but `` `Exercise` ``, directly under a `##` heading. It renders as a chip on the heading, emphasises the entry in the sidebar outline, and feeds a generated *"What you actually do in this station"* index at the top of the station. Kept as its own line rather than baked into the heading text so the markdown still reads correctly on GitHub.
- `build-site.py` — the exercise index matters most on a phone: the sidebar is hidden below 960px, so it is the only overview a mobile reader gets.
- `build-site.py` — added a single `slugify()`; `render()`, `outline()` and the marker scan had three copies of the same regex and had to agree exactly or anchors would silently miss.
- `docs/01-the-interview.md` — five sections marked as exercises: the sections where you work on your own material or produce something. `1.9 How you'll know it's good` is deliberately not one; it is the check on an exercise, not an exercise.
- `docs/00-intro.md` — the skeleton section now explains the two-part numbering and the `Exercise` marker. It previously claimed the station was the only number in the course, which this change made untrue.

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
