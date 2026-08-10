#!/usr/bin/env python3
"""
Generate site/index.html from README.md and docs/.

docs/ is canonical. This script exists so the site is never a second
hand-maintained copy. It is a maintenance tool, not a build step for the
reader: site/index.html is committed, opens by double-clicking, and deploys
to GitHub Pages unchanged.

Run after editing any page:

    python3 build-site.py

No dependencies. Standard library only. Handles the markdown subset
actually used in this repo -- if you introduce new syntax, teach it here.

This is a course, not a reference. The order in COURSE below is the order of
the course and the order of the navigation; nothing else determines either.
Stations that are not written yet stay in the list with a `pending` line, so
a reader can see where the course goes before it gets there.
"""

import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
LAST_REVIEWED = "2026-08-10"

# Set once the repo has a home. GitHub-relative links in README.md (such as
# ../../issues) have no meaning on the published site, so they are rewritten
# against this.
REPO_URL = "https://github.com/betterbecurious/ClaudeOnboarding"

# The course, in order. A written station needs only its slug -- the title
# comes from the page's own H1. A station that is not written yet carries the
# title and the promise from the station table in README.md, so the reader can
# see the whole arc from the first page.
COURSE = [
    {"slug": "00-intro"},
    {"slug": "01-the-interview"},
    {"slug": "02-onboarding",
     "nav": "Station 2 — The Onboarding",
     "pending": "Set up a recurring task once, instead of explaining it "
                "again every time."},
    {"slug": "03-first-day",
     "nav": "Station 3 — The First Real Day",
     "pending": "Turn unsorted material into finished work."},
    {"slug": "04-tools-and-access",
     "nav": "Station 4 — Tools and Access",
     "pending": "Give access to real systems — and build yourself a tool."},
    {"slug": "05-promotion",
     "nav": "Station 5 — Promotion to Team Lead",
     "pending": "Write a standard that holds across several tasks."},
]

COMPETENCIES = ["Delegation", "Description", "Discernment", "Diligence"]

SPINE = "Intro → Interview → Onboarding → First day → Tools → Promotion"


# --------------------------------------------------------------------------
# Inline markdown
# --------------------------------------------------------------------------

def rewrite_href(href):
    """Turn a docs-relative link into a single-page anchor."""
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return href
    href = href.replace("../../", "").replace("../", "")
    if href in ("issues", "issues/"):
        return REPO_URL + "/issues"
    if href.startswith("README.md"):
        frag = href.split("#", 1)
        return "#" + frag[1] if len(frag) > 1 else "#top"
    if href.startswith("site/index.html"):
        return "#top"
    # Repo files that live outside site/. Pages serves site/ as its root, so a
    # relative "../" escapes the deployment and 404s. Absolute repo URLs work
    # from the published site and from a double-clicked local copy alike.
    if href.startswith("templates/") or href == "LICENSE":
        return REPO_URL + "/blob/main/" + href
    href = re.sub(r"^docs/", "", href)
    m = re.match(r"^([0-9a-z-]+)\.md(?:#(.*))?$", href)
    if m:
        # Headings inside a page are slugged with the page slug as a prefix,
        # so a cross-page deep link has to carry the prefix too.
        return "#" + m.group(1) + ("-" + m.group(2) if m.group(2) else "")
    return href


def inline(text):
    """Convert inline markdown to HTML. Input is raw markdown, not escaped."""
    placeholders = []

    def stash(rendered):
        placeholders.append(rendered)
        return "\x00%d\x00" % (len(placeholders) - 1)

    # Code spans first: their contents must not be treated as markdown.
    text = re.sub(
        r"`([^`]+)`",
        lambda m: stash("<code>%s</code>" % html.escape(m.group(1))),
        text,
    )

    # Links, before escaping, so URLs survive intact.
    def link(m):
        label, href = m.group(1), rewrite_href(m.group(2))
        ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        return stash('<a href="%s"%s>%s</a>' % (html.escape(href), ext, inline(label)))

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)

    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)([^*]+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)

    for i, rendered in enumerate(placeholders):
        text = text.replace("\x00%d\x00" % i, rendered)
    return text


# --------------------------------------------------------------------------
# Block markdown
# --------------------------------------------------------------------------

def render(lines, heading_offset=1, slug_prefix=""):
    """Render a list of markdown lines to HTML."""
    out = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Fenced code
        if stripped.startswith("```"):
            i += 1
            body = []
            while i < n and not lines[i].strip().startswith("```"):
                body.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % "\n".join(body))
            continue

        # Raw HTML passthrough (details / summary blocks)
        if stripped.startswith("<details"):
            out.append('<details class="expand">')
            i += 1
            continue
        if stripped.startswith("</details>"):
            out.append("</details>")
            i += 1
            continue
        if stripped.startswith("<summary>"):
            inner = re.sub(r"^<summary>|</summary>$", "", stripped)
            # Summaries wrap their label in <strong> for GitHub's renderer.
            # Here the weight comes from CSS, so drop the tags rather than
            # escaping them into visible markup.
            inner = re.sub(r"</?strong>|</?b>", "", inner)
            out.append("<summary>%s</summary>" % inline(inner))
            i += 1
            continue

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            i += 1
            continue

        # Headings
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = min(len(m.group(1)) + heading_offset, 6)
            text = m.group(2)
            slug = slug_prefix + re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            out.append('<h%d id="%s">%s</h%d>' % (level, slug, inline(text), level))
            i += 1
            continue

        # Tables
        if stripped.startswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            if len(rows) >= 2 and all(set(c) <= set("-: ") for c in rows[1]):
                head, body = rows[0], rows[2:]
            else:
                head, body = None, rows
            t = ['<div class="table-wrap"><table>']
            if head:
                t.append("<thead><tr>%s</tr></thead>" % "".join(
                    "<th>%s</th>" % inline(c) for c in head))
            t.append("<tbody>")
            for r in body:
                t.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r))
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue

        # Blockquote
        if stripped.startswith(">"):
            body = []
            while i < n and lines[i].strip().startswith(">"):
                body.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            out.append("<blockquote>%s</blockquote>" % render(body, heading_offset, slug_prefix))
            continue

        # Ordered list
        if re.match(r"^\d+\.\s", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            out.append("<ol>%s</ol>" % "".join("<li>%s</li>" % inline(x) for x in items))
            continue

        # Unordered list
        if stripped.startswith("- "):
            items = []
            while i < n and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(x) for x in items))
            continue

        # Paragraph
        body = []
        while i < n and lines[i].strip() and not re.match(
                r"^(#{1,6}\s|\||>|-\s|\d+\.\s|```|<details|</details|<summary|---$)",
                lines[i].strip()):
            body.append(lines[i].strip())
            i += 1
        if body:
            out.append("<p>%s</p>" % inline(" ".join(body)))
        else:
            i += 1

    return "\n".join(out)


# --------------------------------------------------------------------------
# Source parsing
# --------------------------------------------------------------------------

def load_page(path, slug):
    """Read a course page: title, competencies, body lines (chrome stripped)."""
    raw = path.read_text(encoding="utf-8").split("\n")
    title = raw[0].lstrip("# ").strip()
    comps = []
    body = []
    for line in raw[1:]:
        s = line.strip()
        m = re.match(r"^`Competencies:\s*(.+?)`", s)
        if m:
            comps = [c.strip() for c in m.group(1).split("·") if c.strip()]
            continue
        if s.startswith("`Last reviewed:"):
            continue
        if s.startswith("[← Index]"):
            continue
        body.append(line)
    for c in comps:
        if c not in COMPETENCIES:
            sys.exit("error: %s names unknown competency %r" % (path, c))
    # offset 1: the page's "## What this is about" becomes h3 under the
    # station's h2.
    return {"slug": slug, "title": title, "comps": comps, "pending": None,
            "html": render(body, heading_offset=1, slug_prefix=slug + "-")}


def load_course():
    """Load every entry in COURSE, written or not, in order."""
    pages = []
    for entry in COURSE:
        slug = entry["slug"]
        path = ROOT / "docs" / (slug + ".md")
        if path.exists():
            pages.append(load_page(path, slug))
        elif "pending" in entry:
            pages.append({"slug": slug, "title": entry["nav"], "comps": [],
                          "pending": entry["pending"], "html": ""})
        else:
            sys.exit("error: docs/%s.md is missing and has no `pending` line "
                     "in COURSE" % slug)
    return pages


def readme_sections():
    """Split README.md into {heading: [lines]} plus the intro."""
    raw = (ROOT / "README.md").read_text(encoding="utf-8").split("\n")
    sections, current, key = {}, [], "__intro__"
    for line in raw:
        m = re.match(r"^##\s+(.*)$", line.strip())
        if m:
            sections[key] = current
            key, current = m.group(1), []
        else:
            current.append(line)
    sections[key] = current
    return sections


# --------------------------------------------------------------------------
# Page assembly
# --------------------------------------------------------------------------

CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --paper:#fbfaf8; --paper-2:#f3f1ed; --ink:#1c1a17; --ink-2:#524d45;
  --ink-3:#847d72; --rule:#e0dcd4; --accent:#3d4f63; --accent-soft:#eaeef3;
  --code-bg:#f0eee9; --max:44rem;
  --delegation:#8a6a2f; --delegation-bg:#f7f0e0;
  --description:#2f5d8a; --description-bg:#e4eef7;
  --discernment:#6a4a86; --discernment-bg:#efe8f6;
  --diligence:#3d6b4a; --diligence-bg:#e5f0e8;
}
@media (prefers-color-scheme:dark){
  :root{
    --paper:#16181a; --paper-2:#1e2124; --ink:#e8e6e3; --ink-2:#b0aca6;
    --ink-3:#84807a; --rule:#2f3337; --accent:#9db6d0; --accent-soft:#23303d;
    --code-bg:#22262a;
    --delegation:#d4ac6a; --delegation-bg:#332a17;
    --description:#8fb8dd; --description-bg:#1b2a38;
    --discernment:#b79ad6; --discernment-bg:#2a2136;
    --diligence:#8dc39d; --diligence-bg:#1c2f23;
  }
}
html{scroll-behavior:smooth;scroll-padding-top:1.5rem;-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--paper);color:var(--ink);
  font:16px/1.65 ui-serif,Charter,"Bitstream Charter","Iowan Old Style",Georgia,serif;
  font-feature-settings:"kern","liga";
}
.layout{display:grid;grid-template-columns:16rem minmax(0,1fr);gap:3.5rem;
  max-width:74rem;margin:0 auto;padding:0 1.5rem}

/* Sidebar */
.sidebar{position:sticky;top:0;align-self:start;height:100vh;overflow-y:auto;
  padding:2.5rem 0 3rem;font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
.sidebar .brand{font-weight:650;font-size:.9rem;letter-spacing:-.01em;
  color:var(--ink);text-decoration:none;display:block;line-height:1.3}
.sidebar .brand span{display:block;font-weight:400;font-size:.76rem;color:var(--ink-3);
  margin-top:.2rem}
.sidebar nav{margin-top:1.75rem}
.sidebar .group{font-size:.68rem;text-transform:uppercase;letter-spacing:.09em;
  color:var(--ink-3);margin:1.5rem 0 .5rem;font-weight:600}
.sidebar a.nav{display:block;padding:.26rem 0 .26rem .7rem;font-size:.83rem;
  color:var(--ink-2);text-decoration:none;border-left:2px solid var(--rule);
  transition:color .12s,border-color .12s}
.sidebar a.nav:hover{color:var(--ink)}
.sidebar a.nav.active{color:var(--accent);border-left-color:var(--accent);font-weight:550}
.sidebar a.nav.soon{color:var(--ink-3);font-style:italic}
.sidebar a.nav.soon:hover{color:var(--ink-2)}
.sidebar .foot{margin-top:2rem;padding-top:1rem;border-top:1px solid var(--rule);
  font-size:.72rem;color:var(--ink-3);line-height:1.5}
.sidebar .foot a{color:var(--ink-3)}

/* Content */
main{padding:2.5rem 0 6rem;min-width:0;max-width:var(--max)}
h1,h2,h3,h4{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
  letter-spacing:-.021em;line-height:1.22;color:var(--ink)}
h1{font-size:2.35rem;font-weight:680;margin:0 0 1rem}
h2{font-size:1.42rem;font-weight:640;margin:0 0 .35rem}
h3{font-size:1.12rem;font-weight:640;margin:2.35rem 0 .6rem}
h4{font-size:.95rem;font-weight:640;margin:1.6rem 0 .4rem}
h5{font-size:.86rem;font-weight:650;margin:1.35rem 0 .35rem;color:var(--ink-2);
  text-transform:uppercase;letter-spacing:.05em;
  font-family:ui-sans-serif,system-ui,-apple-system,sans-serif}
h6{font-size:.85rem;font-weight:620;margin:1.2rem 0 .3rem;color:var(--ink-2)}
p{margin:0 0 1rem}
a{color:var(--accent);text-decoration:underline;text-decoration-thickness:1px;
  text-underline-offset:2px}
ul,ol{margin:0 0 1rem;padding-left:1.25rem}
li{margin-bottom:.4rem}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.855em;
  background:var(--code-bg);padding:.1em .35em;border-radius:3px}
pre{background:var(--code-bg);padding:1rem 1.1rem;border-radius:6px;overflow-x:auto;
  margin:0 0 1.25rem;border:1px solid var(--rule)}
pre code{background:none;padding:0;font-size:.83rem;line-height:1.55}
blockquote{margin:0 0 1.25rem;padding:.1rem 0 .1rem 1.1rem;
  border-left:2px solid var(--rule);color:var(--ink-2)}
blockquote p:last-child{margin-bottom:0}
hr{border:0;border-top:1px solid var(--rule);margin:3rem 0}
.table-wrap{overflow-x:auto;margin:0 0 1.35rem;
  -webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;font-size:.87rem;
  font-family:ui-sans-serif,system-ui,-apple-system,sans-serif}
th,td{text-align:left;padding:.5rem .7rem;border-bottom:1px solid var(--rule);
  vertical-align:top}
th{font-weight:620;font-size:.76rem;text-transform:uppercase;letter-spacing:.05em;
  color:var(--ink-3);border-bottom-width:1.5px}
details.expand{margin:0 0 1.35rem;border:1px solid var(--rule);border-radius:6px;
  background:var(--paper-2)}
details.expand summary{cursor:pointer;padding:.6rem .9rem;font-size:.85rem;font-weight:600;
  font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;color:var(--ink-2);
  list-style:none;user-select:none}
details.expand summary::-webkit-details-marker{display:none}
details.expand summary::before{content:"\\203A";display:inline-block;margin-right:.5rem;
  transition:transform .15s;color:var(--ink-3)}
details.expand[open] summary::before{transform:rotate(90deg)}
details.expand summary:hover{color:var(--ink)}
details.expand > *:not(summary){padding-left:.9rem;padding-right:.9rem}
details.expand > *:last-child{padding-bottom:.4rem}

/* Section headers */
section{scroll-margin-top:1.5rem}
.section-head{margin:4.5rem 0 1.5rem;padding-top:1.5rem;border-top:1px solid var(--rule)}
.section-head:first-child{border-top:0;padding-top:0}
.comps{margin-top:.55rem;display:flex;flex-wrap:wrap;gap:.35rem}
.comp{display:inline-block;font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;
  font-size:.66rem;font-weight:650;text-transform:uppercase;letter-spacing:.08em;
  padding:.2rem .5rem;border-radius:3px}
.comp-Delegation{color:var(--delegation);background:var(--delegation-bg)}
.comp-Description{color:var(--description);background:var(--description-bg)}
.comp-Discernment{color:var(--discernment);background:var(--discernment-bg)}
.comp-Diligence{color:var(--diligence);background:var(--diligence-bg)}
.comp-soon{color:var(--ink-3);background:var(--paper-2);border:1px solid var(--rule)}

/* Not-yet-written stations */
section.soon h2{color:var(--ink-2)}
.soon-note{color:var(--ink-3);font-size:.95rem}

/* Hero */
.hero{padding:3.5rem 0 1rem}
.thesis{font-size:1.16rem;line-height:1.55;color:var(--ink);margin:0 0 1.25rem}
.spine{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92rem;
  background:var(--paper-2);border:1px solid var(--rule);border-radius:6px;
  padding:.9rem 1.1rem;margin:0 0 1.25rem;text-align:center;overflow-x:auto;
  white-space:nowrap}
.meta{font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;font-size:.78rem;
  color:var(--ink-3);margin:0}

footer{border-top:1px solid var(--rule);margin-top:5rem;padding:2rem 0 4rem;
  font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;font-size:.82rem;
  color:var(--ink-3)}
footer .reviewed{font-weight:600;color:var(--ink-2)}

@media (max-width:960px){
  .layout{grid-template-columns:1fr;gap:0}
  .sidebar{position:static;height:auto;padding:1.75rem 0 1.25rem;
    border-bottom:1px solid var(--rule)}
  .sidebar nav,.sidebar .foot{display:none}
  main{padding-top:1.5rem}
  .hero{padding-top:2rem}
  h1{font-size:1.85rem}
}
"""

JS = r"""
/* Scroll-spy. Nav order and document order are not identical -- the
   "What this course is not" link points into the intro page -- so targets are
   sorted by document position before the first-visible scan. */
(function(){
  var links = [].slice.call(document.querySelectorAll(".sidebar a.nav"));
  var map = {};
  links.forEach(function(l){ map[l.getAttribute("href").slice(1)] = l; });
  var targets = Object.keys(map)
    .map(function(id){ return document.getElementById(id); })
    .filter(Boolean)
    .sort(function(a, b){
      return (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING) ? -1 : 1;
    });
  if (!targets.length) return;

  var visible = {};
  var obs = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ visible[e.target.id] = e.isIntersecting; });
    var current = null;
    for (var i = 0; i < targets.length; i++){
      if (visible[targets[i].id]){ current = targets[i].id; break; }
    }
    if (!current) return;
    links.forEach(function(l){ l.classList.remove("active"); });
    if (map[current]){
      map[current].classList.add("active");
      map[current].scrollIntoView({block:"nearest"});
    }
  }, {rootMargin:"0px 0px -70% 0px", threshold:0});

  targets.forEach(function(t){ obs.observe(t); });
})();
"""


def build():
    sec = readme_sections()
    pages = load_course()

    intro = sec["__intro__"]
    thesis = next(l.strip().strip("*") for l in intro if l.strip().startswith("**"))

    # Sidebar
    nav = ['<a class="brand" href="#top">Claude, your new Employee'
           '<span>A course in five stations</span></a>', "<nav>"]
    nav.append('<div class="group">The course</div>')
    for p in pages:
        nav.append('<a class="nav%s" href="#%s">%s</a>' % (
            " soon" if p["pending"] else "", p["slug"], html.escape(p["title"])))
    nav.append('<div class="group">About the course</div>')
    nav.append('<a class="nav" href="#00-intro-what-this-course-is-not">'
               "What this course is not</a>")
    nav.append('<a class="nav" href="#freshness">Freshness</a>')
    nav.append('<a class="nav" href="#about">Author &amp; license</a>')
    nav.append("</nav>")
    nav.append('<div class="foot">Canonical source is <code>docs/</code>.<br>'
               'This page is generated from it.<br><br>'
               '<a href="%s">Repository</a></div>' % html.escape(REPO_URL))

    def section(p):
        if p["pending"]:
            chips = '<div class="comps"><span class="comp comp-soon">Not yet ' \
                    "published</span></div>"
            body = '<p class="soon-note">%s</p>' % inline(p["pending"])
            cls = ' class="soon"'
        else:
            chips = ""
            if p["comps"]:
                chips = '<div class="comps">%s</div>' % "".join(
                    '<span class="comp comp-%s">%s</span>' % (c, c) for c in p["comps"])
            body = p["html"]
            cls = ""
        return (
            '<section id="%s"%s>\n'
            '<div class="section-head"><h2>%s</h2>%s</div>\n'
            "%s\n</section>" % (p["slug"], cls, html.escape(p["title"]), chips, body)
        )

    body = []
    body.append('<div class="hero" id="top">')
    body.append("<h1>Claude, your new Employee</h1>")
    body.append('<p class="thesis">%s</p>' % inline(thesis))
    body.append('<div class="spine">%s</div>' % SPINE)
    body.append(render(sec["The five stations"], heading_offset=2, slug_prefix="stations-"))
    body.append('<p class="meta">A course, not a reference. There is a reading order '
                'and it is not decorative.</p>')
    body.append("</div>")

    body.extend(section(p) for p in pages)

    body.append('<section id="freshness"><div class="section-head"><h2>Freshness</h2></div>')
    body.append(render(sec["Freshness"], heading_offset=2, slug_prefix="fresh-"))
    body.append("</section>")

    body.append('<section id="about"><div class="section-head">'
                "<h2>Contributing, license, author</h2></div>")
    body.append(render(sec["Contributing"], heading_offset=2, slug_prefix="contrib-"))
    body.append(render(sec["License"], heading_offset=2, slug_prefix="lic-"))
    body.append(render(sec["Author"], heading_offset=2, slug_prefix="author-"))
    body.append("</section>")

    doc = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Claude, your new Employee</title>
<meta name="description" content="A course in five stations, built along an employment relationship: the interview, the onboarding, the first real day, tools and access, promotion.">
<meta name="author" content="Billie Jeurink">
<meta property="og:title" content="Claude, your new Employee">
<meta property="og:description" content="Most courses on this subject demonstrate features. This one is built along an employment relationship — from the interview to the promotion.">
<meta property="og:type" content="website">
<!--
  GENERATED FILE - do not edit by hand.
  Canonical source is README.md and docs/. Regenerate with:  python3 build-site.py
-->
<style>__CSS__</style>
</head>
<body>
<div class="layout">
<aside class="sidebar">__NAV__</aside>
<main>
__BODY__
<footer>
<p><span class="reviewed">Last reviewed: __REVIEWED__</span> &mdash; reviewed, not merely updated.
Reviewed monthly and after any significant Claude platform release.</p>
<p>Written and maintained by Billie Jeurink.
<a href="mailto:billie@bjeurink.com">billie@bjeurink.com</a>.
Licensed <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>.</p>
<p>The canonical source for this content is <code>docs/</code> in the repository.
This page is generated from it by <code>build-site.py</code>; where they disagree, the docs are right.</p>
</footer>
</main>
</div>
<script>__JS__</script>
</body>
</html>
"""
    doc = doc.replace("__CSS__", CSS.strip())
    doc = doc.replace("__NAV__", "\n".join(nav))
    doc = doc.replace("__BODY__", "\n".join(body))
    doc = doc.replace("__REVIEWED__", LAST_REVIEWED)
    doc = doc.replace("__JS__", JS.strip())

    out = ROOT / "site" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    written = [p for p in pages if not p["pending"]]
    print("wrote %s (%.1f KB)" % (out, len(doc) / 1024))
    print("  %d course pages written, %d still pending"
          % (len(written), len(pages) - len(written)))


if __name__ == "__main__":
    build()
