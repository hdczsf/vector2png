# API Reference

## AIConverter
- `convert(source, target=None, options=None) -> Path`
  - `source`: path to `.ai`.
  - `target`: path to `.png` (defaults to `source` stem).
  - `options`: `AIOptions`.
  - Raises `ConversionError`, `DependencyMissingError`, `FileNotFoundError`.
- `get_info(ai_path) -> dict`: presence, size, PDF-based flag, page count, dimensions.

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
- Transparency overrides background color.
- Background color applies only when not transparent; both PyMuPDF and pdf2image honor it when Pillow is installed.
- `prefer_method` selects renderer order; `fallback=False` stops after the first choice.

## DXFConverter
- `convert(source, target=None, options=None) -> Path`
  - `source`: path to `.dxf`.
  - `target`: path to `.png` (defaults to `source` stem).
  - `options`: `DXFOptions`.
  - Raises `ConversionError`, `DependencyMissingError`, `FileNotFoundError`.

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

## Exceptions
- `ConversionError`: generic conversion failure (missing pages, empty output, invalid layout, etc.).
- `DependencyMissingError`: optional dependency not installed; message includes install hint.

## Logging
Converters are lightweight; enable logging in your app as needed:
```python
import logging
logging.basicConfig(level=logging.INFO)
``` 
