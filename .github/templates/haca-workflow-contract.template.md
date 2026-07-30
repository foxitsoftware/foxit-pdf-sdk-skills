---
task_id: <task-id>
current_step: step1_draft
last_updated_at: <iso-8601-timestamp>
---

# HACA Workflow Contract

<!-- Document structure: each workflow step is exactly one ## (H2) heading. Under a step, use ### for "Task Input" and "AI Decision Summary" (and other step-specific ### sections). Use #### for fields under those. Never add a new ## inside a step body — it would break the outline. Replace all TBD / angle-bracket placeholders with real content when drafting. -->

## Workflow Status

### Overall
- Workflow overall status: Step 1 draft has been generated and is pending human confirmation.
- Current step: `step1_draft`
- Last updated at: `<iso-8601-timestamp>`

### Status Maintenance Note
After humans update this file offline, they should first review and synchronize the statuses of Step 1 through Step 4 before continuing. Step statuses are prerequisite checks for stepwise commands: before running `/haca-step2`, confirm Step 1 is eligible with status `confirmed`; before running `/haca-step3`, confirm Step 2 is eligible with status `confirmed`; before running `/haca-step4`, confirm Step 3 is eligible with status `confirmed`.

### Step Status Matrix
| Step | Name | Status |
| --- | --- | --- |
| Step 1 | Requirement Clarification | draft |
| Step 2 | Solution Design | pending |
| Step 3 | Task Decomposition | pending |
| Step 4 | Build | pending |

## Step 1 Requirement Clarification

<!-- Step 1: Map from clarify-requirements skill. SDK Environment MUST be filled first. Requirement description MUST use the bullet labels below (Goal through Acceptance criteria). Key assumptions: one bullet per assumption, or "- None." if none. -->

### SDK Environment

#### Product
TBD

#### Platform
TBD

#### Architecture
TBD

#### Language
TBD

#### SDK Feasibility
TBD (✅ Feasible / ⚠️ Partially feasible / ❌ Not feasible)

#### Config source
TBD (foxit-sdk.config.json / user confirmation / context inference)

### Task Input

#### Jira ticket
N/A

#### Requirement description
- **Goal:** TBD
- **Functional requirements:**
  - TBD
- **Non-functional attributes:** TBD
- **Constraints:** TBD
- **Acceptance criteria:**
  - TBD

### AI Decision Summary

#### Requirement understanding
TBD

#### Key assumptions
- TBD

#### SDK capability notes
- TBD

## Step 2 Solution Design

<!-- Step 2: Input source MUST cite the contract path and the Step 1 heading, plus Step 1 matrix status `confirmed`. SDK Reference Basis: list consulted SDK reference files. Solution Comparison: present alternatives with pros/cons when multiple approaches exist. Known risks: one bullet per risk; each bullet should state trigger, impact, and mitigation (same sentence or sub-clauses). Decomposition Strategy: record the resolved strategy for Step 3 (`Decompose` vs `Single-task`) per haca.agent.md / governance; quote human choice or document default resolution. -->

### Task Input

#### Input source
`artifacts/<task-id>/haca-workflow.md` — `## Step 1 Requirement Clarification` (Step 1 status in matrix: `confirmed`)

### SDK Reference Basis

#### Referenced materials
TBD (list of SDK reference files consulted, or "general SDK knowledge" if none available)

#### SDK product
TBD

#### Target environment
TBD (platform / architecture / language)

### Solution Comparison

<!-- List alternative solutions when multiple approaches exist. Use #### for each solution. -->

#### Solution A: TBD (Recommended)
- **Description:** TBD
- **SDK APIs:** TBD
- **Pros:** TBD
- **Cons:** TBD

#### Solution B: TBD (Alternative)
- **Description:** TBD
- **SDK APIs:** TBD
- **Pros:** TBD
- **Cons:** TBD

### AI Decision Summary

#### Requirement understanding
TBD

#### Adopted approach
- TBD

#### Rejected approach
- TBD

#### Key assumptions
- TBD

#### Known risks
- **TBD (risk title):** Trigger: TBD. Impact: TBD. Mitigation: TBD.

#### Uncovered scenarios
- TBD

#### SDK-specific considerations
- TBD

### Decomposition Strategy Choice

#### Selected strategy
TBD

## Step 3 Task Decomposition

<!-- Step 3: Input source cites Step 2 + confirmed. Superpowers: name each skill considered, trigger reason, and adopted/rejected; or state explicitly that none were triggered and why. Subtasks: #### / ##### rules in the Subtasks comment. Execution Order: Serial / Parallel / Converge lines; use "N/A" for unused dependency patterns. -->

### Task Input

#### Input source
`artifacts/<task-id>/haca-workflow.md` — `## Step 2 Solution Design` (Step 2 status in matrix: `confirmed`)

### AI Decision Summary

#### Superpowers assist (Step 3)
- TBD (e.g. `writing-plans` / `using-git-worktrees`: not triggered — reason; or triggered — summary and outcome)

### Subtasks

<!-- Contract authors / Step 3 AI: Subtasks must stay under this H3. Use #### for each subtask title (e.g. #### T1 — [AI] type(scope): subject). Use ##### for Task Input and AI Decision Summary inside each subtask. Never use ## or ### for those — they break the document outline. Do not separate subtasks with a --- line. -->

#### T1 — [AI] &lt;type&gt;(&lt;scope&gt;): &lt;subject&gt;

##### Task Input
- Jira ticket: N/A
- Requirement description:
  - TBD

##### AI Decision Summary
- Requirement understanding: TBD
- Adopted approach: TBD
- Rejected approach: TBD
- Key assumptions: TBD
- Known risks: TBD
- Uncovered scenarios: TBD

### Execution Order
- **Serial:** T1 → T2 → …
- **Parallel:** TBD or N/A
- **Converge:** TBD or N/A

### Step Transition Note
TBD (one short paragraph: recommended order for Step 4, review handoff, or dependency caveats)

## Step 4 Build

<!-- Step 4: Input source cites Step 3 + confirmed. Build Execution Summary: one bullet per subtask (prefix **Tn —**), plus optional repo-wide bullets (changed files, config). TDD Evidence: for each behavior-changing subtask use a **Tn（label）** bold header (not ## headings) then bullets Subtask ID, Red / Green / Refactor / Regression / Uncovered; for docs-only subtasks use one bullet **TDD Evidence:** N/A with justification. SDK Quality Evidence: compilation, runtime, API correctness per subtask. Mandatory Capability Evidence: one line per required superpower (trigger, execution, conclusion or Not Triggered). Evidence Gate: transition + final lines with Pass/Fail and reason. Completion prompt: exact sentence required by haca.agent.md + UTC timestamp. -->

### Task Input

#### Input source
`artifacts/<task-id>/haca-workflow.md` — `## Step 3 Task Decomposition` (Step 3 status in matrix: `confirmed`)

### AI Decision Summary

#### Build Execution Summary
- **T1 — [AI] &lt;type&gt;(&lt;scope&gt;):** TBD (what shipped; files touched; TDD phase summary if applicable)
- **T2 — …:** TBD
- **Changed paths:** TBD

#### TDD Evidence

**T1（behavior-changing example）**
- **Subtask ID:** TBD
- **Red evidence:** TBD
- **Green evidence:** TBD
- **Refactor notes:** TBD
- **Regression checks:** TBD
- **Uncovered scenarios:** TBD

**T2（docs-only example）**
- **TDD Evidence:** N/A — TBD (justify: no runtime/API/schema/permission change; note minimal manual check if any)

#### SDK Quality Evidence

**T1**
- **Compilation:** TBD (PASS/FAIL — build command, platform, output summary)
- **Runtime:** TBD (PASS/FAIL — run command, execution result)
- **SDK API correctness:** TBD (VERIFIED/NOT VERIFIED — API calls checked)
- **SDK lifecycle:** TBD (CORRECT/ISSUES — init/cleanup details)

#### Mandatory Capability Evidence
- **test-driven-development:** TBD (trigger / execution / conclusion, or Not Triggered + reason)
- **verification-before-completion:** TBD
- **systematic-debugging:** TBD
- **requesting-code-review:** TBD
- **receiving-code-review:** TBD

#### Evidence Gate Result
- **Step 3 → Step 4 (before build):** TBD (Pass | Fail — reason)
- **Step 4 final:** TBD (Pass | Fail — reason)

#### Step 4 Completion Prompt Evidence
- **Exact completion prompt text:** `All subtasks are complete, pending human verification before human-led git commit.`
- **Output timestamp (UTC):** TBD
