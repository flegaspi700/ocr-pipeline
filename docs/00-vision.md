# Vision

Why this project exists. Keep it to one page — if it needs more, the
project is probably two projects. Everything in `01-requirements.md` should
trace back to a goal here; if something doesn't, question whether it
belongs.

## Problem

Text locked in scanned documents, photos, and multi-page PDFs can't be
searched, copied, or processed. Getting it out as structured data means
juggling separate tools for PDF rasterization, image cleanup, and OCR, then
reshaping whatever comes back. This project wraps that chain into one
command that produces JSON or CSV.

## Who it's for

Me — a developer trying out an OCR pipeline on my own scanned documents and
PDFs. I want to run it from the command line on a batch of files and get
structured text back, and be able to call it from Python. Without it, I'd be
using one-off scripts or online OCR tools file by file.

## Why build it

A trial and learning project: get hands-on with an end-to-end OCR pipeline
(PDF rasterization, preprocessing, calling an OCR service, exporting
results) and find out whether the approach and backend are good enough to
invest more in. "Good enough" means it works reliably on my own sample
documents — not production-hardened; parts can be rebuilt or the backend
swapped along the way.

## Goals

Numbered so epics can reference them (`01-requirements.md` → "Serves: G1").

- **G1:** I can point one command at a mix of images and multi-page PDFs
  and get each page's text back as usable JSON or CSV.
- **G2:** I can tell whether the OCR is good enough on my own documents —
  and compare backends without rewriting the pipeline.
- **G3:** I can reuse the pipeline from my own Python code, not just the
  CLI.
- **G4:** I can trust a change didn't break it — tests run green locally
  and in CI.

## Success looks like

How you'll know it worked. Measurable where possible.

- One CLI run on a folder of ~10 sample files (images + a multi-page PDF)
  completes without errors and produces one result per page, in both JSON
  and CSV.
- On my sample documents, extracted text is readable and mostly correct
  when spot-checked against the originals (my judgment, not a formal
  accuracy score).
- A second OCR backend (e.g. local Tesseract) can be added without changing
  anything outside the backend module and a CLI option.
- `pytest` passes locally and in CI on every PR.

## Non-goals

What this project deliberately won't do — saying it upfront stops scope
creep, including from AI agents.

**Not in this version** (candidates for a future version):

- A production service — hosting, API server, multi-user, uptime or scale
  targets
- A full desktop or hosted web app — only a simple local web UI to
  drag/select files and folders and view results
- Training or fine-tuning OCR models
- Layout reconstruction — tables, columns, Word or searchable-PDF output
- Handwriting-specific tuning beyond what the backend already does

## Constraints

- **Time:** spare time, no fixed deadline — it's a trial
- **Budget:** free tools and free tiers only; a paid OCR API only within its
  free quota — limits and tracking in `16-budget.md`
- **Platform / environment:** Windows 11, runs locally; Python 3.11+ (CI
  tests on 3.13, Windows)
- **Other:** pip install once failed here with an SSL handshake error; it
  no longer reproduces (2026-10-10, see `03-tech-stack.md`). API keys never
  committed; they go in environment variables / `.env`.

## Assumptions and risks

- **Assumption:** the dependencies (Pillow, PyMuPDF, requests) install and
  the existing tests pass → **confirmed 2026-10-10** (S4.1.1): clean
  install in a fresh venv, all 8 existing tests pass. (`requests` was later
  removed with the Baidu backend, S1.1.2.)
- **Closed:** the Baidu assumption and risk (unverified API, no key) —
  Baidu was removed in S1.1.2 (`05-decisions-log.md` → 2026-10-10 Phase
  order changed); a free local engine replaces it in Phase 2.
- **Risk:** no free local engine reads my documents well enough, blocking
  G1 → the S2.2.1 spike compares Tesseract and RapidOCR on the samples
  before one is built in.
- **Risk:** fixed-threshold binarization hurts accuracy on photos or
  low-contrast scans → spot-check against samples; make preprocessing
  optional or tunable.
- **Risk:** large PDFs at high DPI use too much memory, since all pages are
  loaded before OCR → process page by page if it becomes a problem.
