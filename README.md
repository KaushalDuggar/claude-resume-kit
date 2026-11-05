# claude-resume-kit

Turn your meeting notes into job applications. You talk through your work once, from [Granola](https://www.granola.ai/) transcripts or by dictation, and Claude Code builds a knowledge base of what you actually did. After that, each application is one command: `/apply` reads the job description, picks and orders your strongest evidence for it, writes a one-page LaTeX resume, and logs the application in your Notion tracker.

Most AI resume tools rewrite whatever you paste in, and they will happily upgrade "helped with" into "led". This one only writes what your notes support. Anything uncertain, like a metric you can't remember or a result you never measured, is marked `TODO` instead of guessed, and it stays flagged until you confirm it.

Built for engineers who apply to many roles and have done more real work than ever made it onto their old resume.

---

## What makes this different

**Built from your notes, not your old resume.** The knowledge base comes from what you said about each project: the problem, what you built, the trade-offs, the result. An old resume is only used for dates and seed bullets.

**`TODO` discipline.** Missing or uncertain facts are marked, never filled in. They carry through to the critique as unverified claims, so you know exactly what an interviewer could catch you on.

**Anti-fabrication rules.** Verb discipline separates what you built from what you contributed to, a corrections log stops fixed errors coming back, and work in progress is written as in progress.

**Fit check before you apply.** `/critique` reads the resume as five different reviewers, ranks your gaps against the JD as fatal, serious or cosmetic, and estimates your interview odds.

**Reads as human-written.** Banned-word lists, structural anti-patterns and a 12-item scan catch the patterns that make a resume sound machine-made.

**Tracked in Notion.** Each `/apply` creates a row with the role, the JD link, what the resume leads with and the gaps to address, with the `.tex` attached.

**Private by default.** Your notes, generated resumes and config are gitignored, and a pre-commit guard blocks any commit containing personal data. See [Privacy](#privacy).

---

## What you actually do

**Once per position (~15 min):**
1. Paste the relevant Granola transcript or summary into `notes/<Org>.md`, or run `/setup-extract-experience capture <Org>` and talk through your projects one at a time
2. Run `/setup-extract-experience notes/<Org>.md` to turn the notes into structured extractions
3. Run `/setup-build-kb` once all positions are done

**Per application:**
1. Run `/apply` with the JD: a file in `JDs/`, pasted text, or a public URL
2. Review the JD match map and bullet plan, then approve or reorder
3. Get `output/<Company_Role>/resume_*.tex` and a new row in your Notion tracker
4. Compile on Overleaf and attach the PDF to the Notion row

**Optional, in a fresh session:** `/critique` for a scored fit review, then `/edit-resume` to apply the fixes.

---

## Prerequisites

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** installed and authenticated
- **A way to compile LaTeX:** [Overleaf](https://www.overleaf.com/), or a local distribution such as [MacTeX](https://tug.org/mactex/) or [TeX Live](https://tug.org/texlive/)
- **Notion connected to Claude Code** if you want the application tracker (optional)
- **A meeting-notes tool** such as Granola (optional, since you can dictate instead)

---

## Setup

### 1. Clone and configure

```bash
git clone https://github.com/KaushalDuggar/claude-resume-kit.git
cd claude-resume-kit
cp config.example.md config.md
sh scripts/install-hooks.sh
```

Fill in `config.md`: **Personal Info** for your resume header, **Positioning** for your headline and anything you must never claim, and **Provenance Flags**. `config.md` is gitignored, and `install-hooks.sh` adds the privacy guard.

### 2. Set up the Notion tracker (optional)

Create a Notion database for your applications, then put its page URL, database URL and data source ID in the **Application Tracker** section of `config.md`. The expected columns are listed there. Leave the section out and `/apply` stops after writing the `.tex`.

### 3. Capture your work

Create one notes file per position, plus a timeline:

```
notes/
├── TIMELINE.md     # dates, employers and titles
├── Acme.md         # one file per position
└── Projects.md     # side projects and research
```

Fill each file from your meeting transcripts, or dictate with `/setup-extract-experience capture Acme`. Don't polish it. The skill structures it and adds a `TODO` wherever a fact is missing.

### 4. Build the knowledge base

```
/setup-extract-experience notes/Acme.md
/setup-build-kb
```

### 5. Apply

```
/apply JDs/company_role.txt
```

See [DOCS.md](DOCS.md) for the experience track in detail, how `/apply` handles Notion's upload limits, and how the critique judges fit.

---

## Also included: papers and academic CVs

This repo is a fork of a kit originally built for researchers, and that path still works. Drop papers into `knowledge_base/papers/` and run `/setup-extract` on each. For academic applications, use `/make-resume` (multi-page resume or CV), `/make-cl` (cover letter) and `/critique` in separate sessions. Paper and experience extractions feed the same knowledge base.

The worked example is upstream's fictional researcher, Dr. Jordan Chen, applying for a faculty position. Here are the [example resume](resume_builder/examples/example_resume.pdf), [cover letter](resume_builder/examples/example_cover_letter.pdf), [session file](resume_builder/examples/example_session_file.md) and [LaTeX source](resume_builder/examples/output/). To try it with no setup, run `/make-resume JDs/example_jd.txt`.

---

## How It Works

```
Your papers     --> /setup-extract             --+
Meeting notes                                    +--> Extractions --> /setup-build-kb --> Knowledge Base
or dictation    --> /setup-extract-experience  --+                                              |
                                                                                                v
Job description --> /make-resume --> Resume/CV (.tex) --> /make-cl --> Cover letter (.tex)
                                            |
                                            +---------> /critique --> Score + AI scan + fixes
                                                             |
                                                             v
                                                       /edit-resume --> Refined package

Job description --> /apply --> 1-page industry resume (.tex) + Notion tracker row
```

| Skill | Purpose | Input | Output |
|-------|---------|-------|--------|
| `/setup-extract` | Extract structured data from a paper | Paper path | `knowledge_base/extractions/*.md` |
| `/setup-extract-experience` | Capture or extract work experience | `capture <Org>`, or a notes path | `knowledge_base/extractions/*.md` |
| `/setup-build-kb` | Build KB from extractions | All extractions | `resume_builder/{experience,bundles,support}/` |
| `/make-resume` | Generate tailored resume or CV | JD path | `output/<Folder>/e2e_*.tex` + session file |
| `/make-cl` | Generate matching cover letter | Session file | `output/<Folder>/*_cover_letter.tex` |
| `/edit-resume` | Edit resume/CV/CL from feedback | Session + feedback | Updated `.tex` files |
| `/critique` | Independent quality review | Session file | `output/<Folder>/critique_*.md` |
| `/apply` | JD → 1-page industry resume, one command | JD path | `output/<Folder>/*.tex` + Notion row |

---

## Documentation

For architecture details, customization tables, the full critique system breakdown, key design decisions, and FAQ, see **[DOCS.md](DOCS.md)**.

---

## Privacy

This repo is designed to be public while your material stays on your machine.
Gitignored: `config.md`, `notes/`, `resume/`, `knowledge_base/`, your built
knowledge base, real `JDs/`, and everything in `output/`.

Because a `.gitignore` is only as good as your next `git add`, there is also a
pre-commit guard:

```bash
sh scripts/install-hooks.sh              # once, after cloning
python3 scripts/check_private.py --all   # scan every tracked file
```

It blocks a commit that stages a private path, or whose added lines contain an
email address, phone number, Notion link, UUID or API-key-shaped token. Its
detectors are generic, so the script is safe to publish; put your own names and
employers in `.private-patterns` (gitignored). Note that your `git config
user.email` is public in every commit on a public repo — use a GitHub noreply
address if that matters to you.

Full table in [DOCS.md](DOCS.md#privacy).

---

## Contributing

Issues and PRs welcome. When contributing:
- Example files use the fictional Dr. Jordan Chen — keep examples in that persona
- Reference docs should stay domain-agnostic
- Test skill changes against the example data before submitting

---

## Credits

A fork of [ARPeeketi/claude-resume-kit](https://github.com/ARPeeketi/claude-resume-kit)
by Akhil Reddy Peeketi, which provides the knowledge-base architecture, the
anti-fabrication rules, the AI fingerprint rules and the 8-part critique system.

Added in this fork: the experience track (`/setup-extract-experience`, capture
mode and `TODO` discipline), `/apply` with Notion tracking, the 1-page industry
resume template, and the privacy guard.

---

## License

MIT — see [LICENSE](LICENSE).
