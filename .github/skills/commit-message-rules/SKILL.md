---
name: commit-message-rules
description: >
  Internal rules for standardized commit messages (templates, length checks, validators). Humans should use
  `.github/prompts/commit-message.prompt.md` (or the synced editor commit-message command) as the entry point;
  agents load this file when executing that prompt. Do not present this skill’s filename or structure to users unless they ask.
argument-hint: "Used when executing the commit-message prompt; context from focused HACA contract or git diff"
---

# Commit Message Rules Skill

This skill supports two modes:
- Workflow-integrated mode: called by an external workflow or agent.
- Standalone mode: used when a human has already modified code and wants an auto-generated compliant commit message.

## User-facing integration

When commit messages are produced through `.github/prompts/commit-message.prompt.md` (or a synced copy), treat this document as an implementation detail.

- Do not mention this skill’s name, path, or validator internals in user-visible chat unless the human explicitly asks.
- User-facing copy should describe outcomes (validated message, confirmation, optional `git commit`), not this file.

## Commit context source selection

Before generating message content, choose the primary context in this order:

1. **HACA Workflow Contract**: If the **currently focused** editor file is a HACA Workflow Contract (e.g. `artifacts/<task-id>/haca-workflow.md`, or the file clearly identifies itself as such), derive the commit message primarily from that contract.
   - **Semantic source:** **`## Step 2 Solution Design`** → **`### AI Decision Summary`** (requirement understanding / 需求理解, adopted approach / 采用方案, rejected approach / 拒绝方案, key assumptions / 关键假设, known risks / 已知风险, uncovered scenarios / 未覆盖场景). Map these into the commit template fields; compress for length limits without changing meaning.
   - **Not a substitute for Step 2:** Do not use **`## Step 4 Build`** (TDD blocks, subtask checklists, changed-path laundry lists) as the primary narrative for *what* or *why*; Step 4 may only disambiguate concrete paths or wording together with git diff.
   - **Jira:** Prefer Step 1 Jira field when present; else `N/A`.
   - **Subject:** Infer `[AI] <type>(<scope>): <subject>` from Step 2 understanding and approach; use git diff only to align scope with changed paths.
   - **Fallback:** If Step 2 is missing or empty, use Step 1 requirement clarification, then git diff; use `N/A` where unknown.
2. **Git changes**: Otherwise use `git diff --staged`; if empty, use `git diff`.

Optional caller hints may refine wording but must not override (1) when it applies.

## Required Field Completion Rule

In both workflow-integrated mode and Standalone mode, every required field must have a non-empty value.

- If reliable information exists, use the real value.
- If reliable information does not exist, fill the field with `N/A`.
- Do not leave any required field empty.

## Length Control Rules

Commit messages should be concise without changing meaning.

- Subject line target: `<= 72` characters; hard limit: `88` characters.
- Each required field value should stay concise; hard limit: `240` characters per field line.
- Total non-empty lines should stay concise; hard limit: `14` non-empty lines.
- Maximum shortening retries: `2` attempts after the initial draft fails the length check.

If a generated commit message exceeds any limit:

1. Shorten the content while preserving the original meaning.
2. Keep the template structure, section headings, field names, and required facts unchanged.
3. Prefer compressing wording in this order: `Requirement description` -> `Adopted approach` -> `Known risks` -> `Uncovered scenarios`.
4. Do not delete required fields; if information is missing, keep `N/A`.
5. Re-run the length check after each shortening attempt.
6. Stop after `2` shortening retries. If the message still fails the length check, hand control back to the human instead of continuing to rewrite automatically.

If the retry limit is reached, stop before commit, return the current overlong message and the length-check failure reason, and ask the human for a shorter revision.

## Required Procedure

Follow this exact sequence:

1. Write commit message to `tmp/<message-file>` in UTF-8. If `tmp/` does not exist, create it.
2. Run length check script:
  - Windows preferred: `py -3 .github/skills/commit-message-rules/scripts/check_commit_message_length.py tmp/<message-file>`
  - macOS/Linux preferred: `python3 .github/skills/commit-message-rules/scripts/check_commit_message_length.py tmp/<message-file>`
  - Fallback: `python .github/skills/commit-message-rules/scripts/check_commit_message_length.py tmp/<message-file>`
3. If the message is too long, shorten it according to `## Length Control Rules`, then re-run the length check. Stop after the retry limit and hand control back to the human.
4. Run validator script:
  - Windows preferred: `py -3 .github/skills/commit-message-rules/scripts/verify_commit_message.py tmp/<message-file>`
  - macOS/Linux preferred: `python3 .github/skills/commit-message-rules/scripts/verify_commit_message.py tmp/<message-file>`
  - Fallback: `python .github/skills/commit-message-rules/scripts/verify_commit_message.py tmp/<message-file>`
5. If commit execution is requested by the caller, run `git commit -F tmp/<message-file>`.
6. Delete `tmp/<message-file>`.

Before validation and commit, ensure every required field is populated. If any field lacks reliable information, use `N/A`. If the message is too long, shorten it before validation.

## Script Check Reference

`check_commit_message_length.py` validates:
- Subject line length ≤ 88 characters
- Total non-empty lines ≤ 14
- Field-matching lines ≤ 240 characters each

`verify_commit_message.py` validates:
- First non-empty line matches `[AI] <type>(<scope>): <subject>` format (scope parentheses optional)
- Contains both required sections: `## Task Input` / `## 任务输入` and `## AI Decision Summary` / `## AI 决策摘要`
- Contains all 8 required fields (English or Chinese variants accepted)
- Each required field has a non-empty value (`N/A` counts as non-empty)

## Standalone Invocation (Human-Modified Code)

When invoked outside HACA, use this flow:

1. Collect change context using `## Commit context source selection` above.
2. Infer `<type>(<scope>)` and `<subject>` from actual change intent.
3. Generate a full commit message using one template language only (English or Chinese), based on conversation language or explicit user preference.
4. If any required field lacks reliable information, fill it with `N/A`.
5. Write message to `tmp/<message-file>` in UTF-8.
6. Run length check script (`.github/skills/commit-message-rules/scripts/check_commit_message_length.py`). If the message is too long, shorten it while preserving meaning, then re-run. Stop after the retry limit and hand control back to the human.
7. Run validator script (`.github/skills/commit-message-rules/scripts/verify_commit_message.py`) until pass.
8. Return the final message body to the user; if explicitly requested, run `git commit -F tmp/<message-file>` and then delete `tmp/<message-file>`.

Standalone output must include all required fields. Do not output title-only commit messages.

## Language Rule

All human-readable outputs and final commit messages must follow the primary language used in the human-AI interaction, unless the user explicitly specifies otherwise.

This rule is mandatory for:
1. Commit message body content.
2. Any questions to the human (including commit execution confirmation prompts).
3. Any explanatory text before/after validation and commit execution.

Do not mix Chinese and English in one output unless the human explicitly requests mixed language.

## Commit Message Template (English)

```markdown
[AI] <type>(<scope>): <subject>

## Task Input
- Jira ticket: ...
- Requirement description: ...

## AI Decision Summary
- Requirement understanding: ...
- Adopted approach: ...
- Rejected approach: ...
- Key assumptions: ...
- Known risks: ...
- Uncovered scenarios: ...
```

## 提交信息模板（中文对照）

```markdown
[AI] <type>(<scope>): <subject>

## 任务输入
- Jira 工单: ...
- 需求描述: ...

## AI 决策摘要
- 需求理解: ...
- 采用方案: ...
- 拒绝方案: ...
- 关键假设: ...
- 已知风险: ...
- 未覆盖场景: ...
```

Choose one language template only for each commit message. Do not output both English and Chinese versions in the same message.

The validator accepts either English or Chinese heading variants. See `.github/skills/commit-message-rules/scripts/verify_commit_message.py` for accepted strings.

## Complete Example

Below is a correctly formatted, length-compliant Chinese commit message:

```
[AI] feat(order): 为订单列表添加游标分页支持

## 任务输入
- Jira 工单: PROJ-123
- 需求描述: 用户列表因数据量增长导致响应超时，需引入分页机制

## AI 决策摘要
- 需求理解: 对 getUserList() 接口添加游标分页，限制每次返回 100 条
- 采用方案: 游标分页（keyset pagination），避免 OFFSET 随页数增大性能下降
- 拒绝方案: OFFSET 分页，大数据量下 DB 全表扫描行数过多
- 关键假设: 前端可接受 cursor 字段替代 page number 参数
- 已知风险: 首次部署需同步更新前端接口调用方式
- 未覆盖场景: N/A
```

