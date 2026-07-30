#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys

REQUIRED_SECTIONS = {
    "Task Input": ("## 任务输入", "## Task Input"),
    "AI Decision Summary": ("## AI 决策摘要", "## AI Decision Summary"),
}

SUBJECT_LINE = re.compile(
    r"^\[AI\]\s+\S+(\([^)]*\))?\s*:\s*\S",
    re.IGNORECASE,
)

REQUIRED_FIELDS = {
    "Jira ticket": (r"-\s*Jira\s*ticket\s*:", r"-\s*Jira\s*工单\s*:"),
    "Requirement description": (r"-\s*Requirement\s*description\s*:", r"-\s*需求描述\s*:"),
    "Requirement understanding": (r"-\s*Requirement\s*understanding\s*:", r"-\s*需求理解\s*:"),
    "Adopted approach": (r"-\s*Adopted\s*approach\s*:", r"-\s*采用方案\s*:"),
    "Rejected approach": (r"-\s*Rejected\s*approach\s*:", r"-\s*拒绝方案\s*:"),
    "Key assumptions": (r"-\s*Key\s*assumptions\s*:", r"-\s*关键假设\s*:"),
    "Known risks": (r"-\s*Known\s*risks\s*:", r"-\s*已知风险\s*:"),
    "Uncovered scenarios": (r"-\s*Uncovered\s*scenarios\s*:", r"-\s*未覆盖场景\s*:"),
}

REQUIRED_FIELD_VALUES = {
    "Jira ticket": (r"-\s*Jira\s*ticket\s*:\s*\S.+|[-\s]*Jira\s*ticket\s*:\s*\S", r"-\s*Jira\s*工单\s*:\s*\S.+|[-\s]*Jira\s*工单\s*:\s*\S"),
    "Requirement description": (r"-\s*Requirement\s*description\s*:\s*\S.+|[-\s]*Requirement\s*description\s*:\s*\S", r"-\s*需求描述\s*:\s*\S.+|[-\s]*需求描述\s*:\s*\S"),
    "Requirement understanding": (r"-\s*Requirement\s*understanding\s*:\s*\S.+|[-\s]*Requirement\s*understanding\s*:\s*\S", r"-\s*需求理解\s*:\s*\S.+|[-\s]*需求理解\s*:\s*\S"),
    "Adopted approach": (r"-\s*Adopted\s*approach\s*:\s*\S.+|[-\s]*Adopted\s*approach\s*:\s*\S", r"-\s*采用方案\s*:\s*\S.+|[-\s]*采用方案\s*:\s*\S"),
    "Rejected approach": (r"-\s*Rejected\s*approach\s*:\s*\S.+|[-\s]*Rejected\s*approach\s*:\s*\S", r"-\s*拒绝方案\s*:\s*\S.+|[-\s]*拒绝方案\s*:\s*\S"),
    "Key assumptions": (r"-\s*Key\s*assumptions\s*:\s*\S.+|[-\s]*Key\s*assumptions\s*:\s*\S", r"-\s*关键假设\s*:\s*\S.+|[-\s]*关键假设\s*:\s*\S"),
    "Known risks": (r"-\s*Known\s*risks\s*:\s*\S.+|[-\s]*Known\s*risks\s*:\s*\S", r"-\s*已知风险\s*:\s*\S.+|[-\s]*已知风险\s*:\s*\S"),
    "Uncovered scenarios": (r"-\s*Uncovered\s*scenarios\s*:\s*\S.+|[-\s]*Uncovered\s*scenarios\s*:\s*\S", r"-\s*未覆盖场景\s*:\s*\S.+|[-\s]*未覆盖场景\s*:\s*\S"),
}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <message-file>", file=sys.stderr)
        return 2

    msg_file = pathlib.Path(argv[1])

    if not msg_file.is_file():
        print(f"Error: message file not found: {msg_file}", file=sys.stderr)
        return 1

    if msg_file.stat().st_size == 0:
        print(f"Error: message file is empty: {msg_file}", file=sys.stderr)
        return 1

    try:
        content = msg_file.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        print(f"Error: message file is not valid UTF-8: {msg_file} ({exc})", file=sys.stderr)
        return 1

    lines = [line.strip() for line in content.splitlines()]

    first_nonempty = next((ln for ln in lines if ln), "")
    if not SUBJECT_LINE.match(first_nonempty):
        print(
            "Error: first non-empty line must match `[AI] <type>(<scope>): <subject>` "
            "(scope parentheses optional; subject must not be empty).",
            file=sys.stderr,
        )
        return 1

    section_headings = {line for line in lines if line.startswith("## ")}
    for section_name, heading_candidates in REQUIRED_SECTIONS.items():
        if not any(heading in section_headings for heading in heading_candidates):
            options = " / ".join(heading_candidates[:2])
            print(f"Error: missing required section '{section_name}': {options}", file=sys.stderr)
            return 1

    full_text = "\n".join(lines)
    for field_name, patterns in REQUIRED_FIELDS.items():
        if not any(re.search(pattern, full_text, re.IGNORECASE) for pattern in patterns):
            options = " / ".join(patterns)
            print(f"Error: missing required field '{field_name}'. Expected pattern: {options}", file=sys.stderr)
            return 1

    for field_name, patterns in REQUIRED_FIELD_VALUES.items():
        if not any(re.search(pattern, full_text, re.IGNORECASE) for pattern in patterns):
            print(
                f"Error: required field '{field_name}' must not be empty. Use a concrete value or 'N/A'.",
                file=sys.stderr,
            )
            return 1

    print(f"OK: commit message structure check passed for {msg_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
