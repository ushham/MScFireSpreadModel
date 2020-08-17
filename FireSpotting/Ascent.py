import numpy as np
import matplotlib.pyplot as plt

class SubModel1:

    def __init__(self, minh, maxh, lam, maxm):
        self.minheight = minh
        self.maxheight = maxh
        self.lam = 1 / lam
        self.maxmass = maxm


    def PDF(self, z):
        fz = self.lam * np.exp(self.lam * (self.minheight - z))
        out = fz
        return out

    def PrdDist(self):
        #Given the mass, returns the prob of reaching height z
        res = 10000
        z = np.linspace(self.minheight, self.maxheight, res)
        p = self.PDF(z)
        return z, p

# n = 1000
#
# hold = np.zeros(n)
# #               minh, maxh, lam, maxm
# test = SubModel1(200, 1000, 400, 1)
# hld = test.PrdDist()
# hld2 = test.PrdDist()
# print(hld)
#
# print(np.sum(hld[1])/10)
#
#
# plt.plot(hld[0], hld[1])
# plt.plot(hld2[0], hld2[1])
# plt.show()