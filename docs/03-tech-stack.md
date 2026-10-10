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
| OCR backend (HTTP) | `requests` ≥ 2.31 → Baidu OCR API | First backend behind the pluggable `OCRBackend` interface |
| Export | `json`, `csv` (standard library) | No extra dependency |
| Persistence | None — output files only | Batch tool, no state between runs |

## Dev environment

| Tool | Purpose |
|---|---|
| <editor> | Primary editor |
| <formatter> | Formatting — not set up yet |
| <linter / type checker> | Linting and type checks — not set up yet |
| pytest | Tests (`tests/`, HTTP calls mocked with `monkeypatch`) |
| <coverage tool> | Coverage report (a hint, no target %) — not set up yet |
| <dependency audit tool, e.g. pip-audit> | Known vulnerabilities in dependencies (`14-security.md`) — not set up yet |
| venv (`.venv/`, git-ignored) | Dependency isolation |
| GitHub Actions (`.github/workflows/python.yml`) | CI: `pip install -e .` + `pytest` on windows-latest, Python 3.13, on push/PR to `main` |

## Starting dependencies

```
Pillow>=10.0.0
PyMuPDF>=1.22.0
requests>=2.31.0
```

Dev: `pytest` (installed separately in CI; not declared in `pyproject.toml`).

## Deferred / not needed yet

- A local OCR backend (e.g. Tesseract) — if Baidu proves unusable or for
  comparison (see `00-vision.md` → risks)
- OpenCV — only if `deskew` (currently a placeholder) needs it
