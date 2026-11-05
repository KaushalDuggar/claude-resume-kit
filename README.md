# claude-resume-kit

Most AI resume tools work the same way: paste resume + paste JD, get a rewrite. They don't know which of your papers is published vs. under review. They don't know you only ran the simulations, not the experiments. They'll upgrade "contributed to" into "developed" without blinking.

This is different. You extract your papers, codebases, and reports once — the system asks structured questions about each one. After that, every new application is just pointing it at a JD. It picks the right achievements, frames them for the audience, enforces accuracy, and generates LaTeX you compile locally.

Two tracks feed one knowledge base. The **paper track** extracts published writing. The **experience track** captures work that was never written down — from meeting transcripts or by dictation — which is what industry applications actually run on. Either one produces an academic CV or a 1-page industry resume.

Built for researchers and engineers with lots of source material (papers, code, reports) who apply to many positions across different employer types.

---

## What makes this different

**Knowledge base, not a rewriter.** You extract once. Every application draws from verified source material — not a pasted resume that gets "improved."

**Anti-fabrication by design.** Provenance flags on every achievement (published / under review / internal). Verb discipline rules prevent overclaiming. A corrections log ensures fixed errors don't reappear.

**AI fingerprint avoidance.** Banned-word lists, structural anti-patterns, and a 12-item post-generation scan so output reads as human-written.

**Multi-perspective critique.** Five reader personas (ATS bot through technical reviewer) score your resume across 8 dimensions in a fresh context window.

**LaTeX output, locally compiled.** No data leaves your machine beyond the Claude Code conversation.

---

## Example Output

Here's what the system generates for the included fictional researcher (Dr. Jordan Chen, computational biologist) applying to a tenure-track faculty position:

- [Example Resume (PDF)](resume_builder/examples/example_resume.pdf) — 2-page resume with JD-tailored bullets, skills, and publications
- [Example Cover Letter (PDF)](resume_builder/examples/example_cover_letter.pdf) — 1-page academic cover letter with specific hooks
- [Example Session File](resume_builder/examples/example_session_file.md) — the decision log that produced this output
- [Source .tex files](resume_builder/examples/output/) — the LaTeX source Claude generated

All example data is in `resume_builder/examples/` — extraction, experience file, bundle, config, and session file.

---

## What you actually do

**One-time setup — papers (~10 min each):**
1. Drop your papers/reports into `knowledge_base/papers/`
2. Run `/setup-extract` on each — Claude reads it and asks you questions about your contributions and publication status
3. Run `/setup-build-kb` — synthesizes everything into your knowledge base

**One-time setup — work experience (~15 min per position):**
1. Paste meeting transcripts (e.g. from [Granola](https://www.granola.ai/)) into `notes/<Org>.md`, or run `/setup-extract-experience capture <Org>` and talk through your projects one at a time
2. Run `/setup-extract-experience notes/<Org>.md` for each position
3. Run `/setup-build-kb`

Uncertain facts get a `TODO` marker rather than a guess, and those markers survive into the critique as unverified claims. See [the experience track](DOCS.md#the-experience-track-work-notes--industry-resume).

**Per application (~15-20 min):**
1. Drop the JD into `JDs/`
2. Run `/make-resume JDs/target_job.txt` — approve the bullet plan, get a `.tex` file
3. Run `/make-cl` for a cover letter
4. Run `/critique` for a scored review with specific fixes

Or, for industry roles once the shape is settled: `/apply JDs/target_job.txt` does it in one command and logs the application to your Notion tracker.

Each step uses a **separate Claude Code session** for best quality (fresh context = less bias).

---

## Prerequisites

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** CLI installed and authenticated
- **A LaTeX distribution** for compiling `.tex` to `.pdf` (e.g., [TeX Live](https://tug.org/texlive/), [MacTeX](https://tug.org/mactex/), [MiKTeX](https://miktex.org/))
- **Your research papers** or project documentation ready for extraction

---

## Try it first (5 minutes)

Want to see what it does before extracting your own papers? The repo includes a complete example knowledge base for a fictional researcher:

```bash
git clone https://github.com/KaushalDuggar/claude-resume-kit.git
cd claude-resume-kit
claude
/make-resume JDs/example_jd.txt
```

This runs the full pipeline — JD analysis, bullet selection, LaTeX generation — using the included example data. No setup required.

---

## Full Setup

### 1. Clone and configure

```bash
git clone https://github.com/KaushalDuggar/claude-resume-kit.git
cd claude-resume-kit
```

```bash
cp config.example.md config.md
sh scripts/install-hooks.sh
```

Edit `config.md` with your details (name, email, provenance flags, role types). See `resume_builder/examples/example_config.md` for a complete example.

`config.md` is gitignored, and `install-hooks.sh` adds a pre-commit guard that blocks a commit containing personal data. See [Privacy](#privacy).

### 2. Extract your papers

Place PDFs or `.tex` source files in `knowledge_base/papers/`, then:

```
/setup-extract knowledge_base/papers/my_paper.pdf
```

Claude reads the paper, asks clarifying questions about your contributions, and creates a structured extraction. Repeat for each paper.

### 3. Build your knowledge base

```
/setup-build-kb
```

This synthesizes all extractions into experience files, role-type bundles, and support files.

### 4. Customize your LaTeX templates

Open the templates in `resume_builder/templates/` and fill in your FIXED sections — education, header, awards, publications. The `[CONFIG: ...]` placeholders show you what to fill in.

### 5. Generate for a job

```
/make-resume JDs/target_job.txt
```

Then in separate sessions: `/make-cl` for the cover letter, `/critique` for a scored review.

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
