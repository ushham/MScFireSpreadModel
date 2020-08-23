import numpy as np

class SubModel3:
    def __init__(self, mid, skew):
        self.mid = mid
        self.skew = 1 / skew

    def PDF(self, r):
        b = -self.skew * self.mid
        pow = b + self.skew * r
        return np.exp(pow) / (1 + np.exp(pow))

