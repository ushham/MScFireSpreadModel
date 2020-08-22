import numpy as np
from numba import jit, int32, boolean, float32
from numba.experimental import jitclass
import random
from CA_Spreading import CA_Definition as p

#Parameters
hour2min = 60
day2hour = 24
K = p.vee * p.delt / p.delx ** 2

spec = [
    ('k', int32),
    ('determinate', boolean),
    ('ell', int32),
    ('initial', float32[:, :, :]),
    ('uwind', float32[:, :, :]),
    ('vwind', float32[:, :, :]),
    ('xslp', float32[:, :]),
    ('yslp', float32[:, :]),
    ('fbrk', float32[:, :]),
    ('timestep', int32)
]

@jitclass(spec)
class  RunCA:
    def __init__(self, k, deturm, L, arr, windarru, windarrv, slparrx, slparry, fbrk, hr):
        # CA Definitions
        self.k = k
        self.determinate = deturm
        self.ell = L
        self.initial = arr

        #External Conditions
        self.uwind = windarru
        self.vwind = windarrv
        self.xslp = slparrx
        self.yslp = slparry
        self.fbrk = fbrk
        self.timestep = hr

    # Definition of Spread (forward Eular)
    #@jit(nopython=True)
    def func(self, x, y, z):
        n = y + K * (x - 2 * y + z) + p.delt * p.gamma * y * (1 - y)
        return n

    ############## Make Transition Matrix ############
    #@jit(nopython = True)
    def Pmaker(self):
        A = range(self.k)
        P = np.zeros((self.k ** 3, self.k))
        for a in A:
            for b in A:
                for c in A:
                    alpha = a * (self.k ** 2) + (b * self.k) + c
                    X = np.zeros(self.k)

                    for ell in range(self.ell):
                        x = np.random.uniform(a / self.k, (a + 1) / self.k)
                        y = np.random.uniform(b / self.k, (b + 1) / self.k)
                        z = np.random.uniform(c / self.k, (c + 1) / self.k)
                        d = np.int(self.k * self.func(x, y, z))
                        X[d] += 1

                    if self.determinate:
                        P[alpha, 0] = np.argmax(X)
                    else:
                        for i in A:
                            if np.sum(X[:]) == 0:
                                print(a, b, c, d)
                            if a == b == c == 0: #unstable equilibria exceptions:
                                P[alpha, i] = 1
                            else:
                                P[alpha, i] = X[i] / np.sum(X[:]) + (P[alpha, i - 1] if i > 0 else 0)
        return P


    ######## Returns column which refers to element with probability prob
    #@jit(nopython = True)
    def colcheck(self, prob, x, P):
        i = 0
        while prob > P[x, i]:
            i += 1
        return i

    #@jit(nopython = True)
    def wind(self, arr, xwind, ywind, m, n):
        #x dir
        if xwind[m, n] > 0:
            x = (arr[m, n] - arr[m, n - 1])
        else:
            x = (arr[m, n + 1] - arr[m, n])

        #y dir
        if ywind[m, n] > 0:
            y = (arr[m + 1, n] - arr[m, n])
        else:
            y = (arr[m, n] - arr[m - 1, n])

        x = x * p.wfac * xwind[m, n]
        y = - y * p.wfac * ywind[m, n]

        return - 1/2 * (p.delt / p.delx) * (x + y)

    #@jit(nopython = True)
    def slope(self, arr, xslp, yslp, m, n):
        #x dir
        if xslp[m, n] > 0:
            x = (arr[m, n] - arr[m, n-1])
        else:
            x = (arr[m, n + 1] - arr[m, n])

        #y dir
        if yslp[m, n] > 0:
            y = (arr[m + 1, n] - arr[m, n])
        else:
            y = (arr[m, n] - arr[m - 1, n])

        x = x * p.sfac * xslp[m, n]
        y = - y * p.sfac * yslp[m, n]

        return - 1/2 * (p.delt / p.delx) * (x + y)

    #@jit(nopython = True)
    def update2D(self, P):
        #loop for time steps
        t, m, n = self.initial.shape

        #calculate no. time steps betweek weather changes
        wetchn = self.timestep * hour2min

        for time in range(1, t):
            if time % 100 == 0:
                print(time)

            wetnum = time // wetchn
            for j in range(1, m-1):
                for ell in range(1, n-1):
                    if time % 4 == 0:
                        alpha = int(self.initial[time - 1, j, ell - 1] * self.k ** 2 + self.initial[time - 1, j, ell] * self.k + self.initial[time - 1, j, ell + 1])
                        beta = int(self.initial[time - 1, j - 1, ell] * self.k ** 2 + self.initial[time - 1, j, ell] * self.k + self.initial[time - 1, j + 1, ell])
                    elif time % 4 == 1:
                        alpha = int(self.initial[time - 1, j, ell + 1] * self.k ** 2 + self.initial[time - 1, j, ell] * self.k + self.initial[time - 1, j, ell - 1])
                        beta = int(self.initial[time - 1, j - 1, ell] * self.k ** 2 + self.initial[time - 1, j, ell] * self.k + self.initial[time - 1, j + 1, ell])
                    elif time % 4 == 2:
                        alpha = int(self.initial[time - 1, j, ell + 1] * self.k ** 2 + self.initial[time - 1, j, ell] * self.k + self.initial[time - 1, j, ell - 1])
                        beta = int(self.initial[time - 1, j + 1, ell] * self.k ** 2 + self.initial[time - 1, j, ell] * self.k + self.initial[time - 1, j - 1, ell])
                    else:
                        alpha = int(self.initial[time - 1, j, ell - 1] * self.k ** 2 + self.initial[time - 1, j, ell] * self.k + self.initial[time - 1, j, ell + 1])
                        beta = int(self.initial[time - 1, j + 1, ell] * self.k ** 2 + self.initial[time - 1, j, ell] * self.k + self.initial[time - 1, j - 1, ell])

                    if self.determinate:
                        self.initial[ell, j] = 1/2 * (P[alpha, 0] + P[beta, 0])
                    else:
                        prob1 = random.random()
                        prob2 = random.random()

                        self.initial[time, j, ell] = np.ceil(1/2 * (self.colcheck(prob1, alpha, P) + self.colcheck(prob2, beta, P)))

                        #wind and slope
                        windcor = self.wind(self.initial[time - 1, :, :], self.uwind[wetnum, :, :], self.vwind[wetnum, :, :], j, ell)
                        slopecor = self.slope(self.initial[time - 1, :, :], self.xslp, self.yslp, j, ell)
                        self.initial[time, j, ell] = round(self.initial[time, j, ell] + windcor + slopecor)
                        self.initial[time, j, ell] = max(min(self.initial[time, j, ell], self.k - 1), 0)

                        #Apply fire breaks
                        if self.fbrk != None:
                            self.initial[time, j, ell] = self.fbrk[j, ell] * self.initial[time, j, ell]

            # loop for array width (set up with neuman BC)
            self.initial[time, 0, :] = self.initial[0, 0, :]
            self.initial[time, -1, :] = self.initial[0, -1, :]
            self.initial[time, :, 0] = self.initial[0, :, 0]
            self.initial[time, :, -1] = self.initial[0, :, -1]

        return  self.initial