# API Reference

## AIConverter
- `convert(source, target=None, options=None) -> Path`
  - `source`: path to `.ai`.
  - `target`: path to `.png` (defaults to the source stem).
  - `options`: `AIOptions`.
  - Raises `ConversionError`, `DependencyMissingError`, `FileNotFoundError`.
- `get_info(ai_path) -> dict`: presence, size, PDF-based flag, page count, dimensions.

Usage examples

```python
from vector2png import AIConverter, AIOptions

# Basic conversion at 200 DPI with transparency
AIConverter().convert(
    "examples/files/example.ai",
    "examples/generated/ai_transparent.png",
    AIOptions(dpi=200, transparent=True),
)

# Force PyMuPDF only; if Pillow is missing and a background is set, a dependency error is raised
AIConverter().convert(
    "examples/files/example.ai",
    "examples/generated/ai_pymupdf_only.png",
    AIOptions(prefer_method="pymupdf", fallback=False, background_color=(240, 240, 240)),
)

# Inspect AI metadata (PDF-based flag, page count, dimensions)
info = AIConverter().get_info("examples/files/example.ai")
print(info)
```

## AIOptions
```python
AIOptions(
    dpi=300,
    transparent=False,
    background_color=None,  # (R, G, B) tuple
    prefer_method="auto",   # auto|pymupdf|pdf2image
    fallback=True,
    timeout=30,
)
```

Notes:
- `transparent=True` overrides `background_color`.
- `background_color` applies only when not transparent; both PyMuPDF and pdf2image composite it (Pillow required).
- `prefer_method` controls renderer order; `fallback=False` stops after the first attempt.

Functional API quickstart

```python
from vector2png import ai_to_png, AIOptions

# Default flow (auto priority, 300 DPI)
ai_to_png("examples/files/example.ai", "examples/generated/ai_default.png")

# Force pdf2image only; suitable when Poppler is installed
ai_to_png(
    "examples/files/example.ai",
    "examples/generated/ai_pdf2image_only.png",
    AIOptions(prefer_method="pdf2image", fallback=False, dpi=150),
)
```

## DXFConverter
- `convert(source, target=None, options=None) -> Path`
  - `source`: path to `.dxf`.
  - `target`: path to `.png` (defaults to the source stem).
  - `options`: `DXFOptions`.
  - Raises `ConversionError`, `DependencyMissingError`, `FileNotFoundError`.

Usage examples

```python
from vector2png import DXFConverter, DXFOptions

# Modelspace render in monochrome with thicker lineweights
DXFConverter().convert(
    "examples/files/example.dxf",
    "examples/generated/dxf_monochrome.png",
    DXFOptions(color_policy="monochrome", lineweight_scaling=1.5),
)

# Render a specific layout, fit within 300x300mm while keeping scale
DXFConverter().convert(
    "examples/files/example.dxf",
    "examples/generated/dxf_layout.png",
    DXFOptions(layout_name="Model", max_width=300, max_height=300, background="white"),
)

# Convenience helper to render a single layout
DXFConverter().convert_layout(
    "examples/files/example.dxf",
    layout_name="Model",
    target="examples/generated/dxf_layout_only.png",
)
```

## DXFOptions
```python
DXFOptions(
    dpi=300,
    page_width=0,
    page_height=0,
    margins=20,
    scale=1.0,
    max_width=None,
    max_height=None,
    background="white",     # white|black|default|off
    color_policy="color",   # color|black|white|monochrome
    lineweight_scaling=1.0,
    layout_name=None,
    pdsize=None,
    normalize_relative_size=False,
)
```

Usage tips
- If `layout_name` is missing a `ConversionError` is raised; inspect `doc.layouts.names()` first. The bundled sample DXF only contains `Model`.
- `page_width/page_height` are in millimeters; `max_width/max_height` constrain the page while keeping aspect ratio.
- `background` and `color_policy` control paper/ink combination; `lineweight_scaling` thickens or thins all lineweights.
- `pdsize`<=0 is coerced to 1 to avoid ezdxf relative point size notices; `normalize_relative_size` expands MTEXT relative sizes `\H...x` to absolute values.

Functional API quickstart

```python
from vector2png import dxf_to_png, DXFOptions

# Default render
dxf_to_png("examples/files/example.dxf", "examples/generated/dxf_default.png")

# Render a specific layout in monochrome on an A3 page with 20mm margins
dxf_to_png(
    "examples/files/example.dxf",
    "examples/generated/dxf_a3_layout.png",
    DXFOptions(layout_name="Model", page_width=420, page_height=297, color_policy="monochrome", margins=20),
)
```

## Exceptions
- `ConversionError`: generic conversion failure (missing pages, empty output, invalid layout/empty layout bounding box, invalid page geometry, etc.). The CLI prints a single-line message; no Python traceback is shown.
- `DependencyMissingError`: optional dependency not installed; message includes install hint.

Error handling example

```python
import logging
from vector2png import ai_to_png, ConversionError, DependencyMissingError

logging.basicConfig(level=logging.INFO)

try:
    ai_to_png("examples/files/example.ai", "examples/generated/ai_error_demo.png")
except DependencyMissingError as exc:
    # Ask the user to install pdf2image/Pillow/ezdxf, etc.
    print(f"Missing dependency: {exc}")
except ConversionError as exc:
    print(f"Conversion failed: {exc}")
```

## Logging
Converters are lightweight; enable logging in your app as needed:
```python
import logging
logging.basicConfig(level=logging.INFO)
```
