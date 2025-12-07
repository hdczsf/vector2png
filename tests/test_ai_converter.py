"""Unit tests for AI conversion utilities."""

from __future__ import annotations

import types
from pathlib import Path

import pytest

import vector2png.converters.ai as ai_module
from vector2png.converters.ai import AIConverter
from vector2png.exceptions import ConversionError, DependencyMissingError
from vector2png.options import AIOptions


class DummyPixmap:
    """Lightweight Pixmap stub that writes placeholder PNG bytes."""

    def save(self, path: str | Path) -> None:
        Path(path).write_bytes(b"PNG-DATA")


class DummyPage:
    """Fake page object exposing rect metadata and render hook."""

    def __init__(self) -> None:
        self.rect = types.SimpleNamespace(width=100.0, height=50.0)

    def get_pixmap(self, matrix, alpha=False):  # noqa: D401 - short description
        return DummyPixmap()


class DummyDocument:
    """Minimal PyMuPDF document replacement."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.page_count = 1

    def __getitem__(self, index: int) -> DummyPage:
        if index != 0:
            raise IndexError
        return DummyPage()

    def close(self) -> None:  # pragma: no cover - simplified stub
        pass


class DummyFitz(types.SimpleNamespace):
    """Simple fitz module stand-in."""

    def __init__(self) -> None:
        super().__init__(
            open=lambda path: DummyDocument(Path(path)),
            Matrix=lambda _x, _y: (1.0, 1.0),
        )


@pytest.fixture
def fitz_stub(monkeypatch):
    """Inject the fake fitz module during tests."""
    stub = DummyFitz()
    monkeypatch.setattr(ai_module, "fitz", stub)
    return stub


def test_ai_converter_writes_png(tmp_path, fitz_stub):
    ai_file = tmp_path / "demo.ai"
    ai_file.write_bytes(b"%PDF-1.7 demo body")
    png_file = tmp_path / "demo.png"

    converter = AIConverter()
    result = converter.convert(ai_file, png_file, AIOptions(dpi=144))

    assert result == png_file
    assert png_file.read_bytes() == b"PNG-DATA"


def test_ai_converter_reports_missing_pymupdf(tmp_path, monkeypatch):
    ai_file = tmp_path / "vector.ai"
    ai_file.write_bytes(b"Not PDF format")

    monkeypatch.setattr(ai_module, "fitz", None)
    converter = AIConverter()

    with pytest.raises(DependencyMissingError):
        converter.convert(
            ai_file,
            ai_file.with_suffix(".png"),
            AIOptions(prefer_method="pymupdf"),
        )


def test_ai_converter_respects_fallback(monkeypatch, tmp_path, fitz_stub):
    ai_file = tmp_path / "fallback.ai"
    ai_file.write_bytes(b"%PDF-1.4 body")
    png_file = tmp_path / "fallback.png"

    converter = AIConverter()

    calls: list[str] = []

    def fail_pymupdf(self, *_args, **_kwargs):
        calls.append("pymupdf")
        raise RuntimeError("intentional failure")

    def succeed_pdf2image(self, *_args, **_kwargs):
        calls.append("pdf2image")
        png_file.write_bytes(b"PDF2IMAGE")
        return True

    monkeypatch.setattr(AIConverter, "_convert_with_pymupdf", fail_pymupdf)
    monkeypatch.setattr(AIConverter, "_convert_with_pdf2image", succeed_pdf2image)
    monkeypatch.setattr(converter, "pdf2image_available", True)

    result = converter.convert(ai_file, png_file, AIOptions(prefer_method="auto", fallback=True))

    assert result == png_file
    assert calls == ["pymupdf", "pdf2image"]
    assert png_file.read_bytes() == b"PDF2IMAGE"


def test_ai_converter_raises_when_pdf2image_unavailable(tmp_path, fitz_stub):
    ai_file = tmp_path / "no_pdf2image.ai"
    ai_file.write_bytes(b"plain content")
    converter = AIConverter()
    converter.pdf2image_available = False

    with pytest.raises(ConversionError):
        converter.convert(
            ai_file,
            ai_file.with_suffix(".png"),
            AIOptions(prefer_method="pdf2image", fallback=False),
        )
