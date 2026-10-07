"""ModelInferenceEngine: loads a detector, runs inference, post-processes raw output."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List

import numpy as np

from vision_types import Detection, PreprocessedFrame


@dataclass
class InferenceConfig:
    model_path: str
    device: str = "cpu"                       # "cpu", "cuda:0", "tensorrt"
    conf_threshold: float = 0.45
    iou_threshold: float = 0.50               # NMS overlap threshold
    max_detections: int = 100
    class_names: Dict[int, str] | None = None


class ModelInferenceEngine(ABC):

    @abstractmethod
    def load_model(self) -> None:
        """Load weights onto the target device and run one warm-up pass."""

    @abstractmethod
    def infer(self, batch: List[PreprocessedFrame]) -> List[np.ndarray]:
        """Run the network. Returns one raw output array per input frame."""

    @abstractmethod
    def postprocess(self, raw: np.ndarray, frame: PreprocessedFrame) -> List[Detection]:
        """Decode raw output, apply confidence filter and NMS, and map boxes
        back to original-frame pixel coordinates using frame.scale and frame.pad."""

    @abstractmethod
    def detect(self, batch: List[PreprocessedFrame]) -> List[List[Detection]]:
        """Convenience wrapper: infer() followed by postprocess() for each frame."""

    @abstractmethod
    def unload(self) -> None:
        """Release model memory and device handles."""


class YoloOnnxEngine(ModelInferenceEngine):

    def __init__(self, config: InferenceConfig) -> None:
        self.config = config

    def load_model(self) -> None:
        raise NotImplementedError

    def infer(self, batch: List[PreprocessedFrame]) -> List[np.ndarray]:
        raise NotImplementedError

    def postprocess(self, raw: np.ndarray, frame: PreprocessedFrame) -> List[Detection]:
        raise NotImplementedError

    def detect(self, batch: List[PreprocessedFrame]) -> List[List[Detection]]:
        raise NotImplementedError

    def unload(self) -> None:
        raise NotImplementedError
