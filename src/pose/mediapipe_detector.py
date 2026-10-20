import cv2
import mediapipe as mp

from src.pose.base import PoseDetector

_P = mp.solutions.pose.PoseLandmark

# Sirf wohi joints jo hamein chahiye (arms). Baad mein knee waghera yahin add honge.
JOINTS = {
    "left_shoulder": _P.LEFT_SHOULDER,
    "left_elbow": _P.LEFT_ELBOW,
    "left_wrist": _P.LEFT_WRIST,
    "right_shoulder": _P.RIGHT_SHOULDER,
    "right_elbow": _P.RIGHT_ELBOW,
    "right_wrist": _P.RIGHT_WRIST,
}


class MediaPipeDetector(PoseDetector):
    def __init__(self, detection_conf=0.5, tracking_conf=0.5, model_complexity=1):
        self._pose = mp.solutions.pose.Pose(
            model_complexity=model_complexity,   # 0 = fast, 1 = balanced, 2 = accurate
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )
        self.last_raw = None  # drawing ke liye poora skeleton (overlay mein kaam aayega)

    def detect(self, frame):
        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # MediaPipe RGB mangta hai
        results = self._pose.process(rgb)
        self.last_raw = results.pose_landmarks

        if not results.pose_landmarks:
            return None

        lm = results.pose_landmarks.landmark
        return {
            name: (lm[idx].x * w, lm[idx].y * h, lm[idx].visibility)
            for name, idx in JOINTS.items()
        }

    def close(self):
        self._pose.close()