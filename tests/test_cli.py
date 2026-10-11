"""Tests for the CLI as a thin caller of run_pipeline() and the exporters (S1.2.2, F1.2)."""

import csv
import json
import logging
from pathlib import Path

import fitz
import pytest
from fakes import FakeBackend
from PIL import Image

from ocr_pipeline import backend, cli
from ocr_pipeline.models import Line


def make_image(path: Path) -> Path:
    Image.new("RGB", (60, 40), color="white").save(path)
    return path


def make_pdf(path: Path, pages: int) -> Path:
    document = fitz.open()
    for _ in range(pages):
        document.new_page(width=100, height=80)
    document.save(str(path))
    document.close()
    return path


@pytest.fixture
def fake_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        backend,
        "BACKENDS",
        {
            "fake": FakeBackend,
            "fails-on-2nd": lambda: FakeBackend(fail_on=(2,)),
            "secret": lambda: FakeBackend(
                lines=[Line(text="SECRET-DOC-TEXT", confidence=1.0)]
            ),
        },
    )


def test_writes_json_via_run_pipeline_for_files_and_folders(
    tmp_path: Path, fake_registry: None
) -> None:
    image = make_image(tmp_path / "single.png")
    folder = tmp_path / "batch"
    folder.mkdir()
    make_pdf(folder / "doc.pdf", pages=2)
    output = tmp_path / "out" / "results.json"

    code = cli.main(
        [str(image), str(folder), "--output", str(output), "--backend", "fake"]
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert [(Path(p["source_file"]).name, p["page"]) for p in payload] == [
        ("single.png", 1),
        ("doc.pdf", 1),
        ("doc.pdf", 2),
    ]
    assert payload[0]["text"] == "hello\nworld"
    assert code == 0


def test_writes_csv_with_one_row_per_page(tmp_path: Path, fake_registry: None) -> None:
    pdf = make_pdf(tmp_path / "doc.pdf", pages=3)
    output = tmp_path / "results.csv"

    code = cli.main(
        [str(pdf), "--output", str(output), "--format", "csv", "--backend", "fake"]
    )

    with open(output, encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["page"] for row in rows] == ["1", "2", "3"]
    assert code == 0


def test_exit_code_1_when_any_page_has_an_error(
    tmp_path: Path, fake_registry: None, caplog: pytest.LogCaptureFixture
) -> None:
    pdf = make_pdf(tmp_path / "doc.pdf", pages=3)
    output = tmp_path / "results.json"

    with caplog.at_level(logging.INFO):
        code = cli.main(
            [str(pdf), "--output", str(output), "--backend", "fails-on-2nd"]
        )

    assert code == 1
    assert output.is_file()
    summary = [
        r
        for r in caplog.records
        if r.name == "ocr_pipeline.cli" and r.levelno == logging.INFO
    ]
    assert any(
        "3 pages" in r.getMessage() and "1 with errors" in r.getMessage()
        for r in summary
    )


def test_exit_code_0_and_summary_when_all_pages_succeed(
    tmp_path: Path, fake_registry: None, caplog: pytest.LogCaptureFixture
) -> None:
    image = make_image(tmp_path / "page.png")

    with caplog.at_level(logging.INFO):
        code = cli.main(
            [str(image), "--output", str(tmp_path / "r.json"), "--backend", "fake"]
        )

    assert code == 0
    summary = [
        r
        for r in caplog.records
        if r.name == "ocr_pipeline.cli" and r.levelno == logging.INFO
    ]
    assert any(
        "1 pages" in r.getMessage() and "0 with errors" in r.getMessage()
        for r in summary
    )


def test_no_inputs_is_a_usage_error(tmp_path: Path, fake_registry: None) -> None:
    with pytest.raises(SystemExit) as exit_info:
        cli.main(["--output", str(tmp_path / "r.json"), "--backend", "fake"])

    assert exit_info.value.code == 2


def test_unknown_backend_is_a_usage_error_listing_backends(
    tmp_path: Path, fake_registry: None, capsys: pytest.CaptureFixture[str]
) -> None:
    image = make_image(tmp_path / "page.png")

    with pytest.raises(SystemExit) as exit_info:
        cli.main(
            [str(image), "--output", str(tmp_path / "r.json"), "--backend", "nope"]
        )

    assert exit_info.value.code == 2
    stderr = capsys.readouterr().err
    assert "nope" in stderr and "fake" in stderr
    assert "Traceback" not in stderr


def test_missing_input_path_is_a_usage_error(
    tmp_path: Path, fake_registry: None, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        cli.main(
            [
                str(tmp_path / "missing.png"),
                "--output",
                str(tmp_path / "r.json"),
                "--backend",
                "fake",
            ]
        )

    assert exit_info.value.code == 2
    assert "missing.png" in capsys.readouterr().err


def test_output_goes_through_logging_and_text_never_above_debug(
    tmp_path: Path,
    fake_registry: None,
    caplog: pytest.LogCaptureFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    image = make_image(tmp_path / "page.png")

    with caplog.at_level(logging.DEBUG):
        cli.main(
            [str(image), "--output", str(tmp_path / "r.json"), "--backend", "secret"]
        )

    assert capsys.readouterr().out == ""
    assert caplog.records, "expected the run to log something"
    leaked = [
        r
        for r in caplog.records
        if r.levelno > logging.DEBUG and "SECRET-DOC-TEXT" in r.getMessage()
    ]
    assert leaked == []


def test_corrupt_file_is_reported_without_stopping_the_run(
    tmp_path: Path, fake_registry: None
) -> None:
    """Phase 1 exit criterion, end to end through the CLI."""
    good = make_image(tmp_path / "good.png")
    corrupt = tmp_path / "corrupt.pdf"
    corrupt.write_bytes(b"not a pdf")
    output = tmp_path / "results.csv"

    code = cli.main(
        [str(corrupt), str(good), "--output", str(output), "--format", "csv"]
        + ["--backend", "fake"]
    )

    with open(output, encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert code == 1
    assert [Path(row["source_file"]).name for row in rows] == [
        "corrupt.pdf",
        "good.png",
    ]
    assert rows[0]["error"] and rows[0]["page"] == ""
    assert rows[1]["error"] == "" and rows[1]["text"] == "hello\nworld"
