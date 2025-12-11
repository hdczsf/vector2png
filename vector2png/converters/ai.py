"""AI to PNG conversion powered by PyMuPDF and pdf2image."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

try:  # pragma: no cover - import guard for test environments
    import fitz  # PyMuPDF
except ModuleNotFoundError:  # pragma: no cover - fall back to dependency error
    fitz = None  # type: ignore[assignment]

from ..exceptions import ConversionError, DependencyMissingError
from ..options import AIOptions
from ..utils import ensure_input_path, ensure_output_path, optional_import
from .base import BaseConverter


class AIConverter(BaseConverter[AIOptions]):
    """Convert Adobe Illustrator (AI) files to PNG images."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.debug("Initializing AIConverter")
        self.pdf2image_available = self._check_pdf2image()

    def convert(
        self,
        source: str | Path,
        target: str | Path | None = None,
        options: AIOptions | None = None,
    ) -> Path:
        opts = options or AIOptions()
        ai_path = ensure_input_path(source)
        png_path = ensure_output_path(ai_path, target)

        methods = self._resolve_methods(ai_path, opts)
        last_error: Optional[Exception] = None

        for method in methods:
            try:
                if method == "pymupdf" and self._convert_with_pymupdf(ai_path, png_path, opts):
                    return png_path
                if method == "pdf2image" and self._convert_with_pdf2image(ai_path, png_path, opts):
                    return png_path
            except DependencyMissingError as exc:  # pragma: no cover - runtime specific
                last_error = exc
                self.logger.debug("Dependency missing when using %s: %s", method, exc)
                if not opts.fallback:
                    raise
            except ConversionError as exc:  # pragma: no cover - integration heavy
                last_error = exc
                self.logger.debug("Conversion error via %s: %s", method, exc)
                if not opts.fallback:
                    raise
            except Exception as exc:  # pragma: no cover - defensive
                wrapped = ConversionError(str(exc))
                last_error = wrapped
                self.logger.debug("Unexpected error via %s: %s", method, exc)
                if not opts.fallback:
                    raise wrapped

        if last_error:
            raise last_error

        raise ConversionError(f"Conversion failed for {ai_path} - no method succeeded")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _resolve_methods(self, ai_path: Path, opts: AIOptions) -> List[str]:
        """Return a prioritized list of conversion methods."""
        prefer = opts.prefer_method
        is_pdf_based = self._is_pdf_based(ai_path)

        if prefer == "auto":
            return ["pymupdf", "pdf2image"] if is_pdf_based else ["pdf2image", "pymupdf"]
        if prefer == "pymupdf":
            return ["pymupdf", "pdf2image"] if opts.fallback else ["pymupdf"]
        if prefer == "pdf2image":
            return ["pdf2image", "pymupdf"] if opts.fallback else ["pdf2image"]
        return ["pymupdf", "pdf2image"]

    def _convert_with_pymupdf(self, ai_path: Path, png_path: Path, opts: AIOptions) -> bool:
        """Render the AI file with PyMuPDF."""
        if fitz is None:
            raise DependencyMissingError("PyMuPDF", "Install the base vector2png package dependencies.")

        doc = fitz.open(ai_path)
        if doc.page_count == 0:
            raise ConversionError("AI file contains no pages")

        page = doc[0]
        zoom = opts.dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        require_alpha = opts.transparent or bool(opts.background_color)
        pix = page.get_pixmap(matrix=mat, alpha=require_alpha)

        if opts.background_color and not opts.transparent:
            pil = optional_import("PIL.Image", package="Pillow")
            mode = "RGBA" if getattr(pix, "alpha", False) else "RGB"
            image = pil.frombytes(mode, (pix.width, pix.height), pix.samples)
            background = pil.new("RGB", image.size, opts.background_color)
            if mode == "RGBA":
                background.paste(image, mask=image.split()[3])
            else:
                background.paste(image)
            background.save(png_path, "PNG")
            doc.close()
            return True

        pix.save(png_path)
        doc.close()
        return True

    def _convert_with_pdf2image(self, ai_path: Path, png_path: Path, opts: AIOptions) -> bool:
        """Render the AI file through pdf2image when available."""
        if not self.pdf2image_available:
            return False

        pdf2image = optional_import(
            "pdf2image",
            hint="Install the 'pdf2image' extra and ensure Poppler is present",
        )
        images = pdf2image.convert_from_path(
            str(ai_path),
            dpi=opts.dpi,
            first_page=1,
            last_page=1,
            fmt="png",
            transparent=opts.transparent,
        )
        if not images:
            raise ConversionError("pdf2image returned no images")

        image = images[0]
        if opts.background_color and not opts.transparent:
            pil = optional_import("PIL.Image", package="Pillow")
            background = pil.new("RGB", image.size, opts.background_color)
            if image.mode == "RGBA":
                background.paste(image, mask=image.split()[3])
            else:
                background.paste(image)
            image = background
        image.save(png_path, "PNG")
        return True

    def _check_pdf2image(self) -> bool:
        try:
            import pdf2image  # noqa: F401

            return True
        except ImportError:
            return False

    def _is_pdf_based(self, ai_path: Path) -> bool:
        try:
            with open(ai_path, "rb") as handle:
                return handle.read(8).startswith(b"%PDF-")
        except OSError:
            return False

    def get_info(self, ai_path: str | Path) -> dict:
        """Return metadata describing the AI file."""
        source = Path(ai_path)
        info = {
            "exists": source.exists(),
            "size": source.stat().st_size if source.exists() else 0,
            "is_pdf_based": False,
            "page_count": 0,
            "dimensions": None,
        }
        if not info["exists"]:
            return info

        info["is_pdf_based"] = self._is_pdf_based(source)
        if fitz is None:
            return info
        try:
            doc = fitz.open(source)
            info["page_count"] = doc.page_count
            if doc.page_count:
                rect = doc[0].rect
                info["dimensions"] = (rect.width, rect.height)
            doc.close()
        except Exception:
            pass
        return info
