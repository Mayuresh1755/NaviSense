"""
=========================================
NaviSense Distance Calculator
=========================================

Estimates approximate object distance using
the pinhole camera model.

Formula:

        F × H
D =    -------
          h

Where:

D = distance to object in meters
F = focal length in pixels
H = real-world object height in meters
h = object height in image pixels

IMPORTANT:
This is an approximate distance estimator.

It works best when:
- Object dimensions are approximately known.
- Object is upright.
- YOLO bounding box is reasonably accurate.
- Camera is reasonably calibrated.

Author: NaviSense Team
"""

import math
from dataclasses import dataclass
from typing import Optional

import config


# ==========================================
# Known Object Heights
# ==========================================
#
# Values are approximate.
#
# You should eventually measure these
# yourself for better accuracy.
#
# Units: meters
# ==========================================

KNOWN_OBJECT_HEIGHTS = {

    "person": 1.70,

    "chair": 0.90,

    "table": 0.75,

    "bottle": 0.25,

    "cup": 0.12,

    "laptop": 0.25,

    "backpack": 0.45,

    "car": 1.50,

    "bicycle": 1.10,

    "motorcycle": 1.20,

    "bus": 3.00,

    "truck": 3.00,

    "dog": 0.50,

    "cat": 0.30,

    "bench": 0.50,

}


# ==========================================
# Distance Result
# ==========================================

@dataclass
class DistanceResult:

    object_name: str

    distance_meters: Optional[float]

    category: str

    pixel_height: float


# ==========================================
# Distance Calculator
# ==========================================

class DistanceCalculator:

    def __init__(
        self,
        horizontal_fov: float = config.CAMERA_HORIZONTAL_FOV
    ):
        """
        Create distance calculator.

        Focal length cannot be calculated until
        the camera's actual frame width is known.

        Parameters
        ----------
        horizontal_fov:
            Horizontal camera field of view
            in degrees.
        """

        self.horizontal_fov = horizontal_fov

        self.focal_length = None

        self.frame_width = None

    # ======================================
    # Configure Camera
    # ======================================

    def configure_camera(
        self,
        frame_width: int
    ):
        """
        Calculate focal length from camera
        frame width and horizontal FOV.

        Formula:

                 width / 2
        F = ---------------------
             tan(FOV / 2)
        """

        if frame_width <= 0:

            raise ValueError(
                "Frame width must be greater than zero."
            )

        if self.horizontal_fov <= 0:

            raise ValueError(
                "Horizontal FOV must be greater than zero."
            )

        if self.horizontal_fov >= 180:

            raise ValueError(
                "Horizontal FOV must be less than 180 degrees."
            )

        self.frame_width = frame_width

        fov_radians = math.radians(
            self.horizontal_fov
        )

        self.focal_length = (
            frame_width / 2
        ) / math.tan(
            fov_radians / 2
        )

        return self.focal_length

    # ======================================
    # Get Focal Length
    # ======================================

    def get_focal_length(self) -> Optional[float]:

        return self.focal_length

    # ======================================
    # Calculate Distance
    # ======================================

    def calculate(
        self,
        object_name: str,
        bbox: tuple
    ) -> Optional[float]:
        """
        Calculate approximate object distance.

        Parameters
        ----------
        object_name:
            YOLO class name.

        bbox:
            (x1, y1, x2, y2)

        Returns
        -------
        float or None:
            Estimated distance in meters.
        """

        # ----------------------------------
        # Check focal length
        # ----------------------------------

        if self.focal_length is None:

            raise RuntimeError(
                "Camera has not been configured. "
                "Call configure_camera() first."
            )

        # ----------------------------------
        # Check known object
        # ----------------------------------

        if object_name not in KNOWN_OBJECT_HEIGHTS:

            return None

        real_height = KNOWN_OBJECT_HEIGHTS[
            object_name
        ]

        # ----------------------------------
        # Extract bounding box
        # ----------------------------------

        x1, y1, x2, y2 = bbox

        # ----------------------------------
        # Calculate pixel height
        # ----------------------------------

        pixel_height = abs(
            float(y2) - float(y1)
        )

        if pixel_height <= 0:

            return None

        # ----------------------------------
        # Pinhole camera formula
        # ----------------------------------

        distance = (
            self.focal_length *
            real_height
        ) / pixel_height

        return distance

    # ======================================
    # Classify Distance
    # ======================================

    def classify_distance(
        self,
        distance: float
    ) -> str:
        """
        Convert distance into a simple
        navigation category.
        """

        if distance <= 0:

            return "unknown"

        if distance <= config.CRITICAL_DISTANCE:

            return "critical"

        if distance <= config.WARNING_DISTANCE:

            return "warning"

        if distance <= 3.0:

            return "near"

        if distance <= 5.0:

            return "medium"

        return "far"

    # ======================================
    # Analyze Object
    # ======================================

    def analyze(
        self,
        object_name: str,
        bbox: tuple
    ) -> DistanceResult:
        """
        Calculate and classify an object's
        approximate distance.
        """

        x1, y1, x2, y2 = bbox

        pixel_height = abs(
            float(y2) - float(y1)
        )

        distance = self.calculate(
            object_name,
            bbox
        )

        if distance is None:

            return DistanceResult(

                object_name=object_name,

                distance_meters=None,

                category="unknown",

                pixel_height=pixel_height
            )

        category = self.classify_distance(
            distance
        )

        return DistanceResult(

            object_name=object_name,

            distance_meters=distance,

            category=category,

            pixel_height=pixel_height
        )

    # ======================================
    # Calibration
    # ======================================

    @staticmethod
    def calibrate_focal_length(
        known_distance: float,
        real_object_height: float,
        pixel_object_height: float
    ) -> float:
        """
        Calculate focal length using a known
        object at a known distance.

        Formula:

            F = D × h
                -----
                  H

        Parameters
        ----------
        known_distance:
            Actual distance in meters.

        real_object_height:
            Actual object height in meters.

        pixel_object_height:
            Object height in image pixels.

        Returns
        -------
        float:
            Calibrated focal length.
        """

        if known_distance <= 0:

            raise ValueError(
                "Known distance must be greater than zero."
            )

        if real_object_height <= 0:

            raise ValueError(
                "Real object height must be greater than zero."
            )

        if pixel_object_height <= 0:

            raise ValueError(
                "Pixel object height must be greater than zero."
            )

        focal_length = (
            known_distance *
            pixel_object_height
        ) / real_object_height

        return focal_length

    # ======================================
    # Set Calibrated Focal Length
    # ======================================

    def set_focal_length(
        self,
        focal_length: float
    ):
        """
        Manually set a calibrated focal length.
        """

        if focal_length <= 0:

            raise ValueError(
                "Focal length must be greater than zero."
            )

        self.focal_length = focal_length

    # ======================================
    # Get Human Readable Distance
    # ======================================

    @staticmethod
    def format_distance(
        distance: Optional[float]
    ) -> str:
        """
        Convert distance to speech/display text.
        """

        if distance is None:

            return "distance unknown"

        if distance < 1.0:

            centimeters = int(
                distance * 100
            )

            return f"{centimeters} centimeters"

        return f"{distance:.1f} meters"