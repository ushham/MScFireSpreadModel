import numpy as np

class SubModel1:
    #Discribes the lofting phase of the firebrand
    def __init__(self, minh, maxh, lam, maxm):
        self.minheight = minh
        self.maxheight = maxh
        self.lam = 1 / lam
        self.maxmass = maxm
        self.res = 10000

    def PDF(self, z):
        fz = self.lam * np.exp(self.lam * (self.minheight - z))
        out = fz
        return out

    def PrdDist(self):
        #Given the mass, returns the prob of reaching height z
        z = np.linspace(self.minheight, self.maxheight, self.res)
        p = self.PDF(z)
        return z, p