"""OCR backend interface and the backend registry.

A backend takes one preprocessed page image (PNG bytes) and returns its
recognized lines. `get_backend()` looks a backend up by name in `BACKENDS`;
the CLI (and later the UI) call it with the user's choice. Adding an engine
means writing an `OCRBackend` subclass here and adding it to `BACKENDS`.
Built for S1.1.2.
"""

import abc
from collections.abc import Callable

from .models import Line


class OCRBackend(abc.ABC):
    @abc.abstractmethod
    def recognize(self, image_bytes: bytes) -> list[Line]:
        """Recognize text in one PNG-encoded page image; return its lines in reading order."""
        raise NotImplementedError


# Empty until the local engine lands (S2.2.2); tests register a fake backend.
BACKENDS: dict[str, Callable[[], OCRBackend]] = {}


def get_backend(name: str) -> OCRBackend:
    """Create the backend registered under `name`.

    Raises ValueError if no backend is installed at all, or if `name` is not
    registered (the message lists the names that are).
    """
    if not BACKENDS:
        raise ValueError(
            "No OCR backend installed. A free local engine is planned "
            "(see docs/04-project-plan.md, Phase 2); until then the pipeline "
            "can only run with a backend you add to BACKENDS in ocr_pipeline/backend.py."
        )
    if name not in BACKENDS:
        available = ", ".join(sorted(BACKENDS))
        raise ValueError(
            f"Unknown OCR backend '{name}'. Available backends: {available}."
        )
    return BACKENDS[name]()
