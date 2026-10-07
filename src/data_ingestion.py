"""DataIngestion: owns the connection to camera sources and yields decoded frames."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterator, Optional

from vision_types import Frame


@dataclass
class StreamConfig:
    camera_id: str
    uri: str                          # rtsp://..., file path, or device index as string
    target_fps: int = 15
    reconnect_attempts: int = 5
    reconnect_backoff_s: float = 2.0
    buffer_size: int = 4              # frames kept in the queue; oldest dropped when full


class DataIngestion(ABC):
    """Contract for any frame source (RTSP, video file, USB camera)."""

    @abstractmethod
    def connect(self, config: StreamConfig) -> bool:
        """Open the stream. Returns True on success, False if all retries fail."""

    @abstractmethod
    def read_frame(self, timeout_s: float = 1.0) -> Optional[Frame]:
        """Return the next frame, or None if nothing arrived before the timeout."""

    @abstractmethod
    def frames(self) -> Iterator[Frame]:
        """Generator that yields frames until the stream is closed."""

    @abstractmethod
    def is_connected(self) -> bool:
        """True while the underlying stream is alive."""

    @abstractmethod
    def release(self) -> None:
        """Close the stream and free all resources. Safe to call more than once."""


class RTSPIngestion(DataIngestion):
    """OpenCV or GStreamer backed RTSP reader. Implementation to be filled in."""

    def __init__(self) -> None:
        raise NotImplementedError

    def connect(self, config: StreamConfig) -> bool:
        raise NotImplementedError

    def read_frame(self, timeout_s: float = 1.0) -> Optional[Frame]:
        raise NotImplementedError

    def frames(self) -> Iterator[Frame]:
        raise NotImplementedError

    def is_connected(self) -> bool:
        raise NotImplementedError

    def release(self) -> None:
        raise NotImplementedError
