---
name: task-decomposition
description: >
  Execute Step 3 of the HACA-SDK workflow: split the confirmed SDK solution into code-review-friendly subtasks with
  annotated dependencies and an execution order plan for human confirmation. SDK initialization, license setup,
  and resource cleanup must be properly sequenced. Refactor and feat changes must be placed in separate subtasks.
  Invoke when HACA is active (via @HACA, /HACA, or /haca-step3), or when users ask to split work or plan
  execution order.
---

# Task Decomposition Skill (Foxit SDK)


Step 3 of the HACA-SDK workflow. Based on confirmed Step 2 output, choose one of two strategies:
- `Decompose` (default): split the confirmed solution into atomic subtasks and output dependency graph as the execution plan for Step 4.
- `Single-task`: skip decomposition and output exactly one executable unit.

## SDK-Specific Decomposition Guidelines

When decomposing SDK-based tasks, ensure:

1. **SDK initialization and license setup** must be the first subtask if not already present in the project.
2. **Resource cleanup and handle disposal** should be the last subtask or included in each subtask that opens SDK resources.
3. **Platform-specific code** (e.g., Windows-only C code, ArkTS Harmony code) must be in dedicated subtasks, not mixed with cross-platform logic.
4. **SDK API call sequences** must respect the SDK's required call order (e.g., initialize library → open document → operate → close document → release library).

## Contract Persistence Action (Route A + Route B)

For every Step 3 output (regardless of route):

- Read Step 2 baseline from `artifacts/<task-id>/haca-workflow.md` (`## Step 2` chapter), treating the latest file content as source of truth.
- If the contract file exists, do not derive Step 3 input from memory/current-conversation context; use the `## Step 2` chapter as the only baseline source.
- Validate `Workflow Status -> Step Status Matrix -> Step 2` is `confirmed` before executing Step 3. If not confirmed, block and require Step 2 confirmation first.
- If the contract header is still `current_step: step2_draft` or the Step 2 row in Step Status Matrix is `draft`, treat Step 2 as unconfirmed. `/haca-step3`, `artifact-path`, or open-file context never counts as implicit Step 2 confirmation.
- Before waiting for confirmation, write Step 3 output (subtask list + execution order) into `## Step 3` chapter.
- Set `Workflow Status -> Step Status Matrix -> Step 3` to `draft`, and update file header to `current_step: step3_draft`, `last_updated_at: <timestamp>`.
- Append to end of step output by using the single merged Step 3 suffix line (do not output a separate `File updated` line).
- After explicit human confirmation, promote `Workflow Status -> Step Status Matrix -> Step 3` to `confirmed`, update file header to `current_step: step3_confirmed`, and refresh `last_updated_at`.
- The decomposition output (single-task or multi-task) must be written in a format that Step 4 can directly consume via document context route.

## Markdown heading hierarchy (contract file — mandatory)

When writing into `artifacts/<task-id>/haca-workflow.md`, subtasks are **nested under** `## Step 3 Task Decomposition` → `### Subtasks`. The outline must stay valid: **nothing inside `### Subtasks` may use `##` or `###` for subtask titles or their inner sections**, or those headings become siblings of Step sections in TOC / parsers and break Step 4 document routing.

| Element | Required level | Example |
|--------|----------------|---------|
| Subtask title | `####` (H4) | `#### T1 — [AI] feat(api): add health endpoint` |
| Inside each subtask | `#####` (H5) | `##### Task Input`, `##### AI Decision Summary` |
| Between subtasks | blank line only | Do **not** use a line containing only `---` (confusable with YAML front matter and adds noise). |

Replace the template’s `### Subtasks` placeholder entirely with one or more subtask blocks following the table. Update the existing `### Execution Order` and `### Step Transition Note` sections in the same Step 3 chapter (do not introduce a new `## Execution Order`).

## Step 3 Decomposition Strategy (Mandatory at Invocation)

When `/haca-step3` is invoked, the agent MUST collect the user's decomposition strategy choice **before producing any output**. This choice may not be skipped or defaulted silently.

Use the `decompose_strategy` input value from the Step 3 prompt invocation.

Resolution priority:

| Priority | Condition | Result |
|------|------|------|
| 1 | User selects `Decompose` at invocation | Use standard decomposition flow |
| 2 | User selects `Single-task` at invocation | Skip split, generate exactly one subtask |
| 3 | Input blank or invalid | Block and ask the user to choose before proceeding; do not default silently |

When `Single-task` is selected:
- Keep the same subtask output contract (`Task Input` + `AI Decision Summary`).
- `Execution Order` is single-task serial only.
- Parallel/converge dependency narration is not applicable.

## Three Granularity Conditions (all required)

Validate each candidate subtask against all conditions:

```
1. Can the subtask intent be explained in one sentence?
   (without joining two different actions using "and")
        No -> split further

2. Is the repository still buildable and testable after merging?
        No -> split further

3. Can a reviewer fully understand it within 30 minutes?
        No -> split further

All three pass -> granularity is appropriate [OK]
```

## Mandatory Splitting Rules

The following cases **must** be split into independent subtasks without exception:

### Rule 1: Separate `refactor` and `feat`

```
[X] Wrong: Refactor UserService and add batch export feature in one commit
[OK] Correct:
  T1: refactor(user): extract shared UserService query methods
  T2: feat(user): add batch export API for user data
```

Reason: once mixed, reviewers cannot tell whether behavior changes come from refactor side effects or intentional new features.

### Rule 2: Database migration must be independent and first

```
[OK] Correct order:
  T1: chore(db): add migration script for `orders.status`  <- must be first
  T2: feat(order): implement order status transition logic
```

### Rule 3: Configuration changes before dependent code

```
[OK] Correct order:
  T1: chore(config): add `FEATURE_NEW_CHECKOUT` feature flag
  T2: feat(checkout): implement new checkout flow (guarded by flag)
```

### Rule 4: Test infrastructure before business test cases

```
[OK] Correct order:
  T1: test(setup): build integration-test mock server
  T2: test(order): add integration tests for order creation flow
```

## Commit Type Quick Reference

| type | Meaning | Granularity constraint |
|------|------|------------|
| `feat` | One user-visible feature point | no refactor, no unrelated fixes |
| `fix` | One independent bug fix | do not merge unrelated bugs |
| `refactor` | Structural changes only, no external behavior change | no feature changes |
| `test` | Test code | may be combined with simple implementation; test infrastructure stays separate |
| `chore` | Build/dependency/config changes | no business logic changes |
| `docs` | Documentation changes | no code changes |
| `perf` | Performance optimization without behavior change | no feature changes |

Subtask title format (with `[AI]` prefix, used as change-type taxonomy):
```
[AI] <type>(<scope>): <subject>
```

## Dependency Annotation

Identify these four dependency types while splitting:

| Type | Identification signal | Example |
|------|----------|------|
| Code dependency | T2 calls new function/interface/class from T1 | T1 adds helper function, T2 uses it |
| Data dependency | T2 depends on schema change from T1 | T1 adds field, T2 writes the field |
| Test dependency | T2 tests depend on T1 test infrastructure | T1 builds mock, T2 uses mock |
| Config dependency | T2 depends on config introduced in T1 | T1 adds flag, T2 reads flag |

## Trigger-Based Superpowers Assist (within Step 3 only)

Use superpowers capabilities to make decomposition directly executable in Step 4.

- Trigger condition A: you MUST use `writing-plans` when decomposition needs a persistent execution plan for worker agents.
- Trigger condition B: you MUST use `using-git-worktrees` when isolated execution workspace is needed.
- Local offline source A: `.github/skills/superpowers/writing-plans/SKILL.md`
- Local offline source B: `.github/skills/superpowers/using-git-worktrees/SKILL.md`

Boundary:
- Keep HACA subtask granularity and output contract unchanged.
- Do not replace Step 3 output with plan-only artifacts.

If triggered and used, record: capability name, trigger reason, key findings, suggested action, adopted/rejected with reason.

## End-of-Step Output Format

Output full description for each subtask **using the heading levels from the "Markdown heading hierarchy" subsection above** when persisting to the contract file:

```markdown
#### T1 — [AI] <type>(<scope>): <subject>

##### Task Input
- Requirement description: [specific goal and acceptance criteria for this subtask]

##### AI Decision Summary
- Requirement understanding:
- Adopted approach:
- Rejected approach:
- Key assumptions:
- Known risks:
- Uncovered scenarios:

#### T2 — [AI] <type>(<scope>): <subject>

##### Task Input
- …

##### AI Decision Summary
- …
```

After all subtask descriptions, fill the contract’s existing **`### Execution Order`** section (same Step 3 chapter, after `### Subtasks`):

```markdown
### Execution Order
- Serial: T1 → T2 → T3
- Parallel: T4 and T5 have no dependency and can run together
- Converge: T6 runs after both T4 and T5 are completed

# Single-task strategy example
- Serial: T1 only
```

Finally append:
```
[HACA Step 3/4: Task Decomposition] - Artifacts: artifacts/<task-id>/haca-workflow.md (draft written before confirmation; you may edit this file, then confirm next step or terminate) - Wait for confirmation before moving to Step 4
```


## References

- Common anti-patterns and correction examples -> `references/antipatterns.md`
