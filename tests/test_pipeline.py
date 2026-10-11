"""Tests for run_pipeline() and its skip-and-report behaviour (S1.1.5, F1.1)."""

import logging
from pathlib import Path

import fitz
import pytest
from PIL import Image

from ocr_pipeline.backend import OCRBackend
from ocr_pipeline.models import Line
from ocr_pipeline.pipeline import run_pipeline


class FakeBackend(OCRBackend):
    """Returns two fixed lines per page; raises on the calls listed in `fail_on` (1-based)."""

    def __init__(self, fail_on: tuple[int, ...] = ()) -> None:
        self.calls = 0
        self.fail_on = fail_on

    def recognize(self, image_bytes: bytes) -> list[Line]:
        self.calls += 1
        if self.calls in self.fail_on:
            raise RuntimeError("engine crashed")
        return [Line(text="hello", confidence=0.9), Line(text="world", confidence=0.8)]


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
    assert results[0].lines == [Line(text="hello", confidence=0.9), Line(text="world", confidence=0.8)]


def test_corrupt_file_is_reported_and_good_pages_still_run(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    good_before = make_image(tmp_path / "good1.png")
    corrupt = make_corrupt(tmp_path / "broken.png")
    good_after = make_image(tmp_path / "good2.png")

    with caplog.at_level(logging.WARNING, logger="ocr_pipeline.pipeline"):
        results = run_pipeline([good_before, corrupt, good_after], FakeBackend())

    assert [r.source_file for r in results] == [str(good_before), str(corrupt), str(good_after)]
    assert results[0].error is None and results[0].text == "hello\nworld"
    assert results[2].error is None and results[2].text == "hello\nworld"

    bad = results[1]
    assert bad.error
    assert bad.text == ""
    assert bad.lines == []
    assert any(
        r.levelno == logging.WARNING and "broken.png" in r.getMessage() for r in caplog.records
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
