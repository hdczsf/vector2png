# CLI Guide

Binary: `vector2png`

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
