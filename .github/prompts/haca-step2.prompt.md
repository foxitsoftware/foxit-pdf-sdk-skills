---
agent: HACA
description: HACA-SDK Step 2: consult SDK references, propose optimal solution with alternatives, systematically identify and mitigate risks, and output a complete AI decision summary for confirmation
tools:
  - read
  - search
  - edit
---

## Instruction

Read `.github/skills/risk-identification/SKILL.md` and perform SDK-referenced solution design and risk identification according to its rules.
Before any Step 2 execution, run the prerequisite contract gate from `.github/skills/evidence-gate/SKILL.md`. If the contract file exists and `Workflow Status -> Step Status Matrix -> Step 1` is not `confirmed` (including `draft`, `pending`, or header `current_step: step1_draft`), block immediately and do not start Step 2. Never treat `/haca-step2` invocation, `artifact_path`, or an open contract file as implicit confirmation of Step 1.

Consult `.github/sdk-references/` for the SDK product identified in Step 1 before proposing solutions.

## Context

All step-transition gates and confirmation behavior are defined in `.github/copilot-instructions.md` and the loaded skill. This prompt provides normalized inputs only — do not redefine workflow rules here.

**Hard prerequisite note:** If the referenced contract shows Step 1 is still draft, `/haca-step2` must stop at the gate and require Step 1 confirmation first.

## Input Data

Provide **one** of the following (Route B takes priority if `artifact_path` is provided). If a contract file exists, Step 2 input MUST be read from its `## Step 1` chapter:

Route A fallback — session history (only when no contract file exists): paste the confirmed Step 1 output below.
${input:task_input:Paste the Step 1 output [Task Input + AI Decision Summary] here, or leave blank if using artifact_path below}

Route B/C — document context: provide the contract file path, or leave blank to use open-file fallback when available.
${input:artifact_path:Leave blank to use an open artifacts/*/haca-workflow.md (Route C) or active task contract (Route A); or enter path to haca-workflow.md (Route B), e.g. artifacts/202603271430/haca-workflow.md}

## Output Indicator

Output must follow the exact End-of-Step Output Format in `risk-identification/SKILL.md`.

Always write the Step 2 output into `artifacts/<task-id>/haca-workflow.md` before the wait-for-confirmation line (Route B uses provided `artifact_path`; Route C uses open-file fallback; Route A uses active task path), and end with the single merged Step 2 suffix line.
