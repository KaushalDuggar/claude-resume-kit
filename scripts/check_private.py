#!/usr/bin/env python3
"""Block a commit that would publish personal data.

Run by the pre-commit hook (see scripts/install-hooks.sh), or by hand:

    python3 scripts/check_private.py            # scan staged changes
    python3 scripts/check_private.py --all      # scan every tracked file

The detectors here are deliberately generic — emails, phone numbers, Notion
links, UUIDs, private paths — so this file stays safe to publish. Your own
names and employers go in `.private-patterns` (gitignored), one regex per line.
"""

import re
import subprocess
import sys
from pathlib import Path

# Paths that must never be committed. Allow-listed exceptions follow.
PRIVATE_PREFIXES = (
    "notes/",
    "resume/",
    "knowledge_base/extractions/",
    "knowledge_base/papers/",
    "knowledge_base/notes/",
    "resume_builder/experience/",
    "resume_builder/bundles/",
    "output/",
    "JDs/",
)
PRIVATE_FILES = ("config.md",)
PATH_ALLOW = {
    "JDs/example_jd.txt",
    "output/.gitkeep",
    "knowledge_base/extractions/_INVENTORY.md",
    "knowledge_base/papers/.gitkeep",
    "knowledge_base/notes/.gitkeep",
    "resume_builder/experience/.gitkeep",
    "resume_builder/bundles/.gitkeep",
    "resume_builder/support/.gitkeep",
    "resume_builder/support/ai_fingerprint_rules.md",
}

# Files whose contents are meant to hold example identifiers.
CONTENT_ALLOW = re.compile(
    r"^(resume_builder/examples/|scripts/check_private\.py$|config\.example\.md$|JDs/example_jd\.txt$)"
)

# Known-fake values used by the shipped examples.
VALUE_ALLOW = re.compile(
    r"your@email\.com|jordan\.chen@email\.com|\+1 5551234567|@example\.(com|org)"
    r"|\[.*?\]|<.*?>|XXXXXXXXXX",
    re.I,
)

DETECTORS = (
    ("email address", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("phone number", re.compile(r"\+\d{1,3}[\s-]?\d{6,}")),
    ("Notion link", re.compile(r"notion\.(?:so|com)/\S+")),
    ("UUID / Notion id", re.compile(r"\b[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}\b")),
    ("API key-ish token", re.compile(r"\b(?:sk|pk|ghp|gho|xox[bap])[-_][A-Za-z0-9]{16,}")),
)


def git(*args):
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=False
    ).stdout


def local_patterns():
    """Extra regexes from .private-patterns, which is gitignored."""
    f = Path(".private-patterns")
    if not f.exists():
        return []
    out = []
    for raw in f.read_text().splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            try:
                out.append(("local pattern", re.compile(line, re.I)))
            except re.error as e:
                print(f"  .private-patterns: bad regex {line!r} ({e})")
    return out


def added_lines(path, scan_all):
    if scan_all:
        try:
            text = Path(path).read_text(errors="replace")
        except OSError:
            return
        for n, line in enumerate(text.splitlines(), 1):
            yield n, line
        return
    diff = git("diff", "--cached", "-U0", "--", path)
    n = 0
    for line in diff.splitlines():
        if line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            n = int(m.group(1)) if m else n
        elif line.startswith("+") and not line.startswith("+++"):
            yield n, line[1:]
            n += 1


def main():
    scan_all = "--all" in sys.argv
    if scan_all:
        files = [f for f in git("ls-files").splitlines() if f]
    else:
        # --diff-filter=d: a staged deletion removes private data, so skip it.
        files = [
            f
            for f in git("diff", "--cached", "--name-only", "--diff-filter=d").splitlines()
            if f
        ]

    findings = []

    for f in files:
        if f in PATH_ALLOW:
            continue
        if f in PRIVATE_FILES or f.startswith(PRIVATE_PREFIXES):
            findings.append(f"{f}: private path — this file should not be committed")

    detectors = DETECTORS + tuple(local_patterns())
    for f in files:
        if f in PATH_ALLOW or CONTENT_ALLOW.match(f):
            continue
        for n, line in added_lines(f, scan_all):
            for label, rx in detectors:
                for hit in rx.findall(line):
                    hit = hit if isinstance(hit, str) else next((h for h in hit if h), "")
                    if not hit or VALUE_ALLOW.search(hit):
                        continue
                    findings.append(f"{f}:{n}: {label} — {hit}")

    if not findings:
        where = "tracked files" if scan_all else "staged changes"
        print(f"check_private: no personal data found in {where}.")
        return 0

    print("check_private: BLOCKED — personal data in what you are about to publish:\n")
    shown = {}
    for finding in dict.fromkeys(findings):
        path = finding.split(":", 1)[0]
        shown.setdefault(path, []).append(finding)
    for path, hits in shown.items():
        for hit in hits[:4]:
            print(f"  {hit}")
        if len(hits) > 4:
            print(f"  {path}: ...and {len(hits) - 4} more in this file")
    print(
        "\nFix the file, or if it is a false positive add the value to VALUE_ALLOW\n"
        "in scripts/check_private.py. To commit anyway: git commit --no-verify\n"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
