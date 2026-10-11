"""Tests for the typed page result passed between components (S1.1.1)."""

from ocr_pipeline.models import Line, PageResult


def test_page_result_holds_all_fields() -> None:
    lines = [Line(text="Hello", confidence=0.98), Line(text="world", confidence=0.91)]
    result = PageResult(source_file="scan.pdf", page=2, text="Hello\nworld", lines=lines)

    assert result.source_file == "scan.pdf"
    assert result.page == 2
    assert result.text == "Hello\nworld"
    assert result.lines[0].text == "Hello"
    assert result.lines[0].confidence == 0.98
    assert result.error is None


def test_page_with_no_text_has_empty_text_and_lines() -> None:
    result = PageResult(source_file="blank.png", page=1)

    assert result.text == ""
    assert result.lines == []


def test_failed_page_holds_error_and_empty_text() -> None:
    result = PageResult(source_file="broken.png", page=1, error="cannot identify image file")

    assert result.error == "cannot identify image file"
    assert result.text == ""
    assert result.lines == []


def test_empty_lines_are_not_shared_between_results() -> None:
    first = PageResult(source_file="a.png", page=1)
    second = PageResult(source_file="b.png", page=1)

    first.lines.append(Line(text="x", confidence=1.0))

    assert second.lines == []
