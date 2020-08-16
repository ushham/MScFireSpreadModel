import numpy as np
import scipy.integrate as int
import matplotlib.pyplot as plt

class SubModel2:
    def __init__(self, r0, rho0, eta, w0, wx, h):
        self.r0 = r0
        self.rho0 = rho0
        self.eta = eta
        self.w0 = w0
        self.wx = wx
        self.Re = 3400
        self.Sc = 0.7
        self.beta = 4.3 * (10 ** -7) * (1 + 0.276 * (self.Re ** (1/2)) * (self.Sc ** (1/3)))
        self.z0 = h

    def r_r0(self, t):
        r4 = self.r0 ** 4 - np.sqrt(3) * (self.beta ** 2) * (t ** 2) / 8
        if r4 < 0:
            r4 = np.nan
        r = r4 ** (1 / 4) / self.r0
        return r

    def rho_rho0(self, t):
        return 1 / (1 + self.eta * t ** 2)

    def terminal_vel(self, t):
        return self.w0 * (self.rho_rho0(t) * self.r_r0(t)) ** (1/2)

    def coord(self, t):
        x = self.wx * t
        time = lambda t: self.terminal_vel(t)
        if np.isnan(self.r_r0(t)):
            y = np.nan
        else:
            y = self.z0 - int.quad(time, 0, t)[0]
        return [x, y]

    def dist(self, t):
        loc = self.coord(t)
        return np.sqrt(loc[0] ** 2 + (loc[1] - self.z0) ** 2)

#############################################
n = 200
                #r0, rho0, eta, w0, wx, h
test = SubModel2(0.01, 545, 0.001, 2, 20, 1000)

hold = np.zeros((n, 6))
for i in range(n):
    hold[i, 0] = test.dist(i)
    hold[i, 1:3] = test.coord(i)
    hold[i, 3] = test.rho_rho0(i)
    hold[i, 4] = test.terminal_vel(i)
    hold[i, 5] = test.r_r0(i)


plt.scatter(hold[:, 1], hold[:, 2])
print(test.beta)
x = np.linspace(0, n/20, n)
#plt.plot(hold[:, 4])
plt.ylim(0, 1000)
plt.show()