"""Command-line entry point (`ocr-pipeline`): parse arguments, run OCR, export.

Still runs its own load/preprocess/recognize loop; S1.2.2 turns it into a thin
caller of `run_pipeline()`. Picks the backend from the registry in
`backend.py` (S1.1.2).
"""

import argparse
from dataclasses import asdict
from io import BytesIO
from pathlib import Path

from .backend import get_backend
from .export import export_to_csv, export_to_json
from .io import load_inputs
from .preprocess import preprocess_image


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run OCR pipeline on image and PDF files.")
    parser.add_argument("inputs", nargs="+", help="Paths to image or PDF files.")
    parser.add_argument("--output", required=True, help="Output path for results.")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Export format.")
    parser.add_argument("--dpi", type=int, default=200, help="Rasterization DPI for PDF pages.")
    # "local" is the name the free local engine will register under (S2.2.2).
    parser.add_argument("--backend", default="local", help="OCR backend to use (default: local).")
    parser.add_argument("--threshold", type=int, default=128, help="Binarization threshold for preprocessing.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    # Checked before loading any file, so a missing backend fails fast with a
    # plain message instead of a stack trace.
    try:
        backend = get_backend(args.backend)
    except ValueError as error:
        parser.error(str(error))

    input_paths = [Path(path) for path in args.inputs]
    loaded = load_inputs(input_paths, dpi=args.dpi)

    results = []
    for path, image in loaded:
        processed = preprocess_image(image, threshold=args.threshold)
        buffer = BytesIO()
        processed.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()

        lines = backend.recognize(image_bytes)
        results.append({
            "source": str(path),
            "results": [asdict(line) for line in lines],
        })

    output_path = Path(args.output)
    if args.format == "json":
        export_to_json(results, output_path)
    else:
        export_to_csv(results, output_path)


if __name__ == "__main__":
    main()
