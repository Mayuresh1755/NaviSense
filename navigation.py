"""
=========================================
NaviSense Navigation Engine
=========================================

Converts detected objects into
meaningful navigation instructions.

Author : NaviSense Team
"""

from detector import Detection

# ----------------------------------------
# Priority Table
# ----------------------------------------

OBJECT_PRIORITY = {

    # Critical

    "car": 1,
    "truck": 1,
    "bus": 1,
    "train": 1,
    "motorcycle": 1,

    # High

    "person": 2,
    "stairs": 2,
    "door": 2,
    "pole": 2,
    "tree": 2,

    # Medium

    "chair": 3,
    "bench": 3,
    "table": 3,
    "bicycle": 3,

    # Low

    "bottle": 5,
    "cup": 5,
    "cell phone": 5,
    "book": 5,

}


class NavigationEngine:

    def __init__(self):

        pass

    # -----------------------------------

    def priority(self, obj: Detection):

        return OBJECT_PRIORITY.get(obj.name, 10)

    # -----------------------------------

    def sort(self, detections):

        return sorted(

            detections,

            key=lambda x: self.priority(x)

        )

    # -----------------------------------

    def generate_message(self, obj):

        return f"{obj.name} {obj.direction}"

    # -----------------------------------

    def analyse(self, detections):

        if len(detections) == 0:

            return []

        ordered = self.sort(detections)

        messages = []

        for obj in ordered:

            messages.append(

                self.generate_message(obj)

            )

        return messages