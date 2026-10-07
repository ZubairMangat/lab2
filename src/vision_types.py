"""Shared data types passed between modules. Keeping them in one place means
no module needs to import another module's internals."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass(frozen=True)
class Frame:
    """A single decoded video frame with capture metadata."""
    camera_id: str
    frame_id: int
    timestamp_ms: int                 # capture time, UTC epoch milliseconds
    image: np.ndarray                 # H x W x 3, uint8, BGR


@dataclass(frozen=True)
class PreprocessedFrame:
    """Model-ready tensor plus the info needed to map results back to the original frame."""
    source: Frame
    tensor: np.ndarray                # 1 x 3 x H x W, float32, normalized
    scale: Tuple[float, float]        # (sx, sy) resize factors
    pad: Tuple[int, int]              # (left, top) letterbox padding in pixels


@dataclass(frozen=True)
class Detection:
    """One detected object, in original-frame pixel coordinates."""
    label: str
    class_id: int
    confidence: float                 # 0.0 to 1.0
    bbox_xyxy: Tuple[int, int, int, int]
    track_id: Optional[int] = None


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Alert:
    alert_id: str
    camera_id: str
    timestamp_ms: int
    severity: Severity
    rule_name: str
    detections: List[Detection] = field(default_factory=list)
    snapshot_path: Optional[str] = None
    extra: Dict[str, str] = field(default_factory=dict)
