import numpy as np
from numba import int32, boolean, float32
from numba.experimental import jitclass
import random
from CA_Spreading import CA_Definition as p


#Parameters
min2sec = 60
hour2min = 60
day2hour = 24
K = p.delt / p.delx ** 2

#### Rates of spread from realwork -> CA
class ROSdef:
    def __init__(self, r0, theta):
        self.spread = r0
        self.burn = theta

    def fuel2fd(self):
        #converts the rates of spread to work in FD given real world numbers
        a = 2.6298  #1st coef of quadratic
        b = -0.0397 #2nd coef of quadratic
        c = 0.0001  #3rd coef of quadratic
        n = 0.092   #above value the relationship becomes linear
        alp = 1.9   #Power law relationship
        inv = 4.8   #Inverse relationship with burn rate

        x = self.burn * self.spread ** alp
        if x <= n:
            out = a * x ** 2 + b * x + c
        else:
            out = (2 * a * n + b) * x - a * n ** 2 + c
        return out, inv / self.burn

    def fd2ca(self, vee, gam):
        #converts the rates from FD to CA
        a, b = 6.28503805, 0.61609013     #power law relation between vee * gamma
        m, c = 4.39303586, 0.40454337     #linear relationship between spread rate

        v = m * vee + c
        y = a * ((vee * gam) ** b)
        return v, y / v

    def convert(self):
        fd = self.fuel2fd()
        output = self.fd2ca(*fd)
        return output


spec = [
    ('k', int32),
    ('determinate', boolean),
    ('ell', int32),
    ('initial', float32[:, :, :]),
    ('vee', float32),
    ('gamma', float32),
    ('uwind', float32[:, :, :]),
    ('vwind', float32[:, :, :]),
    ('xslp', float32[:, :]),
    ('yslp', float32[:, :]),
    ('fbrk', float32[:, :]),
    ('timestep', int32)
    # ('jcalc', int32),
    # ('ellcalc', int32)
]


#### CA production
@jitclass(spec)
class  RunCA:
    def __init__(self, k, deturm, L, arr, windarru, windarrv, slparrx, slparry, fbrk, hr, vee, gamma):
        # CA Definitions
        self.k = k
        self.determinate = deturm
        self.ell = L
        self.initial = arr
        self.vee = vee
        self.gamma = gamma

        #External Conditions
        self.uwind = windarru
        self.vwind = windarrv
        self.xslp = slparrx
        self.yslp = slparry
        self.fbrk = fbrk
        self.timestep = hr


    # Definition of Spread (forward Eular)
    def func(self, x, y, z):
        n = y + self.vee * K * (x - 2 * y + z) + p.delt * self.gamma * y * (1 - y)
        return n

    ############## Make Transition Matrix ############
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
    def colcheck(self, prob, x, P):
        i = 0
        while prob > P[x, i]:
            i += 1
        return i


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

        #Quadratic Increase in wind speed as defined in paper
        x = x * (p.awfac * xwind[m, n] + p.bwfac) * xwind[m, n]
        y = - y * (p.awfac * ywind[m, n] + p.bwfac) * ywind[m, n]

        return - 1/2 * (p.delt / p.delx) * (x + y)


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

        # Quadratic Increase in Slope speed as defined in paper
        x = x * (p.asfac * xslp[m, n] ** 2 + p.bsfac * xslp[m, n] + p.csfac)
        y = - y * (p.asfac * yslp[m, n] ** 2 + p.bsfac * yslp[m, n] + p.csfac)

        return - 1/2 * (p.delt / p.delx) * (x + y)


    def update2D(self, P, fb, delx, hrstart):
        #loop for time steps
        t, m, n = self.initial.shape

        #calculate no. time steps betweek weather changes
        wetchn = int(self.timestep * hour2min * min2sec / (delx * 1000))

        for time in range(1, t):
            wetnum = time // wetchn + hrstart
            if time % 100 == 0:
                print(time, wetnum)

            for j in range(1, m-1):
                for ell in range(1, n-1):
                    #Alter the direction of update on each pass
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

                        #Update from spread
                        self.initial[time, j, ell] = np.ceil(1/2 * (self.colcheck(prob1, alpha, P) + self.colcheck(prob2, beta, P)))

                        #wind and slope
                        windcor = self.wind(self.initial[time - 1, :, :], self.uwind[wetnum, :, :], self.vwind[wetnum, :, :], j, ell)
                        slopecor = self.slope(self.initial[time - 1, :, :], self.xslp, self.yslp, j, ell)
                        self.initial[time, j, ell] = round(self.initial[time, j, ell] + windcor + slopecor)
                        self.initial[time, j, ell] = max(min(self.initial[time, j, ell], self.k - 1), 0)

                        #Run Firebrands
                        if p.frbuse:
                            if self.initial[time, j, ell] > p.minKval and self.initial[time, j, ell] < p.maxKval:

                                row = random.randint(0, p.num)
                                if ~np.isnan(fb[wetnum, row, 0]) and ~np.isnan(fb[wetnum, row, 1]):
                                    jcalc, ellcalc = int(fb[wetnum, row, 0]), int(fb[wetnum, row, 1])
                                    if self.initial[time - 1, j + jcalc, ell + ellcalc] == 0:
                                        self.initial[time - 1, (j + jcalc), (ell + ellcalc)] = 1
                                        self.initial[time, (j + jcalc), (ell + ellcalc)] = 1

                                #Apply fire breaks
                        if self.fbrk != None:
                            self.initial[time, j, ell] = self.fbrk[j, ell] * self.initial[time, j, ell]

            # loop for array width (set up with neuman BC)
            self.initial[time, 0, :] = self.initial[0, 0, :]
            self.initial[time, -1, :] = self.initial[0, -1, :]
            self.initial[time, :, 0] = self.initial[0, :, 0]
            self.initial[time, :, -1] = self.initial[0, :, -1]

        return self.initial