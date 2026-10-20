import time
import cv2


def save_snapshot(frame, angle, directory):
    angle_txt = "NA" if angle is None else f"{int(round(angle))}deg"
    name = f"elbow_{time.strftime('%Y%m%d_%H%M%S')}_{angle_txt}.jpg"
    path = directory / name
    cv2.imwrite(str(path), frame)
    return path