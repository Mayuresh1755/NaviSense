"""
=========================================
NaviSense Object Detector
=========================================

YOLO-based object detection module.

Responsibilities:
    - Load YOLO model
    - Detect objects
    - Filter detections
    - Calculate object direction
    - Calculate approximate distance

Author: NaviSense Team
"""

from dataclasses import dataclass
from typing import List

from ultralytics import YOLO

import config
from direction import DirectionCalculator
from distance import DistanceCalculator


# ==========================================
# Detection Data
# ==========================================

@dataclass
class Detection:

    name: str

    confidence: float

    bbox: tuple

    center: tuple

    direction: str

    distance: float = -1.0

    distance_category: str = "unknown"

    tracked_id: int = -1


# ==========================================
# Object Detector
# ==========================================

class ObjectDetector:

    def __init__(self):

        print("Loading YOLO model...")

        self.model = YOLO(
            config.YOLO_MODEL
        )

        self.direction = DirectionCalculator()

        self.distance = DistanceCalculator()

        print(
            "YOLO loaded successfully."
        )

    # ======================================
    # Configure Camera
    # ======================================

    def configure_camera(
        self,
        frame_width: int
    ):
        """
        Configure distance calculator using
        the actual camera width.
        """

        focal_length = (
            self.distance.configure_camera(
                frame_width
            )
        )

        print(
            f"Camera width: {frame_width}px"
        )

        print(
            f"Estimated focal length: "
            f"{focal_length:.2f}px"
        )

    # ======================================
    # Detect Objects
    # ======================================

    def detect(
        self,
        frame
    ) -> List[Detection]:
        """
        Run YOLO on a camera frame.

        Returns a list of Detection objects.
        """

        frame_height, frame_width = (
            frame.shape[:2]
        )

        # ----------------------------------
        # YOLO inference
        # ----------------------------------

        results = self.model(

            frame,

            imgsz=config.IMAGE_SIZE,

            conf=config.CONFIDENCE_THRESHOLD,

            verbose=False
        )

        detections = []

        # ----------------------------------
        # Process detections
        # ----------------------------------

        for box in results[0].boxes:

            confidence = float(
                box.conf[0]
            )

            if (
                confidence <
                config.CONFIDENCE_THRESHOLD
            ):
                continue

            # ------------------------------
            # Class
            # ------------------------------

            cls = int(
                box.cls[0]
            )

            name = self.model.names[
                cls
            ]

            # ------------------------------
            # Bounding box
            # ------------------------------

            x1, y1, x2, y2 = (
                box.xyxy[0]
            )

            bbox = (

                int(x1),

                int(y1),

                int(x2),

                int(y2)
            )

            # ------------------------------
            # Center
            # ------------------------------

            center_x = int(
                (x1 + x2) / 2
            )

            center_y = int(
                (y1 + y2) / 2
            )

            center = (
                center_x,
                center_y
            )

            # ------------------------------
            # Direction
            # ------------------------------

            direction = (
                self.direction.get_direction(
                    bbox,
                    frame_width
                )
            )

            # ------------------------------
            # Distance
            # ------------------------------

            distance_result = (
                self.distance.analyze(
                    name,
                    bbox
                )
            )

            if (
                distance_result
                .distance_meters
                is not None
            ):

                distance = (
                    distance_result
                    .distance_meters
                )

            else:

                distance = -1.0

            # ------------------------------
            # Create Detection
            # ------------------------------

            detection = Detection(

                name=name,

                confidence=confidence,

                bbox=bbox,

                center=center,

                direction=direction,

                distance=distance,

                distance_category=(
                    distance_result
                    .category
                )
            )

            detections.append(
                detection
            )

        return detections

    # ======================================
    # Annotate Frame
    # ======================================

    def annotate(
        self,
        frame,
        detections: List[Detection]
    ):
        """
        Draw detection information onto
        the camera frame.
        """

        import cv2

        for detection in detections:

            x1, y1, x2, y2 = (
                detection.bbox
            )

            # ------------------------------
            # Bounding box
            # ------------------------------

            cv2.rectangle(

                frame,

                (x1, y1),

                (x2, y2),

                config.GREEN,

                2
            )

            # ------------------------------
            # Object name
            # ------------------------------

            label = (
                f"{detection.name} "
                f"{detection.confidence:.2f}"
            )

            # ------------------------------
            # Distance
            # ------------------------------

            if detection.distance > 0:

                label += (
                    f" | "
                    f"{detection.distance:.1f}m"
                )

            # ------------------------------
            # Direction
            # ------------------------------

            label += (
                f" | "
                f"{detection.direction}"
            )

            # ------------------------------
            # Draw label
            # ------------------------------

            cv2.putText(

                frame,

                label,

                (x1, max(25, y1 - 10)),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.55,

                config.YELLOW,

                2,

                cv2.LINE_AA
            )

        return frame