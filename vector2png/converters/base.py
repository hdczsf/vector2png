"""Base classes and shared helpers for converters."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

OptionsT = TypeVar("OptionsT")


class BaseConverter(ABC, Generic[OptionsT]):
    """Provide a thin abstraction that all converters inherit from."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def convert(self, source: str | Path, target: str | Path | None = None, options: OptionsT | None = None) -> Path:
        """Convert the given vector file to PNG and return the PNG path."""
