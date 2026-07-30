---
name: tdd-loop
description: >
  Enforce Red-Green-Refactor execution and compilation/runtime correctness in HACA-SDK Step 4. Require
  test-first evidence and compilation pass evidence, block progress when either is missing. Code produced
  must compile without errors and run correctly on the target SDK platform. Invoke only within an active
  HACA session (via @HACA, /HACA, or /haca-step4).
---

# TDD Loop Skill (Foxit SDK)


This skill enforces test-driven execution and SDK code quality in HACA-SDK Step 4. The goal is to make testing drive implementation decisions, ensure all generated code compiles and runs correctly, and keep execution evidence auditable.

## When to use

- Build phase of HACA starts.
- Subtask changes business behavior, boundary handling, or bug fixes.
- Team wants to reduce regression risk through test-first execution.

## SDK Code Quality Chain (mandatory, per subtask)

Every subtask in Step 4 MUST pass the following quality chain before completion:

### Q1: Compilation Verification
1. Run the appropriate build command for the target platform/language.
2. All code must compile without errors.
3. Record: build command, build output (success/errors), platform/compiler version.
4. If compilation fails: diagnose the error, fix the code, and re-run. Do not proceed until compilation passes.

### Q2: Runtime Verification
1. Run the generated code or test suite against the target SDK.
2. Verify that the primary use case executes without runtime errors (no crashes, no unhandled exceptions, no SDK error codes).
3. Record: run command, execution output, SDK API return values for key operations.
4. If runtime fails: apply systematic-debugging, fix the issue, and re-verify.

### Q3: SDK API Correctness Verification
1. Verify all Foxit SDK API calls use correct:
   - Class/module names
   - Method/function signatures
   - Parameter types and valid ranges
   - Return type handling and error checking
2. Verify proper SDK lifecycle management:
   - Library initialization before any SDK calls
   - License validation
   - Document/object handle cleanup
   - Library release on exit
3. Cross-check against `.github/sdk-references/` when available.

**Document route (Route B) — first-batch scope:** When Step 4 is invoked via `artifact-path`, "whole-step execution" is the default mode (read confirmed Step 3 output from `## Step 3` chapter, execute the full step, write evidence summary to `## Step 4` chapter). This means: (a) do not output RGR progress at each subtask boundary, and (b) defer the final completion summary until all subtasks finish. This is a presentation optimization, NOT a license to skip the TDD chain or SDK quality chain for any subtask. The TDD Red-Green-Refactor cycle and SDK quality checks must be applied to each behavior-changing subtask regardless of routing mode. If the human explicitly requests subtask-level RGR reporting and per-subtask confirmations, provide that level of detail, but the underlying discipline remains mandatory and unchanged.

**Contract-first input rule (Route A + Route B + Route C):** If `artifacts/<task-id>/haca-workflow.md` exists, Step 4 must read baseline input from confirmed `## Step 3` chapter in that file before processing. Do not derive Step 4 baseline input from memory/current-conversation context.

**Contract persistence timing (Route A + Route B):** Before every wait-for-confirmation point in Step 4, write the latest Step 4 evidence summary into `artifacts/<task-id>/haca-workflow.md`, set `Workflow Status -> Step Status Matrix -> Step 4` to `draft`, set header `current_step: step4_draft`, and refresh `last_updated_at`. After explicit human confirmation to continue, promote Step 4 row back to `confirmed` at the corresponding checkpoint.

**Prerequisite gate (mandatory):** Validate `artifacts/<task-id>/haca-workflow.md` has `Workflow Status -> Step Status Matrix -> Step 3 = confirmed` before executing Step 4. If Step 3 is not confirmed, block and require Step 3 confirmation first.

Record `TDD Evidence: N/A` only when all conditions are true:
- Subtask is docs-only or formatting-only.
- No runtime behavior, API contract, schema, or permission changes.
- Existing tests are unaffected.

## Required inputs

- Confirmed subtask objective and scope
- Testable acceptance criteria
- Affected modules, interfaces, and dependencies
- Known risks and uncovered scenarios

## Execution rules

1. Red
- Write or update tests first.
- Execute tests and observe failures.
- Record failed test names, failure symptoms, and expected behavior.

2. Green
- Implement the minimum change to make tests pass.
- Avoid unrelated optimizations during Green.
- Record why the implementation is minimal and sufficient.

3. Refactor
- Refactor only when tests are green.
- Preserve external behavior and contract compatibility.
- Record what was improved and why behavior is unchanged.

## Hard gates

Before proceeding to each phase, verify:
- **Before Green**: Red evidence must be present — failing test names, failure symptoms, and expected behavior.
- **Before Refactor**: Green evidence must be present — tests passing with the minimum implementation.
- **Before subtask completion**: Refactor must leave all tests passing; no new failures introduced.
- **Before subtask completion handoff**: TDD evidence is required for behavior-changing subtasks. Record `TDD Evidence: N/A` with justification only for docs-only or non-behavior-changing work.
- **Before next subtask**: Subtask evidence and available project checks must be complete and recorded.

## Exception handling

- If tests cannot reproduce stably, roll back to HACA Step 2.
- If subtask boundary mismatches failing tests, roll back to HACA Step 3.
- If requirements changed, roll back to HACA Step 1.
- If the subtask qualifies for the documented Step 4 exception, record `TDD Evidence: N/A` with justification and minimum regression checks.

## Mandatory Superpowers Controls (within Step 4 only)

In Step 4, use these capabilities as mandatory quality controls to improve code quality:

- `test-driven-development`: enforce failing-test-first execution for behavior-changing work.
- `verification-before-completion`: require fresh command evidence before completion claims.
- `systematic-debugging`: require root-cause-first investigation before attempting fixes.
- `requesting-code-review`: require structured review before completion.
- `receiving-code-review`: require technical evaluation and feedback handling before accepting review outcomes.

Local offline sources:
- `.github/skills/superpowers/test-driven-development/SKILL.md`
- `.github/skills/superpowers/verification-before-completion/SKILL.md`
- `.github/skills/superpowers/systematic-debugging/SKILL.md`
- `.github/skills/superpowers/requesting-code-review/SKILL.md`
- `.github/skills/superpowers/receiving-code-review/SKILL.md`

Required execution chain per subtask:
1. Red-Green-Refactor or `TDD Evidence: N/A` with justification for docs-only or non-behavior-changing work
2. Verification evidence
3. Systematic debugging evidence when failures or unexpected results occur, or `Not Triggered` evidence when no failures are observed
4. Review request and review reception evidence
5. Evidence Gate validation
6. Acceptance handoff:
   - Summarize changed files, test outcomes, and unresolved risks for human acceptance.
   - Do not execute `git commit` in Step 4; commit actions are human-led after acceptance.
7. After all subtasks are complete:
   - Execute final Evidence Gate validation.
   - If the final gate passes, output exactly `All subtasks are complete, pending human verification before human-led git commit.`.
   - After outputting the completion prompt, wait for human follow-up instructions.

For mandatory Step 4 capabilities, record in the evidence pack: capability name, trigger reason, key findings, suggested action, adopted/rejected with reason.

## Output format

## TDD Evidence
- Subtask ID:
- Red evidence:
- Green evidence:
- Refactor notes:
- Regression checks:
- Uncovered scenarios:

## SDK Quality Evidence
- Compilation: [PASS/FAIL] — build command: [command], platform: [platform], output summary: [summary]
- Runtime: [PASS/FAIL] — run command: [command], execution result: [summary]
- SDK API correctness: [VERIFIED/NOT VERIFIED] — API calls checked: [list of key APIs used]
- SDK lifecycle: [CORRECT/ISSUES] — init/cleanup properly handled: [yes/no with details]

[HACA Step 4/4: Build] - Artifacts: artifacts/<task-id>/haca-workflow.md (draft written before confirmation; you may edit this file, then start human acceptance and human-led commit actions)
