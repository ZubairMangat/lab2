"""ImagePreprocessor: turns raw frames into model-ready tensors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

from vision_types import Frame, PreprocessedFrame


@dataclass
class PreprocessConfig:
    input_size: Tuple[int, int] = (640, 640)          # (width, height) the model expects
    mean: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    std: Tuple[float, float, float] = (255.0, 255.0, 255.0)
    letterbox: bool = True                             # keep aspect ratio with padding
    bgr_to_rgb: bool = True


class ImagePreprocessor(ABC):

    @abstractmethod
    def process(self, frame: Frame) -> PreprocessedFrame:
        """Resize, pad, color convert and normalize one frame."""

    @abstractmethod
    def process_batch(self, frames: List[Frame]) -> List[PreprocessedFrame]:
        """Same as process() for several frames, preserving order."""

    @abstractmethod
    def is_blurry(self, frame: Frame, threshold: float = 100.0) -> bool:
        """Quality gate. True when the Laplacian variance falls below threshold."""


class LetterboxPreprocessor(ImagePreprocessor):

    def __init__(self, config: PreprocessConfig) -> None:
        self.config = config

    def process(self, frame: Frame) -> PreprocessedFrame:
        raise NotImplementedError

    def process_batch(self, frames: List[Frame]) -> List[PreprocessedFrame]:
        raise NotImplementedError

    def is_blurry(self, frame: Frame, threshold: float = 100.0) -> bool:
        raise NotImplementedError
