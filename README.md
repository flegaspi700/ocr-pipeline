# ocr_pipeline

A small Python CLI and library that turns images and multi-page PDFs into
per-page text as JSON or CSV: it rasterizes PDF pages, preprocesses each page
(resize, grayscale, binarize), sends it to a pluggable OCR backend, and exports
the results.

**Status:** no OCR backend is installed yet. A free local engine is planned
(Phase 2 in `docs/04-project-plan.md`); until then `ocr-pipeline` stops with
"No OCR backend installed".


## Project target (current)

**In:** a CLI, Python API, and simple local web UI that turn images and
multi-page PDFs into per-page text as JSON or CSV, with pluggable OCR
backends (a free local engine first), tested locally and in CI.
**Out (for now):** a hosted service or full desktop app, cloud backends, model training, layout
reconstruction, handwriting tuning.

See `docs/00-vision.md` for goals and `docs/` for the full project docs.
