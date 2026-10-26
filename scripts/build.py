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
    ("politics", "Israeli politics"),
    ("israel", "Israel today"),
    ("ai", "Artificial intelligence"),
    ("nature", "Nature"),
    ("spacex", "SpaceX"),
    ("study", "Daily study"),
]


def e(s):
    return html.escape(str(s or ""), quote=True)


def fail(msg):
    sys.exit(f"build.py: {msg}")


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


def paras(items):
    return "".join(f"<p>{e(p)}</p>" for p in items or [])


def page(name, number, content):
    return (f'<section class="page" data-name="{e(name)}" aria-label="{e(name)}">'
            f'<div class="inner"><div class="folio"><strong>{e(name)}</strong>'
            f'<span>Page {number}</span></div>{content}</div></section>')


def news(d):
    lead = d.get("lead") or fail("news section is missing 'lead'")
    for k in ("headline", "paragraphs"):
        if not lead.get(k):
            fail(f"lead is missing '{k}'")
    out = (f'<article class="lead"><h2>{e(lead["headline"])}</h2>'
           f'<p class="stand">{e(lead.get("standfirst"))}</p>'
           f'<div class="body">{paras(lead["paragraphs"])}</div>')
    if lead.get("sources"):
        out += f'<p class="source">Sources: {source_links(lead["sources"])}</p>'
    out += "</article>"
    briefs = d.get("briefs") or []
    if briefs:
        out += '<div class="briefs">'
        for b in briefs:
            src = source_links([{"name": b.get("source") or "Source", "url": b.get("url")}]) if b.get("url") else ""
            out += (f'<div class="brief"><h3>{e(b["headline"])}</h3>'
                    f'<p>{e(b["text"])} {src}</p></div>')
        out += "</div>"
    return out


def nature(d):
    for k in ("headline", "url", "paragraphs", "key_points"):
        if not d.get(k):
            fail(f"nature is missing '{k}'")
    points = "".join(f"<li>{e(p)}</li>" for p in d["key_points"])
    return (f'<article class="lead"><h2>{e(d["headline"])}</h2>'
            f'<p class="stand">{e(d.get("standfirst"))}</p>'
            f'<div class="body">{paras(d["paragraphs"])}</div>'
            f'<ol class="points">{points}</ol>'
            f'<a class="readlink" href="{e(d["url"])}">Read the article on {e(d.get("source") or "nature.com")}</a>'
            f'</article>')


def spacex(d):
    if d.get("quiet"):
        return (f'<article class="lead"><h2>No major SpaceX news today</h2>'
                f'<p class="stand">{e(d.get("note") or "Nothing worth your time since yesterday.")}</p></article>')
    return news(d)


def study(d):
    for k in ("track", "title", "what", "how", "why_xlio", "question", "answer"):
        if not d.get(k):
            fail(f"study is missing '{k}'")
    rows = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in d.get("numbers") or [])
    out = (f'<article class="lead"><h2>{e(d["title"])}</h2>'
           f'<p class="stand">{e(d["track"])}</p><dl>'
           f'<dt>What it is</dt><dd>{e(d["what"])}</dd>'
           f'<dt>How it works</dt><dd>{e(d["how"])}</dd>'
           f'<dt>Why it matters for XLIO</dt><dd>{e(d["why_xlio"])}</dd>')
    if d.get("example"):
        out += f'<dt>Example</dt><dd>{e(d["example"])}</dd>'
    if rows:
        out += f'<dt>Key numbers</dt><dd><table class="numbers">{rows}</table></dd>'
    if d.get("pitfall"):
        out += f'<dt>Common pitfall</dt><dd>{e(d["pitfall"])}</dd>'
    out += (f'</dl><details><summary>Self-test: {e(d["question"])}</summary>'
            f'<p>{e(d["answer"])}</p></details>')
    if d.get("reading"):
        out += f'<p class="source">Further reading: {source_links(d["reading"])}</p>'
    return out + "</article>"


RENDER = {"politics": news, "israel": news, "ai": news, "nature": nature, "spacex": spacex, "study": study}


def teaser(key, d):
    if key == "spacex" and d.get("quiet"):
        return "Quiet day"
    if key in ("nature",):
        return d["headline"]
    if key == "study":
        return d["title"]
    return d["lead"]["headline"]


def front(date, issue_no, sections):
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
        for i, (key, name) in enumerate(SECTIONS, start=1))
    return (f'<section class="page" data-name="Front page" aria-label="Front page"><div class="inner">'
            f'<header class="masthead"><h1>{e(PAPER)}</h1>'
            f'<div class="dateline"><span>{e(long_date(date))}</span><span>No. {issue_no}</span></div></header>'
            f'{listen}<nav class="contents" aria-label="Contents"><h2>In this issue</h2><ol>{items}</ol></nav>'
            f'<a class="archive" href="../../">Past issues</a></div></section>')


def all_issues():
    return sorted(p.parent.name for p in (DOCS / "issues").glob("*/issue.json"))


def write_archive():
    issues = list(reversed(all_issues()))
    rows = ""
    for d in issues:
        data = json.loads((DOCS / "issues" / d / "issue.json").read_text())
        rows += (f'<li><a href="issues/{d}/">{e(long_date(d))}</a>'
                 f'<span>{e(data["sections"]["politics"]["lead"]["headline"])}</span></li>')
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
<body><main><h1>{e(PAPER)}</h1><h2>Past issues</h2><ul>{rows}</ul></main></body></html>""")
    if issues:
        latest = DOCS / "latest"
        latest.mkdir(exist_ok=True)
        (latest / "index.html").write_text(
            f'<!DOCTYPE html><meta http-equiv="refresh" content="0; url=../issues/{issues[0]}/">'
            f'<a href="../issues/{issues[0]}/">Latest issue</a>')


def main():
    if len(sys.argv) != 2:
        fail("usage: build.py YYYY-MM-DD")
    date = sys.argv[1]
    folder = DOCS / "issues" / date
    src = folder / "issue.json"
    if not src.exists():
        fail(f"{src} not found")
    data = json.loads(src.read_text())
    sections = data.get("sections") or fail("issue.json is missing 'sections'")
    for key, _ in SECTIONS:
        if key not in sections:
            fail(f"missing section '{key}'")

    issue_no = all_issues().index(date) + 1
    pages = [front(date, issue_no, sections)]
    for i, (key, name) in enumerate(SECTIONS, start=2):
        pages.append(page(name, i, RENDER[key](sections[key])))

    out = TEMPLATE.read_text()
    out = out.replace("{{TITLE}}", e(f"{PAPER}, {long_date(date)}")).replace("{{PAGES}}", "\n".join(pages))
    (folder / "index.html").write_text(out)
    write_archive()
    print(f"Built issue No. {issue_no}: docs/issues/{date}/index.html")


if __name__ == "__main__":
    main()
