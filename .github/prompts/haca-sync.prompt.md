---
description: Sync HACA customizations from .github to .cursor/.opencode, update only manual adaptation layer files, run sync check, report completion with evidence of orchestration layer sync
tools:
  - read
  - search
  - edit
  - execute
---

You are the HACA maintenance execution assistant. Follow the sequence below strictly. Do not skip, merge, or reorder steps.

## P) Load domain knowledge (mandatory, before any edits)

Before running any script or touching any file, read the following document in full:

- `docs/prompt-writing-best-practices-research-report.md`

This document is the authoritative domain knowledge source for prompt writing standards and best practices. When updating the manual adaptation layer files (`.cursor/AGENTS.md`, `.cursor/rules/haca.mdc`, `opencode.json`), apply its principles to ensure instructions in those files are clear, structured, and use positive-instruction style rather than prohibitions only.

Record in your final report whether this domain knowledge was consulted and any adjustments made as a result.

## 0) Change Boundary (Hard Constraint)

You may modify only the following manual adaptation layer files:
- `.cursor/AGENTS.md`
- `.cursor/rules/haca.mdc`
- `.opencode/agents/haca.agent.md`
- `opencode.json`

**Note: `.opencode/agents/haca.agent.md` remains a manual adaptation file.** Do not treat it as an auto-generated target when evaluating sync results.

**Platform frontmatter preservation rule (mandatory):** treat the frontmatter in `.cursor/agents/*.md` and `.opencode/agents/*.md` as platform-owned configuration. Synchronization may update only the transformed agent body; it must not rewrite, normalize, or regenerate target frontmatter fields, ordering, nesting, or platform-specific syntax.

Do not modify any other file.
Do not run any VCS write operation, including `git commit`, `git push`, `git merge`, or `git rebase`.

## 1) Run Synchronization First

Execute:

```bash
python3 scripts/sync_haca_customizations.py
```

Expected behavior: sync HACA source customizations from `.github/` into the generated Cursor/OpenCode targets. `.opencode/agents/haca.agent.md` remains manual and may require separate review/update within the allowlist above.

**Critical checkpoint after sync:**
- Verify whether `.opencode/agents/haca.agent.md` still matches the intended latest build loop definitions (§4.5)
- If Step 4 orchestration was modified in `.github/agents/haca.agent.md`, manually align `.opencode/agents/haca.agent.md` when needed
- Verify that agent frontmatter in `.cursor/agents/*.md` and `.opencode/agents/*.md` was preserved as-is; only the synchronized body may change
- Do not assume `.opencode/agents/haca.agent.md` was updated by the sync script

**Mandatory anti-omission check (blocking):**
- You MUST compare `.opencode/agents/haca.agent.md` against `.github/agents/haca.agent.md` in this run, even when sync/check already passes.
- You MUST output one explicit conclusion line in the final report:
  - `OpenCode orchestration alignment: Updated` (and list what changed), or
  - `OpenCode orchestration alignment: Already aligned` (and list the compared sections, at minimum: §2.2, §3.1 Step 4 skills, §4.2-§4.5, §5, §7 Step 4 suffix)
- If this conclusion line is missing, treat the run as incomplete and do not report success.

## 2) Understand Source Changes and Update Adaptation Layer

Goal: identify what changed in the current `.github/` source, then update the manual adaptation layer files using Cursor/OpenCode custom-agent rules and best practices so that the latest HACA behavior is fully aligned with:
- `docs/haca-execution-flow.md`

Execution rules:
- Apply only necessary edits within the four files listed in Step 0.
- If a file does not need changes, explicitly report "No changes required" for that file.
- Do not edit any sync-managed generated target file outside the Step 0 allowlist.
- Do not propose or apply any change that regenerates `.cursor/agents/*.md` or `.opencode/agents/*.md` frontmatter from `.github/agents/*.md`; if a sync rule touches those files, preserve their existing frontmatter verbatim.

## 3) Run Consistency Check

Before running the script, check prompt input variable consistency:

**Prompt input consistency check list:**
1. All four `haca-step*.prompt.md` files use `${input:artifact_path}` (not `artifact-path`, `artifactPath`, or any alias).
2. `haca-step1.prompt.md` treats `artifact_path` as optional (new task if blank).
3. `haca-step2.prompt.md`, `haca-step3.prompt.md`, `haca-step4.prompt.md` declare Route B takes priority when `artifact_path` is provided.
4. `haca-step2.prompt.md`, `haca-step3.prompt.md`, `haca-step4.prompt.md` state session-history input is fallback only when no contract file exists.
5. `haca-step2.prompt.md`, `haca-step3.prompt.md`, `haca-step4.prompt.md` reference Route C open-file fallback and active Route A contract wording consistently.
6. No prompt file duplicates orchestration logic (gate rules, route resolution, commit policy belong in `haca.agent.md` and skills only).
7. The four step prompts use Instruction / Context / Input Data / Output Indicator structure.
8. `commit-message.prompt.md` exists under `.github/prompts/`, uses Instruction / Context / Input Data / Output Indicator structure, requires human confirmation before `git commit`, and states that the focused HACA Workflow Contract (if any) takes priority over git diff as the primary message source.
9. `commit-message.prompt.md` is not added to `EXCLUDED_PROMPT_FILES`, so sync generates corresponding targets in `.cursor/commands/` and `.opencode/prompts/`.

**Orchestration layer sync verification (NEW):**
10. `.cursor/agents/haca.agent.md` contains the latest build loop logic from `.github/agents/haca.agent.md`
11. `.opencode/agents/haca.agent.md` is reviewed as a manual adapter and updated only if its Step 4 logic no longer matches the current intended behavior
12. `.cursor/agents/*.md` and `.opencode/agents/*.md` frontmatter remains platform-specific after sync or manual alignment: no source-derived field replacement, no schema normalization, and no loss of platform-only keys
13. Final report includes the exact `OpenCode orchestration alignment: Updated` or `OpenCode orchestration alignment: Already aligned` line; otherwise this step fails

Fix any inconsistency in the allowed files before proceeding.

Execute:

```bash
python3 scripts/sync_haca_customizations.py --check
```

Pass criteria: command output must contain the exact text below:

```text
CHECK OK: no stale markdown targets.
```

If the check fails:
- Continue fixing issues only within the four files allowed in Step 0.
- Re-run the check until it passes.

## 4) Print Final Result (No Commit)

Return a concise completion message that must include:
- "Synchronization completed"
- The Step 3 pass text: `CHECK OK: no stale markdown targets.`
- A statement clarifying whether `.opencode/agents/haca.agent.md` required manual review/update
- The exact alignment conclusion line from Step 1 mandatory anti-omission check
- An explicit statement that no commit operation was executed
