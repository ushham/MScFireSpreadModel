import numpy as np
import scipy.integrate as int
import matplotlib.pyplot as plt
from scipy.optimize import minimize as mzn
from scipy.optimize import root
class SubModel2:
    #Assumptions
    Re = 10000   #Reynolds number from litrature
    Sc = 0.7    #Schmidt number, from litrature
    beta = 4.3 * (10 ** -7) * (1 + 0.276 * (Re ** (1 / 2)) * (Sc ** (1 / 3)))

    def __init__(self, eta, w0, wx):
        self.eta = eta
        self.w0 = w0
        self.wx = wx

    def r_r0(self, t, r0):
        r4 = r0 ** 4 - np.sqrt(3) * (self.beta ** 2) * (t ** 2) / 8
        if r4 < 0:
            r4 = np.nan
        r = r4 ** (1 / 4) / r0
        return r

    def rho_rho0(self, t):
        return 1 / (1 + self.eta * t ** 2)

    def terminal_vel(self, t, r0):
        return self.w0 * (self.rho_rho0(t) * self.r_r0(t, r0)) ** (1/2)

    def coord(self, t, r0, z0):
        x = self.wx * t
        time = lambda t: self.terminal_vel(t, r0)
        if np.isnan(self.r_r0(t, r0)):
            y = np.nan
        else:
            y = z0 - int.quad(time, 0, t)[0]
        return [x, y]

    def f(self, t, r0, z0):
        t = t[0]
        return abs(self.coord(t, r0, z0)[1])

    def ground(self, r0, z0):
        #returns time when firebrand hits the ground.
        #Calcs time taken for y distance = z
        #time = mzn(self.f, [1], args=(r0, z0))
        time = root(self.f, 1, args=(r0, z0))
        if time.success:
            out = time.x[0]
        else:
            out = np.nan
        return out

#############################################
# test = SubModel2(0.02, 20, 5)
# # n = 100
# # coord=np.zeros((n, 2))
# # count=0
# print(test.ground(0.005, 240))
# for i in range(n):
#     hol = test.coord(i, 0.009, 140)
#     if hol[1]>0:
#         coord[i] = hol
#         count += 1
# print(coord)
# plt.plot(coord[:count, 0], coord[:count, 1])
# plt.xlabel("x-Distance (m)")
# plt.ylabel("z-Height (m)")
#
# plt.show()

# test = SubModel2(0.02, 16, 5)
# n = 1000
# coord=np.zeros((n, 2))
# count=0
# for i in range(n):
#     hol = test.terminal_vel(i, 0.02)
#     coord[i, 0] = i
#     coord[i, 1] = hol
#
#
#
# plt.plot(coord[:, 0], coord[:, 1])
# plt.xlabel("Time (s)")
# plt.axvline(x=51, linestyle="--", color="grey")
# plt.ylabel(r"$w_f\ (ms^{-1}$)")
#
# plt.show()

# test = SubModel2(0.02, 16, 5)
# n = 1000
# coord=np.zeros((n, 2))
# count=0
# for i in range(n):
#     hol = test.r_r0(i, 0.02)
#     coord[i, 0] = i
#     coord[i, 1] = hol
#
#
#
# plt.plot(coord[:, 0], coord[:, 1]*0.02)
# plt.xlabel("Time (s)")
# plt.axvline(x=51, linestyle="--", color="grey")
# plt.ylabel(r"$r(t)\ (m)$")
#
# plt.show()