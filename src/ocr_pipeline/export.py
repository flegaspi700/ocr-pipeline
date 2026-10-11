"""Write page results to a JSON or CSV file.

The last step of a run: the CLI (and later the UI) passes the `PageResult`
list from `run_pipeline()` here. JSON keeps every field, including each
line; CSV has one row per page for reading in a spreadsheet.
Built for S1.2.1.
"""

import csv
import json
from dataclasses import asdict
from pathlib import Path
from statistics import fmean

from .models import PageResult

CSV_COLUMNS = ["source_file", "page", "text", "confidence", "error"]


def export_to_json(results: list[PageResult], output_path: Path) -> None:
    """Write `results` as a JSON list of page results with all fields (`[]` if empty)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(
            [asdict(result) for result in results], handle, ensure_ascii=False, indent=2
        )


def export_to_csv(results: list[PageResult], output_path: Path) -> None:
    """Write `results` as CSV, one row per page with `CSV_COLUMNS`.

    `confidence` is the mean over the page's lines, empty when it has none;
    `page` and `error` are empty when not set. An empty list writes the
    header row only.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # utf-8-sig adds a byte-order mark so Excel opens non-ASCII text correctly.
    with open(output_path, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "source_file": result.source_file,
                    "page": result.page,
                    "text": result.text,
                    "confidence": fmean(line.confidence for line in result.lines)
                    if result.lines
                    else None,
                    "error": result.error,
                }
            )
