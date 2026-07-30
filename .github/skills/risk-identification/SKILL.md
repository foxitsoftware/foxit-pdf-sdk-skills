---
name: risk-identification
description: >
  Execute Step 2 of the HACA-SDK workflow: consult SDK reference materials, propose optimal solution(s)
  from confirmed requirements, compare alternatives with pros/cons for user selection, identify risks
  across five dimensions, iterate mitigations, and output a complete "AI Decision Summary" for human
  confirmation. Invoke when HACA is active (via @HACA, /HACA, or /haca-step2), or when users ask to
  evaluate risks or compare trade-offs. Each risk must be context-specific with trigger, impact, and
  mitigation stated.
---

# Solution Design Skill (Foxit SDK)


Step 2 of the HACA-SDK workflow. Consult SDK reference materials to propose the optimal solution, present alternatives when multiple approaches exist, identify and mitigate risks systematically, and output a structured decision summary.

## Phase 0: SDK Reference Consultation (mandatory, before solution proposal)

### 0.1 Read SDK Environment from Step 1

Before designing a solution, read the confirmed Step 1 output to extract:
- **Product**: which Foxit SDK product
- **Platform / Architecture / Language**: target environment
- **SDK Feasibility**: any noted limitations from Step 1

### 0.2 Consult SDK Reference Materials

1. Read relevant files from `.github/sdk-references/` for the identified product:
   - API documentation summaries
   - Code sample templates
   - Capability matrices
   - Known limitations and workarounds
2. If `.github/sdk-references/` does not contain materials for the target product, note this gap and proceed with general SDK knowledge. Clearly mark which recommendations are based on reference materials vs. general knowledge.

### 0.3 Solution Proposal with Alternatives

When proposing solutions:

1. **Always provide the recommended (optimal) solution** with clear justification based on SDK capabilities and best practices.
2. **If multiple viable approaches exist**, list each alternative with:
   - Approach name and brief description
   - **Pros**: advantages, performance benefits, simplicity, etc.
   - **Cons**: disadvantages, limitations, complexity, etc.
   - **SDK API basis**: which APIs / classes / methods are used
   - **Recommendation level**: Recommended / Alternative / Not recommended
3. **Let the user choose** — present alternatives clearly and wait for user selection before proceeding to risk analysis.

### Solution Comparison Template

```markdown
### Solution A: [name] (Recommended)
- Description: [approach description]
- SDK APIs: [key classes/methods used]
- Pros: [advantages]
- Cons: [disadvantages]

### Solution B: [name] (Alternative)
- Description: [approach description]
- SDK APIs: [key classes/methods used]
- Pros: [advantages]
- Cons: [disadvantages]

### Solution C: [name] (Not recommended)
- Description: [approach description]
- SDK APIs: [key classes/methods used]
- Pros: [advantages]
- Cons: [disadvantages]
- Not recommended because: [specific reason]
```

## Valid Risk Description Format

Each risk **must** include three elements:

```
[Risk name]: [trigger condition] -> [impact]. Mitigation: [specific action]
```

**Valid example:**
```
SDK API version mismatch: using deprecated API from SDK 9.x when target SDK is 10.1 -> compile error on target platform.
Mitigation: verify API availability in target SDK version's reference documentation before implementation.
```

**Invalid examples (not accepted):**
```
There may be performance issues.   <- no trigger, no impact, no mitigation
Need better error handling.        <- generic and not task-specific
```

## Five-Dimension Checklist

Review each of the following five dimensions in current task context:

### 1. SDK API & Logic Boundaries
- [ ] SDK API parameter boundary values (null document, invalid page index, empty path)
- [ ] SDK handle / object lifecycle management (open/close, init/destroy)
- [ ] SDK license initialization and validation
- [ ] PDF document locking and concurrent access scenarios
- [ ] Timeout and retry: fallback logic when SDK operations fail
- [ ] Platform-specific API behavior differences

### 2. Dependency Coupling
- [ ] SDK version compatibility with target platform / compiler / runtime
- [ ] Compatibility between SDK and existing project dependencies
- [ ] SDK native library loading and path configuration
- [ ] Cross-language binding constraints (JNI, P/Invoke, NAPI, etc.)

### 3. Data Integrity
- [ ] PDF document save operations (incremental save vs full save)
- [ ] Concurrent document modification risks
- [ ] Large file handling and memory management
- [ ] Temporary file cleanup

### 4. Security
- [ ] PDF encryption and permission handling
- [ ] Digital signature verification
- [ ] Sensitive data in PDF metadata or annotations
- [ ] SDK license key exposure in source code

### 5. Impact Scope
- [ ] Platform-specific code paths (Windows vs Linux vs Mac)
- [ ] SDK version upgrade impact on existing code
- [ ] Effect on existing PDF processing pipeline
- [ ] Output PDF compatibility with other PDF viewers

## Trigger-Based Superpowers Assist (within Step 2 only)

Use superpowers capabilities to improve option analysis quality, while preserving Step 2 required output fields.

- Trigger condition A: you SHOULD selectively borrow `brainstorming`'s option-comparison approach when solution options need comparison with trade-offs.
- Trigger condition B: you SHOULD use `dispatching-parallel-agents` when analysis domains are independent.
- Local offline source A: `.github/skills/superpowers/brainstorming/SKILL.md`
- Local offline source B: `.github/skills/superpowers/dispatching-parallel-agents/SKILL.md`
- **HACA context constraint**: In Step 2, only borrow brainstorming's option comparison and trade-off analysis capability. Do NOT execute brainstorming's full flow (design doc writing, git commit, spec review loop, writing-plans transition); those phases are already governed by HACA Step 3 and Step 4.

Parallel dispatch constraints:
- Use only when domains are independent and have no shared state coupling.
- If domains are coupled, keep analysis serial in this step.

If triggered and used, record into the AI Decision Summary or evidence pack: capability name, trigger reason, key findings, suggested action, adopted/rejected with reason.

## Iterative Mitigation Loop

```
Identify risks -> adjust solution to mitigate -> re-check
  ^___________________________v (risks remain and < 10 iterations)
          v (no risks or threshold reached)
        output AI Decision Summary
```

**Three mitigation methods:**

| Method | Use case | Example |
|------|----------|------|
| Change solution structure | Risk comes from design and can be avoided by redesign | Replace synchronous API with async callback pattern |
| Add technical constraints | Keep solution, add safeguards | Add SDK handle null-check and resource cleanup |
| Mark as uncovered scenario | Cannot be mitigated within current scope, needs human decision | Feature requires SDK module not included in current license |

**When threshold is reached (10 iterations):** move unresolved risks to "Uncovered Scenarios" and state they are unresolved due to iteration limit, not omission.

## Known Risks vs Uncovered Scenarios

- **Known Risks**: identified and addressed through solution adjustments; record under "Known Risks".
- **Uncovered Scenarios**: identified but cannot be mitigated within current information/capability; record under "Uncovered Scenarios" and mark human decision points.

## Contract Persistence Action (Route A + Route B)

For every Step 2 output (regardless of route):

- Read Step 1 baseline from `artifacts/<task-id>/haca-workflow.md` (`## Step 1` chapter), treating the latest file content as source of truth.
- If the contract file exists, do not derive Step 2 input from memory/current-conversation context; use the `## Step 1` chapter as the only baseline source.
- Validate `Workflow Status -> Step Status Matrix -> Step 1` is `confirmed` before executing Step 2. If not confirmed, block and require Step 1 confirmation first.
- If the contract header is still `current_step: step1_draft` or the Step 1 row in Step Status Matrix is `draft`, treat Step 1 as unconfirmed. `/haca-step2`, `artifact-path`, or open-file context never counts as implicit Step 1 confirmation.
- Before waiting for confirmation, write Step 2 output into `## Step 2` chapter of the same file.
- Set `Workflow Status -> Step Status Matrix -> Step 2` to `draft`, and update file header to `current_step: step2_draft`, `last_updated_at: <timestamp>`.
- Append to end of step output by using the single merged Step 2 suffix line (do not output a separate `File updated` line).
- After explicit human confirmation, promote `Workflow Status -> Step Status Matrix -> Step 2` to `confirmed`, update file header to `current_step: step2_confirmed`, and refresh `last_updated_at`.

## End-of-Step Output Format

```markdown
## SDK Reference Basis
- Referenced materials: [list of SDK reference files consulted, or "general SDK knowledge" if none available]
- SDK product: [product name]
- Target environment: [platform / architecture / language]

## Solution Comparison
### Solution A: [name] (Recommended)
- Description:
- SDK APIs:
- Pros:
- Cons:

### Solution B: [name] (Alternative) — if applicable
- Description:
- SDK APIs:
- Pros:
- Cons:

## AI Decision Summary
- Requirement understanding:
- Adopted approach:
- Rejected approach:
- Key assumptions:
- Known risks:
- Uncovered scenarios:
- SDK-specific considerations: [any SDK version, license, or platform-specific notes]

### Decomposition Strategy Choice
Please choose Step 3 decomposition strategy: Decompose into subtasks (default) or Single-task execution (no decomposition). Reply with "Decompose" or "Single-task".

[HACA Step 2/4: Solution Design] - Artifacts: artifacts/<task-id>/haca-workflow.md (draft written before confirmation; you may edit this file, then confirm next step or terminate) - Wait for confirmation before moving to Step 3
```

> Humans may request revisions or add constraints. Keep updating the summary until explicit confirmation.
> Upon explicit confirmation, execute Evidence Gate before loading Step 3. Do not proceed when the gate is blocked.

## References

- SDK reference materials -> `.github/sdk-references/`
- Detailed examples by dimension -> `references/risk-examples.md`
