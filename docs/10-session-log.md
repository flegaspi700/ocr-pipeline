# Session log

A handoff note at the end of every working session, so the next session
(yours or an AI agent's) can pick up without re-reading everything. Newest
entry at the top. Keep each entry short — a few lines per heading.

AI agents: read the latest entry at the start of a session; add a new one
at the end (see `AGENTS.md`).

---

## 2026-10-11 — F1.1 Clean pipeline core built

**Worked on:** `/story F1.1` — S1.1.1, S1.1.2, S1.1.4, S1.1.5 (S1.1.3 stays
Dropped)

**Time spent:** to be filled in at wrap-up

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
