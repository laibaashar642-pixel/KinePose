import cv2
from src.pose.mediapipe_detector import MediaPipeDetector
from src.analysis.angle import calculate_angle

detector = MediaPipeDetector()
cap = cv2.VideoCapture(0)

while True:
    ok, frame = cap.read()
    if not ok:
        break

    kp = detector.detect(frame)
    if kp:
        sh, el, wr = kp["right_shoulder"], kp["right_elbow"], kp["right_wrist"]
        if min(sh[2], el[2], wr[2]) > 0.6:
            angle = calculate_angle(sh[:2], el[:2], wr[:2])
            print(f"Right elbow angle: {angle:.1f}")
    else:
        print("Koi insan nahi mila")

    cv2.imshow("test", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
detector.close()
cv2.destroyAllWindows()