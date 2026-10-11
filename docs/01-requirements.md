# Requirements

What the project must do, broken down as **Epic → Feature → Story**. The
project plan (`04-project-plan.md`) decides *when* each piece gets built;
this doc decides *what* gets built and how you know it's done.

- **Epic:** a large capability or outcome. Too big to build in one go.
  Usually spans several phases.
- **Feature:** a piece of an epic that is useful on its own. Fits in one
  phase.
- **Story:** the smallest unit of work: one prompt-sized change to one
  component, with acceptance criteria that can be tested. If a story needs
  more than ~a day or touches several components, split it.

**Baseline (2026-10-10):** the project already exists — a Python CLI and
library that loads images and multi-page PDFs, preprocesses them, sends each
page to a pluggable OCR backend (Baidu, to be removed in S1.1.2), and exports per-page results as
JSON or CSV. No stories are written for that existing code; new work starts
from `/breakdown`.

## How to work with this doc

- Every epic serves at least one goal from `00-vision.md`. An epic that
  serves none is out of scope until the vision changes.
- A small project can have a single epic with a few features, and stories
  for the current phase only — don't pad it to look complete.
- Break requirements down top-down when starting the project: write the
  epics first, then features, then stories only for the current and next
  phase. Stories for later phases get written when you reach them.
- IDs are stable — never renumber. Removed items get status `Dropped`, not
  deleted.
- Every story's acceptance criteria become its tests (see
  `07-testing-checklist.md`).
- Reference story IDs in the project plan, commit messages and prompts
  (e.g. "Implement S1.2.3").
- A story is done when it meets its acceptance criteria *and* the
  Definition of Done below. Then update its status here and in the summary
  table.

**Statuses:** `Backlog` → `Ready` (acceptance criteria written) →
`In progress` → `Done` · or `Dropped`

## Definition of Done

A story is `Done` only when it meets **its own acceptance criteria** *and*
**every item below**. This list is the same for every story — edit it here
if the project needs more (or fewer) checks, never per story.

- [ ] Each acceptance criterion has a test, written first and seen failing;
      the tests now pass, and the output has been seen (not just reported)
- [ ] No test was deleted, skipped, or weakened to get there
- [ ] The full test suite still passes
- [ ] The code is the simplest version that works — nothing speculative
      (`06-coding-conventions.md` → Simplicity first)
- [ ] New/changed files have a header note; non-obvious functions have a
      doc comment; existing notes still match the code
- [ ] Any new decision is logged in `05-decisions-log.md`; any new term is
      in `11-glossary.md`; diagrams in `02-architecture.md` still match
      the code
- [ ] No non-functional requirement (below) is broken by the change
- [ ] Security checks for the change pass (`14-security.md` → Every
      change); accessibility checks too if the UI changed
      (`15-accessibility.md`)
- [ ] Story status is updated here (story + summary table)
- [ ] A session log entry is written in `10-session-log.md`

**Reporting the DoD:** when a story (or feature) is checked, report the
result as a table with one row per item above. Status is `Met` or
`Not met`, with a short note, and any caveat is named in its row (e.g.
"no code, so a failing state was never seen"). Items that can only be
checked by hand are listed for the user. The same results go into the
PR's Definition of Done checklist, which is where the record is kept.
Example (shortened):

| Item | Status |
|---|---|
| Each criterion tested, failing first, now passing | Met (5/5) |
| Full suite passes | Met (42 passed) |
| Security checks | Not met: <what's missing and the fix> |

A **feature** is done when all its stories are `Done`, its integration
and manual tests pass (`07-testing-checklist.md` → Before marking a feature
done), and its **Done when** line is demonstrated. An **epic** is done when all its features are.

## Non-functional requirements

Qualities the whole system must have, rather than things it does —
how fast, how secure, how accessible, how reliable, how cheap. They apply
to every story, so they're checked by the Definition of Done and verified
at each phase end (`07-testing-checklist.md`).

- Each one must be **measurable** — "fast" isn't a requirement; "≥ 20
  updates/sec on the target machine" is.
- Delete the example rows that don't apply; add your own. Stories that
  exist mainly to meet an NFR reference its ID in **Notes**.

| ID | Category | Requirement (measurable) | How verified | Status |
|---|---|---|---|---|
| NFR1 | Performance | The 5 sample pages (`samples/`) finish in under 60 s on this machine with the local engine | Timed CLI run in S2.2.3, each phase end | Not met yet |
| NFR2 | Security | No known high-severity vulnerabilities in dependencies | Dependency audit + Dependabot, each phase end (`14-security.md`) | Met (2026-10-11): `pip-audit` clean after upgrading the venv's pip; Dependabot alerts are off for the repo |
| NFR3 | Accessibility | The local web UI meets the "Apps and websites" checklist in `15-accessibility.md` (WCAG 2.2 AA, where the UI library allows) | Manual pass per `15-accessibility.md` | Not met yet |
| NFR4 | Reliability | One bad input file never stops a run: it is reported as an error and the other pages still finish | Test in S1.1.5 + manual run with a corrupt file | Not met yet: tests pass through `run_pipeline()` and the CLI (2026-10-11); manual run waits for a real backend (Phase 2) |
| NFR5 | Privacy | OCR runs fully offline (no network calls), and document text is never logged above DEBUG | Tests in S1.2.2 / S2.2.2 + review of logs | Not met yet: no network code or library since S1.1.2, log test passes (2026-10-11); local engine checked in S2.2.2 |
| NFR6 | Cost | Monthly spend $0: free, local tools only (`16-budget.md`) | Monthly log in `16-budget.md` | Met (2026-10-11): $0 so far, free tools only, public repo so Actions is free; monthly log starts 2026-11 |

**Statuses:** `Not met yet` · `Met` (with date last verified) · `At risk`

## Summary

| ID | Title | Type | Phase | Status |
|---|---|---|---|---|
| E1 | Batch OCR to structured output | Epic | 1 | Backlog |
| F1.1 | Clean pipeline core | Feature | 1 | Done |
| S1.1.1 | Typed page result | Story | 1 | Done |
| S1.1.2 | Backend registry; Baidu removed | Story | 1 | Done |
| S1.1.3 | Pages loaded one at a time | Story | 1 | Dropped |
| S1.1.4 | Folder inputs expand to their files | Story | 1 | Done |
| S1.1.5 | `run_pipeline()` with skip-and-report | Story | 1 | Done |
| F1.2 | Export and CLI on the core | Feature | 1 | Done |
| S1.2.1 | JSON and CSV from page results | Story | 1 | Done |
| S1.2.2 | CLI is a thin caller of `run_pipeline()` | Story | 1 | Done |
| E2 | A free local engine I can judge | Epic | 2, 4 | Backlog |
| F2.1 | Generated sample documents | Feature | 2 | Ready |
| S2.1.1 | Sample document generator | Story | 2 | Ready |
| F2.2 | Local OCR backend | Feature | 2 | Ready |
| S2.2.1 | Engine spike: Tesseract vs RapidOCR | Story | 2 | Ready |
| S2.2.2 | Local OCR backend | Story | 2 | Ready |
| S2.2.3 | Local engine as default; end-to-end on samples | Story | 2 | Ready |
| F2.3 | Tunable preprocessing | Feature | 4 | Backlog |
| E3 | Simple local web UI | Epic | 3 | Backlog |
| F3.1 | Pick UI library and show a page | Feature | 3 | Backlog |
| F3.2 | Select or drag files and folders, then run | Feature | 3 | Backlog |
| F3.3 | Page and text side by side, plus JSON/CSV download | Feature | 3 | Backlog |
| E4 | Safe to change | Epic | 1 | Backlog |
| F4.1 | Working dev environment and CI | Feature | 1 | Done |
| S4.1.1 | Dependencies install and existing tests pass locally | Story | 1 | Done |
| S4.1.2 | CI runs on every PR | Story | 1 | Done |

Build order in Phase 1: F4.1 first (nothing can be tested before it), then
F1.1, then F1.2.

---

## E1 — Batch OCR to structured output

**Goal:** One command (or one Python call) turns a mix of images, multi-page
PDFs and folders into per-page text as JSON or CSV — built on one clean
`run_pipeline()` that the CLI and later the UI both call.
**Serves:** G1, G3
**Out of scope:** layout reconstruction, cloud backends, recursive folders.

### F1.1 — Clean pipeline core

**Description:** A typed page result, a backend registry, folder expansion
and one `run_pipeline()` that keeps going when a file fails.
**Phase:** 1
**Depends on:** F4.1
**Done when:** `run_pipeline()` on a mix of images, a 3-page PDF, a folder
and one corrupt file (with a fake backend) returns one page result per page,
and the corrupt file shows as an error, not a crash.

#### S1.1.1 — Typed page result

**Story:** Technical — a `PageResult` dataclass replaces the raw dicts passed
between components, so the interface is self-documenting
(`06-coding-conventions.md` → Typing).

**Component:** `src/ocr_pipeline/models.py`
**Status:** Done

**Acceptance criteria:**
- [x] Given OCR output for one page, when a `PageResult` is built, then it
      holds `source_file`, `page` (1-based), `text`, `lines` (each with
      `text` and `confidence`) and `error`
- [x] Given a page with no text, when it is built, then `text == ""` and
      `lines == []` (not `None`)
- [x] Given a failed page, when it is built, then `error` holds the message
      and `text` is empty

#### S1.1.2 — Backend registry; Baidu removed

**Story:** As a developer, I want to pick an OCR backend by name from one
registry, so that adding an engine touches only the backend module and a
CLI option (`00-vision.md` → Success looks like).

**Component:** `src/ocr_pipeline/backend.py`
**Status:** Done

**Acceptance criteria:**
- [x] Given a backend registered under a name, when `get_backend(name)` is
      called, then it returns that backend
- [x] Given an unknown name, when `get_backend(name)` is called, then the
      error lists the available names
- [x] Given an empty registry, when a backend is requested, then the error
      says "no OCR backend installed" and what to do — not a stack trace
- [x] Given the change is done, then the Baidu backend, its tests, its
      `.env.example` entries and `requests` (if nothing else uses it) are
      gone, and `AGENTS.md`, `README.md`, `00-vision.md`,
      `02-architecture.md`, `03-tech-stack.md` and the `14-security.md`
      threat model no longer describe Baidu as current

**Notes:** Baidu removed by user choice (`05-decisions-log.md`, 2026-10-10
"Phase order changed"). Until S2.2.2 the registry has no real backend;
tests register a fake one.

#### S1.1.3 — Pages loaded one at a time

**Story:** Technical — yield pages one at a time instead of loading every
page before OCR, to bound memory on large PDFs.

**Component:** `src/ocr_pipeline/io.py`
**Status:** Dropped

**Notes:** Cut during `/breakdown` (2026-10-10) — the trial's documents are
small. Revisit if a large PDF runs out of memory (risk in `00-vision.md`).

#### S1.1.4 — Folder inputs expand to their files

**Story:** As a user, I want to pass a folder instead of listing every
file, so that I can OCR a batch in one command.

**Component:** `src/ocr_pipeline/io.py`
**Status:** Done

**Acceptance criteria:**
- [x] Given a folder with images, PDFs and a `.txt`, when it is expanded,
      then the supported files come back in sorted order and the `.txt` is
      skipped with a debug log
- [x] Given a folder with subfolders, when it is expanded, then files in
      subfolders are ignored (top level only)
- [x] Given an empty folder or one with no supported files, when it is the
      only input, then a clear error names the folder; when other inputs
      exist, a warning is logged and the run continues
- [x] Given a path that doesn't exist, when it is expanded, then the error
      names the path

#### S1.1.5 — `run_pipeline()` with skip-and-report

**Story:** As a developer, I want one `run_pipeline(paths, backend)` call
that returns page results, so that the CLI, the UI and my own code share
the same logic.

**Component:** `src/ocr_pipeline/pipeline.py`
**Status:** Done

**Acceptance criteria:**
- [x] Given image and PDF paths and a backend, when `run_pipeline()` runs,
      then it returns one `PageResult` per page, in input order
- [x] Given one corrupt file among good ones, when it runs, then the good
      pages are processed and the bad file appears as a `PageResult` with
      `error` set, plus a logged warning
- [x] Given a backend that raises on one page, when it runs, then only that
      page carries the error
- [x] Given no input paths, when it runs, then it raises "no input files"

**Notes:** Skip-and-report chosen in `/breakdown` (NFR4).

### F1.2 — Export and CLI on the core

**Description:** Export page results as JSON or one-row-per-page CSV, and
make the CLI a thin caller of `run_pipeline()`.
**Phase:** 1
**Depends on:** F1.1
**Done when:** the CLI, run in a test with a fake backend, writes JSON and
CSV with one row per page and exits non-zero when any file failed.

#### S1.2.1 — JSON and CSV from page results

**Story:** As a user, I want one CSV row per page with readable text, so
that I can open the results in a spreadsheet.

**Component:** `src/ocr_pipeline/export.py`
**Status:** Done

**Acceptance criteria:**
- [x] Given page results, when exported as JSON, then the file is a list of
      page results with all fields
- [x] Given page results, when exported as CSV, then there is one row per
      page with columns `source_file, page, text, confidence, error`;
      `confidence` is the mean over lines, empty when there are none
- [x] Given text with commas, quotes, newlines and non-ASCII characters,
      when exported to CSV and read back, then it is unchanged
- [x] Given an empty results list, when exported, then CSV has headers only
      and JSON is `[]` (no error)

#### S1.2.2 — CLI is a thin caller of `run_pipeline()`

**Story:** As a user, I want `ocr-pipeline <files/folders> --output <path>`
to run the whole pipeline, so that one command gives me the results.

**Component:** `src/ocr_pipeline/cli.py`
**Status:** Done

**Acceptance criteria:**
- [x] Given files and/or folders and `--output`, when the CLI runs, then it
      writes the chosen format via `run_pipeline()` and the exporters
- [x] Given all pages succeed, then exit code is 0; given any page has an
      error, then exit code is 1; either way a summary line is logged
- [x] Given no inputs or an unknown `--backend`, then a usage error is shown
      and exit code is 2
- [x] Given any run, then output goes through `logging` (no `print`), and
      document text is never logged above DEBUG

**Notes:** No real backend exists until S2.2.2 — tests use a fake one.

---

## E2 — A free local engine I can judge

**Goal:** Real OCR output, offline and free, on documents whose text is
known, so I can judge whether it's good enough.
**Serves:** G2
**Out of scope:** model training, handwriting tuning, formal accuracy
scoring, cloud backends.

### F2.1 — Generated sample documents

**Description:** A script that renders synthetic sample documents with
known text.
**Phase:** 2
**Depends on:** none
**Done when:** one script produces a receipt, a form and a 3-page PDF, each
with its known text.

#### S2.1.1 — Sample document generator

**Story:** As a user, I want reproducible sample documents with known
text, so that I can compare OCR output against what's really on the page.

**Component:** `scripts/`
**Status:** Ready

**Acceptance criteria:**
- [ ] Given the script runs, then `samples/receipt.png`, `samples/form.png`
      and `samples/multipage.pdf` (3 pages) exist, each with a `.txt` file
      holding its known text (one per page for the PDF)
- [ ] Given the script runs twice, then the output files are byte-identical
      (fixed content, no randomness or clock)
- [ ] Given the samples, then they contain no real personal data

**Notes:** Uses Pillow and PyMuPDF (already dependencies). Font: Pillow's
default or a bundled one, so it works on any machine.

### F2.2 — Local OCR backend

**Description:** A free, offline OCR engine behind the backend registry,
used by default.
**Phase:** 2
**Depends on:** F1.2, F2.1
**Done when:** `ocr-pipeline samples/ --output r.csv` runs offline with no
flags, and the text is readable when spot-checked against the known text
(manual test in `12-manual-tests.md`).

#### S2.2.1 — Engine spike: Tesseract vs RapidOCR

**Story:** Technical — try both candidate engines on the samples so the
engine choice is made from evidence, not guessed.

**Component:** throwaway script outside the package — no package code
**Status:** Ready

**Acceptance criteria:**
- [ ] Given both engines installed in a throwaway venv, when each is run on
      the 3 samples, then a table in `05-decisions-log.md` records install
      effort on this machine, seconds per page, and readability against
      the known text
- [ ] Given the table, then the user picks one and the decision is logged
      (each package verified in its official registry first —
      `14-security.md`)

#### S2.2.2 — Local OCR backend

**Story:** As a user, I want OCR to run on my machine for free, so that I
need no account or key and documents never leave the machine.

**Component:** `src/ocr_pipeline/backend.py`
**Status:** Ready

**Acceptance criteria:**
- [ ] Given a generated image showing "HELLO 123", when recognized, then a
      line contains that text with confidence between 0 and 1
- [ ] Given a blank white image, when recognized, then no lines are
      returned and there is no error
- [ ] Given the engine is not installed, when the backend is requested,
      then the error says what's missing and how to install it
- [ ] Given an A4 page at 300 DPI, when recognized, then it completes
      without error
- [ ] Given any run, then no network call is made (NFR5)

**Notes:** Engine chosen in S2.2.1. Add it to `03-tech-stack.md`.

#### S2.2.3 — Local engine as default; end-to-end on samples

**Story:** As a user, I want the CLI to use the local engine without
flags, so that one command on my samples gives real results.

**Component:** `src/ocr_pipeline/cli.py`
**Status:** Ready

**Acceptance criteria:**
- [ ] Given `samples/` and no `--backend`, when the CLI runs with JSON and
      then CSV output, then each has one result per page (5 pages)
- [ ] Given the output, then a manual spot-check against the `.txt` files is
      recorded in `12-manual-tests.md`
- [ ] Given the 5 sample pages, then the run takes under 60 s (NFR1)

### F2.3 — Tunable preprocessing

**Description:** Binarization can be turned off or its threshold changed,
since a fixed threshold may hurt photos and low-contrast scans.
**Phase:** 4
**Depends on:** F2.2
**Done when:** the samples are run with and without binarization and the
difference is recorded.

---

## E3 — Simple local web UI

**Goal:** A local web page to drag or select files and folders, run OCR,
and see each page next to its text — the easiest way to judge the OCR.
**Serves:** G2
**Out of scope:** hosting, multi-user, full desktop app (`00-vision.md` →
Non-goals).

### F3.1 — Pick UI library and show a page

**Description:** Choose the UI library (Streamlit vs Gradio — open in
`05-decisions-log.md`) and serve a local page.
**Phase:** 3
**Depends on:** F2.2
**Done when:** a local page opens in the browser from one command.

### F3.2 — Select or drag files and folders, then run

**Description:** Pick inputs in the page and run `run_pipeline()` on them.
**Phase:** 3
**Depends on:** F3.1
**Done when:** dropping the samples folder produces results in the page.

### F3.3 — Page and text side by side, plus JSON/CSV download

**Description:** Show each page image next to its text and errors; download
results as JSON or CSV.
**Phase:** 3
**Depends on:** F3.2
**Done when:** all 5 sample pages can be reviewed side by side and
downloaded, and the `15-accessibility.md` checklist passes (NFR3).

---

## E4 — Safe to change

**Goal:** Tests run green locally and in CI, so a change can be trusted.
**Serves:** G4
**Out of scope:** coverage targets; linter/formatter choice (pending
decision in `05-decisions-log.md`).

### F4.1 — Working dev environment and CI

**Description:** Fix the pip SSL failure and confirm CI checks every PR.
**Phase:** 1
**Depends on:** none
**Done when:** `pytest` is green locally and on a PR.

#### S4.1.1 — Dependencies install and existing tests pass locally

**Story:** Technical — packages must install on this machine before any
test-first work is possible (riskiest assumption in `05-decisions-log.md`).

**Component:** environment / `pyproject.toml`
**Status:** Done

**Acceptance criteria:**
- [x] Given a fresh venv, when `pip install -e .` and `pip install pytest`
      run, then both finish without the SSL handshake error
- [x] Given the installed package, when `pytest` runs, then all existing
      tests pass and the output has been seen
- [x] Given the fix needs a machine setting (proxy, certificates), then it
      is written down in `03-tech-stack.md` — no `--trusted-host` or
      certificate-verification bypass

**Notes:** Done 2026-10-10. The SSL error no longer reproduces: a fresh
`.venv` (Python 3.13) installed everything over HTTPS with `--no-cache-dir`,
with no machine setting needed; 8/8 existing tests pass. Recorded in
`03-tech-stack.md` → Local setup.

#### S4.1.2 — CI runs on every PR

**Story:** Technical — every PR is checked by CI so a change can't break
`main` unnoticed.

**Component:** `.github/workflows/`
**Status:** Done

**Acceptance criteria:**
- [x] Given a PR, when CI runs, then `pytest` runs on Python 3.13 on
      Windows and the result shows on the PR
- [x] Given a deliberately failing test on a throwaway branch, when CI
      runs, then it goes red

**Notes:** Done 2026-10-10. Green: PR #4's CI ran on `windows-2025`
with CPython 3.13.15, 8 passed, result shown on the PR. Red: throwaway
draft PR #5 with one deliberately failing test; the `test` job failed
(`1 failed, 8 passed`, exit code 1) and the PR showed it as failing. PR #5
was closed without merging and its branch deleted. A red check doesn't
block merging unless `main` is protected (`13-git-workflow.md`, optional).

---

## Bugs

Bugs found in finished work. Each one gets a regression test before it's
fixed (`07-testing-checklist.md` → Bugs). Small bugs found while a story is
still in progress are just part of that story.

| ID | Title | Found in | Severity | Status | Test |
|---|---|---|---|---|---|
| B1 | <what's wrong, in one line> | <story/feature ID> | High / Medium / Low | Open | <test name> |

**Statuses:** `Open` → `In progress` → `Fixed` · or `Won't fix` (with a
reason in Notes)

### B1 — <Bug title>

**Steps to reproduce:**
1. <...>

**Expected:** <what should happen>
**Actual:** <what happens instead>
**Notes:** <cause once found, related decisions>

---

## Template for new items

```
## E<n> — <Epic title>

**Goal:** <outcome>
**Serves:** <G-IDs from 00-vision.md>
**Out of scope:** <exclusions>

### F<n>.<m> — <Feature title>

**Description:** <what it adds>
**Phase:** <n>
**Depends on:** <IDs or "none">
**Done when:** <end-to-end demo>

#### S<n>.<m>.<k> — <Story title>

**Story:** As a <user>, I want <capability>, so that <benefit>.
**Component:** <folder>
**Status:** Backlog

**Acceptance criteria:**
- [ ] Given <state>, when <action>, then <result>

**Notes:** <optional>
```
