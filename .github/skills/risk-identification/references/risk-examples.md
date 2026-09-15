# Risk Identification Examples by Dimension

## Logic Boundary Risk Examples

**Scenario:** implement bulk email sending

| Risk item | Description |
|----------|------|
| Empty list not handled | Calling send API with empty recipient list triggers third-party API 400 error. Mitigation: validate non-empty list at entry point |
| Excessive concurrency | Sending 1000 emails at once triggers third-party rate limit (100/min). Mitigation: switch to queued batch sending, 50 per batch with 30s interval |

---

## Dependency Coupling Risk Examples

**Scenario:** upgrade payment SDK version

| Risk item | Description |
|----------|------|
| API signature change | New SDK changes `createOrder()` parameter schema, causing compilation failures in existing callers. Mitigation: read changelog, adapt to new signature, and update all call sites |
| Hidden environment variable | New SDK requires `PAYMENT_REGION`; missing deployment config causes runtime errors. Mitigation: add this variable to deployment config and update local `.env.example` |

---

## Data Integrity Risk Examples

**Scenario:** migrate user accounts and merge old-table data into new table

| Risk item | Description |
|----------|------|
| Migration not rollback-safe | Old-table data cannot be recovered after deletion. Mitigation: full backup before migration, migrate first and soft-delete old data (physically delete after 30 days) |
| Concurrent writes | Users can still update old-table data during migration, leaving new table behind after completion. Mitigation: add write lock during migration or use dual-write strategy |

---

## Security Risk Examples

**Scenario:** implement file download API

| Risk item | Description |
|----------|------|
| Path traversal | User input like `../../etc/passwd` can read arbitrary server files. Mitigation: apply path whitelist validation and restrict access to designated directory |
| Unauthorized download | User A guesses file ID and downloads user B's file. Mitigation: verify file ownership before download and confirm requester authorization |

---

## Impact Scope Risk Examples

**Scenario:** change method signature of `UserService.getUserById()`

| Risk item | Description |
|----------|------|
| Hidden callers | Global search finds 12 call sites, 3 owned by other teams; change causes compilation failures. Mitigation: keep old signature via adapter pattern, add overloaded method, notify related teams |
| API contract breakage | Public REST API response format changed, causing frontend parsing failures. Mitigation: add new fields in a backward-compatible way, keep deprecated fields for at least one version, notify frontend team |

---

## Uncovered Scenario Examples (Human Decision Required)

```
- Audit logs: whether this operation requires compliance audit logging depends on business compliance requirements and needs product confirmation.
- Data retention policy: how long order history should be kept after account deletion involves legal requirements and needs legal confirmation.
- Degradation strategy: whether to skip this step and continue flow when third-party services are unavailable requires product decision.
```

---

## Foxit PDF SDK Domain Examples

These risk examples are grounded in the Foxit SDK lifecycle. Product/platform support claims must be
checked against the single source of truth [`sdk-matrix.md`](../../../sdk-references/sdk-matrix.md).

### Logic Boundary Risk — Desktop C++ lifecycle order

**Scenario:** add a watermark to every page of a PDF (Desktop, C++, Windows).

| Risk item | Description |
|----------|------|
| `Initialize` return code ignored | Foxit APIs are only valid after `Library::Initialize(sn, key)` returns `e_ErrSuccess`. Mitigation: check `code != foxit::e_ErrSuccess` and abort before any API call |
| Operation before document load | Calling page APIs before `PDFDoc::Load` succeeds yields null page handles. Mitigation: validate load result and page count first |
| Save before mutation completes | Saving mid-operation leaves a partially written output. Mitigation: complete all page mutations, then `SaveAs` once |

### Dependency Coupling Risk — Web async / WASM initialization

**Scenario:** embed a PDF viewer in a web page (Web, JavaScript).

| Risk item | Description |
|----------|------|
| Synchronous use of async viewer | `new UIExtension.PDFUI({...})` initializes asynchronously (WASM + license); calling document APIs immediately fails intermittently. Mitigation: wait for the init callback/promise before use |
| `libPath` mismatch | Wrong `libPath` causes WASM assets to 404 at runtime, not at build time. Mitigation: verify the deployed asset path in a real browser |
| License SN/Key hard-coded | Shipping the license in client code leaks it. Mitigation: load from server-side config / env, not source |

### Resource Leak Risk — Mobile handle release

**Scenario:** render a page to a bitmap in a loop (Mobile, Android, Java).

| Risk item | Description |
|----------|------|
| Page handle not closed | Each `doc.getPage()` handle must be `close()`d; leaking them grows native memory across iterations. Mitigation: close page in a `finally` block per iteration |
| Document handle not closed | `PDFDoc` wraps native memory; skipping `doc.close()` leaks it. Mitigation: close in `finally` |
| `Library.release()` called too early | Releasing the library while a document is still open crashes. Mitigation: release once, strictly after all documents/pages are closed |

### Impact Scope Risk — product / platform mismatch

**Scenario:** a task requests a product/language combination that the SDK does not support.

| Risk item | Description |
|----------|------|
| Unsupported combination promised | e.g. Desktop `C` is Windows-only; Desktop `Objective-C` is macOS-only; Harmony OpenHarmony has no UI Extensions. Mitigation: confirm the combination against `sdk-matrix.md` before designing |
| Cloud API assumed to have a local file system | Cloud API is a REST service — there is no local path; files are uploaded/downloaded over HTTP. Mitigation: redesign I/O around the REST contract, not local `File` APIs |
