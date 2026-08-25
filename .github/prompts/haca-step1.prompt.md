---
agent: HACA
description: "HACA-SDK Step 1: identify Foxit SDK product/platform/language, assess feasibility, clarify requirements, and output structured task input for confirmation"
tools:
  - read
  - search
  - edit
---

## Instruction

Read `.github/skills/clarify-requirements/SKILL.md` and perform SDK environment identification and requirement clarification according to its rules.

Before processing, check if `foxit-sdk.config.json` exists in the project root and read SDK configuration if available. Also consult `.github/sdk-references/` for product capability information.

## Context

All step-transition gates and confirmation behavior are defined in `.github/copilot-instructions.md` and the loaded skill. This prompt provides normalized inputs only — do not redefine workflow rules here.

## Input Data

Task description: ${input:task:Please enter task details — include which Foxit SDK product, platform, and language if known}

Contract file path (optional):
${input:artifact_path:Leave blank to use an open artifacts/*/haca-workflow.md if available, otherwise auto-generate a new task-id; or enter an existing path (e.g. artifacts/202603271430/haca-workflow.md)}

## Output Indicator

Output must follow the exact End-of-Step Output Format in `clarify-requirements/SKILL.md`, including the SDK Environment section.

Always write the Step 1 output into `artifacts/<task-id>/haca-workflow.md` before the wait-for-confirmation line (use provided `artifact_path`, open-file fallback, or auto-generate path), and end with the single merged Step 1 suffix line defined by the skill.
