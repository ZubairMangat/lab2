"""AlertLogger: evaluates rules on detections, raises alerts, and persists events."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Protocol

from vision_types import Alert, Detection, Frame, Severity


@dataclass
class AlertRule:
    name: str
    target_labels: List[str]                  # e.g. ["person"]
    min_confidence: float = 0.60
    min_consecutive_frames: int = 3           # debounce to cut false alarms
    cooldown_s: int = 30                      # no repeat alert inside this window
    severity: Severity = Severity.WARNING


class NotificationChannel(Protocol):
    def send(self, alert: Alert) -> bool: ...


class AlertLogger(ABC):

    @abstractmethod
    def add_rule(self, rule: AlertRule) -> None:
        """Register a rule. Rules are evaluated in insertion order."""

    @abstractmethod
    def evaluate(self, frame: Frame, detections: List[Detection]) -> List[Alert]:
        """Apply all rules to one frame's detections. Returns alerts that fired."""

    @abstractmethod
    def log_detections(self, frame: Frame, detections: List[Detection]) -> None:
        """Append every detection to the event store (database or file)."""

    @abstractmethod
    def dispatch(self, alert: Alert) -> bool:
        """Save a snapshot, write the alert record, and notify channels.
        Returns True if at least one channel accepted it."""

    @abstractmethod
    def query(self, camera_id: Optional[str], start_ms: int, end_ms: int) -> List[Alert]:
        """Fetch stored alerts for a time window, optionally for one camera."""

    @abstractmethod
    def close(self) -> None:
        """Flush buffers and close database connections."""


class SqliteAlertLogger(AlertLogger):

    def __init__(self, db_path: str, channels: List[NotificationChannel]) -> None:
        self.db_path = db_path
        self.channels = channels

    def add_rule(self, rule: AlertRule) -> None:
        raise NotImplementedError

    def evaluate(self, frame: Frame, detections: List[Detection]) -> List[Alert]:
        raise NotImplementedError

    def log_detections(self, frame: Frame, detections: List[Detection]) -> None:
        raise NotImplementedError

    def dispatch(self, alert: Alert) -> bool:
        raise NotImplementedError

    def query(self, camera_id: Optional[str], start_ms: int, end_ms: int) -> List[Alert]:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
