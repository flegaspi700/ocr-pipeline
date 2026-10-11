# Tech stack

Every dependency in the project should appear here with a reason. If an AI
agent wants to add one that isn't listed, it logs the decision in
`05-decisions-log.md` first.

This doc shows what was *chosen*. For significant choices (language,
framework, storage, anything hard to swap out), the options that were
compared and why the others lost are in the matching
`05-decisions-log.md` entry — link it in the Rationale column.

## Core

Existing stack, recorded as found in the repo (see `05-decisions-log.md` →
"Existing stack, kept as is").

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python 3.11+ (`requires-python = ">=3.11"`; CI on 3.13) | Existing code |
| Packaging | setuptools via `pyproject.toml`, `src/` layout, console script `ocr-pipeline` | Existing code |
| CLI | `argparse` (standard library) | No extra dependency |
| PDF rasterization | PyMuPDF (`fitz`) ≥ 1.22 | Renders PDF pages to images at a chosen DPI |
| Image preprocessing | Pillow ≥ 10.0 | Resize, grayscale, binarize |
| OCR backend | None yet — backend registry in `backend.py` (S1.1.2); a free local engine comes in Phase 2 | Baidu removed (`05-decisions-log.md` → Phase order changed) |
| Export | `json`, `csv` (standard library) | No extra dependency |
| Persistence | None — output files only | Batch tool, no state between runs |

## Dev environment

| Tool | Purpose |
|---|---|
| <editor> | Primary editor |
| <formatter> | Formatting — not set up yet |
| <linter / type checker> | Linting and type checks — not set up yet |
| pytest | Tests (`tests/`, a fake backend registered with `monkeypatch`) |
| <coverage tool> | Coverage report (a hint, no target %) — not set up yet |
| <dependency audit tool, e.g. pip-audit> | Known vulnerabilities in dependencies (`14-security.md`) — not set up yet |
| venv (`.venv/`, git-ignored) | Dependency isolation |
| GitHub Actions (`.github/workflows/python.yml`) | CI: `pip install -e .` + `pytest` on windows-latest, Python 3.13, on push/PR to `main` |

**Local setup (verified 2026-10-10, S4.1.1):** `python -m venv .venv` with
Python 3.13, then `pip install -e .` and `pip install pytest` inside it. No
machine setting was needed: no pip config, proxy, or custom certificates.
The earlier `SSLV3_ALERT_HANDSHAKE_FAILURE` from `files.pythonhosted.org`
(`review_notes.md`) no longer reproduces, even with `--no-cache-dir`; it
was most likely a network-side issue at the time. If it comes back, check
the network/proxy and the Python version first. Never work around it with
`--trusted-host` or by turning off certificate verification.

## Starting dependencies

```
Pillow>=10.0.0
PyMuPDF>=1.22.0
```

(`requests` was removed with the Baidu backend in S1.1.2.)

Dev: `pytest` (installed separately in CI; not declared in `pyproject.toml`).

## Deferred / not needed yet

- A local OCR backend — chosen in the S2.2.1 spike (Tesseract vs RapidOCR)
- OpenCV — only if `deskew` (currently a placeholder) needs it
