"""
=========================================
NaviSense Camera Manager
=========================================

Features:
- Automatically scans available cameras
- Allows user selection
- Retrieves camera properties
- Provides simple read() interface

Author : NaviSense Team
"""

import cv2


class CameraManager:

    def __init__(self):

        self.cap = None
        self.camera_index = None

        self.width = 0
        self.height = 0
        self.fps = 0

    # -------------------------------------

    def scan_cameras(self, max_devices=10):
        """
        Scan available camera indices.
        """

        available = []

        print("Scanning cameras...\n")

        for index in range(max_devices):

            cap = cv2.VideoCapture(index)

            if cap.isOpened():

                ret, frame = cap.read()

                if ret:
                    available.append(index)
                    print(f"[{index}] Camera detected")

                cap.release()

        return available

    # -------------------------------------

    def select_camera(self):

        cameras = self.scan_cameras()

        if len(cameras) == 0:
            raise RuntimeError("No camera found.")

        if len(cameras) == 1:

            self.camera_index = cameras[0]

            print(f"\nUsing Camera {self.camera_index}\n")

        else:

            print("\nAvailable Cameras:")

            for cam in cameras:
                print(f"{cam}")

            while True:

                try:

                    choice = int(input("\nSelect Camera Index : "))

                    if choice in cameras:
                        self.camera_index = choice
                        break

                    print("Invalid selection.")

                except ValueError:
                    print("Enter a valid number.")

        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("Unable to open selected camera.")

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

        print("\nCamera Information")
        print("-------------------------")
        print(f"Resolution : {self.width} x {self.height}")
        print(f"FPS        : {self.fps:.2f}")
        print()

    # -------------------------------------

    def read(self):

        return self.cap.read()

    # -------------------------------------

    def release(self):

        if self.cap is not None:
            self.cap.release()

    # -------------------------------------

    def get_resolution(self):

        return self.width, self.height

    # -------------------------------------

    def get_fps(self):

        return self.fps