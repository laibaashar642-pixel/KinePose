import time
import cv2


class VideoRecorder:
    def __init__(self, directory, fps=20):
        self.directory = directory
        self.fps = fps
        self._writer = None
        self.path = None

    @property
    def is_recording(self):
        return self._writer is not None

    def start(self, frame):
        h, w = frame.shape[:2]
        self.path = self.directory / f"session_{time.strftime('%Y%m%d_%H%M%S')}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self._writer = cv2.VideoWriter(str(self.path), fourcc, self.fps, (w, h))

    def write(self, frame):
        if self._writer is not None:
            self._writer.write(frame)

    def stop(self):
        if self._writer is not None:
            self._writer.release()
            self._writer = None
        return self.path