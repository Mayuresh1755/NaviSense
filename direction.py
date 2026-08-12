"""
=========================================
NaviSense Direction Module
=========================================

Determines where an object is located
relative to the camera.

Author : NaviSense Team
"""

from dataclasses import dataclass


# ---------------------------------------
# Direction Labels
# ---------------------------------------

LEFT = "left"
CENTER = "ahead"
RIGHT = "right"


# ---------------------------------------
# Screen Zones
# ---------------------------------------

@dataclass
class ScreenZones:

    left_boundary: float
    right_boundary: float


# ---------------------------------------
# Direction Calculator
# ---------------------------------------

class DirectionCalculator:

    def __init__(self,
                 left_ratio=0.33,
                 right_ratio=0.66):

        self.left_ratio = left_ratio
        self.right_ratio = right_ratio

    # -----------------------------------

    def get_boundaries(self, frame_width):

        left = frame_width * self.left_ratio
        right = frame_width * self.right_ratio

        return ScreenZones(left, right)

    # -----------------------------------

    def object_center(self, bbox):

        """
        bbox format:

        x1,y1,x2,y2
        """

        x1, y1, x2, y2 = bbox

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        return center_x, center_y

    # -----------------------------------

    def get_direction(self, bbox, frame_width):

        center_x, _ = self.object_center(bbox)

        boundaries = self.get_boundaries(frame_width)

        if center_x < boundaries.left_boundary:
            return LEFT

        elif center_x > boundaries.right_boundary:
            return RIGHT

        else:
            return CENTER

    # -----------------------------------

    def direction_vector(self, bbox, frame_width):

        """
        Returns a normalized direction.

        -1.0  -> Far Left
         0.0  -> Center
         1.0  -> Far Right
        """

        center_x, _ = self.object_center(bbox)

        frame_center = frame_width / 2

        return (center_x - frame_center) / frame_center

    # -----------------------------------

    def horizontal_offset(self, bbox, frame_width):

        center_x, _ = self.object_center(bbox)

        frame_center = frame_width / 2

        return center_x - frame_center