"""Tests for the backend registry and the CLI's use of it (S1.1.2)."""

import tomllib
from pathlib import Path

import pytest

from ocr_pipeline import backend, cli
from ocr_pipeline.backend import OCRBackend, get_backend
from ocr_pipeline.models import Line

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class FakeBackend(OCRBackend):
    def recognize(self, image_bytes: bytes) -> list[Line]:
        return [Line(text="fake", confidence=1.0)]


def test_get_backend_returns_registered_backend(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(backend, "BACKENDS", {"fake": FakeBackend})

    assert isinstance(get_backend("fake"), FakeBackend)


def test_unknown_backend_error_lists_available_names(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(backend, "BACKENDS", {"fake": FakeBackend, "other": FakeBackend})

    with pytest.raises(ValueError) as error:
        get_backend("missing")

    message = str(error.value)
    assert "missing" in message
    assert "fake" in message
    assert "other" in message


def test_empty_registry_says_no_backend_installed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(backend, "BACKENDS", {})

    with pytest.raises(ValueError, match="(?i)no OCR backend installed"):
        get_backend("anything")


def test_cli_reports_missing_backend_without_stack_trace(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    monkeypatch.setattr(backend, "BACKENDS", {})
    monkeypatch.setattr(
        "sys.argv", ["ocr-pipeline", str(tmp_path / "a.png"), "--output", str(tmp_path / "out.json")]
    )

    with pytest.raises(SystemExit) as exit_info:
        cli.main()

    stderr = capsys.readouterr().err
    assert exit_info.value.code != 0
    assert "no ocr backend installed" in stderr.lower()
    assert "Traceback" not in stderr


def test_baidu_backend_and_requests_are_gone() -> None:
    assert not hasattr(backend, "BaiduUnlimitedOCRBackend")

    pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = " ".join(pyproject["project"]["dependencies"]).lower()
    assert "requests" not in dependencies

    env_example = (PROJECT_ROOT / ".env.example").read_text(encoding="utf-8")
    assert "BAIDU" not in env_example
