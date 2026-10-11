"""Command-line entry point (`ocr-pipeline`): parse arguments, run, export.

A thin caller: gets the backend from the registry (`backend.py`), calls
`run_pipeline()` (`pipeline.py`) and writes the page results with
`export.py`. Exit code 0 = every page succeeded, 1 = some page or file
failed (see the output file and warnings), 2 = usage error.
Built for S1.1.2 (registry) and S1.2.2 (thin caller).
"""

import argparse
import logging
from pathlib import Path

from .backend import get_backend
from .export import export_to_csv, export_to_json
from .pipeline import run_pipeline

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run OCR on image and PDF files, or folders of them.")
    parser.add_argument("inputs", nargs="+", help="Image or PDF files, or folders (top level only).")
    parser.add_argument("--output", required=True, help="Output path for results.")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Export format.")
    parser.add_argument("--dpi", type=int, default=200, help="Rasterization DPI for PDF pages.")
    # "local" is the name the free local engine will register under (S2.2.2).
    parser.add_argument("--backend", default="local", help="OCR backend to use (default: local).")
    parser.add_argument("--threshold", type=int, default=128, help="Binarization threshold for preprocessing.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI on `argv` (default: the command line); return the exit code.

    Usage errors (no inputs, unknown backend, missing path, only empty
    folders) exit with code 2 via argparse, without a stack trace.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args(argv)

    # Checked before loading any file, so a missing backend fails fast.
    try:
        backend = get_backend(args.backend)
    except ValueError as error:
        parser.error(str(error))

    # run_pipeline only raises for unusable input as a whole (a missing path,
    # only empty folders); bad files and pages come back as page results.
    try:
        results = run_pipeline(
            [Path(path) for path in args.inputs], backend, dpi=args.dpi, threshold=args.threshold
        )
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))

    output_path = Path(args.output)
    if args.format == "json":
        export_to_json(results, output_path)
    else:
        export_to_csv(results, output_path)

    failed = sum(1 for result in results if result.error)
    logger.info("Wrote %d pages to %s (%d with errors)", len(results), output_path, failed)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
