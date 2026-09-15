# Requirement Clarification Scenario Examples

## Scenario 1: Requirement Source Provides Partial Information

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

---

## Scenario 4: Foxit PDF SDK Task (Product / Platform Must Be Pinned First)

**Trigger condition:** user says "add annotation to a PDF" / "convert PDF to image" / "build a PDF viewer" without naming the Foxit product or platform.

**Handling method:** for any Foxit SDK task, Step 1 must pin the SDK environment before the requirement is
actionable. Blocking questions:

- Which Foxit product? (Desktop / Mobile / Harmony / Web / Cloud API / Conversion) — see
  [`sdk-matrix.md`](../../../sdk-references/sdk-matrix.md) for the single source of truth.
- Which platform / architecture, and which language binding?
- Which SDK version / license environment? (basis version differs per product; must be recorded)

**Example:**

User input: `给 PDF 加个水印`

Missing and blocking:
- Product + platform + language: Desktop (Windows) C++ vs Web (browser) JavaScript change the whole design.
- Input/output: in-place modification vs save-as a new file? (changes the Desktop lifecycle to `SaveAs`).
- Acceptance criteria: watermarks on all pages? rotated? opacity? must be testable.

Non-blocking (assume defaults, record in Key Assumptions):
- License SN/Key from environment variable vs hard-coded config.

See the "Scenario: Desktop C++ Open → Modify → Save Lifecycle" and
"Scenario: Web Async / WASM Initialization" and "Scenario: Mobile Handle Release" sections below for
how these answers drive the design.

---

## Scenario: Desktop C++ Open → Modify → Save Lifecycle

**Task:** "Add a text watermark to every page of a PDF" — Desktop, Windows, C++.

**Clarified Task Input:**

- Product / platform / language: PDF SDK for Desktop, Windows x86_64, C++.
- Input: `input.pdf`; Output: save as a new file `output.pdf` (do not overwrite the original).
- Acceptance: watermark text on all pages, 45° rotation, 30% opacity; output opens without repair.

**Why the lifecycle matters (drives Step 2/3):**

The Desktop C++ flow is a strict ordered lifecycle — initialize the library once, open the document,
operate, save, then release. Getting the order wrong is the most common defect:

```cpp
#include "../../../include/pdf/fs_pdfdoc.h"
#include "../../../include/pdf/fs_pdfpage.h"

foxit::ErrorCode code = Library::Initialize(sn, key);
if (code != foxit::e_ErrSuccess) {
    // MUST check the return code before using any API.
    return;
}

PDFDoc doc("input.pdf");
if (!doc.Load(nullptr)) { /* handle load failure */ }

PDFPage page = doc.GetPage(0);          // operate per page
// ... add watermark ...

doc.SaveAs("output.pdf", PDFDoc::e_SaveFlagNoOriginal);
Library::Release();                     // release once, after all documents are done
```

**Decomposition hint:** T1 initialize + open + save round-trip (no watermark) → T2 add watermark to one
page → T3 apply to all pages → T4 verify output opens and watermark is present.

---

## Scenario: Web Async / WASM Initialization

**Task:** "Embed a PDF viewer in our web page" — PDF SDK for Web, browser, JavaScript.

**Clarified Task Input:**

- Product / platform / language: PDF SDK for Web, browser, JavaScript.
- Acceptance: viewer renders a sample PDF; license SN/Key supplied from config, not hard-coded.

**Why async init matters (drives Step 2/3):**

The Web SDK initializes asynchronously (WASM load + license). The viewer object is created with a
license config and only becomes usable after initialization resolves — code that assumes synchronous
availability will fail intermittently:

```javascript
var pdfui = new UIExtension.PDFUI({
    viewerOptions: {
        libPath: 'lib',
        jr: {
            licenseSN: licenseSN,
            licenseKey: licenseKey
        }
    }
});
// Do not assume the viewer is ready synchronously; wait for the init callback/promise
// before calling document APIs.
```

**Decomposition hint:** T1 create viewer with license config → T2 wait for init then load a document →
T3 wire UI events → T4 verify render in a real browser (not just unit tests).

---

## Scenario: Mobile Handle Release

**Task:** "Render the first page of a PDF as a bitmap" — PDF SDK for Mobile, Android, Java.

**Clarified Task Input:**

- Product / platform / language: PDF SDK for Mobile, Android, Java.
- Acceptance: first page rendered to a `Bitmap`; no native handle leak across repeated calls.

**Why release matters (drives Step 2/3):**

Mobile SDK objects wrap native handles. Every opened document/page must be released, and the library
must be released once at the end — otherwise repeated open/render cycles leak native memory:

```java
int error_code = Library.initialize(sn, key);
if (error_code != ErrorCode.e_ErrSuccess) {
    return; // MUST check before using any API
}

PDFDoc doc = new PDFDoc("input.pdf");
doc.load(null);
PDFPage page = doc.getPage(0);
// ... render page to Bitmap ...
page.close();   // release page handle
doc.close();    // release document handle
Library.release();
```

**Decomposition hint:** T1 initialize + open + close round-trip → T2 render one page → T3 add a
repeated-call test asserting no handle growth → T4 verify on a real device/emulator.
