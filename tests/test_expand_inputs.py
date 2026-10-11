"""Tests for expanding folder inputs into their files (S1.1.4)."""

import logging
from pathlib import Path

import pytest

from ocr_pipeline.io import expand_inputs


def touch(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")
    return path


def test_folder_expands_to_supported_files_in_sorted_order(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    folder = tmp_path / "batch"
    touch(folder / "b.pdf")
    touch(folder / "a.png")
    touch(folder / "C.JPG")
    touch(folder / "notes.txt")

    with caplog.at_level(logging.DEBUG, logger="ocr_pipeline.io"):
        expanded = expand_inputs([folder])

    assert expanded == sorted([folder / "a.png", folder / "b.pdf", folder / "C.JPG"])
    skipped = [r for r in caplog.records if "notes.txt" in r.getMessage()]
    assert len(skipped) == 1
    assert skipped[0].levelno == logging.DEBUG


def test_files_in_subfolders_are_ignored(tmp_path: Path) -> None:
    folder = tmp_path / "batch"
    touch(folder / "top.png")
    touch(folder / "nested" / "deep.png")

    assert expand_inputs([folder]) == [folder / "top.png"]


def test_empty_folder_as_only_input_is_an_error_naming_it(tmp_path: Path) -> None:
    folder = tmp_path / "empty"
    folder.mkdir()

    with pytest.raises(ValueError, match="empty"):
        expand_inputs([folder])


def test_folder_without_supported_files_as_only_input_is_an_error(tmp_path: Path) -> None:
    folder = tmp_path / "text_only"
    touch(folder / "notes.txt")

    with pytest.raises(ValueError, match="text_only"):
        expand_inputs([folder])


def test_empty_folder_among_other_inputs_logs_warning_and_continues(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    folder = tmp_path / "empty"
    folder.mkdir()
    image = touch(tmp_path / "page.png")

    with caplog.at_level(logging.WARNING, logger="ocr_pipeline.io"):
        expanded = expand_inputs([folder, image])

    assert expanded == [image]
    warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert any("empty" in r.getMessage() for r in warnings)


def test_missing_path_error_names_the_path(tmp_path: Path) -> None:
    missing = tmp_path / "nope.png"

    with pytest.raises(FileNotFoundError, match="nope.png"):
        expand_inputs([missing])


def test_files_keep_input_order_and_pass_through(tmp_path: Path) -> None:
    second = touch(tmp_path / "z.png")
    first = touch(tmp_path / "a.pdf")

    assert expand_inputs([second, first]) == [second, first]


def test_no_inputs_expand_to_nothing() -> None:
    assert expand_inputs([]) == []
