"""Tests for exporting page results as JSON and CSV (S1.2.1)."""

import csv
import json
from pathlib import Path

from ocr_pipeline.export import CSV_COLUMNS, export_to_csv, export_to_json
from ocr_pipeline.models import Line, PageResult


def sample_results() -> list[PageResult]:
    return [
        PageResult(
            source_file="scan.pdf",
            page=1,
            text="Hello\nworld",
            lines=[Line(text="Hello", confidence=0.9), Line(text="world", confidence=0.7)],
        ),
        PageResult(source_file="blank.png", page=1),
        PageResult(source_file="broken.pdf", page=None, error="cannot open broken document"),
    ]


def read_csv(path: Path) -> list[dict[str, str]]:
    with open(path, encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_json_is_a_list_of_page_results_with_all_fields(tmp_path: Path) -> None:
    output_path = tmp_path / "results.json"

    export_to_json(sample_results(), output_path)

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload[0] == {
        "source_file": "scan.pdf",
        "page": 1,
        "text": "Hello\nworld",
        "lines": [{"text": "Hello", "confidence": 0.9}, {"text": "world", "confidence": 0.7}],
        "error": None,
    }
    assert payload[2]["page"] is None
    assert payload[2]["error"] == "cannot open broken document"
    assert len(payload) == 3


def test_csv_has_one_row_per_page_with_mean_confidence(tmp_path: Path) -> None:
    output_path = tmp_path / "results.csv"

    export_to_csv(sample_results(), output_path)

    with open(output_path, encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    assert header == ["source_file", "page", "text", "confidence", "error"]
    assert CSV_COLUMNS == header

    rows = read_csv(output_path)
    assert len(rows) == 3
    assert rows[0]["source_file"] == "scan.pdf"
    assert rows[0]["page"] == "1"
    assert float(rows[0]["confidence"]) == 0.8
    assert rows[0]["error"] == ""
    assert rows[1]["confidence"] == ""
    assert rows[2]["page"] == ""
    assert rows[2]["error"] == "cannot open broken document"


def test_csv_round_trips_awkward_text(tmp_path: Path) -> None:
    awkward = 'Total, incl. "VAT"\nline two — café, naïve, 東京, Ελλάδα'
    results = [PageResult(source_file="odd, name.png", page=1, text=awkward)]
    output_path = tmp_path / "results.csv"

    export_to_csv(results, output_path)

    rows = read_csv(output_path)
    assert rows[0]["text"] == awkward
    assert rows[0]["source_file"] == "odd, name.png"


def test_empty_results_give_headers_only_csv_and_empty_json(tmp_path: Path) -> None:
    csv_path = tmp_path / "results.csv"
    json_path = tmp_path / "results.json"

    export_to_csv([], csv_path)
    export_to_json([], json_path)

    with open(csv_path, encoding="utf-8-sig", newline="") as handle:
        assert list(csv.reader(handle)) == [["source_file", "page", "text", "confidence", "error"]]
    assert json.loads(json_path.read_text(encoding="utf-8")) == []


def test_export_creates_missing_output_folder(tmp_path: Path) -> None:
    output_path = tmp_path / "new" / "folder" / "results.csv"

    export_to_csv(sample_results(), output_path)

    assert output_path.is_file()
