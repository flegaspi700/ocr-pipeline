# ocr_pipeline

A lightweight repository containing examples and utilities to build a scalable OCR pipeline using Baidu's Unlimited-OCR. This project focuses on processing high-resolution images and extracting text from multi-page PDFs, with components for image preprocessing, PDF rasterization, parallel inference, and result post-processing (JSON/CSV export). Ideal for document digitization, automated data extraction, and batch processing workflows.


## Project target (current)

**In:** a CLI, Python API, and simple local web UI that turn images and
multi-page PDFs into per-page text as JSON or CSV, with pluggable OCR
backends (a free local engine first), tested locally and in CI.
**Out (for now):** a hosted service or full desktop app, cloud backends, model training, layout
reconstruction, handwriting tuning.

See `docs/00-vision.md` for goals and `docs/` for the full project docs.
