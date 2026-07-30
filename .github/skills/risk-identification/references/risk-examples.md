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
