# Decisions log

Running log of design and technology decisions, in ADR-style (Architecture
Decision Record). Add new entries at the top. Copy the template at the
bottom for new entries.

- Log open questions too, as `Proposed` entries with the decision left
  pending and a note on what result will settle it — that way they don't
  get decided silently.
- For significant choices (see `02-architecture.md` → Design options and
  trade-offs), fill in **Options considered** with every serious option,
  not just the winner. Knowing what was rejected and why stops the same
  debate from restarting later.
- Small choices can skip the options table — a one-line Decision and Why
  is enough.
- Never delete or rewrite an accepted entry. If a decision changes, add a
  new entry and mark the old one `Superseded by <new entry>`.

---

## 2026-10-10 — Next direction: clean core + simple local UI

**Status:** Accepted

**Context:** The scaffold has never run its tests locally (pip SSL error),
its only backend (Baidu) is unverified and there is no Baidu key, CSV
export flattens nested results, and pages run one at a time. The user wants
code that is easy to read *and* easy to extend, a simple UI to drag or
select files/folders, and OCR options beyond Baidu — free first, cloud
later. Documents: PDFs, receipts, forms (samples to be generated).

**Options considered:**

| Option | Pros | Cons | Cost |
|---|---|---|---|
| A. Make it work — fix pip, green tests, one free local engine, fix CSV, sample docs; no UI | Fastest to real OCR results | No UI; code stays as is | $0 |
| B. Clean core + simple local UI — A, plus one `run_pipeline()` used by CLI and UI, a backend registry, readable modules, a local Python web page (drag/select files and folders, page + text side by side, download JSON/CSV) | Covers all three wishes; free and offline; UI is just another caller of the core | Adds a UI library and accessibility work | $0 |
| C. B + cloud backends (e.g. Google Vision, Azure) and a comparison view | Answers "which engine is best for my receipts?" | Accounts, keys, billing alerts, data leaves the machine; bigger scope | Free tier, usage-based beyond |
| D. Rewrite as a web app (separate frontend + backend) | Most flexible UI | Throws away working code; second language; overkill for a trial | $0 |

**Decision:** B. Work starts with A's items (environment, tests, a free
local engine, sample documents) so real OCR output comes early, then the
refactor, then the UI.

**Why:** Meets the user's goals (readable + extensible code, a UI, non-Baidu
engines) within the free-only constraint; the backend registry keeps C
cheap to add later.

**Trade-offs accepted:** No cloud-vs-local comparison yet; a UI library and
an accessibility pass are added. The vision's "no graphical interface"
non-goal is narrowed to "no full desktop or hosted app".

**Revisit if:** The free local engine is not good enough on receipts/forms
(→ bring C forward), or the UI library can't handle folder selection.

**Riskiest assumption:** packages can be installed on this machine (pip
failed with an SSL handshake error before). Cheap test: `pip install
pytest` in a fresh venv — if it fails, fix it before anything else. Second:
a free local engine reads receipts/forms well enough — test on 3 generated
samples before building the UI.

**Open (decide during `/breakdown` / `/decide`):** which local engine
(Tesseract / RapidOCR / EasyOCR) and which UI library (Streamlit / Gradio).

---

## 2026-10-10 — Existing stack, kept as is

**Status:** Accepted

**Context:** The template was added to an existing repo that already has
working code. The stack is recorded, not re-chosen.

**Decision:** Keep the existing stack: Python 3.11+, setuptools
(`pyproject.toml`, `src/` layout), argparse, PyMuPDF, Pillow, requests,
pytest, GitHub Actions. Details in `03-tech-stack.md`.

**Why:** It already fits the goals in `00-vision.md`; changing it would add
work without serving any goal.

**Revisit if:** A goal can't be met with it — e.g. a local OCR backend
needs a dependency that conflicts with these.

---

## YYYY-MM-DD — Formatter, linter and test runner

**Status:** Proposed

**Context:** Tooling needs to be fixed early so AI-generated code stays
consistent between sessions. Follows from the language choice above.

**Decision:** _Partly decided — test runner is pytest (already in use).
Formatter and linter still pending._

**Why:** _Fill in once chosen._

---

## Template for new entries

```
## YYYY-MM-DD — <short decision title>

**Status:** Proposed | Accepted | Superseded by <link>

**Context:** What prompted this decision? What constraints or goals
(from 00-vision.md) apply?

**Options considered:**   (skip for small choices)

| Option | Pros | Cons | Cost |
|---|---|---|---|
| <simplest option that could work> | | | <$0 / $X per month / usage-based> |
| <option B> | | | |
| <option C, if any> | | | |

**Decision:** What was decided?

**Why:** Which criteria decided it — e.g. simplicity, effort, performance,
cost, security, ease of changing later.

**Trade-offs accepted:** What we give up with this choice.

**Revisit if:** The condition or measurement that would make this worth
reconsidering (e.g. "capture rate drops below 20 fps").
```
