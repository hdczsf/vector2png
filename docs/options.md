# Options Deep Dive

## AI options and combinations
- `dpi`: scales the rendered output; typical values 144–600.
- `transparent`:
  - `True`: force RGBA PNG, background is transparent; ignores `background_color`.
  - `False`: opaque output; background is white unless `background_color` is set.
- `background_color`:
  - Applies only when `transparent=False`.
  - Works in PyMuPDF and pdf2image paths when Pillow is present.
  - In PyMuPDF with `background_color` but no Pillow, a dependency error is raised.
- `prefer_method`:
  - `auto`: PDF-based AI → PyMuPDF first; otherwise pdf2image first.
  - `pymupdf` | `pdf2image`: force order; `fallback` controls whether the other method is tried on failure.
- `fallback`: if `False`, no secondary renderer is attempted.

Common recipes
- Transparent logo: `transparent=True`, `prefer_method=pymupdf`.
- Solid brand color: `transparent=False`, `background_color=(R,G,B)`.
- Poppler environment available: `prefer_method=pdf2image` for consistency with poppler rendering.

## DXF options
- `dpi`: rasterization DPI; higher yields larger PNGs.
- `background`: white/black/default/off; maps to ezdxf background policies.
- `color_policy`: color/black/white/monochrome.
- `scale`: geometric scale applied to the drawing.
- `layout_name`: choose a layout; defaults to modelspace.
- `page_width` / `page_height`: page size in mm (0 means auto).
- `margins`: mm for all sides.
- `max_width` / `max_height`: clamp page size.
- `pdsize`: POINT entity size; <=0 coerced to 1 to avoid ezdxf relative-size notice.
- `normalize_relative_size`: normalize MTEXT relative height markers to avoid size surprises. 
