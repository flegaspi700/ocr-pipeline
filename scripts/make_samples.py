"""Generate synthetic sample documents with known text (S2.1.1).

Writes a receipt and a form as PNG, and a 3-page PDF, each next to a `.txt`
file holding the exact text drawn on it (one `.txt` per PDF page). They give
the OCR pipeline real input whose correct answer is known, for judging the
local engine in Phase 2. A standalone helper: it doesn't use the
`ocr_pipeline` package, only Pillow and PyMuPDF.

All content is fixed and fictional (example.com emails, 555-01xx phone
numbers), and nothing depends on the clock or randomness, so every run
writes byte-identical files.

Run from the repo root: `python scripts/make_samples.py` (writes to `samples/`).
"""

import io
import logging
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

RECEIPT_LINES = [
    "EXAMPLE CORNER SHOP",
    "12 Sample Street, Testville",
    "Date: 2026-01-15  Time: 10:42",
    "",
    "Bread            2 x 2.50    5.00",
    "Milk 1L          1 x 1.20    1.20",
    "Apples 1kg       1 x 3.40    3.40",
    "Coffee beans     1 x 8.90    8.90",
    "",
    "Subtotal                    18.50",
    "Tax 10%                      1.85",
    "TOTAL                       20.35",
    "",
    "Paid by card",
    "Thank you for shopping!",
]

FORM_LINES = [
    "MEMBERSHIP APPLICATION FORM",
    "",
    "Full name: Jane Sample",
    "Date of birth: 1990-04-01",
    "Address: 34 Placeholder Road, Testville",
    "Email: jane.sample@example.com",
    "Phone: 555-0142",
    "Membership type: Standard",
    "Start date: 2026-02-01",
    "",
    "Signature: J. Sample",
]

MULTIPAGE_PAGES = [
    [
        "QUARTERLY NOTES - PAGE 1",
        "",
        "This document is a generated sample.",
        "It has three pages of plain printed text.",
        "Each page has its own known text file.",
    ],
    [
        "QUARTERLY NOTES - PAGE 2",
        "",
        "Item          Count    Price",
        "Widgets          40     2.75",
        "Gadgets          15    12.00",
        "Gizmos            8    31.50",
    ],
    [
        "QUARTERLY NOTES - PAGE 3",
        "",
        "Summary: all figures above are invented.",
        "Contact: notes@example.org",
        "End of document.",
    ],
]

# Pillow's bundled FreeType font, so the script works on any machine without
# a font file. 28 px is a guess at "normal printed text" for these sizes.
FONT = ImageFont.load_default(size=28)
LINE_HEIGHT_PX = 40
MARGIN_PX = 50

# A4 at 150 DPI, so a PDF page rasterized at the CLI's default 200 DPI isn't
# upscaled much from the drawn pixels.
A4_PX = (1240, 1754)
A4_PT = (595, 842)


def render_page(lines: list[str], size: tuple[int, int]) -> Image.Image:
    """Draw `lines` in black on a white grayscale image of `size` (w, h) px."""
    image = Image.new("L", size, color=255)
    draw = ImageDraw.Draw(image)
    for index, line in enumerate(lines):
        draw.text((MARGIN_PX, MARGIN_PX + index * LINE_HEIGHT_PX), line, font=FONT)
    return image


def write_known_text(lines: list[str], path: Path) -> Path:
    """Write the lines as UTF-8 text, one per line, ending with a newline."""
    # newline="\n" keeps the bytes the same on Windows and elsewhere.
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


def write_pdf(pages: list[list[str]], path: Path) -> None:
    """Write one A4 PDF page per entry in `pages`, each a scanned-like image."""
    with fitz.open() as pdf:
        for lines in pages:
            buffer = io.BytesIO()
            render_page(lines, A4_PX).save(buffer, format="PNG")
            page = pdf.new_page(width=A4_PT[0], height=A4_PT[1])
            page.insert_image(page.rect, stream=buffer.getvalue())
        # A new PDF gets a random file ID unless told not to; the dates in the
        # metadata are left empty. Both keep the output byte-identical.
        pdf.set_metadata({})
        pdf.save(path, garbage=4, deflate=True, no_new_id=True)


def generate_samples(out_dir: Path) -> list[Path]:
    """Write every sample and its known text into `out_dir`.

    Creates `out_dir` if needed and overwrites existing samples. Returns the
    written paths, sorted by name.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []

    for name, lines, size in [
        ("receipt", RECEIPT_LINES, (700, 700)),
        ("form", FORM_LINES, (900, 560)),
    ]:
        image_path = out_dir / f"{name}.png"
        render_page(lines, size).save(image_path)
        written += [image_path, write_known_text(lines, out_dir / f"{name}.txt")]

    pdf_path = out_dir / "multipage.pdf"
    write_pdf(MULTIPAGE_PAGES, pdf_path)
    written.append(pdf_path)
    for number, lines in enumerate(MULTIPAGE_PAGES, start=1):
        written.append(write_known_text(lines, out_dir / f"multipage_p{number}.txt"))

    return sorted(written, key=lambda path: path.name)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    out_dir = Path(__file__).resolve().parent.parent / "samples"
    written = generate_samples(out_dir)
    logger.info("Wrote %d sample files to %s", len(written), out_dir)


if __name__ == "__main__":
    main()
