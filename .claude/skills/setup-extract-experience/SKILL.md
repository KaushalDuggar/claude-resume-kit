---
description: Build knowledge base extractions from work experience — voice-note transcripts, notes files, old resumes, and GitHub repos (no papers needed)
user-invocable: true
---

# /setup-extract-experience

**User input:** `$ARGUMENTS`

Parse `$ARGUMENTS`:
- `capture <Org>` (e.g., `capture Acme`) → **Capture Mode**: user dictates projects one by one; append each to `notes/<Org>.md`
- Path to a notes file (e.g., `notes/Acme.md`) → **Extract Mode** for that position
- Several notes paths separated by spaces → Extract Mode, batch (one position at a time)
- `status` → show which positions in `notes/TIMELINE.md` have notes, open TODOs, and extractions
- Empty → run `status`, then ask which position to capture or extract

This skill replaces `/setup-extract` for users whose material is industry work rather than papers. Output files use the same location and inventory as `/setup-extract`, so `/setup-build-kb` consumes them unchanged.

---

## Source Types

| Source | Where it lives | How to read it |
|--------|---------------|----------------|
| Notes / voice-note transcripts | `notes/<Org>.md` | Read directly. Transcripts pasted in chat are first written into the notes file (Capture Mode). |
| Old resumes | `resume/*.pdf`, `resume/*.docx` | Read tool. Use for timeline, titles, dates, and seed bullets. **Old resume bullets are claims to verify, not facts.** |
| GitHub repos | Links in the notes file or `notes/Projects.md` | Public repo → fetch README and key files. Local clone → read directly. Confirm stack and what the code actually does. |
| Timeline | `notes/TIMELINE.md` | One row per position with dates and its notes file. |

Audio files cannot be processed. If the user has voice notes, ask them to paste a transcript (phone dictation, WhatsApp transcript, Whisper, etc.).

---

## Startup

1. Read `CLAUDE.md` — check KB Corrections Log
2. Read `config.md` — Personal Info, Provenance Flags, KB Corrections Log
3. Read `notes/TIMELINE.md` — positions and dates (create it from the old resumes if missing)
4. Read `knowledge_base/extractions/_INVENTORY.md` — avoid duplicate extractions

---

## Capture Mode (`capture <Org>`)

Purpose: turn rambling 1–2 minute voice transcripts into structured notes without losing anything.

**Loop for each message the user sends:**
1. Append the content to `notes/<Org>.md` under the right project heading (create the heading if it is a new project). Keep the user's facts; restructure into bullets; fix obvious transcription errors and **state each interpretation** (e.g., "worn" → "warn").
2. Add an ASCII architecture/workflow diagram when the project has a flow (pipeline, request path, layered checks). Update it as later messages add detail.
3. Mark gaps inline as `` `TODO` `` — ownership, numbers, stack, outcomes.
4. Flag accuracy risks inline with ⚠️ (e.g., a named technique the description doesn't fully match, a client name that may be under NDA).
5. Reply briefly: what was added, at most 2–4 targeted questions, and an invitation to continue. Do not repeat the note back.

If the transcript cuts off mid-sentence, save what exists and tell the user where to resume.

Capture Mode has no stop gates — it continues until the user says the position is done, then suggest: "Run `/setup-extract-experience notes/<Org>.md` to extract."

---

## Phase 1: Gather Sources for the Position

1. Read the notes file.
2. Read every old resume in `resume/`; pull the bullets for this position. Note differences between versions (older resumes often have numbers newer ones dropped).
3. Read any linked GitHub repos.
4. Identify the **position**: organisation, team, title, dates (from TIMELINE / resumes).

Progress: "Gathered [N] sources for [Org]: notes ([K] projects), [R] resume versions, [G] repos"

---

## Phase 2: Split into Achievements and Reconcile

**Unit of extraction = one project or achievement within the position** (not one source file). One project may draw on notes + resume + repo; one resume covers many positions.

For each achievement, build an evidence list. Then produce a reconciliation table:

| # | Achievement | Sources | Conflicts / gaps |
|---|-------------|---------|------------------|
| 1 | Prompt-injection guardrail | notes, resume v1 | Resume says "system vs user prompt tags"; notes say "untrusted-source tags on tool output" |

Conflict types to look for: different names for the same library/tool, different numbers, different scope ("built" vs "set up"), claims on the resume with no supporting notes, notes material missing from the resume.

---

## Phase 3: Interview

Ask only what the sources don't already answer. Group by achievement. Skip anything answered.

1. **Ownership:** "What did you do yourself vs. the team? Did you design it, build it, or extend an existing system?"
2. **Numbers:** "Any metric you can stand behind — scale, latency, accuracy, % improvement, users, clients, time or cost saved? Exact or approximate? How was it measured?"
3. **Stack:** languages, frameworks, models, infrastructure.
4. **Outcome:** shipped to production / POC / internal only? Who used it?
5. **Confidentiality:** "Can client names, product names, or numbers appear on a resume?"
6. **Conflicts:** resolve every row from the Phase 2 table.

### >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<<
Present the achievement list, the reconciliation table, and the questions.
**You MUST wait for the user's explicit text response before continuing.**

Write the answers back into the notes file so it stays the source of truth.

Unanswered items are allowed: record them as `unverified` in the extraction and keep them out of Safe-to-claim.

---

## Phase 4: Write Extractions

One file per achievement: `knowledge_base/extractions/<org>_<YYYY>_<2-3_word_descriptor>.md`
- Lowercase, underscores. `<YYYY>` = position start year. Examples: `acme_2026_prompt_injection.md`, `globex_2024_kernel_optimization.md`

```markdown
# [Achievement Title]

## Metadata
- **Type:** experience
- **Organisation:** [org — team/practice]
- **Position:** [title] ([dates])
- **Project dates:** [if known, else "within position dates"]
- **User's role:** [sole owner | led | core contributor | contributor]
- **Status:** [production | POC | internal | shipped to clients]
- **Sources:** [notes/<Org>.md §section, resume/<file> (version/date), repo URL, interview <date>]

## Context
[1–3 sentences: the platform/product, the problem, who it served]

## Methods & Tools
- **Languages/frameworks:** [...]
- **Models/services:** [...]
- **Infrastructure:** [...]
- **Key techniques:** [specific design decisions that map to resume skills]

## Architecture
[Copy or condense the diagram from the notes file, if any]

## Key Results
[Numbered. Mark each: (verified — source) or (approx — user estimate) or (unverified)]
1. [...]

## Design Decisions Worth Highlighting
[Trade-offs the user made and why — strong interview material]
- [...]

## Scope & Ownership
- **User did:** [...]
- **Team did:** [...]
- **Pre-existing / not the user's:** [...]

## Provenance Notes
- **Safe to claim:** [...]
- **Needs hedging:** [...]
- **Do NOT claim:** [...]
- **Confidential:** [client names / numbers that must be generalised, with the approved generic wording]

## Resume Bullet Seeds
[3–5 STAR seeds. Full-ownership verbs only where "User's role" is sole owner/led.]
1. [...]
```

Show each extraction to the user after writing it.

---

## Phase 5: Update Inventory and Config

1. Add one row per extraction to `knowledge_base/extractions/_INVENTORY.md`:
   ```
   | [#] | [file] | [achievement title] | [position] | experience | [user's role] | [status] |
   ```
2. Propose (do not silently write) additions to `config.md`:
   - **Provenance Flags** — e.g., "Client names: use 'tier-1 banking and enterprise clients'"
   - **KB Corrections Log** — every resolved conflict (e.g., "Library is OpenRedaction, not OpenRedact")
   Apply them after the user approves.
3. Mark the position's extraction status in `notes/TIMELINE.md` (add a `Extracted` column if missing).

---

## Phase 6: Next Steps

Present:
1. **Summary:** [N] achievements extracted, [M] verified numbers, [K] unverified items
2. **Open TODOs** still in the notes file
3. **Next action:**
   - More positions without extractions → "Run `/setup-extract-experience notes/<next>.md`" (or `capture <Org>` if notes are thin)
   - All positions done → "Run `/setup-build-kb`"

### >>>>>> MANDATORY STOP <<<<<<
Wait for the user's response.

---

## Rules

- **Notes are raw; extractions are vetted.** Nothing reaches an extraction without a source.
- **Old resumes are not ground truth.** A resume-only claim stays `unverified` until the user confirms it.
- **Never invent numbers.** "Measurable gains" stays vague until the user supplies a figure.
- **Name techniques accurately.** If the user's implementation is "inspired by" a named method, say so; don't claim the method.
- **Shared work gets hedged verbs** per the CLAUDE.md Verb Discipline rules.
