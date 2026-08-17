#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys

SUBJECT_HARD_LIMIT = 88
FIELD_LINE_HARD_LIMIT = 240
NONEMPTY_LINE_HARD_LIMIT = 14

FIELD_PATTERNS = {
    "Requirement description": (r"^-\s*Requirement\s*description\s*:.*$", r"^-\s*需求描述\s*:.*$"),
    "Requirement understanding": (r"^-\s*Requirement\s*understanding\s*:.*$", r"^-\s*需求理解\s*:.*$"),
    "Adopted approach": (r"^-\s*Adopted\s*approach\s*:.*$", r"^-\s*采用方案\s*:.*$"),
    "Rejected approach": (r"^-\s*Rejected\s*approach\s*:.*$", r"^-\s*拒绝方案\s*:.*$"),
    "Key assumptions": (r"^-\s*Key\s*assumptions\s*:.*$", r"^-\s*关键假设\s*:.*$"),
    "Known risks": (r"^-\s*Known\s*risks\s*:.*$", r"^-\s*已知风险\s*:.*$"),
    "Uncovered scenarios": (r"^-\s*Uncovered\s*scenarios\s*:.*$", r"^-\s*未覆盖场景\s*:.*$"),
}


def find_first_nonempty_line(lines: list[str]) -> str:
    for line in lines:
        if line.strip():
            return line.rstrip("\n")
    return ""


def matches_any(patterns: tuple[str, str], line: str) -> bool:
    return any(re.search(pattern, line, re.IGNORECASE) for pattern in patterns)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <message-file>", file=sys.stderr)
        return 2

    msg_file = pathlib.Path(argv[1])
    if not msg_file.is_file():
        print(f"Error: message file not found: {msg_file}", file=sys.stderr)
        return 1

    content = msg_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    nonempty_lines = [line for line in lines if line.strip()]

    subject = find_first_nonempty_line(lines)
    if len(subject) > SUBJECT_HARD_LIMIT:
        print(
            f"Error: subject line too long ({len(subject)} > {SUBJECT_HARD_LIMIT}). Shorten the subject while preserving meaning.",
            file=sys.stderr,
        )
        return 1

    if len(nonempty_lines) > NONEMPTY_LINE_HARD_LIMIT:
        print(
            f"Error: commit message too long ({len(nonempty_lines)} non-empty lines > {NONEMPTY_LINE_HARD_LIMIT}). Shorten the body while preserving meaning.",
            file=sys.stderr,
        )
        return 1

    for line in nonempty_lines:
        for field_name, patterns in FIELD_PATTERNS.items():
            if matches_any(patterns, line) and len(line) > FIELD_LINE_HARD_LIMIT:
                print(
                    f"Error: field '{field_name}' is too long ({len(line)} > {FIELD_LINE_HARD_LIMIT}). Shorten this field while preserving meaning.",
                    file=sys.stderr,
                )
                return 1

    print(f"OK: commit message length check passed for {msg_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
