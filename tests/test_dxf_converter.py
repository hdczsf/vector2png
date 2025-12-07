"""Unit tests for the DXF converter."""

from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest

from vector2png.converters.dxf import DXFConverter
from vector2png.exceptions import ConversionError
from vector2png.options import DXFOptions


class DummyLayout:
    """Placeholder layout object."""

    def __init__(self, name: str) -> None:
        self.name = name


class DummyLayouts:
    """Lightweight container mimicking ezdxf layouts."""

    def __init__(self) -> None:
        self._names = {"Model", "Layout1"}

    def __contains__(self, name: str) -> bool:
        return name in self._names

    def names(self):  # noqa: D401 - simple pass-through
        return list(self._names)

    def get(self, name: str) -> DummyLayout:
        return DummyLayout(name)


class DummyDoc:
    """Fake ezdxf document exposing modelspace and layouts."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.layouts = DummyLayouts()

    def modelspace(self) -> DummyLayout:
        return DummyLayout("Model")


def register_dxf_stubs(monkeypatch):
    """Register DXF-related stub modules inside sys.modules."""

    ezdxf_mod = types.ModuleType("ezdxf")
    ezdxf_mod.readfile = lambda path: DummyDoc(Path(path))

    addons_pkg = types.ModuleType("ezdxf.addons")
    addons_pkg.__path__ = []

    drawing_pkg = types.ModuleType("ezdxf.addons.drawing")
    drawing_pkg.__path__ = []

    class DummyRenderContext:
        def __init__(self, _doc):
            pass

    class DummyFrontend:
        def __init__(self, _ctx, _backend, config=None):
            self.config = config

        def draw_layout(self, _layout):
            return None

    drawing_pkg.RenderContext = DummyRenderContext
    drawing_pkg.Frontend = DummyFrontend

    layout_mod = types.ModuleType("ezdxf.addons.drawing.layout")
    layout_mod.__path__ = []

    class DummyMargins:
        def __init__(self, value: float) -> None:
            self.value = value

        @classmethod
        def all(cls, value: float):
            return cls(value)

    class DummyUnits:
        mm = "mm"

    class DummyPage:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    class DummySettings:
        def __init__(self, scale: float, fit_page: bool) -> None:
            self.scale = scale
            self.fit_page = fit_page

    layout_mod.Margins = DummyMargins
    layout_mod.Units = DummyUnits
    layout_mod.Page = DummyPage
    layout_mod.Settings = DummySettings

    config_mod = types.ModuleType("ezdxf.addons.drawing.config")
    config_mod.__path__ = []

    class DummyPolicy:
        def __init__(self, name: str) -> None:
            self.name = name

    class DummyConfiguration:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def with_changes(self, **changes):
            data = dict(self.kwargs)
            data.update(changes)
            return DummyConfiguration(**data)

    config_mod.Configuration = DummyConfiguration
    config_mod.BackgroundPolicy = types.SimpleNamespace(
        WHITE=DummyPolicy("white"),
        BLACK=DummyPolicy("black"),
        DEFAULT=DummyPolicy("default"),
        OFF=DummyPolicy("off"),
    )
    config_mod.ColorPolicy = types.SimpleNamespace(
        COLOR=DummyPolicy("color"),
        BLACK=DummyPolicy("black"),
        WHITE=DummyPolicy("white"),
        MONOCHROME=DummyPolicy("mono"),
    )

    pymupdf_mod = types.ModuleType("ezdxf.addons.drawing.pymupdf")

    class DummyBackend:
        def get_pixmap_bytes(self, _page, fmt: str, settings, dpi: int):  # noqa: D401
            payload = f"fmt={fmt},dpi={dpi},scale={settings.scale}".encode()
            return payload

    pymupdf_mod.PyMuPdfBackend = DummyBackend

    modules = {
        "ezdxf": ezdxf_mod,
        "ezdxf.addons": addons_pkg,
        "ezdxf.addons.drawing": drawing_pkg,
        "ezdxf.addons.drawing.layout": layout_mod,
        "ezdxf.addons.drawing.config": config_mod,
        "ezdxf.addons.drawing.pymupdf": pymupdf_mod,
    }

    for name, module in modules.items():
        monkeypatch.setitem(sys.modules, name, module)

    addons_pkg.drawing = drawing_pkg

    return modules


def test_dxf_converter_produces_png(tmp_path, monkeypatch):
    register_dxf_stubs(monkeypatch)
    dxf_file = tmp_path / "mock.dxf"
    dxf_file.write_text("0\nSECTION\n")
    png_file = tmp_path / "mock.png"

    converter = DXFConverter()
    result = converter.convert(dxf_file, png_file, DXFOptions(dpi=150, scale=2.0))

    assert result == png_file
    assert png_file.read_bytes() == b"fmt=png,dpi=150,scale=2.0"


def test_dxf_converter_reports_missing_layout(tmp_path, monkeypatch):
    register_dxf_stubs(monkeypatch)
    dxf_file = tmp_path / "layout.dxf"
    dxf_file.write_text("0\nSECTION\n")

    converter = DXFConverter()

    with pytest.raises(ConversionError):
        converter.convert(dxf_file, dxf_file.with_suffix(".png"), DXFOptions(layout_name="UNKNOWN"))
