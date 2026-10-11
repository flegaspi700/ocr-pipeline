"""The pipeline core: `run_pipeline()` turns input paths into page results.

Expands folders, loads each file's pages (`io.py`), preprocesses each page
(`preprocess.py`), sends it to the given backend (`backend.py`) and collects
one `PageResult` per page (`models.py`). The CLI and, later, the UI both call
it. A file or page that fails is recorded as an error and the run goes on
(skip-and-report, NFR4). Built for S1.1.5.
"""

import logging
from io import BytesIO
from pathlib import Path
from typing import Iterable

from PIL import Image

from .backend import OCRBackend
from .io import expand_inputs, is_image_file, load_image, rasterize_pdf
from .models import PageResult
from .preprocess import preprocess_image

logger = logging.getLogger(__name__)


def run_pipeline(paths: Iterable[Path], backend: OCRBackend) -> list[PageResult]:
    """OCR every page of `paths` (files and folders) with `backend`.

    Returns one `PageResult` per page, in input order (a folder's files in
    name order, a PDF's pages in page order). A file that can't be loaded
    gives one result with `page=None` and `error` set; a page the backend
    fails on gives a result with `error` set. Both are logged as warnings.

    Raises ValueError if `paths` is empty, and whatever `expand_inputs()`
    raises for a missing path or an input made only of empty folders.
    """
    paths = list(paths)
    if not paths:
        raise ValueError("No input files given. Pass at least one image, PDF or folder.")

    results: list[PageResult] = []
    for path in expand_inputs(paths):
        source_file = str(path)
        # Any exception here means this one file is unusable (corrupt, wrong
        # type, unreadable); record it and move on so one bad file never stops
        # the run (NFR4).
        try:
            pages = load_pages(path)
        except Exception as error:
            logger.warning("Skipping file %s: %s", source_file, error)
            logger.debug("Load failure details for %s", source_file, exc_info=True)
            results.append(PageResult(source_file=source_file, page=None, error=str(error)))
            continue

        for page_number, image in enumerate(pages, start=1):
            results.append(ocr_page(source_file, page_number, image, backend))

    failed = sum(1 for result in results if result.error)
    logger.info("Run finished: %d page results, %d with errors", len(results), failed)
    return results


def load_pages(path: Path) -> list[Image.Image]:
    """Return the RGB page images of one image or PDF file; ValueError for other types."""
    if is_image_file(path):
        return [load_image(path)]
    if path.suffix.lower() == ".pdf":
        return rasterize_pdf(path)
    raise ValueError(f"Unsupported file type '{path.suffix}'. Use an image or PDF file.")


def ocr_page(source_file: str, page: int, image: Image.Image, backend: OCRBackend) -> PageResult:
    """Preprocess one page, OCR it, and return its result (with `error` set if that failed)."""
    try:
        buffer = BytesIO()
        preprocess_image(image).save(buffer, format="PNG")
        lines = backend.recognize(buffer.getvalue())
    # Backends are third-party engines that can fail in any way; one page's
    # failure must not stop the others (NFR4).
    except Exception as error:
        logger.warning("OCR failed on %s page %d: %s", source_file, page, error)
        logger.debug("OCR failure details for %s page %d", source_file, page, exc_info=True)
        return PageResult(source_file=source_file, page=page, error=str(error))

    return PageResult(
        source_file=source_file,
        page=page,
        text="\n".join(line.text for line in lines),
        lines=lines,
    )
