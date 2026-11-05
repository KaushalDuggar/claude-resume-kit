# Documentation

Detailed reference for claude-resume-kit. For the quick overview, see [README.md](README.md).

---

## Architecture

```
claude-resume-kit/
├── CLAUDE.md                          # Auto-loaded project instructions
├── config.example.md                  # Template — copy to config.md (gitignored)
├── .claude/skills/                    # 8 skills (invoked as /skill-name)
│   ├── setup-extract/SKILL.md         # Extract from papers → structured data
│   ├── setup-extract-experience/      # Extract from work notes / voice transcripts
│   ├── setup-build-kb/SKILL.md        # Synthesize KB from extractions
│   ├── apply/SKILL.md                 # JD → 1-page industry resume → Notion row
│   ├── make-resume/SKILL.md           # JD → tailored resume/CV (.tex)
│   ├── make-cl/SKILL.md              # Session → cover letter (.tex)
│   ├── edit-resume/SKILL.md           # Edit from critique/feedback
│   └── critique/SKILL.md             # Independent quality review
├── resume_builder/
│   ├── reference/                     # Generation rules and protocols
│   │   ├── shared_ops.md              # Session workflow (all skills read this)
│   │   ├── resume_reference.md        # Resume/CV formatting rules
│   │   ├── cl_reference.md            # Cover letter rules
│   │   ├── critical_rules.md          # Compact re-read for generation phase
│   │   ├── session_file_template.md   # Session file format spec
│   │   └── critique_framework.md      # 8-part critique system
│   ├── templates/                     # LaTeX .cls classes + .tex templates
│   │   ├── resume.cls                 # 2-page resume class
│   │   ├── cv.cls                     # Multi-page CV class
│   │   ├── resume_template.tex        # Resume structural template
│   │   ├── cv_template.tex            # CV structural template
│   │   ├── industry_resume_template.tex # 1-page industry resume (used by /apply)
│   │   └── coverletter_template.tex   # Cover letter template
│   ├── helpers/
│   │   └── char_count.py              # Character counting utility for bullets
│   ├── examples/                      # Fictional "Dr. Jordan Chen" — full worked example
│   ├── experience/                    # YOUR experience files (built by /setup-build-kb)
│   ├── bundles/                       # YOUR role-type bundles (built by /setup-build-kb)
│   └── support/                       # Skills taxonomy, pub metadata, AI fingerprint rules
├── knowledge_base/
│   ├── extractions/                   # Paper extractions (built by /setup-extract)
│   ├── papers/                        # Drop your PDFs / .tex source here
│   └── notes/                         # Any other reference material
├── notes/                             # YOUR work notes, one per position (gitignored)
├── scripts/
│   ├── check_private.py               # Privacy guard — blocks commits with personal data
│   └── install-hooks.sh               # Installs it as a pre-commit hook
├── JDs/                               # Job descriptions (gitignored except the example)
└── output/                            # Generated .tex, session files, critiques (gitignored)
```

---

## Concepts

### Session Files

Every JD gets a session file (`output/<Folder>/session_<name>.md`) that tracks:
- JD analysis and ATS keywords
- Which bundle was selected
- Bullet plan (which achievements, in what order, at what length)
- All generation decisions and their rationale
- Cover letter plan
- Critique scores

All 4 generation skills read and update this file. It's the single source of truth for each application.

### Experience Files

One file per position (e.g., `experience_postdoc_university.md`). Each achievement has:
- **Source paper** with citation
- **Methods and tools** used
- **Quantitative results**
- **Pre-written bullet variants** (2-line and 3-line)
- **Tags** for which role types this achievement is relevant to
- **Significance** context for cover letters

### Role-Type Bundles

One file per target audience (e.g., `bundle_academic.md`). Each bundle contains:
- **S1: Role Profile** — what this audience values, positioning strategy
- **S2: Summary Guide** — how to write the summary for this role type
- **S3: Achievement Reframing Map** — priority ranking of your achievements for this audience
- **S4: Skills Guide** — which tools to bold, which to include, grouping strategy
- **S5: Cover Letter Guide** — opening hooks, paragraph templates, anti-patterns

### Provenance Flags

The system enforces accuracy through provenance tracking in `config.md`. Every achievement is tagged with its publication status. The skills check this table before every output and will never:
- Claim unpublished work is published
- Claim internal tools are peer-reviewed
- Use full-ownership verbs for shared work
- Inflate author position

### The Critique System

The `/critique` skill runs a multi-part assessment:
1. **Domain-Specialist Lens** — reviewer persona, gap analysis, competitive landscape
2. **Five-Perspective Read-Through** — ATS bot, recruiter (10s), HR (30s), hiring manager (2min), technical reviewer (10min)
3. **Eight-Dimension Scoring** — weighted score out of 100
4. **Interview Likelihood** — per-reader probability estimates
5. **Tiered Improvements** — ranked by point impact
6. **Interview Bridge Points** — resume-to-interview talking points
7. **Cover Letter Critique** — 6 sub-checks (anti-patterns, tailoring, context-specific, ATS keywords, structural, package cohesion)
8. **Post-Generation Verification** — mechanical and content checklists including AI fingerprint scan

---

## Three-Session Workflow

For best results, use a **separate Claude Code session** for each step. This gives each skill fresh context, which produces better quality (especially for critique — you want fresh eyes, not the same context that generated the resume).

```
Session 1:  /make-resume JDs/job.txt     → resume/CV .tex
            /clear
Session 2:  /make-cl                      → cover letter .tex
            /clear
Session 3:  /critique                     → critique .md with score
            /clear
            /edit-resume                  → refined .tex (if needed)
```

---

## Customization

### Everything in `config.md` (edit directly)

| Setting | What it controls | Example |
|---------|-----------------|---------|
| **Personal Info** | Name, email, phone, links on all outputs | Your contact details |
| **Document Preferences** | Page counts, bullet line variants, skills layout | `Resume: 2 pages, CV: 5 pages` |
| **Provenance Flags** | What claims are safe to make | `ML paper: under review → never say "published"` |
| **Role Types** | Target audiences and their bundles | `Academic (Tier 1), Industry R&D (Tier 2)` |
| **Decision Tree** | How JD keywords map to role types | `"tenure-track" → Academic` |
| **FIXED Sections** | Template sections that never change per JD | `Education, Publications, Awards` |
| **Output Rules** | Package formats and constraints | `Resume: 2pg + 1pg CL = 3pg package` |
| **KB Corrections** | Errors to never re-introduce | `Spearman is 0.82, not 0.85` |

### LaTeX Templates (edit directly)

- **Fonts, colors, spacing** — modify `.cls` files
- **Section order** — reorder sections in `.tex` templates
- **FIXED content** — fill in education, awards, publications, header
- **Icons** — replace `GS.png` / `orcid.png` with your own
- **Page geometry** — adjust margins in `.cls` if needed

### Knowledge Base (built by skills, then editable)

| File | How to customize |
|------|-----------------|
| **Experience files** | Edit bullet text, add/remove achievements, adjust tags |
| **Bundles** | Change priority matrices, rewrite summary guides, add role types |
| **Skills taxonomy** | Add/remove skills, change groupings, adjust bold rules |
| **Pub metadata** | Update citation counts, add new publications |

### Reference Docs (advanced)

| File | What you'd change |
|------|-------------------|
| `resume_reference.md` | Page budgets, character limits, section specs |
| `cl_reference.md` | Cover letter paragraph templates, word count targets |
| `critical_rules.md` | Generation-time rules tables |
| `critique_framework.md` | Scoring weights, critique dimensions |
| `shared_ops.md` | Session workflow, file derivation logic |

### Skill Prompts (advanced)

Each skill is a markdown file in `.claude/skills/<name>/SKILL.md`. You can:
- Add STOP points for more user control
- Change the number of web searches in Phase 0
- Adjust how many bullets per position
- Modify the critique scoring weights
- Add new skills for your workflow

---

## Key Design Decisions

- **Accuracy > Relevance > Impact > ATS > Brevity** — the priority hierarchy for every generation decision
- **LaTeX-only output** — Claude generates `.tex`, you compile locally. No formatting surprises.
- **FLIPPED position format** — the bold line under each position title is a JD-customized theme, not a generic description. This is the strongest tailoring lever.
- **Structured provenance** — every achievement is tracked from source paper through extraction to experience file to resume bullet
- **Character-precise budgets** — every bullet is calibrated to fit the template geometry, not "try to keep it short"
- **Session files as state** — all decisions for a JD live in one file. Skills can recover from interruptions.
- **Anti-fabrication by design** — provenance flags, verb discipline, and corrections logs prevent overclaiming even under pressure to impress
- **AI fingerprint avoidance** — a dedicated rules file is loaded by all generation and critique skills, covering banned words and phrases (with technical exceptions), structural anti-patterns, positive markers, and a 12-item post-generation checklist

---

## FAQ

**Q: Do I need to know LaTeX?**
No. Claude generates the `.tex` files. You just compile them (`pdflatex file.tex`). The templates handle all formatting.

**Q: How many papers should I extract?**
All papers where you're first author or co-first author, plus key contributing-author papers. Quality matters more than quantity — 5 well-extracted papers beat 20 shallow ones.

**Q: Can I use this for non-academic roles?**
Yes. The framework supports any role type — define them in `config.md`. Industry R&D, consulting, data science, and engineering roles all work. Just create appropriate bundles.

**Q: What if I don't have a Google Scholar / ORCID?**
Remove those lines from the templates. The framework adapts to what you have.

**Q: How do I update after publishing new papers?**
Run `/setup-extract` on the new paper, then update your experience file and bundles. Existing session files are not affected.

**Q: Can I use this with resume formats other than the included templates?**
Yes. The `.cls` files define the visual style. You can modify them or write your own. The skills generate content based on the template structure — update the `[GENERATE: ...]` and `[FIXED: ...]` markers in your template.

**Q: Can multiple people use the same kit?**
Each person needs their own clone with their own `config.md`, knowledge base, and templates. The framework itself is shared; the content is personal.

**Q: What Claude model should I use?**
The skills are designed for Claude's most capable models (Opus, Sonnet). Less capable models may skip steps or produce lower-quality output.

---

## The experience track (work notes → industry resume)

The paper track above assumes your source material is published writing. For
industry roles, most of what matters was never written down: it lives in your
head, in Slack, and in meeting recordings. The experience track turns that into
the same kind of knowledge base.

```
Meeting recordings ──► transcripts ──► notes/<Org>.md ──► /setup-extract-experience
(Granola, Otter, …)    /capture mode    (one per position)           │
                                                                     ▼
                                              knowledge_base/extractions/*.md
                                                                     │
                                                    /setup-build-kb  ▼
                                              resume_builder/experience/ + bundles/
```

### 1. Capture: get the work out of your head

Two ways in, and you can mix them:

- **From meeting notes.** A tool like [Granola](https://www.granola.ai/) that
  transcribes and summarizes your standups, design reviews and 1:1s is a good
  source, because it already holds the decisions you made and why. Paste the
  relevant transcript or summary into `notes/<Org>.md`.
- **By dictation.** Run `/setup-extract-experience capture <Org>` and talk
  through one project at a time. Each project is appended to `notes/<Org>.md`
  as you go, so a long history can be captured over several sittings.

Keep one file per position (`notes/Acme.md`), plus `notes/TIMELINE.md` for dates
and `notes/Projects.md` for side projects. These files are gitignored.

### 2. Mark what you are unsure of, instead of guessing

Capture writes a `TODO` marker wherever a fact is missing or uncertain — a metric
you can't remember, which employer a project belonged to, whether a result was
measured or estimated:

```markdown
- **What:** cut LLM spend with prompt caching
  - ⚠️ `TODO` what's the actual figure, over what period, and how was it
    measured (billing dashboard before vs. after, or an estimate)?
```

This matters more than it looks. Unmarked gaps are where a resume quietly
acquires numbers nobody can defend in an interview. `TODO`s survive into the
critique, which reports them as unverified claims rather than letting them pass.

### 3. Extract and build

```
/setup-extract-experience notes/Acme.md     # one position → structured extractions
/setup-build-kb                             # all extractions → experience files + bundles
```

From here the per-application flow is identical to the paper track.

---

## /apply: one command per job

`/make-resume` is the long form: JD research, a bullet plan you approve, then
generation. `/apply` is the short form for industry roles where you are applying
to many positions and the shape of the resume is settled.

```
/apply JDs/target_job.txt
```

It reads the JD, picks and orders bullets from your knowledge base, renders the
1-page `industry_resume_template.tex`, and writes the usual
`output/<Company_Role>/` folder. Then, if you have configured a tracker, it
creates the application row for you.

### Notion tracker

Configure the **Application Tracker** section of `config.md` with your parent
page, database and data source id. `/apply` then creates a row with the company,
role, level, location, JD link, a one-line note on what the resume leads with,
and the local `.tex` path, at status `To apply`.

Two Notion limitations shape this, and both are handled in the skill rather than
left to surprise you:

- Notion rejects a `.tex` upload, so the source is uploaded as `<name>.tex.txt`
  and placed as a file block in the row's page body.
- The Files property cannot take an upload over MCP, so you attach the compiled
  PDF to the **Resume** property by hand.

The tracker is optional. Leave that config section out and `/apply` stops after
writing the `.tex`.

---

## Does the resume actually fit the job?

`/critique` answers this in a fresh session, scoring the generated package from
five reader perspectives across eight weighted dimensions. For fit specifically,
the parts that matter are:

- **JD vocabulary extraction** — the JD's own terms, ranked by weight, each
  marked matched / partial / missing against your resume.
- **Gap ranking** — gaps sorted into fatal, serious and cosmetic, so you know
  which ones to fix and which to ignore.
- **Methodology transfer test** — how a specialist in *their* domain reads each
  of your achievements, which is usually where a career change either works or
  doesn't.
- **Interview likelihood** — a per-reader probability, plus a ceiling: the score
  this resume cannot exceed without facts you don't currently have.
- **Tiered fixes** — Tier 1 (worth ≥1 point each) down to Tier 3 (skip).

The recommendation is deliberately bounded by what your knowledge base can
support. Where a gap could only be closed by a claim you haven't evidenced, the
critique says so and leaves it open rather than inventing a bullet. Suggested
additions are marked **only if real** — your job is to confirm or drop them.

---

## Privacy

Everything personal is gitignored, so the repository can be public while your
material stays local:

| Gitignored | What it holds |
|---|---|
| `config.md` | Your name, email, phone, tracker ids. Ship `config.example.md` instead |
| `notes/` | Work notes and meeting transcripts |
| `resume/` | Old resumes used as a timeline source |
| `knowledge_base/` | Extractions, papers, reference material |
| `resume_builder/{experience,bundles}/` | Your built knowledge base |
| `JDs/` | Real job descriptions (`example_jd.txt` is kept) |
| `output/` | Generated resumes, cover letters, critiques |
| `.private-patterns` | Your own names and employers, for the guard below |

A `.gitignore` is only as good as your next `git add`. The repo also ships a
pre-commit guard:

```bash
sh scripts/install-hooks.sh          # once, after cloning
python3 scripts/check_private.py     # or run it by hand on staged changes
python3 scripts/check_private.py --all   # scan every tracked file
```

It blocks a commit that stages a private path, or whose added lines contain an
email address, phone number, Notion link, UUID or API-key-shaped token. The
detectors are generic so the script itself is safe to publish; your specific
names and employers go in `.private-patterns`, which is gitignored. Bypass with
`git commit --no-verify` when you genuinely mean to.

One thing the guard cannot cover: **your git identity is in every commit.** On a
public repo, `git config user.email` becomes public with it. Use a GitHub
noreply address if you would rather it didn't:

```bash
git config user.email "<id>+<username>@users.noreply.github.com"
```
