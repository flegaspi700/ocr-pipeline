# Decisions

Design and technology decisions for this project, newest first. When to log
one, and the entry format: the standard's `decisions.md`. Never rewrite an
accepted entry: add a new one and mark the old one `Superseded by`.

Entries before 2026-11-13 were written under the v1 template and refer to
its numbered docs. Where they live now: `00`, `01`, `04` → `requirements.md`;
`02`, `03`, `11` → `architecture.md`; `05` → `decisions.md`; `10` →
`session-log.md`; `12`, `14`, `15`, `16` → `manual-tests.md`, `security.md`,
`accessibility.md`, `budget.md`; `06`, `07`, `13` → the standard's
`coding.md`, `testing.md`, `git.md`.

---

## 2026-10-10 — Phase order changed: refactor first; Baidu removed

**Status:** Accepted

**Context:** During `/breakdown`, the user chose a different order from the
one in "Next direction" below (which put real OCR output before the
refactor), and chose to drop the unverified Baidu backend (no key, request
format guessed).

**Options considered:**

| Option | Pros | Cons | Cost |
|---|---|---|---|
| Working pipeline first (A's items), then refactor, then UI — as previously decided | Real OCR output early; tests the riskiest assumption sooner | Engine is wired into code that's about to be restructured | $0 |
| Refactor first, then local engine, then UI | Engine lands on the clean core and registry; no rework | No real OCR until Phase 2; engine risk discovered later | $0 |

Baidu: keep and park / verify now / remove.

**Decision:** Refactor first (Phase 1 — Clean core), then a free local
engine (Phase 2), then the local web UI (Phase 3). Remove the Baidu
backend in S1.1.2. The environment fix (S4.1.1) still comes first,
because test-first is impossible without it. The order part of "Next
direction" below is superseded; its choice of Option B stands. The open
engine choice is settled by spike S2.2.1; the UI library in F3.1.

**Why:** User preference — build the engine on the final structure once.
Removing Baidu makes the pipeline fully offline and $0 (NFR5, NFR6) and
removes the only secret and network call.

**Trade-offs accepted:** No real OCR until Phase 2. Between S1.1.2 and
S2.2.2 the CLI has no working backend (tests use a fake one). G2's "compare
backends" relies on the registry, not on having two backends today.

**Revisit if:** the local engine spike (S2.2.1) finds both candidates
unusable on this machine → reconsider a cloud backend (Option C).

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

## 2026-10-11 — Formatter, linter and test runner

**Status:** Accepted

**Context:** Tooling needs to be fixed early so AI-generated code stays
consistent between sessions. Follows from the language choice above. Test
runner was already pytest; formatter and linter were the last Phase 1 task.

**Options considered:**

| Option | Pros | Cons | Cost |
|---|---|---|---|
| A: Ruff for formatting and linting | One dev tool, one `pyproject.toml` section; very fast; Black-compatible formatting; widely used, maintained by Astral | Younger than Black/Flake8; some niche lint rules missing | $0 |
| B: Black + Flake8 | Long-established, widely documented | Two tools and two configs (Flake8 needs its own file or a plugin); slower | $0 |
| C: Ruff lint only, no formatter | Least setup | Style drifts between sessions — the reason this decision exists | $0 |

**Decision:** Option A — Ruff (`ruff format`, `ruff check`). pytest stays
the test runner. Config: `target-version = "py311"`, default line length
(88), default lint rules plus import sorting (`I`). Ruff verified on PyPI
(publisher Astral Software, 0.17.0) before installing. CI runs `ruff check .`
and `ruff format --check .` after the tests, with Ruff pinned to 0.17.0 so
local and CI formatting match.

**Why:** The smallest setup that both formats and lints, which keeps
AI-written code consistent (`00-vision.md` → readable, extensible code).
Trade-off accepted: relying on a younger tool, low risk for a trial.

---

## 2026-10-11 — Coverage and dependency audit tools

**Status:** Accepted

**Context:** The Phase 1 end checks (`07-testing-checklist.md`) need a
coverage report and a dependency audit; `AGENTS.md` → Commands had neither.

**Options considered:**

| Option | Pros | Cons | Cost |
|---|---|---|---|
| A: `pytest-cov` + `pip-audit` | Standard tools; `pytest-cov` plugs into pytest (one command); `pip-audit` maintained by PyPA, audits what's actually installed | Two more dev tools | $0 |
| B: `coverage.py` directly + `pip-audit` | One fewer plugin | Two commands for coverage | $0 |
| C: No coverage; Dependabot only | Nothing to install | Checklist asks for both; Dependabot sees only declared deps, and is off for this repo | $0 |

**Decision:** Option A. `pytest-cov==7.1.0` (pytest-dev) and
`pip-audit==2.10.1` (PyPA), both verified on PyPI before installing. Run
locally at each phase end, not in CI.

**Why:** Smallest standard setup that meets the phase-end checklist.
Trade-off accepted: two more dev tools, used only at phase end.

---
