# CLI Guide

Binary: `vector2png`

## Quick examples

AI conversions

```bash
# Basic preview at 200 DPI
vector2png ai examples/files/example.ai examples/generated/ai_basic.png --dpi 200

# Transparent PNG (alpha channel), keeps background ignored
vector2png ai examples/files/example.ai examples/generated/ai_transparent.png --transparent

# Composite a light-gray background (requires Pillow when using pdf2image or PyMuPDF alpha output)
vector2png ai examples/files/example.ai examples/generated/ai_background.png --background 240,240,240

# Force PyMuPDF only and fail fast (no fallback to pdf2image)
vector2png ai examples/files/example.ai examples/generated/ai_pymupdf_only.png --prefer pymupdf --no-fallback
```

DXF conversions

```bash
# Default modelspace render, monochrome on white background
vector2png dxf examples/files/example.dxf examples/generated/dxf_basic.png --color monochrome --background white

# Render a specific layout with custom scale and A3 page size (mm)
vector2png dxf examples/files/example.dxf examples/generated/dxf_layout.png --layout Model --scale 0.8 --page-width 420 --page-height 297

# Fit within a bounding box while keeping scale, and thicken lineweights
vector2png dxf examples/files/example.dxf examples/generated/dxf_fit.png --max-width 300 --max-height 300 --lineweight 1.5

# Normalize relative MTEXT sizes and set explicit point size to silence ezdxf notices
vector2png dxf examples/files/example.dxf examples/generated/dxf_textsize.png --normalize-relative-size --pdsize 2.5
```

> Notes: pdf2image+Poppler (and Pillow for backgrounds) are required when preferring pdf2image; ezdxf is required for all DXF commands. Replace `--layout` with a layout that exists in your DXF (the bundled sample only has `Model`). Layouts without drawable entities will fail to render; switch to a layout containing geometry.

## AI command
```
vector2png ai <source.ai> [target.png]
  --dpi <int>            Render DPI (default 300)
  --transparent          Output RGBA PNG with transparency
  --background R,G,B     Solid background color (applies only when not transparent)
  --prefer {auto,pymupdf,pdf2image}
                         Preferred renderer (default auto)
  --no-fallback          Disable trying the secondary renderer on failure
```

Behavior notes
- Transparency has priority: `--transparent` ignores any `--background`.
- `--background` applies only when not transparent. PyMuPDF and pdf2image both honor it when Pillow is available.
- `--prefer auto`: if the AI file is PDF-based, try PyMuPDF then pdf2image; otherwise try pdf2image then PyMuPDF.
- If `--prefer pymupdf` is used without Pillow and `--background` is set, a dependency error is raised.
- Errors are printed as single-line messages (no traceback); empty/invalid layouts will report a clear `ConversionError`.

## DXF command
```
vector2png dxf <source.dxf> [target.png]
  --dpi <int>            Render DPI (default 300)
  --background {white,black,default,off}
  --color {color,black,white,monochrome}
  --scale <float>        Drawing scale (default 1.0)
  --layout <name>        Layout to render (default modelspace)
  --page-width <float>   Page width (mm)
  --page-height <float>  Page height (mm)
  --margins <float>      Margins (mm, all sides)
  --lineweight <float>   Lineweight scaling factor
  --max-width <float>    Maximum width (mm)
  --max-height <float>   Maximum height (mm)
  --pdsize <float>       POINT entity size (<=0 coerced to 1 to avoid ezdxf warnings)
  --normalize-relative-size
                         Normalize MTEXT relative heights to absolute sizes
```

Exit codes
- `0` on success.
- `1` on conversion or dependency errors (printed to stderr). 
