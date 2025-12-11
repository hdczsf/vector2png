# vector2png Overview

`vector2png` converts Adobe Illustrator (AI) and DXF files to crisp PNGs using a small, testable Python core. Two rendering pipelines are supported for AI (PyMuPDF and pdf2image) and one for DXF (ezdxf + PyMuPDF backend).

## Highlights
- Simple CLI and Python API with option dataclasses for autocomplete.
- Dual AI renderers: PyMuPDF by default, pdf2image as fallback or preference.
- Background handling: transparency first, optional solid background when non-transparent.
- DXF rendering via ezdxf with layout selection, scaling, and background presets.
- MIT licensed; dependencies kept small and optional extras split by feature.

## When to Use
- Quick previews of AI/DXF assets without opening heavyweight design tools.
- Batch conversions in pipelines or CI.
- Testing DXF layouts or AI exports for correctness at specific DPI. 
- 2D vector content only (lines, shapes, text, gradients); 3D objects or heavy effects are not rendered—flatten/project upstream first.
