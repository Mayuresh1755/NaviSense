"""
=========================================
NaviSense Tracker
=========================================

Tracks detected objects between frames.

Responsibilities
----------------
- Remember objects
- Assign IDs
- Detect new objects
- Detect disappeared objects
- Prevent repeated announcements

Author : NaviSense Team
"""

from dataclasses import dataclass
from typing import Dict
import math
import time

import config
from detector import Detection


# --------------------------------------
# Tracked Object
# --------------------------------------

@dataclass
class TrackedObject:

    id: int

    detection: Detection

    first_seen: float

    last_seen: float

    announced: bool = False


# --------------------------------------
# Tracker
# --------------------------------------

class ObjectTracker:

    def __init__(self):

        self.objects: Dict[int, TrackedObject] = {}

        self.next_id = 0

    # ----------------------------------

    def distance(self, c1, c2):

        return math.sqrt(

            (c1[0] - c2[0]) ** 2 +

            (c1[1] - c2[1]) ** 2

        )

    # ----------------------------------

    def match(self, detection):

        """
        Try to match with an existing object.
        """

        best_id = None

        best_distance = 999999

        for object_id, tracked in self.objects.items():

            if tracked.detection.name != detection.name:
                continue

            d = self.distance(

                tracked.detection.center,

                detection.center

            )

            if d < best_distance:

                best_distance = d

                best_id = object_id

        if best_distance < 120:

            return best_id

        return None

    # ----------------------------------

    def update(self, detections):

        current_time = time.time()

        new_objects = []

        disappeared = []

        matched = set()

        # ------------------------------

        for detection in detections:

            object_id = self.match(detection)

            if object_id is None:

                tracked = TrackedObject(

                    id=self.next_id,

                    detection=detection,

                    first_seen=current_time,

                    last_seen=current_time

                )

                self.objects[self.next_id] = tracked

                detection.tracked_id = self.next_id

                new_objects.append(tracked)

                self.next_id += 1

            else:

                tracked = self.objects[object_id]

                tracked.detection = detection

                tracked.last_seen = current_time

                detection.tracked_id = object_id

                matched.add(object_id)

        # ------------------------------

        remove = []

        for object_id, tracked in self.objects.items():

            if current_time - tracked.last_seen > config.OBJECT_TIMEOUT:

                disappeared.append(tracked)

                remove.append(object_id)

        for object_id in remove:

            del self.objects[object_id]

        return {

            "new": new_objects,

            "active": list(self.objects.values()),

            "gone": disappeared

        }