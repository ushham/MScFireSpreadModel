import numpy as np

class SubModel1:
    def __init__(self, minh, maxh, skew, maxm, mean):
        self.minheight = minh
        self.maxheight = maxh
        self.skw = skew
        self.lamba = mean
        self.maxmass = maxm

    def ProbDist(self, m, z):
        fz = self.lamba * np.exp(- self.lamba * z)
        fm = m ** -0.5
        return fz * fm