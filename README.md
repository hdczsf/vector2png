# vector2png

Elegant Python utilities to transform Adobe Illustrator (`.ai`) and AutoCAD DXF (`.dxf`) files into crisp PNG previews. The project focuses on a polished developer experience with both programmatic and CLI workflows.

**[📖 中文文档](README.cn.md)**

## Highlights

- Intuitive functional API (`vector2png.ai_to_png`, `vector2png.dxf_to_png`) plus configurable converter classes
- Dual rendering strategy for AI files (PyMuPDF and pdf2image) with graceful fallback logic
- DXF rendering powered by `ezdxf` + `PyMuPdfBackend`, supporting custom layouts, page sizes, and color policies
- Lightweight CLI for quick conversions directly from the terminal
- Optional extras to keep the base install lean (`pip install vector2png[ai]`, `vector2png[dxf]`)

## Installation

```bash
pip install vector2png           # installs the PyMuPDF core
pip install vector2png[ai]       # adds pdf2image + Pillow for the AI pipeline
pip install vector2png[dxf]      # adds ezdxf for DXF rendering
pip install vector2png[full]     # pulls in every optional dependency
```

> pdf2image requires Poppler. On Windows install `pdftoppm.exe` (e.g., via [OSGeo4W](https://trac.osgeo.org/osgeo4w/)), on macOS use `brew install poppler`, and on Linux install the `poppler-utils` package.

### License Notice

PyMuPDF (MuPDF) ships under the AGPLv3 by default. Because `vector2png` depends on PyMuPDF for both AI and DXF rendering, anyone redistributing or offering services built on this project must comply with the AGPL requirements **or** obtain a commercial MuPDF license from Artifex. MIT licensing only covers the code in this repository and does not waive the obligations imposed by PyMuPDF.

## Quick Start

### Python API

```python
from vector2png import ai_to_png, dxf_to_png, AIOptions, DXFOptions

# AI example
ai_to_png("logo.ai", "logo.png", AIOptions(dpi=200, transparent=True))

# DXF example with custom layout
options = DXFOptions(layout_name="ISO_A1", background="white", color_policy="monochrome")
dxf_to_png("floorplan.dxf", "floorplan.png", options)
```

### CLI

```bash
vector2png ai source.ai output.png --dpi 200 --transparent
vector2png dxf drawing.dxf output.png --layout Layout1 --color monochrome
# Optional DXF helpers:
#   --pdsize 2.5                 # explicit point size to silence ezdxf relative-size notice
#   --normalize-relative-size    # expand MTEXT relative \\H...x markers to absolute sizes
```

Run `vector2png --help` to see all flags and defaults.

## Example Scripts

The `examples/` directory contains simple scripts:

- `examples/ai_basic.py`: reads `examples/files/example.ai` and exports PNG preview.
- `examples/dxf_basic.py`: reads `examples/files/example.dxf` and exports PNG preview.

## Configuration Overview

| Converter | Key options |
| --------- | ----------- |
| AI | `dpi`, `transparent`, `background_color`, `prefer_method`, `fallback` |
| DXF | `dpi`, `background`, `color_policy`, `scale`, `layout_name`, `page_width`, `page_height`, `margins`, `lineweight_scaling`, `max_width`, `max_height`, `pdsize`, `normalize_relative_size` |

Every option is exposed through the corresponding dataclass (`AIOptions`, `DXFOptions`) so IDEs can offer autocomplete and validation.

## Error Handling

All Runtime errors funnel through `ConversionError` (or the more specific `DependencyMissingError`). When an optional dependency is missing, the error message explains which extra to install. The CLI echoes the same error text and exits with a non-zero status code.

 

## Roadmap Ideas

- SVG and PDF conversion support using the same interface
- Batch-processing helpers with concurrency controls
- Richer diagnostic logging (page bounding boxes, render duration)

## Acknowledgements

- [PyMuPDF (MuPDF)](https://pymupdf.readthedocs.io/) for high-quality PDF/AI rendering.
- [pdf2image](https://github.com/Belval/pdf2image) and [Pillow](https://python-pillow.org/) for the alternate AI pipeline.
- [ezdxf](https://ezdxf.mozman.at/) for DXF parsing and drawing helpers.
- The broader open-source community for testing tools and inspiration.

Contributions and suggestions are welcome!
