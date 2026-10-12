"""Tests for the sample document generator in scripts/make_samples.py (S2.1.1)."""

import re
from pathlib import Path

import fitz
from fakes import FakeBackend
from make_samples import generate_samples
from PIL import Image

from ocr_pipeline.pipeline import run_pipeline

EXPECTED_FILES = [
    "form.png",
    "form.txt",
    "multipage.pdf",
    "multipage_p1.txt",
    "multipage_p2.txt",
    "multipage_p3.txt",
    "receipt.png",
    "receipt.txt",
]


def test_writes_receipt_form_and_three_page_pdf_with_known_text(
    tmp_path: Path,
) -> None:
    written = generate_samples(tmp_path)

    assert sorted(path.name for path in written) == EXPECTED_FILES
    for name in ["receipt.png", "form.png"]:
        with Image.open(tmp_path / name) as image:
            # Not blank: the rendered text leaves some dark pixels.
            assert image.convert("L").getextrema()[0] < 100
    with fitz.open(tmp_path / "multipage.pdf") as pdf:
        assert pdf.page_count == 3
    for name in EXPECTED_FILES:
        if name.endswith(".txt"):
            assert (tmp_path / name).read_text(encoding="utf-8").strip()


def test_two_runs_give_byte_identical_files(tmp_path: Path) -> None:
    first = generate_samples(tmp_path / "first")
    second = generate_samples(tmp_path / "second")

    assert [path.name for path in first] == [path.name for path in second]
    for first_path, second_path in zip(first, second, strict=True):
        assert first_path.read_bytes() == second_path.read_bytes(), first_path.name


def test_known_text_has_no_real_personal_data(tmp_path: Path) -> None:
    written = generate_samples(tmp_path)
    text = "\n".join(
        path.read_text(encoding="utf-8") for path in written if path.suffix == ".txt"
    )

    # Emails only on the reserved example domains (RFC 2606).
    for email in re.findall(r"[\w.+-]+@([\w-]+(?:\.[\w-]+)+)", text):
        assert email in {"example.com", "example.org", "example.net"}, email
    # Phone numbers only in the 555-0100..0199 range reserved for fiction.
    for phone in re.findall(r"\d{3}[-. ]\d{4}", text):
        assert re.fullmatch(r"555[-. ]01\d\d", phone), phone
    # No long digit runs that could be card, account or ID numbers.
    assert not re.search(r"\d{9,}", text.replace(" ", "").replace("-", ""))


def test_creates_missing_output_folder_and_overwrites_old_files(
    tmp_path: Path,
) -> None:
    out_dir = tmp_path / "does" / "not" / "exist"

    generate_samples(out_dir)
    (out_dir / "receipt.txt").write_text("stale", encoding="utf-8")
    generate_samples(out_dir)

    assert (out_dir / "receipt.txt").read_text(encoding="utf-8") != "stale"


def test_samples_folder_runs_through_the_pipeline_as_five_pages(
    tmp_path: Path,
) -> None:
    generate_samples(tmp_path)

    results = run_pipeline([tmp_path], FakeBackend())

    # The .txt files are skipped; receipt + form + 3 PDF pages remain.
    assert [(Path(r.source_file).name, r.page) for r in results] == [
        ("form.png", 1),
        ("multipage.pdf", 1),
        ("multipage.pdf", 2),
        ("multipage.pdf", 3),
        ("receipt.png", 1),
    ]
    assert all(result.error is None for result in results)
