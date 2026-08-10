# Changelog

What changed, when, and why. Review entries are logged even when nothing changed — "reviewed, no changes" is information.

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
