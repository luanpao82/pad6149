#!/usr/bin/env python3
"""Convert assignment markdown -> Canvas-ready HTML fragments.

Reads:
  ../Assignments/Week*.md            -> html/optB-weekNN.html   (Option B, Build)
  ../Assignments/ePortfolio/Week*.md -> html/optA-weekNN.html   (Option A, ePortfolio)
  _sources/*.md                      -> html/<stem>.html        (common case, choose-your-path)

Week 11 is skipped in both tracks (covered by the common Leadership Case).
Strips the H1 title and the "**Due:** ... | **Points:** ..." line (those go in
Canvas fields). Obsidian callouts -> gold-accent blockquotes with inline styles
(Canvas RCE keeps inline styles). Wikilinks -> plain display text.

Also prints a TSV metadata table (name, title, points, due) to stdout.

Usage:  python3 build_canvas.py
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
REPO = ROOT.parent
OUT = ROOT / "html"
OUT.mkdir(exist_ok=True)

BQ_STYLE = ('border-left:4px solid #FFC904;background:#fffdf3;'
            'padding:8px 14px;margin:12px 0;border-radius:4px;')
TABLE_STYLE = 'border-collapse:collapse;width:100%;margin:10px 0;'
TH_STYLE = 'border:1px solid #ccc;padding:6px 10px;background:#1f1f1f;color:#fff;text-align:left;'
TD_STYLE = 'border:1px solid #ccc;padding:6px 10px;text-align:left;vertical-align:top;'

CALLOUT_RE = re.compile(r"^> \[!(\w+)\](.*)\n((?:^>.*\n?)*)", re.MULTILINE)

def strip_comments(md):
    return re.sub(r"<!--.*?-->", "", md, flags=re.DOTALL)

def transform_callouts(md):
    """'> [!info] Title\\n> body' -> '> **Title**\\n> body' (stays a blockquote)."""
    def sub(m):
        kind, title = m.group(1), m.group(2).strip()
        body = m.group(3)
        label = title if title else kind.capitalize()
        return f"> **{label}**\n>\n{body}\n"
    return CALLOUT_RE.sub(sub, md)

def strip_wikilinks(md):
    md = re.sub(r"\[\[Week\s+\d+[a-z]?\s+([^\]]+)\]\]", r"\1", md)
    md = re.sub(r"\[\[([^\]]+)\]\]", r"\1", md)
    return md

def parse_header(lines):
    title = re.sub(r"^#+\s*", "", lines[0]).strip()
    h1 = title.split(":", 1)[1].strip() if ":" in title else title
    due = pts = ""
    body_start = 1
    for i, ln in enumerate(lines[1:6], start=1):
        if ln.strip().startswith("**Due:**"):
            for part in ln.split("|"):
                mm = re.match(r"\s*\*\*([^*]+):\*\*\s*(.+?)\s*$", part)
                if mm:
                    k, v = mm.group(1).strip().lower(), mm.group(2).strip()
                    if k == "due":
                        due = v
                    elif k == "points":
                        pts = v
            body_start = i + 1
            break
    return h1, due, pts, body_start

def pandoc(md):
    p = subprocess.run(
        ["pandoc", "-f", "markdown+pipe_tables-smart", "-t", "html", "--wrap=none"],
        input=md, capture_output=True, text=True, check=True,
    )
    return p.stdout

def style_html(html):
    html = html.replace("<blockquote>", f'<blockquote style="{BQ_STYLE}">')
    html = html.replace("<table>", f'<table style="{TABLE_STYLE}">')
    html = html.replace("<th>", f'<th style="{TH_STYLE}">')
    html = html.replace("<td>", f'<td style="{TD_STYLE}">')
    html = re.sub(r"<h([1-6])>", r'<h\1 style="margin:14px 0 6px;">', html)
    return html.strip()

def convert(md_path, out_name):
    raw = md_path.read_text()
    raw = strip_comments(raw)
    lines = raw.splitlines()
    h1, due, pts, body_start = parse_header(lines)
    body = "\n".join(lines[body_start:]).strip()
    body = transform_callouts(body)
    body = strip_wikilinks(body)
    html = style_html(pandoc(body))
    (OUT / f"{out_name}.html").write_text(html)
    return h1, pts, due

def slug(md_path, prefix):
    m = re.match(r"Week\s+(\d+)([a-z]?)\s", md_path.stem)
    num, suf = int(m.group(1)), m.group(2)
    return f"{prefix}-week{num:02d}{suf}"

def main():
    rows = []
    jobs = []
    for md in sorted((REPO / "Assignments").glob("Week *.md")):
        if md.stem.startswith("Week 11 "):
            continue
        jobs.append((md, slug(md, "optB")))
    for md in sorted((REPO / "Assignments" / "ePortfolio").glob("Week *.md")):
        if md.stem.startswith("Week 11 "):
            continue
        jobs.append((md, slug(md, "optA")))
    for md in sorted((ROOT / "_sources").glob("*.md")):
        jobs.append((md, md.stem))

    for md, name in jobs:
        h1, pts, due = convert(md, name)
        rows.append((name, h1, pts, due))
        print(f"  ✓ html/{name}.html")

    print("\nNAME\tTITLE\tPOINTS\tDUE")
    for r in rows:
        print("\t".join(r))
    print(f"\n{len(rows)} fragment(s) written to {OUT}/")

if __name__ == "__main__":
    main()
