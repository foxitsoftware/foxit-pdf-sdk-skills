---
description: Generate a validated commit message from the focused HACA Workflow Contract or git changes, then run git commit only after one explicit human confirmation
tools:
  - read
  - search
  - execute
---

## Instruction

Strictly enforce `.github/copilot-instructions.md` `Language Rule` for all output in this prompt, including commit message content, explanations, and human confirmation questions.

### Internal rules (do not surface to the human)

Before drafting text, read `.github/skills/commit-message-rules/SKILL.md` in full and follow its required procedure, templates, required-field rule, length control, and validator scripts. That file is the technical source of truth for format and validation. In conversation, do not name that file, call it a “skill,” quote its section titles, or explain validator implementation unless the human explicitly asks.

### Primary context for what changed (mandatory order)

1. **HACA Workflow Contract**: If the file **currently open and focused** in the editor (the active document) is a HACA Workflow Contract — e.g. path like `artifacts/<task-id>/haca-workflow.md`, or the body clearly identifies itself as the HACA Workflow Contract — use that file as the **primary** source for the commit message.
2. **Git changes**: Otherwise, use `git diff --staged`; if staged diff is empty, use `git diff`.

Optional `change_summary` may only refine or disambiguate; it must **not** replace primary context from (1) or (2).

### HACA Workflow Contract → commit semantics (mandatory)

When (1) applies and the focused file is a HACA Workflow Contract:

1. **Step 2 is authoritative for meaning.** Use **`## Step 2 Solution Design`** and its **`### AI Decision Summary`** — including **Requirement understanding / 需求理解**, **Adopted approach / 采用方案**, **Rejected approach / 拒绝方案**, **Key assumptions / 关键假设**, **Known risks / 已知风险**, and **Uncovered scenarios / 未覆盖场景** — to populate the commit template’s **Task Input** and **AI Decision Summary** fields (compress for length; keep intent).
2. **Do not substitute Step 4 for Step 2.** **`## Step 4 Build`** (implementation summary, TDD evidence, subtask T1–T4 prose, changed-path lists) must **not** replace Step 2 as the source of *what* the change is for and *why*; Step 4 may only refine wording (e.g. concrete filenames) when Step 2 plus **git diff** require disambiguation.
3. **Subject line** `[AI] <type>(<scope>): <subject>`: derive **type**, **scope**, and **subject** from Step 2 **requirement understanding** and **adopted approach**, using **git diff** only to align scope with paths actually changed when needed.
4. **Fallback:** If Step 2 is missing or unusable, use **`## Step 1 Requirement Clarification`**, then **git diff**; use `N/A` where still unknown.

Generate one full commit message in a **single** template language (Chinese or English), following the conversation language unless the human overrides via the language input. Populate every required field; when reliable information is unavailable, use `N/A`.

Write the message to `tmp/<message-file>`, run the length check and structure validation steps from the internal rules, and fix length within the allowed retry limit before presenting the result.

### One confirmation, then optional `git commit`

After validation passes:

- Show the final commit message once.
- Ask a single, explicit question whether to run `git commit -F tmp/<message-file>` (word this in the interaction language).
- Do **not** run `git commit` unless the human clearly agrees. Treat as consent, for example: `confirm`, `ok`, `yes`, `LGTM`, `proceed`, `y`; in Chinese also `确认`, `同意`, `执行`, `好`, `可以`.
- If the human declines or wants edits, update the file, re-validate, show the message again, and ask the same single question again.

When the human consents:

- Run `git commit -F tmp/<message-file>`.
- Report the new commit hash and subject line.
- Delete `tmp/<message-file>` after a successful commit.

If no commit runs:

- Keep `tmp/<message-file>` for the session unless the human asks to delete it.

## Context

This prompt is the user-facing shortcut entry for commit-message generation. It does not redefine HACA orchestration.

## Input Data

Optional change summary override:
${input:change_summary:Leave blank to infer from the active HACA Workflow Contract or git changes, or provide extra context to refine the commit message}

Optional language override:
${input:language:Leave blank to follow conversation language, or enter 中文 / English}

## Output Indicator

Output one validated commit message using a single language template, then ask whether to execute the commit.
