import numpy as np


def calculate_angle(a, b, c):
    """
    Teen points ke beech angle (degrees) nikalta hai, vertex b par.

    a: pehla point (e.g. shoulder)
    b: vertex       (e.g. elbow)
    c: teesra point (e.g. wrist)

    Points (x, y) ya (x, y, z) ho sakte hain.
    Agar koi vector zero length ka ho (do points ek hi jagah), None return karta hai.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    c = np.asarray(c, dtype=float)

    v1 = a - b
    v2 = c - b

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return None

    cos_theta = np.dot(v1, v2) / (norm1 * norm2)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)

    return float(np.degrees(np.arccos(cos_theta)))