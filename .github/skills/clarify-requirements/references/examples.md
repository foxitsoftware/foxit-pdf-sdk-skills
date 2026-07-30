# Requirement Clarification Scenario Examples

## Scenario 1: Jira Ticket Provides Partial Information

**Handling method:**
1. Read available information from the ticket and fill it into the "Task Input" format.
2. Ask only about items that are missing and require confirmation.
3. Do not ask again about content that is already explicit in the ticket.

**Example:**

User input: `Implement user login, see PROJ-123`

Already in ticket: tech stack (React + Node.js), deadline

Missing and requires follow-up:
- Acceptance criteria (blocking): what are the conditions for login success/failure?
- Need remember-me login state? (non-blocking, assume yes with default 7-day token)

---

## Scenario 2: Requirements Are Extremely Vague

**Trigger condition:** user says "optimize login flow" or "make this better".

**Handling method:** run full clarification flow. Blocking questions should include at least:
- What is the concrete current problem (performance / UX / security)?
- What are the optimization target metrics (must be testable)?
- Scope impact: frontend only, backend only, or end-to-end?

---

## Scenario 3: Requirements Are Clear but Technical Constraints Are Missing

**Handling method:**
- Treat implementation details as non-blocking questions.
- Provide default options (e.g., "default to JWT unless you prefer another approach").
- Continue execution and record assumptions in "Key Assumptions".

---

## Valid vs Invalid Acceptance Criteria Examples

| Invalid (vague) | Valid (testable) |
|------------|--------------|
| "Login should be fast" | "P99 login response time < 500ms (100 concurrent users)" |
| "Code should be good" | "Unit test coverage >= 80% and no critical lint errors" |
| "Support multiple login methods" | "Support email/password and GitHub OAuth, both covered by E2E tests" |
| "Security should be high" | "Store password with bcrypt (cost=12); lock account for 15 minutes after 5 failed attempts" |
