#!/usr/bin/env python3
"""Build reveal.js decks from Obsidian-friendly markdown.

Usage:
    python3 build_slides.py            # build all decks in md/
    python3 build_slides.py overview   # build one deck (md/overview.md)

Source format (md/*.md):

    ---
    title: "Deck title (HTML <title>)"
    footer_left: "Left footer"
    footer_right: "Right footer"
    ---

    # Title Slide Heading
    *Label Text*

    First paragraph becomes the subtitle.

    Meta line one
    Meta line two

    > [!notes]
    > Speaker notes here

    ---

    ## Regular Slide Heading
    *Label Text*

    Body markdown: **bold**, *italic*, lists, tables, raw HTML.

    > [!highlight]
    > Gold-background callout.

    > [!dark]
    > Dark-background callout.

    > [!quote] Attribution line
    > Quote body. **Bold** inside renders as a gold accent.

    > [!notes]
    > Speaker notes.

    ---

Slide separators are lines containing only `---` (outside the opening
frontmatter). Fenced divs (`::: two-col`, `::: compare`, …) and raw HTML
pass through to pandoc unchanged. Callouts keep their position in the
slide; `[!notes]` is always collected into `<aside class="notes">` at the
end of the section.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
MD_DIR = ROOT / "md"
TEMPLATE = (ROOT / "_deck_template.html").read_text()


# ---------- pandoc ----------

def pandoc(md: str) -> str:
    if not md.strip():
        return ""
    proc = subprocess.run(
        ["pandoc",
         "-f", "markdown+fenced_divs+pipe_tables-smart-auto_identifiers",
         "-t", "html", "--wrap=none"],
        input=md, capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()


def extract_html_blocks(text: str) -> tuple[str, dict[str, str]]:
    """Pull top-level HTML blocks out as placeholders.

    A block is any run of non-blank lines where the first line starts with
    `<` at column 0. This lets the markdown source keep indented, readable
    HTML without pandoc trying to reinterpret nested tags.
    """
    lines = text.split("\n")
    out: list[str] = []
    blocks: dict[str, str] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        at_block_start = (
            line.startswith("<")
            and (i == 0 or lines[i - 1].strip() == "")
        )
        if at_block_start:
            buf = [line]
            j = i + 1
            while j < len(lines) and lines[j].strip() != "":
                buf.append(lines[j])
                j += 1
            ph = f"HTMLBLOCK{len(blocks)}X"
            blocks[ph] = "\n".join(buf)
            out.append(ph)
            i = j
        else:
            out.append(line)
            i += 1
    return "\n".join(out), blocks


def substitute_html_blocks(html: str, blocks: dict[str, str]) -> str:
    for tag, raw in blocks.items():
        html = html.replace(f"<p>{tag}</p>", raw)
        html = html.replace(tag, raw)
    return html


# ---------- frontmatter ----------

def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_text = text[4:end]
    rest = text[end + 5 :]
    meta = {}
    for line in fm_text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, rest


# ---------- callouts ----------

CALLOUT_RE = re.compile(
    r"(^> \[!(\w+)\][^\n]*\n(?:^>[^\n]*\n?)*)",
    re.MULTILINE,
)


def parse_callout_block(block: str) -> tuple[str, str, str]:
    lines = block.strip("\n").splitlines()
    header = lines[0]
    m = re.match(r"> \[!(\w+)\](.*)", header)
    kind = m.group(1).lower()
    title = m.group(2).strip()
    body_lines = []
    for ln in lines[1:]:
        if ln.startswith("> "):
            body_lines.append(ln[2:])
        elif ln.startswith(">"):
            body_lines.append(ln[1:])
        else:
            body_lines.append(ln)
    return kind, title, "\n".join(body_lines).strip()


def render_highlight(_title: str, body_md: str) -> str:
    return f'<div class="gold-bg">\n{pandoc(body_md)}\n</div>'


def render_dark(_title: str, body_md: str) -> str:
    return f'<div class="dark-bg">\n{pandoc(body_md)}\n</div>'


def render_quote(title: str, body_md: str) -> str:
    html = pandoc(body_md)
    html = re.sub(
        r"<strong>(.*?)</strong>",
        r'<span class="gold-accent">\1</span>',
        html,
        flags=re.DOTALL,
    )
    # Collapse multi-paragraph quotes to <br>-joined single block
    html = html.replace("</p>\n<p>", "<br>\n")
    html = re.sub(r"^<p>(.*)</p>$", r"\1", html, flags=re.DOTALL)
    attrib = f'<span class="attrib">— {title}</span>' if title.strip() else ""
    return f'<div class="pull-quote">\n{html}\n{attrib}\n</div>'


def render_notes(title: str, body_md: str) -> str:
    lead = f"<p><strong>{title}</strong></p>\n" if title.strip() else ""
    return f'<aside class="notes">\n{lead}{pandoc(body_md)}\n</aside>'


INLINE_RENDERERS = {
    "highlight": render_highlight,
    "dark": render_dark,
    "quote": render_quote,
}


def extract_callouts(text: str):
    """Replace inline callouts with placeholders, collect notes separately.

    Returns (text_with_placeholders, placeholder_html_map, notes_list).
    """
    placeholder_html: dict[str, str] = {}
    notes: list[tuple[str, str]] = []
    counter = [0]

    def sub(match):
        block = match.group(1)
        kind, title, body_md = parse_callout_block(block)
        if kind == "notes":
            notes.append((title, body_md))
            return ""
        if kind in INLINE_RENDERERS:
            ph_id = counter[0]
            counter[0] += 1
            ph_tag = f"CALLOUT_PH_{ph_id}"
            placeholder_html[ph_tag] = INLINE_RENDERERS[kind](title, body_md)
            # Wrap in blank lines so pandoc treats the placeholder as its
            # own paragraph and doesn't merge it with neighboring text.
            return f"\n\n{ph_tag}\n\n"
        return block  # unknown kind — leave as-is

    cleaned = CALLOUT_RE.sub(sub, text)
    return cleaned, placeholder_html, notes


def substitute_placeholders(html: str, placeholder_html: dict[str, str]) -> str:
    for tag, block in placeholder_html.items():
        # Pandoc wraps bare tokens in <p>…</p>; replace the wrapped form first.
        html = html.replace(f"<p>{tag}</p>", block)
        html = html.replace(tag, block)
    return html


# ---------- slide rendering ----------

LABEL_RE = re.compile(r"^\*([^*\n][^\n]*[^*\n])\*$")


def parse_slide_head(body: str):
    """Return (heading_line, label, remaining_md)."""
    lines = body.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    heading_line = lines[i] if i < len(lines) else ""
    i += 1
    label = ""
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines):
        m = LABEL_RE.match(lines[i].strip())
        if m:
            label = m.group(1).strip()
            i += 1
    rest_md = "\n".join(lines[i:]).strip()
    return heading_line, label, rest_md


def build_slide(md_block: str) -> str:
    body = md_block.strip()
    if not body:
        return ""

    body, ph_map, notes = extract_callouts(body)
    body, html_blocks = extract_html_blocks(body)
    heading_line, label, rest_md = parse_slide_head(body)

    notes_html = "\n".join(render_notes(t, b) for t, b in notes)
    combined_ph = {**ph_map, **html_blocks}

    is_title = heading_line.startswith("# ") and not heading_line.startswith("## ")
    if is_title:
        section = build_title_slide(heading_line, label, rest_md, combined_ph, notes_html)
    else:
        section = build_regular_slide(heading_line, label, rest_md, combined_ph, notes_html)
    return section


def build_title_slide(heading_line, label, rest_md, ph_map, notes_html):
    h1 = heading_line.lstrip("# ").strip()

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", rest_md) if p.strip()]
    subtitle_md = paragraphs[0] if paragraphs else ""
    meta_md = "\n\n".join(paragraphs[1:])

    subtitle_html = pandoc(subtitle_md)
    subtitle_html = re.sub(r"^<p>(.*)</p>$", r"\1", subtitle_html, flags=re.DOTALL)
    meta_html = pandoc(meta_md)

    subtitle_html = substitute_placeholders(subtitle_html, ph_map)
    meta_html = substitute_placeholders(meta_html, ph_map)

    label_html = f'<span class="label">{label}</span>\n  ' if label else ""
    subtitle_block = (
        f'<p class="subtitle">{subtitle_html}</p>\n  '
        if subtitle_html.strip() else ""
    )
    meta_block = (
        f'<div class="meta">\n{meta_html}\n</div>\n  '
        if meta_html.strip() else ""
    )

    return (
        '<section class="title-slide">\n'
        '  <div class="brand-bar"></div>\n'
        f'  {label_html}'
        f'<h1>{h1}</h1>\n  '
        f'{subtitle_block}'
        f'{meta_block}'
        f'{notes_html}\n'
        '</section>'
    )


def build_regular_slide(heading_line, label, rest_md, ph_map, notes_html):
    m = re.match(r"^#+\s*(.*)$", heading_line)
    h2 = m.group(1).strip() if m else heading_line

    body_html = pandoc(rest_md)
    body_html = substitute_placeholders(body_html, ph_map)

    label_html = f'<span class="label">{label}</span>\n  ' if label else ""

    return (
        '<section>\n'
        f'  {label_html}'
        f'<h2>{h2}</h2>\n'
        f'{body_html}\n'
        f'{notes_html}\n'
        '</section>'
    )


# ---------- deck ----------

SLIDE_SEP_RE = re.compile(r"\n---\n")


def build_deck(md_path: Path) -> Path:
    text = md_path.read_text()
    meta, body = split_frontmatter(text)

    body = body.replace("\r\n", "\n")
    body = "\n" + body.strip() + "\n"
    raw_slides = SLIDE_SEP_RE.split(body)

    sections = []
    for slide_md in raw_slides:
        section = build_slide(slide_md)
        if section:
            sections.append(section)

    out = TEMPLATE
    out = out.replace("{{TITLE}}", meta.get("title", md_path.stem))
    out = out.replace("{{FOOTER_LEFT}}", meta.get("footer_left", ""))
    out = out.replace("{{FOOTER_RIGHT}}", meta.get("footer_right", ""))
    out = out.replace("{{SLIDES}}", "\n\n".join(sections))

    out_path = ROOT / f"{md_path.stem}.html"
    out_path.write_text(out)
    print(f"  ✓ {out_path.name}  ← md/{md_path.name}  ({len(sections)} slides)")
    return out_path


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    mds = sorted(MD_DIR.glob("*.md"))
    if not mds:
        print(f"No markdown decks found in {MD_DIR}")
        return
    built = 0
    for md in mds:
        if target and md.stem != target:
            continue
        build_deck(md)
        built += 1
    print(f"\nBuilt {built} deck(s).")


if __name__ == "__main__":
    main()
