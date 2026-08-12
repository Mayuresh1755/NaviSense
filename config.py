"""
=========================================
NaviSense Configuration
=========================================

Central configuration for the NaviSense
system.

Author: NaviSense Team
"""

# =========================================
# Camera
# =========================================

CAMERA_INDEX = 0

# Camera resolution is NOT hardcoded.
# CameraManager determines the actual resolution.

TARGET_FPS = 30


# =========================================
# YOLO
# =========================================

YOLO_MODEL = "models/yolo11n.pt"

CONFIDENCE_THRESHOLD = 0.45

IMAGE_SIZE = 416

DETECTION_INTERVAL = 3


# =========================================
# Object Tracking
# =========================================

OBJECT_TIMEOUT = 3.0

MAX_OBJECTS = 25


# =========================================
# Distance Estimation
# =========================================

# Approximate horizontal field of view
# of the camera in degrees.
#
# This should ideally be calibrated for
# your actual camera.
#
# Typical webcams:
# 60° - 75°

CAMERA_HORIZONTAL_FOV = 70.0


# =========================================
# Navigation Distance Thresholds
# =========================================

WARNING_DISTANCE = 1.5

CRITICAL_DISTANCE = 0.75


# =========================================
# Speech
# =========================================

VOICE_RATE = 170

VOICE_VOLUME = 1.0

ENABLE_SPEECH = True


# =========================================
# Direction
# =========================================

LEFT_BOUNDARY = 0.33

RIGHT_BOUNDARY = 0.66


# =========================================
# ESP32
# =========================================

ENABLE_SERIAL = False

SERIAL_PORT = "COM5"

BAUD_RATE = 115200


# =========================================
# Debugging
# =========================================

SHOW_FPS = True

PRINT_DETECTIONS = True


# =========================================
# OpenCV Colors
# =========================================

GREEN = (0, 255, 0)

RED = (0, 0, 255)

BLUE = (255, 0, 0)

YELLOW = (0, 255, 255)

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)


# =========================================
# Application
# =========================================

WINDOW_NAME = "NaviSense AI"

EXIT_KEY = "q"