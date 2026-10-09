# Task Decomposition Anti-Patterns and Corrections

## Anti-Pattern 1: Kitchen-Sink Commit

**Problem:** one commit changes multiple unrelated things, so reviewers cannot focus.

```
[X] Wrong:
  [AI] feat(user): add user export, fix login timeout bug, and update README

[OK] Correct (split into three):
  [AI] feat(user): add CSV export API for user data
  [AI] fix(auth): fix login session timeout renewal issue
  [AI] docs: update API usage section in README
```

---

## Anti-Pattern 2: Half-Finished Commit

**Problem:** splitting one complete logic unit into two dependent halves makes the first commit non-runnable.

```
[X] Wrong:
  T1: feat(payment): add payment API (real gateway not integrated, calls fail)
  T2: feat(payment): integrate Alipay gateway

[OK] Correct:
  T1: feat(payment): implement payment flow skeleton (with mock gateway for local validation)
  T2: feat(payment): replace mock gateway with real Alipay integration
```

---

## Anti-Pattern 3: Mixed refactor + feat

**Problem:** reviewers cannot tell whether behavior changes are refactor side effects or intentional new features.

```
[X] Wrong:
  [AI] refactor(order): refactor order service and add batch-cancel feature

[OK] Correct:
  T1: [AI] refactor(order): extract shared state-transition methods in OrderService (no external behavior change)
  T2: [AI] feat(order): implement batch order cancellation API using refactored methods
```

---

## Anti-Pattern 4: Mixing Tests with Complex Implementation

**Problem:** when test logic is complex, mixing implementation and tests prevents focused review of coverage quality.

```
[X] Wrong (when test volume is large):
  [AI] feat(checkout): implement checkout flow + add 200 lines of integration tests

[OK] Correct:
  T1: [AI] feat(checkout): implement core checkout flow logic
  T2: [AI] test(checkout): add integration tests for checkout flow (normal/error/concurrency scenarios)
```

> Note: when test code is small (< 50 lines), it can be committed with implementation.

---

## Anti-Pattern 5: Over-Splitting

**Problem:** changing only one or two lines per commit creates too many commits and noisy history.

```
[X] Wrong:
  T1: refactor: rename user_name to username
  T2: refactor: rename user_email to email
  T3: refactor: rename user_phone to phone

[OK] Correct:
  T1: [AI] refactor(user): standardize User model naming by removing `user_` prefix
```

---

## Correct Decomposition Example: Full Feature Development

**Scenario:** implement "user invitation signup" feature

```
T1: [AI] chore(db): add migration script for `invitations` table
T2: [AI] feat(invite): implement invitation code generation and storage
T3: [AI] feat(invite): implement invitation code verification and signup API
T4: [AI] feat(email): add invitation email template and trigger logic
T5: [AI] test(invite): add integration tests for invitation signup flow

Execution order:
- T1 -> T2 -> T3 (data dependency)
- T4 and T2 can run in parallel (no dependency)
- T5 depends on both T3 and T4
```

---

## Correct Decomposition Example: Foxit Desktop C++ PDF Task

**Scenario:** add a text watermark to every page of a PDF
(Desktop, Windows, C++; strict SDK lifecycle: `Initialize` → `PDFDoc` → `SaveAs` → `Release`)

```
T1: [AI] feat(sdk): initialize Foxit library, open and save a PDF round-trip (verify return codes)
T2: [AI] feat(sdk): add watermark to a single page with given text, angle, opacity
T3: [AI] feat(sdk): apply watermark to all pages and save as a new file
T4: [AI] test(sdk): verify output opens, watermark present on all pages, no handle leak

Execution order:
- T1 -> T2 -> T3 (strict lifecycle dependency — do not reorder)
- T4 depends on T2 (and T3 for all-page assertions)
```

**Why this ordering:** T1 proves the SDK lifecycle works before any feature logic; skipping the
round-trip means a broken `Initialize`/`SaveAs` only surfaces after feature code is written.

## Anti-Pattern 6: Sheet-Metal Lifecycle (Foxit domain)

**Problem:** initializing / releasing the Foxit library or document/page handles multiple times in
different subtasks, or ignoring `Initialize` return codes.

```
[X] Wrong — each subtask re-initializes and releases:
  T1: feat(sdk): initialize library and open PDF
  T2: feat(sdk): re-initialize library to add watermark (Library::Initialize called again)
  T3: feat(sdk): open same PDF again, save, and release (duplicate open)

[OK] Correct — lifecycle owned by one flow:
  T1: feat(sdk): initialize library once, open PDF, return doc handle
  T2: feat(sdk): add watermarks to all pages (reuses the handle)
  T3: feat(sdk): save as new file and release library once
```

**Rule of thumb:** the SDK lifecycle (`Initialize`/`Release`, document/page open/close) should be a
single concern. If the AI proposes a second `Initialize` or `Release`, flag it during Review.
