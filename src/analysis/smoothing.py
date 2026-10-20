import math


class OneEuroFilter:
    """
    min_cutoff: kam karo -> ruke hue haath par zyada stable (lekin thora lag)
    beta:       barhao -> tez movement par lag kam
    """

    def __init__(self, min_cutoff=0.5, beta=0.05, d_cutoff=1.0):
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.reset()

    def reset(self):
        self._x_prev = None
        self._dx_prev = 0.0
        self._t_prev = None

    @staticmethod
    def _alpha(cutoff, dt):
        tau = 1.0 / (2 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / dt)

    def __call__(self, x, t):
        """x: naya angle, t: time (seconds)."""
        if self._x_prev is None:
            self._x_prev, self._t_prev = x, t
            return x

        dt = t - self._t_prev
        if dt <= 0:
            return self._x_prev

        # speed (degrees/second) ka smoothed andaza
        dx = (x - self._x_prev) / dt
        a_d = self._alpha(self.d_cutoff, dt)
        dx_hat = a_d * dx + (1 - a_d) * self._dx_prev

        # speed zyada = cutoff zyada = kam smoothing
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = self._alpha(cutoff, dt)
        x_hat = a * x + (1 - a) * self._x_prev

        self._x_prev, self._dx_prev, self._t_prev = x_hat, dx_hat, t
        return x_hat