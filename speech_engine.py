"""
=========================================
NaviSense Speech Engine
=========================================

Handles all speech synthesis.

Features
--------
✓ Background thread
✓ Queue based
✓ Duplicate prevention
✓ Priority support
✓ Thread-safe

Author : NaviSense Team
"""

import queue
import threading
import time
import pyttsx3

import config


class SpeechEngine:

    def __init__(self):

        self.engine = pyttsx3.init()

        self.engine.setProperty(
            "rate",
            config.VOICE_RATE
        )

        self.engine.setProperty(
            "volume",
            config.VOICE_VOLUME
        )

        self.queue = queue.PriorityQueue()

        self.running = False

        self.last_spoken = {}

        self.cooldown = 2.5

    # ---------------------------------

    def start(self):

        if self.running:
            return

        self.running = True

        thread = threading.Thread(
            target=self.worker,
            daemon=True
        )

        thread.start()

    # ---------------------------------

    def stop(self):

        self.running = False

        self.queue.put((999, None))

    # ---------------------------------

    def worker(self):

        while self.running:

            priority, text = self.queue.get()

            if text is None:
                break

            self.engine.say(text)

            self.engine.runAndWait()

    # ---------------------------------

    def speak(self,
              text,
              priority=5):

        current = time.time()

        if text in self.last_spoken:

            if current - self.last_spoken[text] < self.cooldown:

                return

        self.last_spoken[text] = current

        self.queue.put((priority, text))

    # ---------------------------------

    def clear(self):

        while not self.queue.empty():

            try:

                self.queue.get_nowait()

            except:

                pass

    # ---------------------------------

    def emergency(self, text):

        """
        Highest priority speech.
        """

        self.speak(

            text,

            priority=0

        )

    # ---------------------------------

    def warning(self, text):

        self.speak(

            text,

            priority=2

        )

    # ---------------------------------

    def info(self, text):

        self.speak(

            text,

            priority=5

        )