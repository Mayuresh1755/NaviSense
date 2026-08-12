"""
=========================================
NaviSense Target Finder
=========================================

Handles object searching mode.

Author : NaviSense Team
"""

from typing import List
from detector import Detection


class TargetFinder:

    def __init__(self):

        self.target = None

        self.active = False

    # -------------------------------------

    def start(self, object_name: str):

        self.target = object_name.lower()

        self.active = True

    # -------------------------------------

    def stop(self):

        self.target = None

        self.active = False

    # -------------------------------------

    def is_active(self):

        return self.active

    # -------------------------------------

    def search(self,
               detections: List[Detection]):

        if not self.active:

            return None

        for obj in detections:

            if obj.name.lower() == self.target:

                return obj

        return None

    # -------------------------------------

    def found_message(self, obj):

        return f"{obj.name} {obj.direction}"

    # -------------------------------------

    def not_found_message(self):

        return f"{self.target} not found"