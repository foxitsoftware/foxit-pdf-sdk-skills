---
name: clarify-requirements
description: >
  Execute Step 1 of the HACA-SDK workflow: identify the target Foxit SDK product, platform, architecture,
  and language; assess SDK capability feasibility; clarify programming task requirements through structured
  interaction and output the standard "Task Input + AI Decision Summary" format for human confirmation.
  Invoke when HACA is active (via @HACA, /HACA, or /haca-step1). Run even for clear-seeming requests to
  verify SDK product selection, testable acceptance criteria, and explicit scope impact are present.
---

# Requirement Clarification Skill (Foxit SDK)


Step 1 of the HACA-SDK workflow. The goal is to identify the correct Foxit SDK product and environment, assess whether the SDK can satisfy the user's requirement, remove requirement ambiguity through human interaction, and output a structured task description as the consensus baseline for later steps.

## Phase 0: SDK Environment Identification (mandatory, before Phase 1)

Before analyzing the programming requirement, you MUST establish the SDK environment context.

### 0.1 Read SDK Configuration

1. Check if `foxit-sdk.config.json` exists in the project root.
2. If it exists, read its content and extract: `product`, `platform`, `architecture`, `language`, and any other specified fields.
3. If it does not exist or fields are missing, proceed to inference and user confirmation.

### 0.2 SDK Product Identification

Determine the target SDK product from the following matrix (source: `.github/copilot-instructions.md`):

| Product | Platforms | Languages |
|---------|-----------|-----------|
| **PDF SDK for Desktop** | Windows (x86/x86_64), Linux (x86/x86_64, armv7, armv8), Mac (x64/arm64) | C++, Python, Java, Node.js, C#, C (Windows only), Go, Objective-C |
| **PDF SDK for Mobile** | Android, iOS | Java (Android), Objective-C / Swift (iOS) |
| **PDF SDK for Harmony** | HarmonyOS Next, OpenHarmony | ArkTS (C++ native core + ArkTS wrapper) |
| **PDF SDK for Web** | Browser | JavaScript / TypeScript |
| **Cloud API** | Cloud service | REST API (Embed Viewer API + PDF Services API) |
| **Conversion SDK** | Windows (x86/x86_64), Linux (x86/x86_64, armv7, armv8) | C++, Python, Java, Node.js, C#, C, Go |

**Identification priority:**
1. If `foxit-sdk.config.json` specifies the product → use it directly (still validate against user's description).
2. If the user's description contains platform/language keywords → infer the product.
3. If ambiguous → ask the user explicitly.

### 0.3 Platform, Architecture, and Language Confirmation

After identifying the product, confirm:
- **Platform**: which OS / environment (e.g., Windows, Linux, Android, iOS, HarmonyOS Next, Browser)
- **Architecture**: which CPU architecture (e.g., x86, x86_64, armv7, armv8, arm64) — where applicable
- **Language**: which programming language for the implementation

If these can be inferred from context or config, state the inference and let the user confirm. Otherwise, ask explicitly.

### 0.4 SDK Capability Feasibility Assessment (mandatory)

After identifying the SDK environment, assess whether the user's requirement can be fulfilled:

1. **Consult SDK reference materials** in `.github/sdk-references/` to check if the requested functionality is supported.
2. **Check the product capability matrix** for the target SDK product.
3. **Evaluate against known SDK limitations**.

Output one of:
- **✅ Feasible** — the SDK supports this functionality. Proceed to Phase 1.
- **⚠️ Partially feasible** — some aspects are supported, but others have limitations. State which parts are feasible and which are not. Proceed to Phase 1 with noted limitations.
- **❌ Not feasible** — the SDK does not support the requested functionality. Clearly state:
  - What the user requested
  - Why the SDK cannot satisfy it (specific limitation)
  - Suggest alternatives if any (different SDK product, workaround, or third-party complement)
  - **Stop and wait for user decision** — do not proceed to Phase 1.

## Phase 1: Requirement Clarification (standard HACA)

### Core Decision: Ask vs Assume

For each missing piece of information, use the following priority:

| Situation | Action |
|------|----------|
| Affects the overall goal direction | **Ask (blocking)** - cannot proceed without an answer |
| Can rely on industry convention or SDK best practice | **Assume and label** - write into "Key Assumptions" |
| High correction cost (architecture/data model/security) | **Ask** - explain why confirmation is required |
| Low correction cost (naming/logging/formatting) | **Assume and label** - write into "Key Assumptions" |

### Execution Rules

1. **Batch questions**: ask all questions in one round, grouped as blocking and non-blocking, instead of back-and-forth one by one.
2. **Provide defaults**: attach a preferred default answer for each question so the human can confirm or correct quickly.
3. **No more than 3 blocking questions** (excluding SDK environment confirmation): if more are needed, the request is too vague; ask for additional context first.

### Question Template

```
**SDK Environment Confirmation:**
- Product: [identified product] — Is this correct?
- Platform: [platform] / Architecture: [architecture] — Is this correct?
- Language: [language] — Is this correct?

**Must confirm (blocking):**
1. [Question] - My understanding is [default answer]. Is this correct?
2. [Question] - I will use [default value] unless you specify otherwise.

**The following will be assumed (non-blocking):**
- Assumption A: [content] (basis: [SDK documentation / industry convention / context inference])
- Assumption B: [content]
```

### Requirement Completeness Checklist

After receiving the request, verify each item is known:

- [ ] SDK environment: product, platform, architecture, language confirmed
- [ ] SDK feasibility: functionality feasibility assessed
- [ ] Goal: what problem to solve / what outcome to achieve
- [ ] Functional requirements: what concrete actions are required
- [ ] Non-functional attributes: performance, security, availability requirements
- [ ] Constraints: SDK version limits, platform restrictions, prohibited modules
- [ ] Acceptance criteria: how completion is verified (must be testable)
- [ ] Scope impact: which modules, services, and data tables are involved

## Trigger-Based Superpowers Assist (within Step 1 only)

Use superpowers capability only as an aid; do not replace HACA Step 1 output format.

- Trigger condition: requirements are ambiguous, user intent is divergent, or scope spans multiple independent subsystems.
- Suggested action when triggered: you SHOULD selectively borrow `brainstorming`'s clarifying-question approach to improve coverage.
- Local offline source: `.github/skills/superpowers/brainstorming/SKILL.md`
- **HACA context constraint**: In Step 1, only borrow brainstorming's clarifying-question capability. Do NOT execute brainstorming's full flow (design doc writing, git commit, spec review loop, writing-plans transition). Step 1's **batch questions rule takes precedence** over brainstorming's one-at-a-time rule.
- Boundary: no implementation actions, no Step 2 design decisions.

If triggered and used, record into the step output context: capability name, trigger reason, key findings, suggested action, adopted/rejected with reason.

## End-of-Step Output Format

After clarification, output the following and **wait for human confirmation**:

```markdown
## SDK Environment
- Product: [identified Foxit SDK product]
- Platform: [target platform]
- Architecture: [target architecture]
- Language: [target programming language]
- SDK Feasibility: [✅ Feasible / ⚠️ Partially feasible (with details) / ❌ Not feasible (with details)]
- Config source: [foxit-sdk.config.json / user confirmation / context inference]

## Task Input
- Jira ticket: [link or "N/A"]
- Requirement description:
  - Goal:
  - Functional requirements:
  - Non-functional attributes:
  - Constraints:
  - Acceptance criteria:

## AI Decision Summary
- Requirement understanding: [complete understanding including SDK context]
- Key assumptions: [list]
- SDK capability notes: [any SDK-specific limitations or considerations]

[HACA Step 1/4: Requirement Clarification] - Artifacts: artifacts/<task-id>/haca-workflow.md (draft written before confirmation; you may edit this file, then confirm next step or terminate) - Wait for your confirmation before moving to the next step
```

> Before confirmation, revisions can be repeated. For each revision, update the full output instead of incremental patches.

## Contract Persistence Action (Route A + Route B)

For every Step 1 output (regardless of route):

1. Ensure contract file exists at `artifacts/<task-id>/haca-workflow.md` (auto-create when needed).
2. Before waiting for confirmation, write the current Step 1 output into the `## Step 1` chapter.
3. Set `Workflow Status -> Step Status Matrix -> Step 1` to `draft`, and update file header to `current_step: step1_draft`, `last_updated_at: <timestamp>`.
4. Append to the end of the step output by using the single merged Step 1 suffix line (do not output a separate `File updated` line).
5. After explicit human confirmation, promote `Workflow Status -> Step Status Matrix -> Step 1` to `confirmed`, update file header to `current_step: step1_confirmed`, and refresh `last_updated_at`.

Field mapping for `haca-workflow.md` Step 1 chapter:
- `SDK Environment` → `SDK Environment` (full section)
- `Task Input.Goal` → `Requirement description.Goal`
- `Task Input.Acceptance criteria` → `Acceptance criteria`
- `AI Decision Summary.Requirement understanding` → `AI Decision Summary.Requirement understanding`
- `AI Decision Summary.Key assumptions` → `AI Decision Summary.Key assumptions`
- `AI Decision Summary.SDK capability notes` → `AI Decision Summary.SDK capability notes`

## References

- SDK product matrix -> `.github/copilot-instructions.md`
- SDK reference materials -> `.github/sdk-references/`
- SDK config schema -> `.github/sdk-references/foxit-sdk-config-schema.md`
- Detailed scenario examples -> `references/examples.md`
