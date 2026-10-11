"""Typed data passed between pipeline components.

`PageResult` is what the pipeline produces for each page and what export
consumes; `Line` is what an OCR backend returns for each recognized line.
Replaces the raw dicts used before, so the interface documents itself.
Built for S1.1.1.
"""

from dataclasses import dataclass, field


@dataclass
class Line:
    """One recognized line of text and the backend's confidence in it (0.0-1.0)."""

    text: str
    confidence: float


@dataclass
class PageResult:
    """The OCR result for one page of one input file.

    `page` is 1-based. A page with no text has `text == ""` and `lines == []`.
    A failed page has `error` set to the message and no text.
    """

    source_file: str
    page: int
    text: str = ""
    lines: list[Line] = field(default_factory=list)
    error: str | None = None
