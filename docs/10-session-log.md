# Session log

A handoff note at the end of every working session, so the next session
(yours or an AI agent's) can pick up without re-reading everything. Newest
entry at the top. Keep each entry short — a few lines per heading.

AI agents: read the latest entry at the start of a session; add a new one
at the end (see `AGENTS.md`).

---

## 2026-10-12 — Session wrap-up: F2.1 done, Phase 2 started

**Worked on:** F2.1 (S2.1.1) — built, PR #13 merged, branch deleted

**Time spent:** ~30 min (whole session; the entry below is part of it).
Phase 2 so far ~0.5h against a 6h estimate.

**Changed:**
- PR #13 — `scripts/make_samples.py` and committed `samples/` (receipt,
  form, 3-page PDF + known text), 5 tests, `.gitattributes` for sample
  bytes, Pillow ≥ 10.1; Phase 2 In progress in `04-project-plan.md`
- This entry

**Stopped at:** `main` clean and in sync after PR #13; 47 tests pass, Ruff
clean. F2.1 Done; F2.2 not started.

**Next step:** first, **manual testing** of what's built so far (user's
request): run `python scripts/make_samples.py`, compare each file in
`samples/` with its `.txt`, and record the result in the F2.1 row of
`docs/12-manual-tests.md`; try the CLI's usage errors (no inputs, missing
path, unknown backend → exit 2, no stack trace). Real OCR runs wait for
S2.2.2. Then `/story S2.2.1` — engine spike, Tesseract vs RapidOCR (a design
choice: options and a recommendation before any code).

**Open questions:** Carried over: Dependabot / secret-scanning alerts on
GitHub (skipped by the user); should `16-budget.md` drop to Optional;
PyMuPDF `import fitz` and Pillow `getdata` deprecation warnings.

---

## 2026-10-12 — F2.1 Generated sample documents built

**Worked on:** `/story F2.1` — S2.1.1 (Phase 2 started)

**Time spent:** counted in the wrap-up entry above

**Changed:**
- `scripts/make_samples.py` — `generate_samples(out_dir)`: receipt and form
  PNGs, 3-page A4 PDF, known text as `.txt` (`multipage_p1..3.txt` per PDF
  page); fixed fictional content, byte-identical runs (PDF saved with empty
  metadata and `no_new_id`)
- `samples/` committed; `.gitattributes` keeps their bytes (LF `.txt`,
  binary PNG/PDF) despite `core.autocrlf`
- `tests/test_make_samples.py` — 5 tests incl. one through `run_pipeline()`
  (5 pages, `.txt` skipped); pytest `pythonpath = ["scripts"]`
- Pillow minimum raised to 10.1 (`load_default(size=...)`)
- Docs: architecture (component + diagram), tech stack, AGENTS command,
  manual test F2.1

**Stopped at:** F2.1 Done on `feature/F2.1-sample-documents`; 47 tests pass,
Ruff clean. Changes staged, not committed, no PR yet.

**Next step:** after the F2.1 PR is merged: `/story S2.2.1` — engine spike,
Tesseract vs RapidOCR (a design choice; ends in a logged decision).

**Open questions:** None blocking. Phase 2 is marked In progress
(started 2026-10-12) in `04-project-plan.md`. Known text keeps column spacing that the
proportional font doesn't show, so OCR comparisons should collapse
whitespace.

---

## 2026-10-11 — Session wrap-up: Phase 1 done

**Worked on:** F1.1 (S1.1.1, S1.1.2, S1.1.4, S1.1.5), F1.2 (S1.2.1,
S1.2.2), formatter/linter, Phase 1 end checks

**Time spent:** ~2h (whole session; the two entries below are part of it).
Phase 1 total ~3h against an 8h estimate.

**Changed:**
- PR #8 — F1.1: `PageResult`, backend registry (Baidu and `requests`
  removed), folder expansion, `run_pipeline()` with skip-and-report
- PR #9 — F1.2: JSON/CSV export from page results, CLI as a thin caller
  (exit 0/1/2), `run_pipeline(dpi, threshold)`; unused `load_inputs()` removed
- PR #10 — Ruff formatter and linter, pinned 0.17.0, run in CI
- PR #11 — `pytest-cov` + `pip-audit` (phase end, local), CLI corrupt-file
  test, NFR statuses, threat-model check; Phase 1 Done
- This entry — session times filled in; Phase 1 actual hours in
  `04-project-plan.md`

**Stopped at:** `main` clean and in sync after PR #11; 42 tests pass, Ruff
clean, coverage 96%, `pip-audit` clean. Phase 1 Done; Phase 2 not started.

**Next step:** `/story S2.1.1` — sample document generator: read S2.1.1 in
`docs/01-requirements.md`, write its tests first (generated files in
`samples/` with their known text saved as `.txt`, no real personal data).

**Open questions:** Turn on Dependabot alerts and check secret-scanning
alerts on GitHub — skipped for now by the user. Should `16-budget.md` drop
to Optional? Follow-ups (not urgent): PyMuPDF `import fitz` deprecation
warning; Pillow `getdata` deprecation in `tests/test_io_and_preprocess.py`
(removed in Pillow 14, 2027-10).

---

## 2026-10-11 — F1.2 Export and CLI built; F1.1 merged

**Worked on:** PR #8 (F1.1) merged, branch deleted; `/story F1.2` —
S1.2.1, S1.2.2

**Time spent:** counted in the wrap-up entry above

**Changed:**
- `export.py` — JSON (all fields) and one-row-per-page CSV from
  `PageResult` (`source_file, page, text, confidence, error`; UTF-8 with BOM)
- `pipeline.py` — `run_pipeline()` takes `dpi` and `threshold` (option A,
  chosen by the user, so the CLI options keep working)
- `cli.py` — thin caller of `run_pipeline()`; exit 0 / 1 (any error) / 2
  (usage); summary line logged; `main(argv)` returns the exit code
- `tests/fakes.py` — shared `FakeBackend` (third copy extracted)
- Docs: architecture (components diagram, contract), AGENTS run command

**Stopped at:** F1.2 Done on `feature/F1.2-export-and-cli`; 42 tests pass.
Not yet pushed, no PR. Phase 1 still has the formatter/linter task left.

**Next step:** after the F1.2 PR is merged: choose formatter and linter
(last Phase 1 task), then the Phase 1 end checks (`07-testing-checklist.md`).

**Open questions:** None. `io.load_inputs()` (unused after S1.2.2) and its
test `test_load_inputs_mixed` were removed with the user's OK.

---

## 2026-10-11 — F1.1 Clean pipeline core built

**Worked on:** `/story F1.1` — S1.1.1, S1.1.2, S1.1.4, S1.1.5 (S1.1.3 stays
Dropped)

**Time spent:** counted in the wrap-up entry above

**Changed:**
- `models.py` (new) — `Line`, `PageResult`; `page=None` when a whole file
  fails to load
- `backend.py` — backend registry (`BACKENDS`, `get_backend()`); Baidu and
  `requests` removed; `recognize()` returns `list[Line]`
- `cli.py` — minimal change: backend from the registry, `--backend`
  defaults to `local`; with no backend it stops with a usage error
- `io.py` — `expand_inputs()` for folders (top level, sorted)
- `pipeline.py` (new) — `run_pipeline()` with skip-and-report
- Docs: README, AGENTS, vision, architecture (diagrams), tech stack,
  glossary, threat model filled in (`14-security.md`), `.env.example`

**Stopped at:** F1.1 Done on `feature/F1.1-clean-pipeline-core`, one commit
per story; 29 tests pass. Not yet pushed, no PR.

**Next step:** after the F1.1 PR is merged, `/story F1.2` (S1.2.1 export
from `PageResult`, S1.2.2 CLI calls `run_pipeline()`).

**Open questions:** Should `16-budget.md` drop to Optional now that no paid
API is planned? Follow-up: PyMuPDF prints "`fitz` API is deprecated, use
`import pymupdf`" on import.

---

## 2026-10-10 — Session wrap-up: breakdown, F4.1 done, Phase 1 started

**Worked on:** `/breakdown`, S4.1.1, S4.1.2 (F4.1 done), DoD report format

**Time spent:** ~1h (whole session; the two entries below are part of it)

**Changed:**
- PR #2 — requirements breakdown: epics E1–E4, Phase 1–2 stories, NFRs,
  hour-based plan, "Phase order changed" decision, glossary
- PR #3 — S4.1.1: SSL error no longer reproduces; setup in `03-tech-stack.md`
- PR #4 — DoD report table format in `01-requirements.md` + `/story` skill
- PR #6 — S4.1.2: CI shown green (PR #4) and red (throwaway PR #5, closed)
- This entry — `04-project-plan.md`: Phase 1 marked In progress (started
  2026-10-10), S4.1.1/S4.1.2 ticked, F4.1 bar marked done

**Stopped at:** `main` clean and in sync; 8 tests pass locally and in CI.
F4.1 Done. All F1.1 / F1.2 stories are Ready; none started.

**Next step:** `/story S1.1.1` — write tests for a `PageResult` dataclass in
`tests/test_models.py` (fields `source_file`, `page`, `text`, `lines`,
`error`; empty page → `text == ""`, `lines == []`), see them fail, then
create `src/ocr_pipeline/models.py`.

**Open questions:** None. Protect `main`? Decided no — solo personal
project; revisit if collaborators get write access or an agent may merge.
Follow-up (not urgent): Pillow `getdata` deprecation in
`tests/test_io_and_preprocess.py:58` (removed in Pillow 14, 2027-10).

---

## 2026-10-10 — S4.1.2 CI verified; F4.1 done

**Worked on:** S4.1.2 (also PR #4: DoD report table format)

**Time spent:** counted in the wrap-up entry above

**Changed:**
- `docs/01-requirements.md` — S4.1.2 and F4.1 Done, with CI evidence
- No code or workflow change: `.github/workflows/python.yml` already runs
  `pytest` on PRs to `main`

**Stopped at:** S4.1.2 done on `feature/S4.1.2-ci-on-every-pr`, not yet
committed. CI shown green (PR #4) and red (throwaway PR #5, closed, branch
deleted). F4.1 Done-when met: `pytest` green locally and on a PR.

**Next step:** S1.1.1 — typed `PageResult` in `src/ocr_pipeline/models.py`,
test-first.

**Open questions:** Protect `main` so a red CI blocks merging? (optional,
`13-git-workflow.md`)

---

## 2026-10-10 — Breakdown written; S4.1.1 environment verified

**Worked on:** `/breakdown` (PR #2, merged), S4.1.1

**Time spent:** counted in the wrap-up entry above

**Changed:**
- `docs/01-requirements.md`, `04-project-plan.md`, `05-decisions-log.md`,
  `02-architecture.md`, `11-glossary.md` — breakdown: epics E1–E4, Phase 1–2
  stories, NFRs, hour-based plan, "Phase order changed" decision (PR #2)
- `docs/03-tech-stack.md` — verified local setup steps; SSL error no longer
  reproduces, no workaround needed
- `docs/00-vision.md`, `review_notes.md` — install assumption marked confirmed
- `docs/01-requirements.md` — S4.1.1 Done

**Stopped at:** S4.1.1 done on `feature/S4.1.1-fix-pip-install`, not yet
committed. Fresh `.venv` installs cleanly; `pytest` 8 passed, 1 warning
(Pillow `getdata` deprecation in `tests/test_io_and_preprocess.py:58`,
removed in Pillow 14, 2027-10).

**Next step:** S4.1.2 — confirm CI runs `pytest` on a PR and goes red on a
deliberately failing test (throwaway branch).

**Open questions:** None

---

## Template

```
## YYYY-MM-DD — <short summary of the session>

**Worked on:** <story IDs, e.g. S1.2.3>

**Time spent:** <hours, e.g. 1.5h — used for the budget in 16-budget.md>

**Changed:**
- <file or folder> — <what changed and why>

**Stopped at:** <exactly where things are: what works, what's half-done,
any failing test and why>

**Next step:** <the very next thing to do — specific enough to start on
without thinking, e.g. "make test_empty_input pass in perception/detect.py">

**Open questions:** <anything waiting on the user, or "None">
```
