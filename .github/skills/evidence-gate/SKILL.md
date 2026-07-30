---
name: evidence-gate
description: >
  Maintain a single evidence pack across HACA steps. Validate required fields and block step transitions or
  subtask completion when evidence is incomplete. Invoke before each step transition and before each Step 4 subtask
  within an active HACA session.
---

# Evidence Gate Skill


This skill keeps one consistent evidence structure across HACA steps and blocks transitions when required evidence is missing.

## Route resolution for pre-execution validation

Resolve command context in this order before running pre-execution checks:

1. Explicit `artifact-path` in the command -> Route B
2. No explicit path, but active/open file matches `artifacts/*/haca-workflow.md` -> Route C (same checks as Route B)
3. Otherwise -> Route A

Step re-run is allowed for `/haca-step1` through `/haca-step4` even when target step is already `status: confirmed`. Pre-execution validation still requires prerequisite step confirmation for `N>1`.

## When to use

- After Step N receives explicit human confirmation and before entering Step N+1 (Route A — session history route)
- Before each Step 4 subtask completion handoff (both routes)
- After all Step 4 subtasks complete and before the final completion prompt (both routes)
- Before executing Step N when invoked via Route B (document context route) — validate the contract file before proceeding

## Route A — Session history prerequisite validation (run before standard evidence pack checks)

When `/haca-step[N]` is invoked without `artifact-path` and `N>1`, apply these checks before proceeding:

1. Active contract file exists at `artifacts/<task-id>/haca-workflow.md`.
2. `Workflow Status -> Step Status Matrix` contains prerequisite step (N-1) and its status is `confirmed`.
3. Required input for Step N is read from the prerequisite step chapter in that contract file, not from session-memory/chat context.

If the header still indicates the prerequisite draft state (for example `current_step: step1_draft`, `step2_draft`, or `step3_draft`), or the prerequisite row in `Step Status Matrix` is `draft`, block immediately. Never treat command invocation, active-file context, or `artifact-path` as implicit confirmation of the prerequisite step.

If any check fails, block with:
`Step [N-1] is not confirmed in artifacts/<task-id>/haca-workflow.md. Confirm Step [N-1] before running Step [N].`

## Route B/C — Document context route validation (run before Route A gate checks)

When `/haca-step[N]` is invoked with an `artifact-path`, apply these pre-execution checks **before** the standard evidence pack checks below:

**Required checks:**
1. `artifact-path` file exists and is a valid Markdown file. If not: block with `Contract file not found. Run /haca-step1 <same-path> first to initialize.`
2. File header contains all required fields: `task_id`, `current_step`, `last_updated_at`. If any are missing: block and list each missing field.
3. For `N>1`, `Workflow Status -> Step Status Matrix` must contain prerequisite step (N-1) row and status `confirmed`. If not: block with the message: `Step [N-1] is not confirmed in <artifact-path>. Confirm or complete it before running Step [N].`
4. All required content fields for the prerequisite step are present (non-empty). If any are missing: block and list each missing field with the step it belongs to.
5. If Step N row in `Step Status Matrix` is already `confirmed`, treat this as a valid re-run entry and continue validation (do not block on already-confirmed status).

**Draft-state clarification (mandatory):** For `N>1`, header values such as `current_step: step1_draft`, `step2_draft`, or `step3_draft` mean the prerequisite step is still unconfirmed. These are explicit blocking states for Step 2, Step 3, and Step 4 respectively.

**Validation principle:** Check field presence and `status: confirmed` only (via `Step Status Matrix`). Do **not** perform hash validation or content authenticity checks. Trust the human's document management authority for content edits, but never infer confirmation from command invocation.

**Input source rule (Route A + Route B/C):** If the contract file exists for the current task, the prerequisite step chapter in that file is the required input source for Step N. Do not use memory, prior dialogue, or pasted session-history text as the primary input source.

**Route B blockage message template:**
```
[HACA Gate: Document Contract Validation] - Blocked

Reason: <one of the following>
  - Contract file not found: <artifact-path>
  - Missing file header fields: <field list>
  - Step [N-1] status is not confirmed in Step Status Matrix (current: <actual status>)
  - Missing required content fields in Step [N-1]: <field list>
  - Header still indicates prerequisite draft state: <current_step>
  - Input source violation: contract exists but Step [N] input was not read from Step [N-1] chapter

Action: <specific repair instruction>
```

**Route A vs Route B/C:** Route B/C pre-checks replace the "prerequisite confirmation in session history" check from Route A. All other evidence pack rules below apply to all routes.

## Required evidence pack

- SDK environment evidence: product, platform, architecture, language confirmed; feasibility assessed
- Requirement evidence: goal, constraints, testable acceptance criteria, scope impact
- Design evidence: adopted approach, rejected approach, key assumptions, SDK reference basis
- Risk evidence: known risks with mitigation actions
- Test evidence: Red-Green-Refactor records and regression checks (required in Step 4; Step 1-3 may be N/A)
- SDK quality evidence (Step 4 mandatory): compilation pass, runtime correctness, SDK API correctness, SDK lifecycle management
- Decision evidence: uncovered scenarios and decision owner
- Capability execution evidence (when superpowers is used): capability name, capability source path, trigger reason, key findings, suggested action, adopted/rejected decision with rationale
- Step 4 mandatory capability evidence: execution evidence for `test-driven-development`, `verification-before-completion`, `systematic-debugging`, `requesting-code-review`, and `receiving-code-review`; if a capability is not triggered in the subtask, record `Not Triggered` evidence with rationale, or provide an explicitly approved exception
- Step 4 completion prompt evidence: exact completion prompt text and output timestamp

## Gate rules

- Missing required evidence for the current step -> block step transition.
- Contract file exists but current step input was not sourced from the prerequisite chapter in that file -> block step transition.
- Missing SDK environment evidence (product, platform, language) in Step 1 -> block transition to Step 2.
- SDK feasibility assessed as "❌ Not feasible" without user acknowledgment -> block transition to Step 2.
- Missing SDK reference basis in Step 2 design evidence -> warn (non-blocking if references not yet available).
- Non-testable acceptance criteria -> return to Step 1.
- Risk entries missing trigger-impact-mitigation format -> return to Step 2.
- Subtask boundaries unclear or dependency conflicts -> return to Step 3.
- If superpowers is used but capability execution evidence is missing -> block step transition.
- If superpowers is used but capability source path is not under `.github/skills/superpowers/` -> block step transition.
- In Step 1-3 transitions, test evidence may be `N/A` and is non-blocking.
- In Step 4 and before each subtask completion handoff, test evidence is mandatory. For docs-only or non-behavior-changing subtasks, `TDD Evidence: N/A` is acceptable when justification and minimum regression checks are provided.
- In Step 4, SDK quality evidence (compilation pass, runtime correctness) is mandatory for all code-producing subtasks. Missing compilation or runtime evidence -> block subtask completion.
- In Step 4 and before each subtask completion handoff, missing evidence for any mandatory capability (`test-driven-development`, `verification-before-completion`, `systematic-debugging`, `requesting-code-review`, `receiving-code-review`) -> block progression unless `Not Triggered` evidence or an explicit approved exception is documented.
- In Step 4 final gate, if completion prompt text is not exactly `All subtasks are complete, pending human verification before human-led git commit.` -> block Step 4 completion.
- Missing execution evidence in Step 4 -> block progression.

## Lightweight mode

> **Terminology clarification**: Lightweight mode governs Evidence Gate's evidence collection granularity — it answers "how much evidence is needed". It is independent from Step 4 acceptance handoff policy, which is defined in `.github/agents/haca.agent.md`.

Lightweight mode is allowed only when all conditions are true:

- Change touches one module only
- No data migration or permission model change
- Expected review time <= 30 minutes

Even in lightweight mode, these are still required:

- Testable acceptance criteria
- Known risks
- Uncovered scenarios
- Minimum test evidence (Step 1-3 may be `N/A` with reason; Step 4 requires execution evidence)

## Output format

## Evidence Check Result
- Current step:
- Passed items:
- Missing items:
- Blocking items:
- Rollback recommendation:
- Decision:

If `Decision: Pass`, do not output a separate HACA Gate wait line.
If blocking items remain, append:

`[HACA Gate: Evidence Validation] - Artifacts: artifacts/<task-id>/haca-workflow.md - Blocked until required evidence is complete`

## Step 4 Acceptance Boundary

This skill validates evidence only.

- It does not define human acceptance policy details.
- It does not execute `git commit`.
- In Step 4, when this gate passes, acceptance handoff behavior must follow `.github/agents/haca.agent.md`.

