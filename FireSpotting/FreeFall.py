import numpy as np
import scipy.integrate as int
from scipy.optimize import root

class SubModel2:

    def __init__(self, eta, w0, wx):
        self.eta = eta
        self.w0 = w0
        self.wx = wx

        # Assumptions
        self.Re = 12000  # Reynolds number from litrature
        self.Sc = 0.7  # Schmidt number, from litrature
        self.beta = 4.3 * (10 ** -7) * (1 + 0.276 * (self.Re ** (1 / 2)) * (self.Sc ** (1 / 3)))

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
        time = root(self.f, 1, args=(r0, z0))
        if time.success:
            out = time.x[0]
        else:
            out = np.nan
        return out
