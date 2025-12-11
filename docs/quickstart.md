# Quickstart

## Install
Use a virtualenv to avoid system-level packages:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install vector2png
```

Optional extras:
- AI extras: `pip install "vector2png[ai]"` (installs `pdf2image`, `Pillow`).
- DXF extras: `pip install "vector2png[dxf]"`.
- All extras: `pip install "vector2png[full]"`.

## Minimal CLI usage
```bash
# AI to PNG (PyMuPDF preferred)
vector2png ai input.ai output.png

# Transparent background
vector2png ai input.ai output.png --transparent

# Solid background (non-transparent)
vector2png ai input.ai output.png --background 255,0,0

# DXF to PNG
vector2png dxf drawing.dxf output.png --scale 1.5 --background white
```

## Minimal Python usage
```python
from vector2png import AIConverter, AIOptions

opts = AIOptions(dpi=300, transparent=False, background_color=(240, 240, 240))
AIConverter().convert("input.ai", "output.png", opts)
```

## Example files
Sample assets live under `examples/files/` for quick testing. 
