import time
import cv2

import config
from src.camera.camera_stream import CameraStream
from src.pose.mediapipe_detector import MediaPipeDetector
from src.analysis.angle import calculate_angle
from src.analysis.smoothing import OneEuroFilter
from src.storage.snapshot import save_snapshot
from src.storage.recorder import VideoRecorder
from src.ui.overlay import draw_arm, draw_status

SIDE = "right"
MIN_VIS = 0.6


def main():
    cam = CameraStream(0).start()
    detector = MediaPipeDetector()
    angle_filter = OneEuroFilter(min_cutoff=0.5, beta=0.05)
    recorder = VideoRecorder(config.VIDEOS_DIR, fps=20)
    message, message_until = "", 0

    try:
        while True:
            frame = cam.read()
            if frame is None:
                if cv2.waitKey(10) & 0xFF == ord("q"):
                    break
                continue

            kp = detector.detect(frame)
            angle = None

            if kp is None:
                angle_filter.reset()
                draw_status(frame, "Koi insan nahi mila", (0, 0, 255))
            else:
                sh = kp[f"{SIDE}_shoulder"]
                el = kp[f"{SIDE}_elbow"]
                wr = kp[f"{SIDE}_wrist"]

                if min(sh[2], el[2], wr[2]) >= MIN_VIS:
                    raw = calculate_angle(sh[:2], el[:2], wr[:2])
                    if raw is not None:
                        angle = angle_filter(raw, time.time())
                else:
                    angle_filter.reset()   # dobara dikhe to purani value se na mile

                draw_arm(frame, kp, SIDE, angle, MIN_VIS)
                if angle is None:
                    draw_status(frame, "Elbow clearly visible nahi", (0, 165, 255))

            # recording: annotated frame save hota hai (skeleton aur angle ke sath)
            if recorder.is_recording:
                recorder.write(frame)
                cv2.circle(frame, (frame.shape[1] - 25, 25), 10, (0, 0, 255), -1)

            if time.time() < message_until:
                cv2.putText(frame, message, (10, frame.shape[0] - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow("KinePose", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
            elif key == ord("s"):
                path = save_snapshot(frame, angle, config.CAPTURES_DIR)
                message, message_until = f"Saved: {path.name}", time.time() + 2
            elif key == ord("r"):
                if recorder.is_recording:
                    path = recorder.stop()
                    message, message_until = f"Video saved: {path.name}", time.time() + 3
                else:
                    recorder.start(frame)
    except KeyboardInterrupt:
        pass
    finally:
        recorder.stop()
        cam.stop()
        detector.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()