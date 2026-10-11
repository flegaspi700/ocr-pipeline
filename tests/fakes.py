"""Test doubles shared by several test files: a fake OCR backend."""

from ocr_pipeline.backend import OCRBackend
from ocr_pipeline.models import Line


class FakeBackend(OCRBackend):
    """Returns two fixed lines per page; raises on the calls listed in `fail_on` (1-based).

    Records the PNG bytes of every page it was sent in `pages`.
    """

    def __init__(
        self, fail_on: tuple[int, ...] = (), lines: list[Line] | None = None
    ) -> None:
        self.calls = 0
        self.fail_on = fail_on
        self.lines = lines or [
            Line(text="hello", confidence=0.9),
            Line(text="world", confidence=0.8),
        ]
        self.pages: list[bytes] = []

    def recognize(self, image_bytes: bytes) -> list[Line]:
        self.calls += 1
        self.pages.append(image_bytes)
        if self.calls in self.fail_on:
            raise RuntimeError("engine crashed")
        return list(self.lines)
