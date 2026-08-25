---
agent: HACA
description: "HACA-SDK Step 3: decompose SDK solution into subtasks with proper SDK initialization/cleanup sequencing, annotate dependencies, and wait for confirmation"
tools:
  - read
  - search
  - edit
---

## Instruction

Read `.github/skills/task-decomposition/SKILL.md` and perform task decomposition according to its rules.
Obtain the decomposition strategy (`decompose_strategy` input) from the user selection below before generating any output. Do not derive strategy from the Step 2 confirmation reply. Block if the input is blank or invalid — do not default silently.
Before any Step 3 execution, run the prerequisite contract gate from `.github/skills/evidence-gate/SKILL.md`. If the contract file exists and `Workflow Status -> Step Status Matrix -> Step 2` is not `confirmed` (including `draft`, `pending`, or header `current_step: step2_draft`), block immediately and do not start Step 3. Never treat `/haca-step3` invocation, `artifact_path`, or an open contract file as implicit confirmation of Step 2.

## Context

All step-transition gates, mode selection, and confirmation behavior are defined in `.github/copilot-instructions.md` and the loaded skill. This prompt provides normalized inputs only — do not redefine workflow rules here.

**Hard prerequisite note:** If the referenced contract shows Step 2 is still draft, `/haca-step3` must stop at the gate and require Step 2 confirmation first.

## Input Data

Provide **one** of the following (Route B takes priority if `artifact_path` is provided). If a contract file exists, Step 3 input MUST be read from its `## Step 2` chapter:

Route A fallback — session history (only when no contract file exists): paste the confirmed Step 2 output below.
${input:decision_summary:Paste the Step 2 output [Complete AI Decision Summary] here, or leave blank if using artifact_path below}

Route B/C — document context: provide the contract file path, or leave blank to use open-file fallback when available.
${input:artifact_path:Leave blank to use an open artifacts/*/haca-workflow.md (Route C) or active task contract (Route A); or enter path to haca-workflow.md (Route B), e.g. artifacts/202603271430/haca-workflow.md}

Decomposition strategy — must be chosen before generating Step 3 output.
${input:decompose_strategy:(Required) Choose decomposition strategy: "Decompose" = split into atomic subtasks; "Single-task" = no split, single commit unit}

## Output Indicator

Output must follow the exact End-of-Step Output Format in `task-decomposition/SKILL.md`, including **Markdown heading hierarchy** for content under `### Subtasks` in the contract file (`####` subtask titles, `#####` Task Input / AI Decision Summary — never `##` / `###` there).
Output format: one full description block per subtask, followed by filling `### Execution Order` (and `### Step Transition Note` when used) in the same Step 3 chapter.

Always write the Step 3 output into `artifacts/<task-id>/haca-workflow.md` before the wait-for-confirmation line (Route B uses provided `artifact_path`; Route C uses open-file fallback; Route A uses active task path), and end with the single merged Step 3 suffix line.
