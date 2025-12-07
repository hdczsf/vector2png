"""Command line interface for vector2png."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Sequence

from . import AIConverter, AIOptions, DXFConverter, DXFOptions, __version__
from .exceptions import ConversionError, DependencyMissingError


def parse_rgb(value: str | None):
    """Parse an ``R,G,B`` string into a tuple."""
    if value is None:
        return None
    parts = value.split(",")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Color must look like '255,255,255'")
    try:
        return tuple(max(0, min(255, int(p.strip()))) for p in parts)
    except ValueError as exc:  # pragma: no cover - defensive
        raise argparse.ArgumentTypeError("Color values must be integers") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert vector graphics to PNG")
    parser.add_argument("--version", action="version", version=f"vector2png {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    ai_parser = subparsers.add_parser("ai", help="Convert Adobe Illustrator files")
    ai_parser.add_argument("source", type=Path)
    ai_parser.add_argument("target", type=Path, nargs="?")
    ai_parser.add_argument("--dpi", type=int, default=300)
    ai_parser.add_argument("--transparent", action="store_true")
    ai_parser.add_argument("--background", type=parse_rgb, default=None)
    ai_parser.add_argument(
        "--prefer",
        choices=["auto", "pymupdf", "pdf2image"],
        default="auto",
        help="Preferred rendering method",
    )
    ai_parser.add_argument("--no-fallback", dest="fallback", action="store_false")
    ai_parser.set_defaults(fallback=True)

    dxf_parser = subparsers.add_parser("dxf", help="Convert DXF drawings")
    dxf_parser.add_argument("source", type=Path)
    dxf_parser.add_argument("target", type=Path, nargs="?")
    dxf_parser.add_argument("--dpi", type=int, default=300)
    dxf_parser.add_argument("--background", choices=["white", "black", "default", "off"], default="white")
    dxf_parser.add_argument(
        "--color",
        choices=["color", "black", "white", "monochrome"],
        default="color",
    )
    dxf_parser.add_argument("--scale", type=float, default=1.0)
    dxf_parser.add_argument("--layout", dest="layout_name")
    dxf_parser.add_argument("--page-width", type=float, default=0)
    dxf_parser.add_argument("--page-height", type=float, default=0)
    dxf_parser.add_argument("--margins", type=float, default=20)
    dxf_parser.add_argument("--lineweight", type=float, default=1.0, help="Lineweight scaling factor")
    dxf_parser.add_argument("--max-width", type=float)
    dxf_parser.add_argument("--max-height", type=float)
    dxf_parser.add_argument(
        "--pdsize",
        type=float,
        help="POINT entity size; values <=0 will be set to 1 to avoid ezdxf relative point size warning",
    )
    dxf_parser.add_argument(
        "--normalize-relative-size",
        action="store_true",
        help="Normalize MTEXT relative height markers (\\H...x) to absolute sizes to avoid ezdxf notice",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO)

    try:
        if args.command == "ai":
            options = AIOptions(
                dpi=args.dpi,
                transparent=args.transparent,
                background_color=args.background,
                prefer_method=args.prefer,
                fallback=args.fallback,
            )
            AIConverter().convert(args.source, target=args.target, options=options)
        elif args.command == "dxf":
            options = DXFOptions(
                dpi=args.dpi,
                background=args.background,
                color_policy=args.color,
                scale=args.scale,
                layout_name=args.layout_name,
                page_width=args.page_width,
                page_height=args.page_height,
                margins=args.margins,
                lineweight_scaling=args.lineweight,
                max_width=args.max_width,
                max_height=args.max_height,
                pdsize=args.pdsize,
                normalize_relative_size=args.normalize_relative_size,
            )
            DXFConverter().convert(args.source, target=args.target, options=options)
    except (ConversionError, DependencyMissingError, FileNotFoundError) as exc:
        logging.error("%s", exc)
        return 1

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
