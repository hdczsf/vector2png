"""Custom exception types for vector2png."""

from __future__ import annotations


class ConversionError(RuntimeError):
    """Base error raised when a conversion fails."""


class DependencyMissingError(ConversionError):
    """Raised when an optional dependency is not installed."""

    def __init__(self, package: str, hint: str | None = None) -> None:
        message = f"Dependency '{package}' is required for this operation."
        if hint:
            message = f"{message} {hint}"
        super().__init__(message)
        self.package = package
        self.hint = hint


class FileInferenceError(ConversionError):
    """Raised when the converter cannot inspect the provided file."""

