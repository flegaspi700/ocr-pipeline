import fitz
from pathlib import Path
from PIL import Image

from ocr_pipeline.io import is_image_file, load_image, rasterize_pdf
from ocr_pipeline.preprocess import binarize, resize_to_fit


def test_is_image_file(tmp_path: Path) -> None:
    assert is_image_file(tmp_path / "document.png")
    assert is_image_file(tmp_path / "photo.JPG")
    assert not is_image_file(tmp_path / "document.pdf")


def test_load_image_and_rasterize_pdf(tmp_path: Path) -> None:
    image_path = tmp_path / "sample.png"
    Image.new("RGB", (100, 100), color="white").save(image_path)

    loaded = load_image(image_path)
    assert loaded.size == (100, 100)
    assert loaded.mode == "RGB"

    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    doc.new_page(width=200, height=100)
    doc.save(str(pdf_path))
    doc.close()

    pages = rasterize_pdf(pdf_path, dpi=72)
    assert len(pages) == 1
    assert pages[0].mode == "RGB"


def test_binarize_and_resize() -> None:
    image = Image.new("RGB", (4000, 3000), color="gray")
    resized = resize_to_fit(image, max_width=1000, max_height=1000)
    assert resized.width <= 1000
    assert resized.height <= 1000

    binary = binarize(image, threshold=128)
    assert binary.mode == "L"
    assert set(binary.getdata()).issubset({0, 255})
