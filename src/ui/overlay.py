import cv2

FONT = cv2.FONT_HERSHEY_SIMPLEX
GREEN = (0, 255, 0)
RED = (0, 0, 255)


def draw_arm(frame, kp, side="right", angle=None, min_vis=0.6):
    names = [f"{side}_shoulder", f"{side}_elbow", f"{side}_wrist"]
    pts = [kp[n] for n in names]
    visible = all(p[2] >= min_vis for p in pts)
    color = GREEN if visible else RED
    xy = [(int(p[0]), int(p[1])) for p in pts]

    cv2.line(frame, xy[0], xy[1], color, 3)
    cv2.line(frame, xy[1], xy[2], color, 3)
    for point in xy:
        cv2.circle(frame, point, 8, color, -1)

    if angle is not None:
        cv2.putText(frame, f"{angle:.0f} deg",
                    (xy[1][0] + 15, xy[1][1] - 15), FONT, 0.9, color, 2)


def draw_status(frame, text, color=(255, 255, 255)):
    cv2.putText(frame, text, (10, 30), FONT, 0.7, color, 2)