"""Input loading: expand folders, load images, rasterize PDF pages.

The boundary where user-given paths enter the pipeline: checks that paths
exist and have a supported type, then turns each file into RGB page images
for preprocessing. Called by the CLI (and `run_pipeline()`). Folder
expansion added for S1.1.4.
"""

import io
import logging
from pathlib import Path
from typing import Iterable, List

from PIL import Image
import fitz

logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".gif"}


def is_image_file(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTENSIONS


def is_supported_file(path: Path) -> bool:
    return is_image_file(path) or path.suffix.lower() == ".pdf"


def expand_inputs(paths: Iterable[Path]) -> list[Path]:
    """Replace each folder in `paths` with its supported files; keep files as given.

    A folder contributes only its top-level image and PDF files, sorted by
    name; other files and subfolders are skipped (logged at DEBUG). Files
    given directly are passed through unchecked so the pipeline can report
    an unsupported one as an error for that file.

    Raises FileNotFoundError for a path that doesn't exist, and ValueError
    if every input was a folder with no supported files. If other inputs
    exist, such a folder only logs a warning.
    """
    expanded: list[Path] = []
    empty_folders: list[Path] = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Input not found: {path}. Check the path and try again.")
        if not path.is_dir():
            expanded.append(path)
            continue

        found = []
        for entry in sorted(path.iterdir()):
            if entry.is_file() and is_supported_file(entry):
                found.append(entry)
            else:
                logger.debug("Skipping %s: not a supported image or PDF file", entry)
        if not found:
            empty_folders.append(path)
        expanded.extend(found)

    if empty_folders and not expanded:
        names = ", ".join(str(folder) for folder in empty_folders)
        raise ValueError(
            f"No image or PDF files found in {names} (folder is empty or has no supported files). "
            "Add .png, .jpg, .tif, .bmp, .gif or .pdf files, or pass the files directly."
        )
    for folder in empty_folders:
        logger.warning("Skipping folder %s: empty or no supported image or PDF files", folder)
    return expanded


def load_image(path: Path) -> Image.Image:
    if not path.is_file():
        raise FileNotFoundError(f"Image file not found: {path}")
    if not is_image_file(path):
        raise ValueError(f"Unsupported image file type: {path}")
    return Image.open(path).convert("RGB")


def rasterize_pdf(path: Path, dpi: int = 200) -> List[Image.Image]:
    if not path.is_file():
        raise FileNotFoundError(f"PDF file not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Unsupported PDF file type: {path}")

    document = fitz.open(path)
    images: List[Image.Image] = []
    matrix = fitz.Matrix(dpi / 72, dpi / 72)

    for page in document:
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        image_bytes = pix.tobytes("png")
        images.append(Image.open(io.BytesIO(image_bytes)).convert("RGB"))

    return images


def load_inputs(paths: Iterable[Path], dpi: int = 200) -> List[tuple[Path, Image.Image]]:
    loaded = []
    for path in paths:
        if is_image_file(path):
            loaded.append((path, load_image(path)))
        elif path.suffix.lower() == ".pdf":
            for index, image in enumerate(rasterize_pdf(path, dpi=dpi), start=1):
                page_path = Path(f"{path.stem}_page_{index}.png")
                loaded.append((page_path, image))
        else:
            raise ValueError(f"Unsupported input file: {path}")
    return loaded
