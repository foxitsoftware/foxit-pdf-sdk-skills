---
agent: HACA
description: "HACA-SDK Step 4 input template: execute build loop with SDK quality chain (compilation + runtime correctness), governed skills and confirmed subtasks"
tools:
  - read
  - search
  - edit
  - execute
  - agent
---

## Instruction

Read and execute `.github/skills/tdd-loop/SKILL.md` and `.github/skills/evidence-gate/SKILL.md`.
Follow `.github/agents/haca.agent.md` for Step 4 gate order, SDK code quality requirements, human-acceptance handoff policy, and completion behavior.
Before any Step 4 execution, run the prerequisite contract gate from `.github/skills/evidence-gate/SKILL.md`. If the contract file exists and `Workflow Status -> Step Status Matrix -> Step 3` is not `confirmed` (including `draft`, `pending`, or header `current_step: step3_draft`), block immediately and do not start the build loop. Never treat `/haca-step4` invocation, `artifact_path`, or an open contract file as implicit confirmation of Step 3.

All generated code MUST compile without errors and run correctly on the target SDK platform. Verify SDK API correctness against `.github/sdk-references/` when available.

## Context

This prompt provides normalized inputs only — do not redefine workflow rules here.

**Document route (Route B) first-batch scope:** When `artifact_path` is provided, execute Step 4 as a whole-step by default. Do not expand into subtask-level orchestration unless the human explicitly requests it.

**Hard prerequisite note:** If the referenced contract shows Step 3 is still draft, `/haca-step4` must stop at the gate and require Step 3 confirmation first.

## Input Data

Provide **one** of the following (Route B takes priority if `artifact_path` is provided). If a contract file exists, Step 4 input MUST be read from its `## Step 3` chapter:

Route A fallback — session history (only when no contract file exists): paste the confirmed Step 3 subtask list below.
${input:subtasks:Paste the Step 3 output [Subtask List + Execution Order] here, or leave blank if using artifact_path below}

Route B/C — document context: provide the contract file path, or leave blank to use open-file fallback when available.
${input:artifact_path:Leave blank to use an open artifacts/*/haca-workflow.md (Route C) or active task contract (Route A); or enter path to haca-workflow.md (Route B), e.g. artifacts/202603271430/haca-workflow.md}

## Output Indicator

Output TDD evidence, subtask-level completion evidence, and final evidence gate result.
Before each wait-for-confirmation point, write the current Step 4 evidence summary into `artifacts/<task-id>/haca-workflow.md` (Route B uses provided `artifact_path`; Route C uses open-file fallback; Route A uses active task path).
