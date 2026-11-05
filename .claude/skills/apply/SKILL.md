---
description: One command per job — tailor a 1-page industry resume to a JD from the notes/KB, write the .tex, and log the application (with the .tex attached) in the Notion tracker
user-invocable: true
---

# /apply

**User input:** `$ARGUMENTS`

Parse `$ARGUMENTS`:
- Path to a JD (e.g., `JDs/databricks_ai_engineer_fde.txt`) → **Apply Mode**
- Pasted JD text or a URL → save it to `JDs/<company>_<role>.txt` first (fetch the URL if public), then Apply Mode
- `status <Company> <Status>` (e.g., `status Databricks Applied`) → **Status Mode**: update that row's Status (and Date applied when the new status is Applied)
- `list` → show tracker rows grouped by Status
- Empty → ask for the JD

---

## Startup

1. Read `CLAUDE.md` (anti-fabrication, verb discipline) and `config.md`, especially **Application Tracker (Notion)** and **Positioning**.
2. Read the source material, best first:
   - `resume_builder/experience/*.md` and bundles, if `/setup-build-kb` has been run
   - otherwise `notes/TIMELINE.md` and every `notes/*.md` (one per position, plus `Projects.md`)
3. Read the layout template `resume_builder/templates/industry_resume_template.tex`.
4. Read `resume_builder/reference/resume_reference.md` sections **Bullet Ordering Within a Position** and **Inline Bold Emphasis**.
5. Check the tracker for an existing row for this company + role (query the data source in config). If one exists, this run updates it instead of creating a duplicate.

---

## Phase 1: JD Analysis

Present:
- Company, role, level, location, link
- Top 6–10 JD requirements / keywords, ranked
- **Match map:** each requirement → the achievement(s) that prove it, or **GAP**
- Gaps the user may be able to fill (ask: "Have you done X?") — never fill a gap by invention

## Phase 2: Bullet Plan

One table per position, rows in final order (scored per resume_reference.md: JD relevance ×3, impact ×2, ownership ×1):

| # | Achievement | Score | Label | Notes (merge? in-progress? unverified?) |

Also propose:
- Summary line (starts from the config.md Positioning headline; adapt the middle to the JD)
- Projects to include (GenAI projects first; GitHub link only if claims match the repo)
- Two-line Technical Skills block (Languages & Tools / GenAI), JD terms first

Budget for one A4 page with the template: ~14–16 two-line bullets total plus 2–3 short project bullets. Default allocation: current role 5, previous role 5, AMD 2, ISRO 1–2, Projects 3–4.

### >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<<
Present the JD analysis and bullet plan. Wait for the user to approve or edit order, merges, and inclusions.

## Phase 3: Write the .tex

Save to `output/<Company>_<Role>/resume_<company>_<role>.tex` (lowercase, underscores), copying the template's preamble and macros unchanged.

Writing rules:
- **Every bullet = exactly 2 rendered lines:** keep label + text to ~170–190 characters; fewer when 3+ terms are bold. A 3rd line with 1–3 words is a defect, so rewrite rather than leave it.
- **Bold** 2–3 JD-matching tools/techniques/metrics per bullet; never whole phrases.
- Dates always top-right; role/subtitle on line 2; no outer bullet on entry headers.
- Work in progress: "building …" / "currently building …", never past tense.
- Only claims backed by the notes/KB. Unconfirmed items stay out or get a `% TODO` LaTeX comment, never rendered text.
- Respect every "Do NOT claim" / Positioning rule in config.md and the notes.
- Escape LaTeX specials (`& % $ # _`). Use `--` for ranges.
- After writing, check brace balance and that every `\resumeItemListStart` has an End.

## Phase 4: Log in Notion

1. Upload the .tex: `create-file-upload` with filename `<name>.tex.txt`, then POST the local file to the returned `upload_url` with curl (`-F "file=@<path>;filename=<name>.tex.txt;type=text/plain"` plus the returned headers).
2. Create (or update) the row in the Job Applications data source with:
   - Company, Role, Level, Location, JD link
   - Status: `To apply`
   - Resume file: local .tex path
   - Resume focus: one line on what leads (e.g., "current role led by agent work; previous led by retrieval")
   - Next step: "Compile on Overleaf, attach PDF, apply via <channel>"
   - Notes: main gaps
3. Page body: `## Resume` with the file block (`<file source="file-upload://…" />`), a line telling the user to compile and attach the PDF to **Resume**, `## Job description` with the JD text, `## Gaps to address`.
4. If a row already existed: replace the Resume section with the new file and note the revision date.

## Phase 5: Hand-off

Report:
- Path to the .tex and the Notion row link
- What leads and what was left out (and why)
- Open questions/gaps
- "Compile on Overleaf (Upload Project → Recompile). Send a screenshot if anything spills or looks off; I'll fix it with /edit-resume or directly."

---

## Status Mode

`/apply status <Company> <Status>`:
- Find the row (ask if several match), set Status. When the new status is `Applied`, also set Date applied to today.
- Optionally take a note: `/apply status Databricks Interviewing "Recruiter call Nov 12"` → append to Notes.
