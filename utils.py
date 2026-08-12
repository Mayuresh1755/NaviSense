"""
=========================================
NaviSense Utility Functions
=========================================

Contains reusable helper functions.

Author : NaviSense Team
"""

import cv2
import time
import logging
import config

# ==========================================
# Logging Configuration
# ==========================================

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("NaviSense")


# ==========================================
# FPS Calculator
# ==========================================

class FPSCounter:

    def __init__(self):

        self.previous_time = time.time()
        self.current_fps = 0

    def update(self):

        current = time.time()

        delta = current - self.previous_time

        if delta > 0:
            self.current_fps = 1 / delta

        self.previous_time = current

        return int(self.current_fps)

    def get(self):

        return int(self.current_fps)


# ==========================================
# Draw Text
# ==========================================

def draw_text(
        frame,
        text,
        x,
        y,
        color=config.GREEN,
        scale=0.7,
        thickness=2):

    cv2.putText(
        frame,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        color,
        thickness,
        cv2.LINE_AA
    )


# ==========================================
# Draw FPS
# ==========================================

def draw_fps(frame, fps):

    if not config.SHOW_FPS:
        return

    draw_text(
        frame,
        f"FPS : {fps}",
        20,
        35,
        config.YELLOW
    )


# ==========================================
# Draw Header
# ==========================================

def draw_header(frame, title):

    draw_text(
        frame,
        title,
        20,
        70,
        config.WHITE,
        scale=0.8
    )


# ==========================================
# Timestamp
# ==========================================

def timestamp():

    return time.strftime("%H:%M:%S")


# ==========================================
# Log Detection
# ==========================================

def log_detection(name, confidence, direction):

    if config.PRINT_DETECTIONS:

        logger.info(
            f"{name:15s}"
            f"{confidence:.2f}"
            f"   {direction}"
        )


# ==========================================
# Confidence Formatter
# ==========================================

def confidence_to_percent(conf):

    return round(conf * 100, 1)


# ==========================================
# Generate Object ID
# ==========================================

def generate_object_id(name, direction):

    """
    Creates a unique identifier.

    Example:

    chair_left

    person_center
    """

    return f"{name}_{direction}"


# ==========================================
# Clamp
# ==========================================

def clamp(value, minimum, maximum):

    return max(minimum, min(value, maximum))


# ==========================================
# Center of Bounding Box
# ==========================================

def bbox_center(box):

    """
    Input:

    x1,y1,x2,y2

    Output:

    center_x, center_y
    """

    x1, y1, x2, y2 = box

    center_x = int((x1 + x2) / 2)
    center_y = int((y1 + y2) / 2)

    return center_x, center_y


# ==========================================
# Distance Between Points
# ==========================================

def euclidean_distance(p1, p2):

    return ((p1[0]-p2[0])**2 +
            (p1[1]-p2[1])**2) ** 0.5


# ==========================================
# Resize Maintaining Aspect Ratio
# ==========================================

def resize_frame(frame, width=800):

    h, w = frame.shape[:2]

    ratio = width / w

    height = int(h * ratio)

    return cv2.resize(frame, (width, height))


# ==========================================
# Safe Exit
# ==========================================

def shutdown(camera=None):

    logger.info("Closing NaviSense...")

    if camera is not None:
        camera.release()

    cv2.destroyAllWindows()

    logger.info("Shutdown Complete.")