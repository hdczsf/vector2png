# Architecture

## Modules
- `vector2png/converters/ai.py`: AI conversion logic, method resolution, PyMuPDF and pdf2image pipelines, background handling.
- `vector2png/converters/dxf.py`: DXF conversion via ezdxf + PyMuPDF backend, layout selection, sizing, and scaling.
- `vector2png/options.py`: dataclasses `AIOptions` and `DXFOptions`.
- `vector2png/cli.py`: CLI argument parsing and converter wiring.
- `vector2png/utils.py`: helpers for paths, optional imports, and small utilities.

## AI pipeline
1. Detect PDF-based AI to decide method order.
2. Render with chosen method:
   - PyMuPDF: render page to pixmap; if non-transparent background is requested, composite with Pillow.
   - pdf2image: use Poppler; if non-transparent background is requested, composite with Pillow.
3. Fallback to the secondary method if enabled.

## DXF pipeline
1. Parse DXF via ezdxf.
2. Select layout (default modelspace) and build rendering config (background, color policy, scaling, page geometry).
3. Render through ezdxf PyMuPDF backend to PNG bytes.

## Extension points
- Add new converters alongside AI/DXF with their own options dataclasses.
- Extend AI method resolution with additional renderers.
- Introduce batch helpers or additional formats (SVG/PDF) reusing the same option patterns.

## Design considerations
- Optional dependencies are isolated and signaled via `DependencyMissingError`.
- Background handling is explicit to avoid silent white fills when a color was requested.
- Dataclasses keep the API discoverable and IDE-friendly. 
- Pipelines are 2D page renderers (PyMuPDF/Poppler + ezdxf drawing); no 3D rasterization or effects. 
