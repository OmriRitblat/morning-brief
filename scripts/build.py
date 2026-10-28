#!/usr/bin/env python3
"""Render docs/issues/<date>/issue.json into index.html and refresh the archive.

Usage: python3 scripts/build.py YYYY-MM-DD
"""
import datetime
import html
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TEMPLATE = ROOT / "template" / "issue.html"
PAPER = "The Seven O'Clock"

# Fixed page order. Page 1 is always the front page.
SECTIONS = [
    ("israel", "Israel News"),
    ("us", "US News & Stock Market"),
    ("ai", "Artificial intelligence"),
    ("nature", "Nature"),
    ("spacex", "SpaceX"),
    ("study", "Daily study"),
]
# Left out of the issue entirely when there's nothing worth reporting.
OPTIONAL = {"spacex"}


def e(s):
    return html.escape(str(s or ""), quote=True)


def fail(msg):
    sys.exit(f"build.py: {msg}")


def require(d, keys, where):
    for k in keys:
        if not d.get(k):
            fail(f"{where} is missing '{k}'")


def long_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d:%A}, {d.day} {d:%B %Y}"


def source_links(sources):
    parts = []
    for s in sources or []:
        if s.get("url"):
            parts.append(f'<a href="{e(s["url"])}">{e(s.get("name") or s["url"])}</a>')
        else:
            parts.append(e(s.get("name")))
    return ", ".join(parts)


def sources_line(sources, label="Sources"):
    return f'<p class="source">{label}: {source_links(sources)}</p>' if sources else ""


def paras(items):
    return "".join(f"<p>{e(p)}</p>" for p in items or [])


def terms(items):
    """Jargon box: [["term", "plain explanation"], ...]."""
    if not items:
        return ""
    rows = "".join(f"<dt>{e(t)}</dt><dd>{e(m)}</dd>" for t, m in items)
    return f'<aside class="terms"><p class="terms-h">Jargon, explained</p><dl>{rows}</dl></aside>'


def page(name, number, content):
    return (f'<section class="page" data-name="{e(name)}" aria-label="{e(name)}">'
            f'<div class="inner"><div class="folio"><strong>{e(name)}</strong>'
            f'<span>Page {number}</span></div>{content}</div></section>')


def news(d, where):
    lead = d.get("lead") or fail(f"{where} is missing 'lead'")
    require(lead, ("headline", "paragraphs"), f"{where} lead")
    out = (f'<article class="lead"><h2>{e(lead["headline"])}</h2>'
           f'<p class="stand">{e(lead.get("standfirst"))}</p>'
           f'<div class="body">{paras(lead["paragraphs"])}</div>'
           f'{sources_line(lead.get("sources"))}</article>')
    briefs = d.get("briefs") or []
    if briefs:
        out += '<div class="briefs">'
        for b in briefs:
            src = source_links([{"name": b.get("source") or "Source", "url": b.get("url")}]) if b.get("url") else ""
            out += (f'<div class="brief"><h3>{e(b["headline"])}</h3>'
                    f'<p>{e(b["text"])} {src}</p></div>')
        out += "</div>"
    return out


def us(d):
    items = d.get("items") or fail("us is missing 'items'")
    if len(items) > 2:
        fail("us has more than 2 items")
    out = ""
    for i, it in enumerate(items):
        require(it, ("label", "headline", "paragraphs"), "us item")
        out += (f'<article class="{"lead" if i == 0 else "lead second"}">'
                f'<p class="label">{e(it["label"])}</p><h2>{e(it["headline"])}</h2>'
                f'<div class="body">{paras(it["paragraphs"])}</div>')
        if it.get("why_it_matters"):
            out += f'<p class="why"><strong>Why it matters:</strong> {e(it["why_it_matters"])}</p>'
        out += f'{sources_line(it.get("sources"))}</article>'
    return out


def ai(d):
    stories = d.get("stories") or fail("ai is missing 'stories'")
    out = ""
    for i, s in enumerate(stories):
        require(s, ("headline", "what_happened", "what_it_means", "why_it_matters"), "ai story")
        out += (f'<article class="{"lead" if i == 0 else "lead second"} story"><h2>{e(s["headline"])}</h2>'
                f'<p class="stand">{e(s.get("standfirst"))}</p><dl>'
                f'<dt>What happened</dt><dd>{e(s["what_happened"])}</dd>'
                f'<dt>What it means, in plain words</dt><dd>{e(s["what_it_means"])}</dd>'
                f'<dt>Why it matters and how it could be used</dt><dd>{e(s["why_it_matters"])}</dd>'
                f'</dl>{terms(s.get("terms"))}{sources_line(s.get("sources"))}</article>')
    return out


def nature(d):
    require(d, ("headline", "url", "paragraphs", "key_points"), "nature")
    points = "".join(f"<li>{e(p)}</li>" for p in d["key_points"])
    return (f'<article class="lead"><h2>{e(d["headline"])}</h2>'
            f'<p class="stand">{e(d.get("standfirst"))}</p>'
            f'<div class="body">{paras(d["paragraphs"])}</div>'
            f'<ol class="points">{points}</ol>{terms(d.get("terms"))}'
            f'<a class="readlink" href="{e(d["url"])}">Read the article on {e(d.get("source") or "nature.com")}</a>'
            f'</article>')


def study(d):
    require(d, ("track", "title", "big_idea", "background", "steps", "example", "why_xlio",
                "question", "answer"), "study")
    steps = "".join(f"<li>{e(s)}</li>" for s in d["steps"])
    rows = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in d.get("numbers") or [])
    out = (f'<article class="lead study"><h2>{e(d["title"])}</h2>'
           f'<p class="stand">{e(d["track"])}</p>'
           f'<p class="bigidea"><strong>The big idea:</strong> {e(d["big_idea"])}</p><dl>'
           f'<dt>First, the basics</dt><dd>{paras(d["background"])}</dd>'
           f'<dt>How it works, step by step</dt><dd><ol class="steps">{steps}</ol></dd>'
           f'<dt>A practical example</dt><dd>{e(d["example"])}</dd>'
           f'<dt>Why it matters for XLIO</dt><dd>{e(d["why_xlio"])}</dd>')
    if rows:
        out += f'<dt>Key numbers</dt><dd><table class="numbers">{rows}</table></dd>'
    if d.get("pitfall"):
        out += f'<dt>Common misconception</dt><dd>{e(d["pitfall"])}</dd>'
    out += (f'</dl>{terms(d.get("terms"))}'
            f'<details><summary>Self-test: {e(d["question"])}</summary><p>{e(d["answer"])}</p></details>')
    if d.get("reading"):
        out += sources_line(d["reading"], "Further reading")
    return out + "</article>"


RENDER = {
    "israel": lambda d: news(d, "israel"),
    "us": us,
    "ai": ai,
    "nature": nature,
    "spacex": lambda d: news(d, "spacex"),
    "study": study,
}


def teaser(key, d):
    if key in ("nature", "study"):
        return d.get("headline") or d["title"]
    if key == "us":
        return " · ".join(it["headline"] for it in d["items"])
    if key == "ai":
        return d["stories"][0]["headline"]
    return d["lead"]["headline"]


def present(sections):
    """The sections that appear in this issue, in page order."""
    out = []
    for key, name in SECTIONS:
        d = sections.get(key)
        if not d or d.get("quiet"):
            if key in OPTIONAL:
                continue
            fail(f"missing section '{key}'")
        out.append((key, name))
    return out


def front(date, issue_no, sections, shown):
    bot = os.environ.get("TELEGRAM_BOT_USERNAME", "").lstrip("@")
    listen = ""
    if bot:
        listen = (f'<a class="episode" href="https://t.me/{e(bot)}">'
                  '<span class="play" aria-hidden="true"><svg viewBox="0 0 10 12"><path d="M0 0 L10 6 L0 12 Z"/></svg></span>'
                  '<div><p class="t">Listen to today\'s issue</p>'
                  '<p class="s">Two hosts walk through every section, in Telegram</p></div></a>')
    items = "".join(
        f'<li><button data-goto="{i}"><span class="sec">{e(name)}</span>'
        f'<span class="pg">p. {i + 1}</span><span class="hl">{e(teaser(key, sections[key]))}</span></button></li>'
        for i, (key, name) in enumerate(shown, start=1))
    return (f'<section class="page" data-name="Front page" aria-label="Front page"><div class="inner">'
            f'<header class="masthead"><h1>{e(PAPER)}</h1>'
            f'<div class="dateline"><span>{e(long_date(date))}</span><span>No. {issue_no}</span></div></header>'
            f'{listen}<nav class="contents" aria-label="Contents"><h2>In this issue</h2><ol>{items}</ol></nav>'
            f'<a class="archive" href="../../">Past issues</a></div></section>')


def all_issues():
    return sorted(p.parent.name for p in (DOCS / "issues").glob("*/issue.json"))


def archive_headline(sections):
    # Older issues used a separate "politics" section.
    s = sections.get("israel") or sections.get("politics")
    return s["lead"]["headline"]


def write_archive():
    issues = list(reversed(all_issues()))
    rows = ""
    for d in issues:
        data = json.loads((DOCS / "issues" / d / "issue.json").read_text(encoding="utf-8"))
        rows += (f'<li><a href="issues/{d}/">{e(long_date(d))}</a>'
                 f'<span>{e(archive_headline(data["sections"]))}</span></li>')
    (DOCS / "index.html").write_text(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(PAPER)}: past issues</title>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,600&family=UnifrakturMaguntia&display=swap" rel="stylesheet">
<style>:root{{--paper:#EFE7D3;--ink:#1A1814;--muted:#5C5446;--rule:#BFB297;--accent:#23406B;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root{{--paper:#1C1A16;--ink:#E9E1CD;--muted:#A99F8B;--rule:#463F33;--accent:#9DB4D8;color-scheme:dark}}}}
body{{margin:0;background:var(--paper);color:var(--ink);font:18px/1.5 Newsreader,Georgia,serif}}
main{{max-width:720px;margin:0 auto;padding:24px 20px}}h1{{font:400 clamp(40px,10vw,72px)/1 UnifrakturMaguntia,serif;text-align:center;margin:0 0 10px}}
h2{{border-top:3px double var(--ink);border-bottom:1px solid var(--ink);padding:6px 0;font-size:16px;font-weight:600;color:var(--muted);margin:0}}
ul{{list-style:none;padding:0;margin:0}}li{{border-bottom:1px solid var(--rule);padding:12px 0;display:grid;gap:2px}}
a{{color:var(--accent);font-weight:600}}span{{color:var(--muted);font-size:15px}}</style></head>
<body><main><h1>{e(PAPER)}</h1><h2>Past issues</h2><ul>{rows}</ul></main></body></html>""", encoding="utf-8")
    if issues:
        latest = DOCS / "latest"
        latest.mkdir(exist_ok=True)
        (latest / "index.html").write_text(
            f'<!DOCTYPE html><meta http-equiv="refresh" content="0; url=../issues/{issues[0]}/">'
            f'<a href="../issues/{issues[0]}/">Latest issue</a>', encoding="utf-8")


def main():
    if len(sys.argv) != 2:
        fail("usage: build.py YYYY-MM-DD")
    date = sys.argv[1]
    folder = DOCS / "issues" / date
    src = folder / "issue.json"
    if not src.exists():
        fail(f"{src} not found")
    data = json.loads(src.read_text(encoding="utf-8"))
    sections = data.get("sections") or fail("issue.json is missing 'sections'")
    shown = present(sections)

    issue_no = all_issues().index(date) + 1
    pages = [front(date, issue_no, sections, shown)]
    for i, (key, name) in enumerate(shown, start=2):
        pages.append(page(name, i, RENDER[key](sections[key])))

    out = TEMPLATE.read_text(encoding="utf-8")
    out = out.replace("{{TITLE}}", e(f"{PAPER}, {long_date(date)}")).replace("{{PAGES}}", "\n".join(pages))
    (folder / "index.html").write_text(out, encoding="utf-8")
    write_archive()
    print(f"Built issue No. {issue_no}: docs/issues/{date}/index.html ({len(shown)} sections)")


if __name__ == "__main__":
    main()
