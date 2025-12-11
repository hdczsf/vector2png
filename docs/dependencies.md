# Dependencies

## Required
- Python >= 3.9
- PyMuPDF (`pymupdf`): base renderer for AI; required for DXF pipeline via ezdxf backend.

## Optional extras
- AI extras (`vector2png[ai]`):
  - `pdf2image`: alternate AI renderer (requires Poppler binaries on your system).
  - `Pillow`: background compositing for AI when not transparent (both PyMuPDF and pdf2image paths).
- DXF extras (`vector2png[dxf]`):
  - `ezdxf`: DXF parsing and rendering helpers.

## System notes
- Poppler: needed only if using pdf2image. Install via your OS package manager and ensure `pdftoppm` is on PATH.
- PyMuPDF wheels: provided for common platforms; ensure your Python version matches.
- Pillow: needed for background compositing when `background_color` is set and `transparent=False`.

## Installation examples
```bash
# Base (PyMuPDF only)
pip install vector2png

# AI stack
pip install "vector2png[ai]"

# DXF stack
pip install "vector2png[dxf]"

# Everything
pip install "vector2png[full]"
```

## Missing dependency behavior
- Missing optional deps raise `DependencyMissingError` with an install hint.
- PyMuPDF + `background_color` without Pillow: error to avoid silent white backgrounds. 
