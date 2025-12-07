"""DXF to PNG conversion powered by ezdxf and PyMuPDF."""

from __future__ import annotations

import logging
import re
from dataclasses import replace
from pathlib import Path
from typing import Dict, Tuple

from ..exceptions import ConversionError
from ..options import DXFOptions
from ..utils import ensure_input_path, ensure_output_path, optional_import
from .base import BaseConverter


class DXFConverter(BaseConverter[DXFOptions]):
    """Convert DXF drawings into PNG previews."""

    # 捕获 \H<倍数>x 或 \H<倍数>x;（大小写均可），用于相对字号。
    _RELATIVE_SIZE_PATTERN = re.compile(r"\\H([0-9]*\\.?[0-9]+)x;?", re.IGNORECASE)

    def __init__(self) -> None:
        super().__init__()
        self._config_cache: Dict[Tuple, object] = {}

    def convert(
        self,
        source: str | Path,
        target: str | Path | None = None,
        options: DXFOptions | None = None,
    ) -> Path:
        opts = options or DXFOptions()
        dxf_path = ensure_input_path(source)
        png_path = ensure_output_path(dxf_path, target)

        ezdxf = optional_import("ezdxf")
        drawing = optional_import("ezdxf.addons.drawing", package="ezdxf")
        layout_module = optional_import("ezdxf.addons.drawing.layout", package="ezdxf")
        config_module = optional_import("ezdxf.addons.drawing.config", package="ezdxf")
        pymupdf_backend = optional_import("ezdxf.addons.drawing.pymupdf", package="ezdxf")
        Frontend = drawing.Frontend
        RenderContext = drawing.RenderContext

        doc = ezdxf.readfile(str(dxf_path))
        if opts.normalize_relative_size:
            self._normalize_relative_point_sizes(doc)

        if opts.layout_name:
            if opts.layout_name not in doc.layouts:
                available = ", ".join(doc.layouts.names())
                raise ConversionError(f"Layout '{opts.layout_name}' not found. Available: {available}")
            drawing_source = doc.layouts.get(opts.layout_name)
        else:
            drawing_source = doc.modelspace()

        cfg = self._get_config(config_module, opts)
        # ezdxf frontend does not support relative pdsize (<=0 means relative) and logs an INFO.
        # Set an explicit positive value ahead of time to suppress the message, preferring CLI option
        # and falling back to DXF header $PDSIZE.
        pdsize = opts.pdsize if opts.pdsize is not None else (doc.header.get("$PDSIZE", 0) or 0)
        if pdsize <= 0:
            pdsize = 1.0
        cfg = cfg.with_changes(pdsize=pdsize)

        context = RenderContext(doc)
        backend = pymupdf_backend.PyMuPdfBackend()
        frontend = Frontend(context, backend, config=cfg)
        frontend.draw_layout(drawing_source)

        margins = (
            layout_module.Margins.all(opts.margins)
            if isinstance(opts.margins, (int, float))
            else opts.margins
        )

        page_kwargs = {
            "width": opts.page_width,
            "height": opts.page_height,
            "units": layout_module.Units.mm,
            "margins": margins,
        }
        if opts.max_width is not None:
            page_kwargs["max_width"] = opts.max_width
        if opts.max_height is not None:
            page_kwargs["max_height"] = opts.max_height

        page = layout_module.Page(**page_kwargs)
        settings = layout_module.Settings(scale=opts.scale, fit_page=True)
        png_bytes = backend.get_pixmap_bytes(page, fmt="png", settings=settings, dpi=opts.dpi)
        png_path.write_bytes(png_bytes)
        return png_path

    def convert_layout(
        self,
        source: str | Path,
        layout_name: str,
        target: str | Path | None = None,
        options: DXFOptions | None = None,
    ) -> Path:
        """Convert a specific layout to PNG."""
        opts = options or DXFOptions()
        patched = replace(opts, layout_name=layout_name)
        return self.convert(source, target=target, options=patched)

    def _get_config(self, config_module, opts: DXFOptions):
        key = (opts.background, opts.color_policy, opts.lineweight_scaling)
        cached = self._config_cache.get(key)
        if cached is not None:
            return cached

        cfg = config_module.Configuration()
        background_policy = {
            "white": config_module.BackgroundPolicy.WHITE,
            "black": config_module.BackgroundPolicy.BLACK,
            "off": config_module.BackgroundPolicy.OFF,
        }.get(opts.background, config_module.BackgroundPolicy.DEFAULT)
        cfg = cfg.with_changes(background_policy=background_policy)

        color_policy = {
            "black": config_module.ColorPolicy.BLACK,
            "white": config_module.ColorPolicy.WHITE,
            "monochrome": config_module.ColorPolicy.MONOCHROME,
        }.get(opts.color_policy, config_module.ColorPolicy.COLOR)
        cfg = cfg.with_changes(color_policy=color_policy)
        cfg = cfg.with_changes(lineweight_scaling=opts.lineweight_scaling)
        self._config_cache[key] = cfg
        return cfg

    def _normalize_relative_point_sizes(self, doc) -> None:
        """Replace MTEXT relative height markers with absolute values to avoid ezdxf warnings."""

        default_size = doc.header.get("$TEXTSIZE", 2.5) or 2.5
        updated = 0

        # Iterate all entities (modelspace, paperspace, block defs) to catch every MTEXT.
        for entity in doc.entitydb.values():
            if entity.dxftype() != "MTEXT":
                continue

            base_size = (
                entity.dxf.char_height
                or getattr(entity.dxf, "height", 0)
                or default_size
            )
            base_size = base_size or default_size

            original = entity.text

            def replace_match(match: re.Match) -> str:
                factor = float(match.group(1))
                absolute = base_size * factor
                return f"\\H{absolute:g};"

            replaced = self._RELATIVE_SIZE_PATTERN.sub(replace_match, original)
            if replaced != original:
                entity.text = replaced
                updated += 1

        if updated:
            logging.debug("Normalized relative text height for %d MTEXT entities", updated)
