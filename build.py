#!/usr/bin/env python3
"""Build weekNN.html from Assignments/Week*.md.

Usage:
    python3 build.py            # build all
    python3 build.py week04a    # build one
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
ASSIGN = ROOT / "Assignments"
TEMPLATE = (ROOT / "_template.html").read_text()

CALLOUT_CLASS = {
    "warning": "card card-warn",
    "danger": "card card-warn",
    "info": "card card-info",
    "note": "card card-note",
    "tip": "card card-note",
    "example": "card card-example",
}

def parse_filename(md_path):
    """'Week 4a Mentor Interview Report.md' -> ('week04a', '04a')."""
    m = re.match(r"Week\s+(\d+)([a-z]?)\s", md_path.stem)
    num, suf = int(m.group(1)), m.group(2)
    return f"week{num:02d}{suf}", f"{num:02d}{suf}"

def build_wikilink_map():
    """Map '[[Week 4b Board Governance Policy]]' display + href."""
    mapping = {}
    for md in ASSIGN.glob("Week *.md"):
        slug, _ = parse_filename(md)
        key = md.stem  # "Week 4a Mentor Interview Report"
        # Display = strip "Week N[a-z] " prefix
        display = re.sub(r"^Week\s+\d+[a-z]?\s+", "", key)
        mapping[key] = (f"{slug}.html", display)
    return mapping

def replace_wikilinks(text, wmap):
    def sub(m):
        key = m.group(1).strip()
        if key in wmap:
            href, disp = wmap[key]
            return f'<a href="{href}">{disp}</a>'
        return m.group(0)  # leave unresolved as-is
    return re.sub(r"\[\[([^\]]+)\]\]", sub, text)

CALLOUT_RE = re.compile(
    r"^> \[!(\w+)\](.*)\n((?:^>.*\n?)*)", re.MULTILINE
)

def extract_callouts(text):
    """Replace callouts with raw-HTML placeholder divs; return (text, [(ph, html)])."""
    callouts = []
    def sub(m):
        kind = m.group(1).lower()
        title = m.group(2).strip()
        body_lines = m.group(3).splitlines()
        body_md = "\n".join(line[2:] if line.startswith("> ") else line[1:] for line in body_lines).strip()
        body_html = pandoc_md_to_html(body_md) if body_md else ""
        cls = CALLOUT_CLASS.get(kind, "card card-note")
        title_html = f'<h4 style="margin-top:0">{title}</h4>\n' if title else ""
        html = f'<div class="{cls}">\n{title_html}{body_html}</div>'
        ph = f'<div data-callout-id="{len(callouts)}"></div>'
        callouts.append((ph, html))
        return f"\n\n{ph}\n\n"
    new_text = CALLOUT_RE.sub(sub, text)
    return new_text, callouts

def pandoc_md_to_html(md):
    if not md.strip():
        return ""
    proc = subprocess.run(
        ["pandoc", "-f", "markdown+pipe_tables-smart", "-t", "html", "--wrap=none"],
        input=md, capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()

def parse_subtitle(line):
    """'**Due:** ... | **Points:** 8 pts | **Length:** 4-5 pages' -> dict."""
    items = {}
    for part in line.split("|"):
        m = re.match(r"\s*\*\*([^*]+):\*\*\s*(.+?)\s*$", part)
        if m:
            items[m.group(1).strip().lower()] = m.group(2).strip()
    return items

def build_one(md_path, wmap):
    slug, num = parse_filename(md_path)
    raw = md_path.read_text()
    lines = raw.splitlines()

    # Title from first line "# Week 4: Mentor Interview Report"
    title_line = re.sub(r"^#+\s*", "", lines[0]).strip()
    h1 = title_line.split(":", 1)[1].strip() if ":" in title_line else title_line

    # Subtitle: first '**Due:**' line
    subtitle_idx = next(
        (i for i, ln in enumerate(lines) if ln.strip().startswith("**Due:**")), None
    )
    subtitle_meta = parse_subtitle(lines[subtitle_idx]) if subtitle_idx is not None else {}

    body_start = subtitle_idx + 1 if subtitle_idx is not None else 1
    body_md = "\n".join(lines[body_start:]).strip()

    body_md = replace_wikilinks(body_md, wmap)
    body_md, callouts = extract_callouts(body_md)
    body_html = pandoc_md_to_html(body_md)
    for i, (_, html) in enumerate(callouts):
        body_html = re.sub(
            rf'<div data-callout-id="{i}">\s*</div>',
            lambda m, h=html: h, body_html, count=1,
        )

    badges = []
    week_label = re.match(r"Week\s+\d+[a-z]?", title_line)
    if week_label:
        badges.append(f'<span class="badge badge-gold">{week_label.group(0)}</span>')
    if "points" in subtitle_meta:
        badges.append(f'<span class="badge">{subtitle_meta["points"]}</span>')

    subtitle_parts = []
    if "due" in subtitle_meta:
        subtitle_parts.append(f"Due: {subtitle_meta['due']}")
    if "points" in subtitle_meta:
        subtitle_parts.append(subtitle_meta["points"])
    if "length" in subtitle_meta:
        subtitle_parts.append(subtitle_meta["length"])
    elif "deliverable" in subtitle_meta:
        subtitle_parts.append(subtitle_meta["deliverable"])
    subtitle_text = " · ".join(subtitle_parts)

    out = TEMPLATE
    out = out.replace("{{TITLE}}", title_line)
    out = out.replace("{{H1}}", h1)
    out = out.replace("{{BADGES}}", " ".join(badges))
    out = out.replace("{{SUBTITLE}}", subtitle_text)
    out = out.replace("{{BODY}}", body_html)

    # Sidebar active state
    for placeholder in re.findall(r"\{\{ACTIVE_(\w+)\}\}", out):
        marker = ' class="active"' if placeholder == slug else ""
        out = out.replace(f"{{{{ACTIVE_{placeholder}}}}}", marker)

    out_path = ROOT / f"{slug}.html"
    out_path.write_text(out)
    print(f"  ✓ {slug}.html  ← {md_path.name}")
    return out_path

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    wmap = build_wikilink_map()
    mds = sorted(ASSIGN.glob("Week *.md"))
    built = 0
    for md in mds:
        slug, _ = parse_filename(md)
        if target and slug != target:
            continue
        build_one(md, wmap)
        built += 1
    print(f"\nBuilt {built} page(s).")

if __name__ == "__main__":
    main()
