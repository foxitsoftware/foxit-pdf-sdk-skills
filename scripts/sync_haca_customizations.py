#!/usr/bin/env python3
"""HACA customization validator (GitHub Copilot only).

This repository targets GitHub Copilot exclusively. There is no cross-platform
mirror to generate, so this script no longer synchronizes into ``.cursor/`` or
``.opencode/``. Instead it validates that the ``.github/`` customization tree is
internally consistent before a commit or release:

1. All required HACA skills are present and non-empty.
2. Internal ``.github/`` path references in Markdown point at real files.
3. Non-superpowers ``SKILL.md`` files declare required frontmatter keys.
4. No shipped file references Cursor / OpenCode artifacts (multi-platform purity).

The legacy filename and the ``CHECK OK: no stale markdown targets.`` success
string are retained so the maintenance prompts (``haca-apply-spec`` /
``haca-sync``) keep working. See ``docs/`` and the release report for the known
maintainer-only limitations.

Usage:
    python3 scripts/sync_haca_customizations.py
    python3 scripts/sync_haca_customizations.py --check
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GITHUB_ROOT = ROOT / ".github"

REQUIRED_HACA_SKILLS = {
    "clarify-requirements",
    "risk-identification",
    "task-decomposition",
    "tdd-loop",
    "evidence-gate",
    "commit-message-rules",
}

# Matches internal path references such as `.github/skills/foo/SKILL.md`.
GITHUB_PATH_REFERENCE = re.compile(
    r"\.github/[A-Za-z0-9_\-/\.]+\.(?:md|py|json|agent|prompt|txt|mdc|yml|yaml)"
)

# Required frontmatter keys for every non-superpowers SKILL.md.
REQUIRED_SKILL_FRONTMATTER_KEYS = ("name", "description")

FRONTMATTER_BLOCK = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# Optional Superpowers skills are installed by the user and are intentionally
# absent from this repository, so their expected install paths are not validated.
OPTIONAL_REFERENCE_PREFIXES = (
    ".github/skills/superpowers/",
)

# Multi-platform purity tokens. These must not appear in shipped Copilot assets.
MULTIPLATFORM_TOKENS = (
    ".cursor/",
    ".opencode/",
    "opencode.json",
    "tool_mapping_template",
)

# Maintainer-only files that intentionally retain multi-platform wording. They
# are excluded from the purity warning and tracked in the release report.
MULTIPLATFORM_LEGACY_ALLOWLIST = {
    ".github/prompts/haca-apply-spec.prompt.md",
    ".github/prompts/haca-sync.prompt.md",
    ".github/skills/superpowers/README.md",
}

LEGACY_SUCCESS_LINE = "CHECK OK: no stale markdown targets."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the GitHub Copilot HACA customization tree under .github/."
        )
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Retained for backward compatibility; validation always runs.",
    )
    return parser.parse_args()


def iter_markdown_files() -> list[Path]:
    if not GITHUB_ROOT.exists():
        return []
    return sorted(
        path for path in GITHUB_ROOT.rglob("*.md") if path.is_file()
    )


def relative_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def validate_required_skills() -> list[str]:
    errors: list[str] = []
    if not GITHUB_ROOT.exists():
        errors.append(f"Missing .github/ customization tree: {GITHUB_ROOT}")
        return errors

    for skill_name in sorted(REQUIRED_HACA_SKILLS):
        skill_file = GITHUB_ROOT / "skills" / skill_name / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"Required HACA skill missing: {relative_posix(skill_file)}")
        elif not skill_file.read_text(encoding="utf-8").strip():
            errors.append(f"Required HACA skill is empty: {relative_posix(skill_file)}")
    return errors


def validate_internal_references() -> list[str]:
    errors: list[str] = []
    for markdown_file in iter_markdown_files():
        content = markdown_file.read_text(encoding="utf-8")
        for match in GITHUB_PATH_REFERENCE.finditer(content):
            reference = match.group(0)
            if reference.startswith(OPTIONAL_REFERENCE_PREFIXES):
                continue
            if not (ROOT / reference).exists():
                errors.append(
                    f"Broken .github reference: {reference} "
                    f"(in {relative_posix(markdown_file)})"
                )
    return errors


def collect_multiplatform_references() -> list[str]:
    findings: list[str] = []
    for markdown_file in iter_markdown_files():
        rel = relative_posix(markdown_file)
        if rel in MULTIPLATFORM_LEGACY_ALLOWLIST:
            continue
        content = markdown_file.read_text(encoding="utf-8")
        for token in MULTIPLATFORM_TOKENS:
            if token in content:
                findings.append(f"{rel} references `{token}`")
    return findings


def validate_skill_frontmatter() -> list[str]:
    """Every non-superpowers SKILL.md must declare the required frontmatter keys."""
    errors: list[str] = []
    skills_root = GITHUB_ROOT / "skills"
    if not skills_root.exists():
        return errors

    for skill_dir in sorted(p for p in skills_root.iterdir() if p.is_dir()):
        if skill_dir.name == "superpowers":
            # Optional upstream install location; structure is not ours to enforce.
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        content = skill_file.read_text(encoding="utf-8")
        match = FRONTMATTER_BLOCK.match(content)
        if not match:
            errors.append(f"SKILL.md missing YAML frontmatter block: {relative_posix(skill_file)}")
            continue
        frontmatter = match.group(1)
        for key in REQUIRED_SKILL_FRONTMATTER_KEYS:
            if not re.search(rf"(?m)^{re.escape(key)}\s*:", frontmatter):
                errors.append(
                    f"SKILL.md frontmatter missing '{key}': {relative_posix(skill_file)}"
                )
    return errors


def main() -> int:
    parse_args()

    errors: list[str] = []
    errors.extend(validate_required_skills())
    errors.extend(validate_internal_references())
    errors.extend(validate_skill_frontmatter())
    warnings = collect_multiplatform_references()

    if warnings:
        print("WARN: multi-platform references found in Copilot assets:")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        for error in errors:
            print(error)
        print(f"CHECK FAILED: {len(errors)} problem(s).")
        return 1

    print(LEGACY_SUCCESS_LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())