# camera_pc/movement_analyzer.py
"""
Analyzes camera frames to determine face movement state.

States:
    MOVE_LEFT   – face is left of center (servo pan left)
    MOVE_RIGHT  – face is right of center (servo pan right)
    CENTERED    – face approximately centered
    NO_FACE     – no face detected

Only returns updates on state changes or after MIN_PUBLISH_INTERVAL.
"""

from __future__ import annotations
import time
from typing import Dict, Optional

from .config import DEAD_ZONE_RATIO, MIN_PUBLISH_INTERVAL


# Movement states
MOVE_LEFT = "MOVE_LEFT"
MOVE_RIGHT = "MOVE_RIGHT"
CENTERED = "CENTERED"
NO_FACE = "NO_FACE"


class CameraMovementAnalyzer:
    """Converts camera frame face data into movement commands."""

    def __init__(self, dead_zone_ratio: float = DEAD_ZONE_RATIO):
        """
        Args:
            dead_zone_ratio: fraction of frame width within which the face is considered CENTERED
        """
        self.dead_zone_ratio = float(dead_zone_ratio)
        self._last_state: Optional[str] = None
        self._last_report_time: float = 0.0

    def analyze_frame(
        self,
        frame_result: Dict,
        frame_width: int,
    ) -> Optional[Dict]:
        """
        Analyze a single camera frame.

        Args:
            frame_result: dict returned by face detection system
            frame_width: width of the camera frame in pixels

        Returns:
            dict ready for MQTT publish if state changed or interval elapsed,
            otherwise None. Format:
            {"status": "...", "confidence": 0.87, "timestamp": 1730...}
        """
        now = time.time()
        state = frame_result.get("state", "searching")
        face_box = frame_result.get("face_box")  # (x1, y1, x2, y2) or None
        confidence = frame_result.get("lock_confidence", 0.0)

        # ── Determine movement state ───────────────────────────────
        if state == "searching" or face_box is None:
            movement = NO_FACE
            confidence = 0.0
        else:
            x1, y1, x2, y2 = face_box
            face_cx = (x1 + x2) / 2.0
            frame_cx = frame_width / 2.0

            offset = (face_cx - frame_cx) / frame_width

            if abs(offset) <= self.dead_zone_ratio:
                movement = CENTERED
            elif offset < 0:
                movement = MOVE_LEFT
            else:
                movement = MOVE_RIGHT

        # ── Anti-flooding: only return on change or interval ───────
        state_changed = (movement != self._last_state)
        interval_elapsed = (now - self._last_report_time) >= MIN_PUBLISH_INTERVAL

        if not state_changed and not interval_elapsed:
            return None

        self._last_state = movement
        self._last_report_time = now

        return {
            "status": movement,
            "confidence": round(float(confidence), 3),
            "timestamp": int(now),
        }
