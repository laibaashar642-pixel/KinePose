from abc import ABC, abstractmethod


class PoseDetector(ABC):
    """Har pose model (MediaPipe, MoveNet, RTMPose) is class ko inherit karega."""

    @abstractmethod
    def detect(self, frame):
        """
        frame: BGR image (OpenCV ka frame)

        Returns:
            dict {joint_name: (x_px, y_px, visibility)} ya None agar koi insan na mile
        """

    def close(self):
        """Resources free karne ke liye (optional)."""
        pass