# PAD 6149 — Canvas Build Kit (Fall 2026)

Step-by-step kit to set up the dual-track capstone in Webcourses (Canvas course **1513945**, `PAD6149-26Fall 0061`). Paste-ready HTML for every assignment is in `Canvas/html/`. Derived from `MASTER_DESIGN_Fall2026.md`.

> **Safety:** The course is **Unpublished** and 18 students are pre-enrolled — they see **nothing** until you publish the whole course. So you can build and "publish" individual assignments freely now; nothing reaches students until the course itself is published. Nothing in this kit deletes data (we *unpublish*, which is reversible).

---

## Order of operations

1. Create two **sections** (Option A, Option B)
2. Set up **assignment group weights** (80 / 20)
3. **Unpublish** the old discussions + old ePortfolio assignment
4. **Edit** the existing Leadership Case Study (20 pts, general analysis, Everyone)
5. **Create** the 27 weekly assignments (14 Option B + 13 Option A)
6. Create the **"Choose Your Path"** page
7. **Verify** weights = 100% and each assignment's Assign-To

---

## 1. Create sections

**Settings → Sections tab.** In the "Name" box add each, click **+ Section**:
- `Option A`
- `Option B`

(Students get added to their section after they declare a path in Week 1. If you can't add students to sections yourself, ask the registrar/Canvas admin, or use per-student "Assign To" as a fallback.)

## 2. Assignment group weights

**Assignments → ⋮ (top right) → Assignment Groups Weight →** check **"Weight final grade based on assignment groups."** Set:

| Assignment group | Weight |
|---|---|
| **Capstone Deliverables** *(create this group)* | **80%** |
| **Leadership Case Study** *(exists)* | **20%** |
| Non-Graded Requirements *(exists)* | 0% |
| Discussion Boards *(exists)* | 0% |
| ePortfolio *(old; will be emptied)* | 0% |
| (any empty "Assignments" groups) | 0% — or delete |

Must total **100%** → 80 + 20 = 100. ✓

> Create the **Capstone Deliverables** group first: Assignments → **+ Group**.

## 3. Unpublish old content (reversible)

- **Discussion Boards group:** unpublish each of the 10 discussion topics (Module 2–9, 11, 12 Discussion Board) — click the green ✓ on each to turn it grey. Leaving the group at 0% also removes them from the grade.
- **ePortfolio group:** unpublish the old **ePortfolio Assignment (50 pts)** — its content is now distributed into the weekly Option A assignments. Keep **Self-Assessment** and the **ePortfolio Examples** page (useful for Option A).
- Keep **Financial Aid Attendance** (Non-Graded).

## 4. Edit the Leadership Case Study (common, 20 pts)

Open the existing **Leadership Case Study** assignment → **Edit**:
- **Points:** change `30` → **`20`**
- **Due:** change to **Nov 2, 2026**
- **Assign To:** Everyone (both sections do this one)
- **Description:** clear it, click **`</>`** (HTML editor) in the toolbar, paste the full contents of `Canvas/html/leadership-case-common.html`
- In the module, unpublish/remove the old **"Policy Memo Guidelines"** attachment (no longer used)
- Keep it in the **Leadership Case Study** group (20%)

---

## 5. Create the 27 weekly assignments

For **each** row: Assignments → **+ Assignment** → set **Name**, **Points**, **Assignment Group = Capstone Deliverables**, **Submission Type = Online** (✔ Text Entry, ✔ File Uploads; for Final/website weeks also ✔ Website URL), **Assign To = the section in the table**, **Due date**, then paste the **body file** via the **`</>` HTML editor**, and **Publish**.

> **Naming tip:** prefix names with the track + week so the gradebook stays readable, e.g. `[B] W03 · Build Your Nonprofit Website` and `[A] W03 · Build Your ePortfolio Site`.

### Option B — assign to **Option B** section

| Wk | Suggested name | Pts | Due (2026) | Body file |
|---|---|---|---|---|
| 1 | [B] W01 · Nonprofit Concept Statement | 2 | Aug 24 | `optB-week01.html` |
| 2 | [B] W02 · Interview Plan | 2 | Aug 31 | `optB-week02.html` |
| 3 | [B] W03 · Build Your Nonprofit Website | 3 | Sep 7 | `optB-week03.html` |
| 4 | [B] W04 · Mentor Interview Report | 6 | Sep 14 | `optB-week04a.html` |
| 4 | [B] W04 · Board Governance Policy | 7 | Sep 14 | `optB-week04b.html` |
| 5 | [B] W05 · HR & Volunteer Management Plan | 7 | Sep 21 | `optB-week05.html` |
| 6 | [B] W06 · Confirming Identity | 3 | Sep 28 | `optB-week06.html` |
| 7 | [B] W07 · Financial Plan & Budget | 3 | Oct 5 | `optB-week07.html` |
| 8 | [B] W08 · Fundraising Strategy | 3 | Oct 12 | `optB-week08.html` |
| 9 | [B] W09 · Strategic Plan | 10 | Oct 19 | `optB-week09.html` |
| 10 | [B] W10 · Program Evaluation Framework | 8 | Oct 26 | `optB-week10.html` |
| 12 | [B] W12 · AI Content Creation & Social Media | 5 | Nov 9 | `optB-week12.html` |
| 13 | [B] W13 · Policy Advocacy Plan | 8 | Nov 16 | `optB-week13.html` |
| 14 | [B] W14 · Final Pitch Presentation | 13 | Dec 3 | `optB-week14.html` |

*Option B deliverables total **80** pts.*

### Option A — assign to **Option A** section

| Wk | Suggested name | Pts | Due (2026) | Body file |
|---|---|---|---|---|
| 1 | [A] W01 · Welcome & Resume | 2 | Aug 24 | `optA-week01.html` |
| 2 | [A] W02 · Competency Self-Assessment & Evidence Plan | 2 | Aug 31 | `optA-week02.html` |
| 3 | [A] W03 · Build Your ePortfolio Site | 3 | Sep 7 | `optA-week03.html` |
| 4 | [A] W04 · Competency 4 — Governance & Ethics | 13 | Sep 14 | `optA-week04.html` |
| 5 | [A] W05 · Competency 3 — HR Evidence | 7 | Sep 21 | `optA-week05.html` |
| 6 | [A] W06 · Competency 3 — Communication Reflection | 3 | Sep 28 | `optA-week06.html` |
| 7 | [A] W07 · Competency 3 — Financial Evidence & Reflection | 3 | Oct 5 | `optA-week07.html` |
| 8 | [A] W08 · Competency 2 — Volunteer Evidence | 3 | Oct 12 | `optA-week08.html` |
| 9 | [A] W09 · Competency 1 — Strategic Plan Evidence | 10 | Oct 19 | `optA-week09.html` |
| 10 | [A] W10 · Competency 2 — Program Evaluation & Reflection | 8 | Oct 26 | `optA-week10.html` |
| 12 | [A] W12 · AI Reflection & Portfolio Polish | 5 | Nov 9 | `optA-week12.html` |
| 13 | [A] W13 · Competency 5 — Policy Evidence & Reflection | 8 | Nov 16 | `optA-week13.html` |
| 14 | [A] W14 · Final ePortfolio Assembly & Presentation | 13 | Dec 3 | `optA-week14.html` |

*Option A deliverables total **80** pts. (No Week-11 row — the common Leadership Case covers it.)*

## 6. "Choose Your Path" page

**Pages → + Page →** title `Choose Your Capstone Path` → `</>` HTML editor → paste `Canvas/html/choose-your-path.html` → **Save & Publish.** Add it to **Module 0** near the top, and link it from the course Home page.

## 7. Verify

- Grade weights total **100%** (Capstone Deliverables 80 + Leadership Case 20).
- Each Option B assignment **Assign To = Option B**; each Option A = **Option A**; Leadership Case = **Everyone**.
- Each track's deliverables sum to 80; with the 20-pt case, each student's max = **100**.
- Old discussions + old ePortfolio assignment are **unpublished**.
- Spot-check one assignment as a Student (Student View) once the course is published.

---

## How to paste a body file

1. In the assignment/page editor, click **`</>`** (HTML Editor) on the right of the rich-content toolbar.
2. Open the matching file in `Canvas/html/`, select all, copy.
3. Paste into the HTML editor. Switch back to the rich view to confirm it rendered (tables, headings, gold callouts).

> Re-generate all HTML anytime after editing the source markdown: `cd Canvas && python3 build_canvas.py`.
