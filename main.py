"""
=========================================
NaviSense Distance Test
=========================================

Tests:

Camera
  ↓
YOLO
  ↓
Direction
  ↓
Distance

Press Q to exit.

Author: NaviSense Team
"""

import cv2

import config

from camera import CameraManager
from detector import ObjectDetector


# ==========================================
# Initialize Camera
# ==========================================

camera = CameraManager()

camera.select_camera()


# ==========================================
# Initialize Detector
# ==========================================

detector = ObjectDetector()


# ==========================================
# Configure Distance Calculator
# ==========================================

detector.configure_camera(
    camera.width
)


# ==========================================
# Main Loop
# ==========================================

while True:

    ret, frame = camera.read()

    if not ret:

        print(
            "Failed to read camera frame."
        )

        break

    # --------------------------------------
    # Detect objects
    # --------------------------------------

    detections = detector.detect(
        frame
    )

    # --------------------------------------
    # Print detections
    # --------------------------------------

    for detection in detections:

        print(
            f"{detection.name:12} | "
            f"Confidence: "
            f"{detection.confidence:.2f} | "
            f"Direction: "
            f"{detection.direction:6} | "
            f"Distance: "
            f"{detection.distance:.2f} m | "
            f"Category: "
            f"{detection.distance_category}"
        )

    # --------------------------------------
    # Draw results
    # --------------------------------------

    detector.annotate(
        frame,
        detections
    )

    # --------------------------------------
    # Display
    # --------------------------------------

    cv2.imshow(
        config.WINDOW_NAME,
        frame
    )

    # --------------------------------------
    # Q = Exit
    # --------------------------------------

    key = cv2.waitKey(1) & 0xFF

    if key == ord(
        config.EXIT_KEY
    ):

        print(
            "Exiting NaviSense..."
        )

        break


# ==========================================
# Cleanup
# ==========================================

camera.release()

cv2.destroyAllWindows()