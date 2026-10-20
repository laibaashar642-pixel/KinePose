import threading
import time

import cv2


class CameraStream:
    def __init__(self, source=0, width=640, height=480):
        self.cap = cv2.VideoCapture(source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self._frame = None
        self._running = False
        self._lock = threading.Lock()
        self._thread = None

    def start(self):
        if not self.cap.isOpened():
            raise RuntimeError("Camera nahi khula. Source number check karo (0, 1, 2...)")
        self._running = True
        self._thread = threading.Thread(target=self._update, daemon=True)
        self._thread.start()
        return self

    def _update(self):
        while self._running:
            ok, frame = self.cap.read()
            if not ok:
                time.sleep(0.01)
                continue
            with self._lock:
                self._frame = frame

    def read(self):
        """Latest frame ki copy, ya None agar abhi tak koi frame nahi aaya."""
        with self._lock:
            return None if self._frame is None else self._frame.copy()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        self.cap.release()