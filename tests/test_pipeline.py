"""Tests for run_pipeline(): skip-and-report (S1.1.5, F1.1); dpi and threshold (S1.2.2)."""

import io
import logging
from pathlib import Path

import fitz
import pytest
from fakes import FakeBackend
from PIL import Image

from ocr_pipeline.models import Line
from ocr_pipeline.pipeline import run_pipeline


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


def make_corrupt(path: Path) -> Path:
    path.write_bytes(b"this is not an image")
    return path


def test_returns_one_result_per_page_in_input_order(tmp_path: Path) -> None:
    image = make_image(tmp_path / "z_first.png")
    pdf = make_pdf(tmp_path / "a_second.pdf", pages=3)

    results = run_pipeline([image, pdf], FakeBackend())

    assert [(r.source_file, r.page) for r in results] == [
        (str(image), 1),
        (str(pdf), 1),
        (str(pdf), 2),
        (str(pdf), 3),
    ]
    assert all(r.error is None for r in results)
    assert results[0].text == "hello\nworld"
    assert results[0].lines == [
        Line(text="hello", confidence=0.9),
        Line(text="world", confidence=0.8),
    ]


def test_corrupt_file_is_reported_and_good_pages_still_run(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    good_before = make_image(tmp_path / "good1.png")
    corrupt = make_corrupt(tmp_path / "broken.png")
    good_after = make_image(tmp_path / "good2.png")

    with caplog.at_level(logging.WARNING, logger="ocr_pipeline.pipeline"):
        results = run_pipeline([good_before, corrupt, good_after], FakeBackend())

    assert [r.source_file for r in results] == [
        str(good_before),
        str(corrupt),
        str(good_after),
    ]
    assert results[0].error is None and results[0].text == "hello\nworld"
    assert results[2].error is None and results[2].text == "hello\nworld"

    bad = results[1]
    assert bad.error
    assert bad.text == ""
    assert bad.lines == []
    assert any(
        r.levelno == logging.WARNING and "broken.png" in r.getMessage()
        for r in caplog.records
    )


def test_backend_error_on_one_page_marks_only_that_page(tmp_path: Path) -> None:
    pdf = make_pdf(tmp_path / "doc.pdf", pages=3)

    results = run_pipeline([pdf], FakeBackend(fail_on=(2,)))

    assert [r.page for r in results] == [1, 2, 3]
    assert results[0].error is None
    assert "engine crashed" in results[1].error
    assert results[1].text == ""
    assert results[2].error is None


def test_no_input_paths_raises_no_input_files() -> None:
    with pytest.raises(ValueError, match="(?i)no input files"):
        run_pipeline([], FakeBackend())


def test_unsupported_file_given_directly_is_reported_not_raised(tmp_path: Path) -> None:
    notes = tmp_path / "notes.txt"
    notes.write_text("hi", encoding="utf-8")
    image = make_image(tmp_path / "page.png")

    results = run_pipeline([notes, image], FakeBackend())

    assert results[0].source_file == str(notes)
    assert results[0].error
    assert results[1].error is None


def test_feature_done_when_mixed_inputs_folder_and_corrupt_file(tmp_path: Path) -> None:
    """F1.1 Done when: images, a 3-page PDF, a folder and one corrupt file."""
    image = make_image(tmp_path / "single.png")
    pdf = make_pdf(tmp_path / "three.pdf", pages=3)
    folder = tmp_path / "folder"
    folder.mkdir()
    make_image(folder / "b.png")
    make_pdf(folder / "a.pdf", pages=1)
    corrupt = make_corrupt(tmp_path / "corrupt.pdf")

    results = run_pipeline([image, pdf, folder, corrupt], FakeBackend())

    assert [(Path(r.source_file).name, r.page) for r in results] == [
        ("single.png", 1),
        ("three.pdf", 1),
        ("three.pdf", 2),
        ("three.pdf", 3),
        ("a.pdf", 1),
        ("b.png", 1),
        ("corrupt.pdf", None),
    ]
    assert [r.error is None for r in results] == [True] * 6 + [False]


def test_dpi_sets_pdf_page_resolution(tmp_path: Path) -> None:
    pdf = make_pdf(tmp_path / "doc.pdf", pages=1)
    low, high = FakeBackend(), FakeBackend()

    run_pipeline([pdf], low, dpi=72)
    run_pipeline([pdf], high, dpi=144)

    low_size = Image.open(io.BytesIO(low.pages[0])).size
    high_size = Image.open(io.BytesIO(high.pages[0])).size
    assert high_size == (low_size[0] * 2, low_size[1] * 2)


def test_threshold_sets_binarization(tmp_path: Path) -> None:
    gray = tmp_path / "gray.png"
    Image.new("RGB", (20, 20), color=(100, 100, 100)).save(gray)
    lenient, strict = FakeBackend(), FakeBackend()

    run_pipeline([gray], lenient, threshold=50)
    run_pipeline([gray], strict, threshold=200)

    assert set(Image.open(io.BytesIO(lenient.pages[0])).getextrema()) == {255}
    assert set(Image.open(io.BytesIO(strict.pages[0])).getextrema()) == {0}
