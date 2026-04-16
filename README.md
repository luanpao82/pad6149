# PAD 6149 — Build Your Nonprofit (Capstone)

UCF MNM capstone course site. Deploys to GitHub Pages.

## Editing weekly content

`Assignments/Week*.md` is the **single source of truth** for each week's page. The `weekNN.html` files are generated.

```bash
# Edit a week's content in Obsidian (or any editor):
#   Assignments/Week 4a Mentor Interview Report.md

python3 build.py week04a    # rebuild one page
python3 build.py            # rebuild all 15 pages
```

The build script preserves the existing design: same sidebar, fonts, cards, badges, tables.

## What the build does

For each `Assignments/Week*.md`:

1. Parse `# Week N: Title` (line 1) and `**Due:** ... | **Points:** ... | **Length:** ...` (line 3)
2. Convert Obsidian callouts (`> [!warning]`, `> [!example]`, `> [!note]`, `> [!info]`, `> [!tip]`) → styled `<div class="card card-warn|card-example|card-note|card-info">` blocks
3. Resolve Obsidian wikilinks (`[[Week 4b Board Governance Policy]]`) → `<a href="week04b.html">Board Governance Policy</a>`
4. Render remaining markdown via pandoc (tables, lists, links, emphasis)
5. Wrap in `_template.html` with sidebar, setting `class="active"` on the current week
6. Write `weekNN.html`

## Adding a new week

1. Create `Assignments/Week 15 Topic Name.md` with the standard header:
   ```markdown
   # Week 15: Topic Name

   **Due:** December 10, 2026 | **Points:** 5 pts | **Length:** 3 pages

   ...
   ```
2. Add the sidebar entry in `_template.html` (under `Service Learning` or `Capstone Project` section)
3. Run `python3 build.py`

## Deployment

```bash
git add -A
git commit -m "Update Week 4 content"
git push
# GitHub Pages auto-deploys from main
```

## Files

| Path | Role |
|---|---|
| `Assignments/Week*.md` | **Source content** (edit these) |
| `_template.html` | Page shell (sidebar, CSS, layout) |
| `build.py` | MD → HTML build script |
| `weekNN.html` | Generated output (committed for Pages) |
| `index.html` | Course landing page (hand-edited, not generated) |
| `_backup_handmade_html/` | Snapshot of pre-pipeline HTML (gitignored) |
| `Slides/`, `Syllabus/`, `Readings/`, `Notes/`, `Resources/` | Source material folders |

## Dependencies

- `pandoc` (3.x) — `brew install pandoc`
- Python 3.9+ (no extra packages)
