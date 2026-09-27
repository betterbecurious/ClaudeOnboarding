# Claude, your new Employee

**Most courses on this subject demonstrate features. This one is built along an employment relationship — from the interview to the promotion.**

A course in five stations, for people who need work to get done rather than a tour of the product.

### → **[Take it on the web](https://betterbecurious.github.io/ClaudeOnboarding/)**

The whole course on one page, in order.

`Last reviewed: 2026-08-10`

---

## The five stations

| # | Station | What you can do afterwards |
| --- | --- | --- |
| 1 | The Interview | Hand over a task so that a usable result comes out — and recognise when it hasn't |
| 2 | The Onboarding | Set up a recurring task once, instead of explaining it again every time |
| 3 | The First Real Workday | Turn unsorted material into finished work |
| 4 | Tools and Access | Give access to real systems — and build yourself a tool |
| 5 | The Promotion | Turn how you work into a standard Claude applies everywhere |

Unlike a reference, there is an order here, and it is not decorative. Station 3 assumes you have done Station 2.

## The course pages

| Page | Competencies | Status |
|---|---|---|
| [Station 0 — Who Are We Hiring?](docs/00-intro.md) | Delegation | Published |
| [Station 1 — The Interview](docs/01-the-interview.md) | Description · Discernment | Published |
| Station 2 — The Onboarding | | Not yet published |
| Station 3 — The First Real Workday | | Not yet published |
| Station 4 — Tools and Access | | Not yet published |
| Station 5 — The Promotion | | Not yet published |

Start with [Station 0](docs/00-intro.md). It states who the course is for, what it deliberately is not, how each station is built, what you need in front of you before you begin, and ends with the first exercise: working out what you would hand over at all.

## The website

[`site/index.html`](site/index.html) is the whole site: one file, no build step, no npm, no framework. Open it by double-clicking. Deploy it to GitHub Pages unchanged. Fork it without installing anything.

**`docs/` is canonical.** The site is generated from it — it is never a second copy to keep in step by hand. After editing any page, regenerate:

```bash
python3 build-site.py
```

That script is a maintenance tool for whoever edits this repo, not a build step for whoever reads it. `site/index.html` is committed. Where the site and the docs ever disagree, the docs are right.

Adding a station means writing `docs/0N-slug.md` and moving its entry in the `COURSE` list in `build-site.py` from a placeholder to a real page. The order of that list is the order of the course; nothing else determines it.

---

## Freshness

This course sits on a fast-moving product surface. A stale public course is worse than none, so this one carries a **reviewed** date rather than an updated one — the claim is that someone checked, not that someone edited.

**Review cadence: monthly**, and immediately after any significant Claude platform release.

The review routine, in order:

1. **Check every outbound link resolves.** Anthropic's docs reorganise. Dead links are the first visible sign of rot.
2. **Re-read every station against current product behaviour.** The stations that name product surfaces go stale first.
3. **Check for hardcoded plan or capability claims** that have crept in. Replace with a link.
4. **Re-read the worked examples.** An example that no longer produces roughly the described result is worse than no example, because a participant will follow it and conclude they did it wrong.
5. **Update the `Last reviewed` date** here, in each station page, and in `LAST_REVIEWED` in `build-site.py`, then run `python3 build-site.py` so the site footer matches.
6. **Add a `CHANGELOG.md` entry** — even when nothing changed. "Reviewed, no changes" is information.

## Contributing

**Issues, yes. Pull requests, no.**

If something is out of date, a link is dead, or you think a position here is wrong — [open an issue](../../issues). Disagreement gets read. The editing stays with one person.

No confidential documents in issues.

## License

[CC BY 4.0](LICENSE). Use it, teach from it, translate it — credit **Billie Jeurink** and link back.

## Author

Written and maintained by **Billie Jeurink**. **billie@bjeurink.com**.
